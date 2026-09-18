"""Local web GUI for authoring a presentation's input JSON without hand-typing
it, plus a one-click "Generate" that runs src/build_presentation.py.

Single-operator local tool: no auth, no database, binds to 127.0.0.1 only.
Run with `python src/gui/app.py` (or ../../run_gui.sh from the repo root).
"""

import base64
import glob
import json
import mimetypes
import re
import subprocess
import sys
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, send_from_directory, url_for
from jsonschema import Draft202012Validator
from werkzeug.utils import secure_filename

import field_catalogue
import slide_preview

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
IMAGES_DIR = PROJECT_ROOT / "images"
OUTPUT_DIR = PROJECT_ROOT / "output"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
SCHEMA_PATH = PROJECT_ROOT / "schema" / "presentation.schema.json"

DATA_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

app = Flask(__name__)

with open(SCHEMA_PATH, encoding="utf-8") as _f:
    _SCHEMA = json.load(_f)
_VALIDATOR = Draft202012Validator(_SCHEMA)

ALLOWED_IMAGE_EXT = {"jpg", "jpeg", "png"}
PROJECT_ID_RE = re.compile(r"^[a-z0-9_]+$")


def available_templates():
    """master_vNN.pptx files first (newest version first), then everything
    else alphabetically — so the current canonical template is pre-selected
    in the GUI's template dropdown by default."""
    names = [Path(p).name for p in glob.glob(str(TEMPLATES_DIR / "*.pptx"))]
    names = [n for n in names if not n.startswith("_preview_")]

    def sort_key(name):
        m = re.match(r"master_v(\d+)\.pptx$", name)
        return (0, -int(m.group(1))) if m else (1, name)

    return sorted(names, key=sort_key)


@app.route("/")
def index():
    files = sorted(p.name for p in DATA_DIR.glob("*.json"))
    return render_template("index.html", files=files)


@app.route("/edit")
@app.route("/edit/<name>")
def edit(name=None):
    initial_data = None
    if name:
        path = DATA_DIR / secure_filename(name)
        if path.exists():
            with open(path, encoding="utf-8") as f:
                initial_data = json.load(f)
    return render_template(
        "edit.html",
        catalogue=field_catalogue.get_field_catalogue(),
        page_types=field_catalogue.PAGE_TYPES,
        initial_data=initial_data,
        templates=available_templates(),
    )


def _validate(data):
    errors = sorted(_VALIDATOR.iter_errors(data), key=lambda e: list(e.path))
    return [
        {"path": "/".join(str(p) for p in e.path) or "(root)", "message": e.message}
        for e in errors
    ]


# build_presentation.py's log already states, line by line, every slide it
# built and every WARNING/drift it hit while doing so (fill_slide() etc.) —
# so post-generation "testing" reuses that as the source of truth instead of
# re-deriving field requirements independently, which would drift out of
# sync with PAGE_FIELD_SPECS over time. This just turns the known log format
# into structured, per-slide issues the GUI can show as a checklist instead
# of a wall of text.
_LOG_LINE_PATTERNS = [
    ("slide_header", re.compile(r"^Slide (\d+): (\S+)$")),
    ("missing_field", re.compile(r"^\s*WARNING: required field (\S+) missing$")),
    ("image_not_found", re.compile(r"^\s*WARNING: (\S+) -> image file not found: (.+)$")),
    ("template_drift", re.compile(r"^\s*! template has no placeholder named (\S+) \(schema/template drift\)$")),
    ("layout_missing", re.compile(r"^\s*ERROR: template has no layout named (\S+), skipping$")),
]

_ISSUE_MESSAGES = {
    "missing_field": lambda field, extra: f"не заповнено обов'язкове поле {field}",
    "image_not_found": lambda field, extra: f"файл зображення для {field} не знайдено ({extra})",
    "template_drift": lambda field, extra: f"у шаблоні немає плейсхолдера {field} (розбіжність шаблону/схеми)",
    "layout_missing": lambda field, extra: f"у шаблоні немає макета для цього типу слайду",
}


def check_generation_log(log_text):
    """Turn the generator's text log into a structured list of per-slide
    issues, so the GUI can show a pass/fail checklist instead of asking the
    user to read raw output."""
    issues = []
    slide_num, page_type = None, None
    for line in log_text.splitlines():
        for kind, pattern in _LOG_LINE_PATTERNS:
            m = pattern.match(line)
            if not m:
                continue
            if kind == "slide_header":
                slide_num, page_type = int(m.group(1)), m.group(2)
            elif kind == "layout_missing":
                issues.append({
                    "slide": slide_num, "page_type": page_type, "kind": kind,
                    "field": None, "message": _ISSUE_MESSAGES[kind](None, None),
                })
            else:
                field = m.group(1)
                extra = m.group(2) if m.lastindex and m.lastindex >= 2 else None
                issues.append({
                    "slide": slide_num, "page_type": page_type, "kind": kind,
                    "field": field, "message": _ISSUE_MESSAGES[kind](field, extra),
                })
            break
    return issues


@app.route("/api/upload-image", methods=["POST"])
def upload_image():
    project_id = request.form.get("project_id", "").strip()
    field_name = request.form.get("field_name", "").strip()
    file = request.files.get("file")
    if not project_id or not PROJECT_ID_RE.match(project_id):
        return jsonify({"error": "Set a valid project_id (lowercase letters/digits/underscore) before uploading images."}), 400
    if not file or not file.filename:
        return jsonify({"error": "No file provided."}), 400
    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_IMAGE_EXT:
        return jsonify({"error": f"Unsupported file type .{ext} — use jpg/jpeg/png."}), 400

    project_dir = IMAGES_DIR / secure_filename(project_id)
    project_dir.mkdir(parents=True, exist_ok=True)
    dest = project_dir / f"{secure_filename(field_name)}.{ext}"
    file.save(dest)

    rel_path = dest.relative_to(PROJECT_ROOT).as_posix()
    return jsonify({"path": rel_path})


@app.route("/api/save", methods=["POST"])
def save():
    data = request.get_json(force=True)
    errors = _validate(data)
    if errors:
        return jsonify({"ok": False, "errors": errors}), 400

    project_id = data["project_id"]
    out_path = DATA_DIR / f"{project_id}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return jsonify({"ok": True, "saved_to": out_path.name})


@app.route("/api/generate", methods=["POST"])
def generate():
    body = request.get_json(force=True)
    data = body["data"]
    template_name = body.get("template") or (available_templates() or [None])[0]
    if not template_name:
        return jsonify({"ok": False, "log": "No .pptx template found in templates/."}), 400

    errors = _validate(data)
    if errors:
        return jsonify({"ok": False, "errors": errors}), 400

    project_id = data["project_id"]
    input_path = DATA_DIR / f"{project_id}.json"
    with open(input_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    template_path = TEMPLATES_DIR / template_name
    result = subprocess.run(
        [
            sys.executable, str(PROJECT_ROOT / "src" / "build_presentation.py"),
            "--input", str(input_path),
            "--template", str(template_path),
            "--output", str(OUTPUT_DIR),
        ],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    log = (result.stdout or "") + (result.stderr or "")
    issues = check_generation_log(log)

    if result.returncode != 0:
        return jsonify({"ok": False, "log": log, "issues": issues})

    candidates = sorted(
        OUTPUT_DIR.glob(f"{project_id}_v*.pptx"),
        key=lambda p: p.stat().st_mtime,
    )
    download_name = candidates[-1].name if candidates else None
    return jsonify({"ok": True, "log": log, "download": download_name, "issues": issues})


@app.route("/api/preview-slide", methods=["POST"])
def preview_slide():
    """Renders just one slide (not the whole deck) via PowerPoint COM, so the
    GUI can show what a slide will look like on click without waiting on a
    full generation. Deliberately skips whole-deck schema validation (unlike
    /api/generate) — the rest of the form may still be incomplete while a
    market is previewing one slide, and build_slide() already degrades
    gracefully (<<MISSING>> markers, skipped images) instead of crashing."""
    body = request.get_json(force=True)
    data = body.get("data", {})
    page_index = body.get("page_index")
    template_name = body.get("template") or (available_templates() or [None])[0]
    if not template_name:
        return jsonify({"ok": False, "error": "No .pptx template found in templates/."}), 400
    if page_index is None:
        return jsonify({"ok": False, "error": "Missing page_index."}), 400

    template_path = TEMPLATES_DIR / template_name
    try:
        png_path, log_text = slide_preview.render_slide_png(template_path, data, page_index)
    except slide_preview.PreviewError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"ok": False, "error": f"Preview failed: {e}"}), 500

    issues = check_generation_log(log_text)
    image_b64 = base64.b64encode(png_path.read_bytes()).decode("ascii")
    # PowerPoint's exported file extension can vary (seen .PNG and, when the
    # format code is wrong, .JPG) — report the real mimetype rather than
    # assuming, so the frontend's data: URI is never mislabeled.
    mimetype = mimetypes.guess_type(png_path.name)[0] or "image/png"
    return jsonify({"ok": True, "image_base64": image_b64, "mimetype": mimetype, "issues": issues})


@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)


@app.route("/image-preview/<path:relpath>")
def image_preview(relpath):
    full = (PROJECT_ROOT / relpath).resolve()
    if not str(full).startswith(str(IMAGES_DIR.resolve())) or not full.exists():
        return "", 404
    return send_from_directory(full.parent, full.name)


if __name__ == "__main__":
    print("Presentation Generator GUI: http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
