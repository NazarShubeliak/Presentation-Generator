"""Extract text and image frame measurements from the reference presentations
(native .ai, saved PDF-compatible).

Used for Work Package 4 (separating fixed from variable elements) and Work
Package 6 (deriving the master template's fonts/colours, since no official
CI package exists — see docs/open-questions.md #17). Reads every .ai in
reference/ and writes one JSON file per presentation to
docs/measurements/<presentation-name>.json, with one entry per artboard
(= slide): every text block's font, size, colour and bounding box; every
vector shape's fill/stroke colour, bounding box and approximate area; and
every image's placement bounding box. This is raw material for
docs/03-elements.md and docs/05-template.md, not the deliverable itself —
do not hand-copy it in, interpret it.
"""

import json
import re
import sys
from pathlib import Path

import fitz  # PyMuPDF

REFERENCE_DIR = Path(__file__).resolve().parent.parent / "reference"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "measurements"


def slugify(stem: str) -> str:
    name = stem.removeprefix("Presentation_")
    name = re.sub(r"\(\d+\)", "", name)
    name = re.sub(r"[^\w]+", "_", name, flags=re.UNICODE)
    return name.strip("_").lower()


def round_bbox(bbox) -> list:
    return [round(c, 1) for c in bbox]


def srgb_int_to_hex(color_int) -> str:
    """PyMuPDF encodes span colour as a single sRGB int (0xRRGGBB)."""
    if color_int is None:
        return None
    return f"#{color_int:06x}"


def color_tuple_to_hex(color) -> str:
    """PyMuPDF drawing fill/stroke colour is a (r, g, b) tuple, 0-1 floats."""
    if color is None:
        return None
    r, g, b = (round(c * 255) for c in color)
    return f"#{r:02x}{g:02x}{b:02x}"


def rect_area(bbox) -> float:
    x0, y0, x1, y1 = bbox
    return abs(x1 - x0) * abs(y1 - y0)


def extract_page(page: fitz.Page) -> dict:
    text_blocks = []
    for block in page.get_text("dict")["blocks"]:
        if block.get("type") != 0:  # 0 = text, 1 = image
            continue
        spans = []
        full_text_parts = []
        for line in block["lines"]:
            for span in line["spans"]:
                spans.append(
                    {
                        "text": span["text"],
                        "font": span["font"],
                        "size": round(span["size"], 2),
                        "color": srgb_int_to_hex(span.get("color")),
                        "bbox": round_bbox(span["bbox"]),
                    }
                )
                full_text_parts.append(span["text"])
            full_text_parts.append("\n")
        text_blocks.append(
            {
                "bbox": round_bbox(block["bbox"]),
                "text": "".join(full_text_parts).strip(),
                "spans": spans,
            }
        )

    images = [
        {
            "bbox": round_bbox(info["bbox"]),
            "native_width": info.get("width"),
            "native_height": info.get("height"),
        }
        for info in page.get_image_info()
    ]

    fills = []
    for drawing in page.get_drawings():
        bbox = drawing.get("rect")
        if bbox is None:
            continue
        bbox = round_bbox(bbox)
        area = rect_area(bbox)
        if area < 100:  # skip hairlines/tiny decorative strokes, not real fills
            continue
        fill_hex = color_tuple_to_hex(drawing.get("fill"))
        stroke_hex = color_tuple_to_hex(drawing.get("color"))
        if fill_hex is None and stroke_hex is None:
            continue
        fills.append(
            {
                "bbox": bbox,
                "area": round(area, 1),
                "fill": fill_hex,
                "stroke": stroke_hex,
            }
        )

    return {
        "page_size": round_bbox(page.rect),
        "text_blocks": text_blocks,
        "images": images,
        "fills": fills,
    }


def extract_ai(ai_path: Path) -> int:
    presentation_name = slugify(ai_path.stem)
    doc = fitz.open(ai_path)

    pages = []
    for page_index, page in enumerate(doc, start=1):
        page_data = extract_page(page)
        page_data["slide"] = page_index
        pages.append(page_data)
        print(f"  slide {page_index:02d}: "
              f"{len(page_data['text_blocks'])} text blocks, "
              f"{len(page_data['images'])} images")

    doc.close()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"{presentation_name}.json"
    out_path.write_text(
        json.dumps({"presentation": presentation_name, "pages": pages}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"{ai_path.name}: {len(pages)} slides -> {out_path.relative_to(OUTPUT_DIR.parent.parent)}")
    return len(pages)


def main() -> None:
    ai_files = sorted(REFERENCE_DIR.glob("*.ai"))
    if not ai_files:
        print(f"No .ai files found in {REFERENCE_DIR}", file=sys.stderr)
        sys.exit(1)

    for ai_path in ai_files:
        print(f"Extracting {ai_path.name} ...")
        extract_ai(ai_path)


if __name__ == "__main__":
    main()
