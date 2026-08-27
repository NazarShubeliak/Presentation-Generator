"""WP8 — turn a presentation JSON file into a finished PowerPoint file.

Usage:
    python src/build_presentation.py --input data/example_01.json \\
        --template templates/master_v01.pptx --output output/

Aspect-ratio decision (per the task brief's WP8 note that this needs writing
down): picture placeholders in `master_v01.pptx` were sized in WP6 to the
frame ratios recorded in docs/04-fields.md, but a real supplied photo won't
match those ratios exactly. `Placeholder.insert_picture()` crops to fill,
centred — fine for a close ratio, but a badly-mismatched one crops away part
of the motif. This script center-crops every image with Pillow to the exact
target placeholder ratio *before* calling insert_picture(), so the later
crop-to-fill is always a no-op. Chosen over "validate ratio and reject
mismatches" because the generator's whole point is to run unattended on
supplied photos without a human re-cropping them first.
"""

import argparse
import copy
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from PIL import Image
from pptx import Presentation

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = PROJECT_ROOT / "schema" / "presentation.schema.json"

# PAGE_06_LOCAL_MOTIFS's headline/subheadline/stats-callout are computed from
# this page's position among the deck's PAGE_06_LOCAL_MOTIFS occurrences, not
# authored in the input JSON (docs/04-fields.md "Fields not included here",
# wording confirmed by the designer, docs/open-questions.md #22/#23).
# Position 4+ gets neither headline/subheadline nor the stats callout — only
# the theme-world-name caption (already an authored field, handled normally).
# Known scope gap: this doesn't model the row-limit-continuation mechanism
# (same theme overflowing onto a 2nd slide, e.g. Freiburg's 5-motif table) —
# the schema has no way to say "this PAGE_06 entry continues the previous
# one", so every entry is treated as a new theme at its sequence position.
MOTIF_POSITION_CONTENT = {
    1: {
        "TXT_MOTIF_HEADLINE": "Das nehmen Ihre Besucher mit — personalisiert, sofort, teilbar.",
        "TXT_MOTIF_SUBHEADLINE": (
            "Jedes Motiv wird individuell auf Ihren Weihnachtsmarkt abgestimmt — "
            "Ihre Besucher werden Teil Ihrer Erlebniswelt. Das teilen sie."
        ),
        "TXT_MOTIF_STATS_CALLOUT": (
            "70 % der Besucher teilen ihr Motiv aktiv auf Facebook, Instagram "
            "oder TikTok — mit Ihrem Markt als Kontext."
        ),
    },
    2: {
        "TXT_MOTIF_HEADLINE": "Ihre Charaktere. Ihre Geschichte.",
        "TXT_MOTIF_SUBHEADLINE": (
            "Gemeinsam mit Ihnen entwickeln wir die Charaktere, die perfekt zu Ihrem Markt passen."
        ),
        "TXT_MOTIF_STATS_CALLOUT": "",
    },
    3: {
        "TXT_MOTIF_HEADLINE": "Ein Weihnachtsmarkt. Mehrere Erlebniswelten.",
        "TXT_MOTIF_SUBHEADLINE": (
            "Jedes Motiv erzählt eine eigene Geschichte — perfekt abgestimmt "
            "auf Ihre Veranstaltung und Ihre Stadt."
        ),
        "TXT_MOTIF_STATS_CALLOUT": "",
    },
}

# Which fields each page_type can carry, split into required/optional, kept
# in sync with schema/presentation.schema.json's fields_PAGE_* defs. The
# schema is the source of truth for validation; this list drives *filling*
# behaviour (required-but-missing -> <<MISSING>> marker, optional-but-absent
# -> remove the unused placeholder so it doesn't show up empty).
PAGE_FIELD_SPECS = {
    "PAGE_01_TITLE": {
        "required": ["TXT_TITLE_SUBLINE", "IMG_THEME_WORLD_PHOTO"],
        "optional": [],
    },
    "PAGE_02_SERVICE": {
        "required": ["IMG_THEME_WORLD_PHOTO"],
        "optional": [],
    },
    "PAGE_03_THEME_SHOWCASE": {
        "required": ["TXT_THEME_WORLD_NAME_1", "IMG_THEME_WORLD_PHOTO_1"],
        "optional": ["TXT_THEME_WORLD_NAME_2", "IMG_THEME_WORLD_PHOTO_2"],
    },
    "PAGE_04_REFERENCES": {"required": [], "optional": []},
    "PAGE_05_USER_FLOW": {
        "required": [
            "TXT_KIOSK_BACKGROUND_LABEL",
            "IMG_KIOSK_SCREENSHOT",
            "IMG_USER_FLOW_CARD_1",
            "IMG_USER_FLOW_CARD_2",
        ],
        "optional": [],
    },
    "PAGE_06_LOCAL_MOTIFS": {
        "required": [
            "TXT_THEME_WORLD_NAME",
            "TXT_MOTIF_1_NAME",
            "IMG_MOTIF_1_PHOTO",
            "IMG_MOTIF_1_BACKGROUND",
            "IMG_MOTIF_1_MASK",
        ],
        "optional": [
            "TXT_MOTIF_2_NAME", "IMG_MOTIF_2_PHOTO", "IMG_MOTIF_2_BACKGROUND", "IMG_MOTIF_2_MASK",
            "TXT_MOTIF_3_NAME", "IMG_MOTIF_3_PHOTO", "IMG_MOTIF_3_BACKGROUND", "IMG_MOTIF_3_MASK",
        ],
    },
    "PAGE_07_BESTSELLERS": {"required": [], "optional": []},
    "PAGE_08_TRANSITION": {
        "required": ["TXT_THEME_WORLD_NAME_1", "IMG_OUTPUT_CARD_1", "TXT_THEME_WORLD_NAME_2", "IMG_OUTPUT_CARD_2"],
        "optional": [],
    },
    "PAGE_09_SOCIAL_REACH": {
        "required": ["IMG_INSTAGRAM_MOCKUP"],
        "optional": [],
    },
    "PAGE_10_CONTACT": {
        "required": ["IMG_LANDMARK_PHOTO"],
        "optional": [],
    },
}


def _make_console_utf8_safe():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def parse_args():
    p = argparse.ArgumentParser(description="Build a presentation .pptx from a JSON data file.")
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--template", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    return p.parse_args()


def load_and_validate(input_path: Path) -> dict:
    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        schema = json.load(f)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    if errors:
        print(f"ERROR: {input_path} failed schema validation ({len(errors)} error(s)):", file=sys.stderr)
        for e in errors:
            location = "/".join(str(p) for p in e.path) or "(root)"
            print(f"  - {location}: {e.message}", file=sys.stderr)
        sys.exit(1)
    return data


def get_layout(prs: Presentation, page_type: str):
    for master in prs.slide_masters:
        for layout in master.slide_layouts:
            if layout.name == page_type:
                return layout
    return None


def crop_to_ratio(image_path: Path, target_ratio: float, tmp_dir: Path) -> Path:
    """Center-crop image_path to target_ratio (width/height), return the path
    to use for insertion (the original, unmodified, if it already matches)."""
    im = Image.open(image_path)
    w, h = im.size
    current_ratio = w / h
    if abs(current_ratio - target_ratio) < 0.01:
        return image_path
    if current_ratio > target_ratio:
        new_w = round(h * target_ratio)
        x0 = (w - new_w) // 2
        box = (x0, 0, x0 + new_w, h)
    else:
        new_h = round(w / target_ratio)
        y0 = (h - new_h) // 2
        box = (0, y0, w, y0 + new_h)
    cropped = im.crop(box)
    tmp_dir.mkdir(parents=True, exist_ok=True)
    out_path = tmp_dir / f"{image_path.stem}_cropped{image_path.suffix}"
    cropped.save(out_path)
    return out_path


def remove_shape(shape):
    shape._element.getparent().remove(shape._element)


def fill_slide(slide, page_type: str, fields: dict, base_dir: Path, tmp_dir: Path, log):
    name_by_idx = {ph.placeholder_format.idx: ph.name for ph in slide.slide_layout.placeholders}
    placeholders = {name_by_idx.get(ph.placeholder_format.idx): ph for ph in slide.placeholders}
    spec = PAGE_FIELD_SPECS.get(page_type, {"required": [], "optional": []})

    for field_name in spec["required"] + spec["optional"]:
        is_required = field_name in spec["required"]
        placeholder = placeholders.get(field_name)
        if placeholder is None:
            log(f"    ! template has no placeholder named {field_name} (schema/template drift)")
            continue

        value = fields.get(field_name)
        is_image = field_name.startswith("IMG_")

        if value is not None:
            if is_image:
                image_path = base_dir / value
                if not image_path.exists():
                    log(f"    WARNING: {field_name} -> image file not found: {image_path}")
                    continue
                ratio = placeholder.width / placeholder.height
                final_path = crop_to_ratio(image_path, ratio, tmp_dir)
                placeholder.insert_picture(str(final_path))
                log(f"    filled {field_name} <- {value}")
            else:
                placeholder.text_frame.text = value
                log(f"    filled {field_name} = {value!r}")
        else:
            if is_required:
                log(f"    WARNING: required field {field_name} missing")
                if not is_image:
                    placeholder.text_frame.text = f"<<MISSING: {field_name}>>"
            else:
                log(f"    optional field {field_name} not provided, removing unused placeholder")
                remove_shape(placeholder)


def fill_motif_computed_fields(slide, position: int, log):
    name_by_idx = {ph.placeholder_format.idx: ph.name for ph in slide.slide_layout.placeholders}
    placeholders = {name_by_idx.get(ph.placeholder_format.idx): ph for ph in slide.placeholders}
    content = MOTIF_POSITION_CONTENT.get(position)

    for field_name in ("TXT_MOTIF_HEADLINE", "TXT_MOTIF_SUBHEADLINE", "TXT_MOTIF_STATS_CALLOUT"):
        placeholder = placeholders.get(field_name)
        if placeholder is None:
            continue
        text = content.get(field_name, "") if content else ""
        if text:
            placeholder.text_frame.text = text
            log(f"    computed {field_name} (world position {position}) = {text!r}")
        else:
            log(f"    computed {field_name} (world position {position}) -> empty, removing placeholder")
            remove_shape(placeholder)


def next_output_path(output_dir: Path, project_id: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    n = 1
    while True:
        candidate = output_dir / f"{project_id}_v{n:02d}.pptx"
        if not candidate.exists():
            return candidate
        n += 1


def main():
    _make_console_utf8_safe()
    args = parse_args()

    def log(msg):
        print(msg)

    log(f"Loading and validating {args.input} against {SCHEMA_PATH} ...")
    data = load_and_validate(args.input)
    log("Validation passed.")

    base_dir = args.input.resolve().parent.parent  # data/ -> project root, so 'images/...' resolves
    tmp_dir = PROJECT_ROOT / "output" / "_build_tmp"

    log(f"Opening template {args.template} ...")
    prs = Presentation(str(args.template))

    motif_table_count = 0
    for i, page in enumerate(data["pages"], start=1):
        page_type = page["page_type"]
        fields = page.get("fields", {})
        log(f"Slide {i}: {page_type}")

        layout = get_layout(prs, page_type)
        if layout is None:
            log(f"  ERROR: template has no layout named {page_type}, skipping")
            continue

        slide = prs.slides.add_slide(layout)
        fill_slide(slide, page_type, fields, base_dir, tmp_dir, log)

        if page_type == "PAGE_06_LOCAL_MOTIFS":
            motif_table_count += 1
            fill_motif_computed_fields(slide, motif_table_count, log)

    out_path = next_output_path(args.output, data["project_id"])
    prs.save(str(out_path))
    log(f"Saved {out_path}")


if __name__ == "__main__":
    main()
