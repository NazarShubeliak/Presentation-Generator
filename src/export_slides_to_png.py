"""Export every page of the reference presentations (PDF) as PNG images.

Used for Work Package 2 (slide inventory). Reads every .pdf in reference/
and writes one PNG per page to docs/slides/<presentation-name>/slide_NN.png,
so nothing gets missed or renumbered by hand.
"""

import re
import sys
from pathlib import Path

import fitz  # PyMuPDF

REFERENCE_DIR = Path(__file__).resolve().parent.parent / "reference"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "slides"
DPI = 200


def slugify(stem: str) -> str:
    name = stem.removeprefix("Presentation_")
    name = re.sub(r"\(\d+\)", "", name)
    name = re.sub(r"[^\w]+", "_", name, flags=re.UNICODE)
    return name.strip("_").lower()


def export_pdf(pdf_path: Path) -> int:
    presentation_name = slugify(pdf_path.stem)
    out_dir = OUTPUT_DIR / presentation_name
    out_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    zoom = DPI / 72
    matrix = fitz.Matrix(zoom, zoom)

    for page_index, page in enumerate(doc, start=1):
        pixmap = page.get_pixmap(matrix=matrix)
        out_path = out_dir / f"slide_{page_index:02d}.png"
        pixmap.save(out_path)
        print(f"  slide {page_index:02d} -> {out_path.relative_to(OUTPUT_DIR.parent.parent)}")

    doc.close()
    print(f"{pdf_path.name}: {page_index} slides exported to {out_dir}")
    return page_index


def main() -> None:
    pdf_files = sorted(REFERENCE_DIR.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in {REFERENCE_DIR}", file=sys.stderr)
        sys.exit(1)

    for pdf_path in pdf_files:
        print(f"Exporting {pdf_path.name} ...")
        export_pdf(pdf_path)


if __name__ == "__main__":
    main()
