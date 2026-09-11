"""Local web GUI for authoring a presentation's input JSON without hand-typing
it, plus a one-click "Generate" that runs src/build_presentation.py.

Single-operator local tool: no auth, no database, binds to 127.0.0.1 only.
Run with `python src/gui/app.py` (or ../../run_gui.sh from the repo root).
"""

import glob
import json
import re
import subprocess
import sys
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, send_from_directory, url_for
from jsonschema import Draft202012Validator
from werkzeug.utils import secure_filename

import field_catalogue

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

    if result.returncode != 0:
        return jsonify({"ok": False, "log": log})

    candidates = sorted(
        OUTPUT_DIR.glob(f"{project_id}_v*.pptx"),
        key=lambda p: p.stat().st_mtime,
    )
    download_name = candidates[-1].name if candidates else None
    return jsonify({"ok": True, "log": log, "download": download_name})


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
