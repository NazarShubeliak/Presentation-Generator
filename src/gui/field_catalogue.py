"""Introspects schema/presentation.schema.json and build_presentation.py's
PAGE_FIELD_SPECS to produce the field catalogue the GUI renders forms from.

Deliberately does not hardcode its own copy of "which fields exist per page
type" — that kind of duplicated source of truth is exactly what caused the
pptx-template placeholder-naming bugs fixed repeatedly elsewhere in this
project. Both sources below already exist and are authoritative; this module
only reads them.
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SCHEMA_PATH = PROJECT_ROOT / "schema" / "presentation.schema.json"

sys.path.insert(0, str(PROJECT_ROOT / "src"))
import build_presentation  # noqa: E402 (sys.path must be set up first)

# Order here drives the "Add page" dropdown and matches the schema's own
# page_type enum order.
PAGE_TYPES = [
    "PAGE_01_TITLE",
    "PAGE_02_SERVICE",
    "PAGE_03_THEME_SHOWCASE",
    "PAGE_04_REFERENCES",
    "PAGE_05_USER_FLOW",
    "PAGE_06_LOCAL_MOTIFS",
    "PAGE_08_TRANSITION",
    "PAGE_09_SOCIAL_REACH",
    "PAGE_10_CONTACT",
]

_PAGE_TO_DEF = {
    "PAGE_01_TITLE": "fields_PAGE_01_TITLE",
    "PAGE_02_SERVICE": "fields_PAGE_02_SERVICE",
    "PAGE_03_THEME_SHOWCASE": "fields_PAGE_03_THEME_SHOWCASE",
    "PAGE_04_REFERENCES": "fields_empty",
    "PAGE_05_USER_FLOW": "fields_PAGE_05_USER_FLOW",
    "PAGE_06_LOCAL_MOTIFS": "fields_PAGE_06_LOCAL_MOTIFS",
    "PAGE_08_TRANSITION": "fields_PAGE_08_TRANSITION",
    "PAGE_09_SOCIAL_REACH": "fields_PAGE_09_SOCIAL_REACH",
    "PAGE_10_CONTACT": "fields_PAGE_10_CONTACT",
}


def _load_schema():
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        return json.load(f)


def get_field_catalogue():
    """{page_type: [{"name", "kind": "text"|"image", "max_length", "required"}]}

    Field order within a page type matches the schema's own declared order
    (Python dicts preserve JSON key order), so PAGE_06's motif 1/2/3 fields
    stay grouped in the UI without any extra logic.
    """
    schema = _load_schema()
    defs = schema["$defs"]
    catalogue = {}
    for page_type in PAGE_TYPES:
        props = defs[_PAGE_TO_DEF[page_type]].get("properties", {})
        spec = build_presentation.PAGE_FIELD_SPECS.get(page_type, {"required": [], "optional": []})
        required = set(spec["required"])
        fields = []
        for name, prop in props.items():
            is_image = prop.get("$ref", "").endswith("/image_path")
            fields.append({
                "name": name,
                "kind": "image" if is_image else "text",
                "max_length": prop.get("maxLength"),
                "required": name in required,
            })
        catalogue[page_type] = fields
    return catalogue
