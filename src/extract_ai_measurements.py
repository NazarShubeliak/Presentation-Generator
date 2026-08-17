"""Extract text and image frame measurements from the reference presentations
(native .ai, saved PDF-compatible).

Used for Work Package 4 (separating fixed from variable elements). Reads
every .ai in reference/ and writes one JSON file per presentation to
docs/measurements/<presentation-name>.json, with one entry per artboard
(= slide): every text block's font, size and bounding box, and every
image's placement bounding box. This is raw material for docs/03-elements.md,
not the deliverable itself — do not hand-copy it in, interpret it.
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

    return {
        "page_size": round_bbox(page.rect),
        "text_blocks": text_blocks,
        "images": images,
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
