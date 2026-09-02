"""Throwaway helper: build one blank slide per layout from a given .pptx
template and export each as a PNG via PowerPoint COM, so the layouts can be
visually reviewed. Not a project deliverable, gitignored / not committed.

Usage: python src/_preview_layouts.py <template.pptx> <out_dir>
"""

import sys
from pathlib import Path

from pptx import Presentation


def build_preview_deck(template_path: Path, tmp_path: Path):
    prs = Presentation(str(template_path))
    while len(prs.slides) > 0:
        rId = prs.slides._sldIdLst[0].get(
            "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
        )
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[0]

    layout_names = []
    for master in prs.slide_masters:
        for layout in master.slide_layouts:
            prs.slides.add_slide(layout)
            layout_names.append(layout.name)

    prs.save(str(tmp_path))
    return layout_names


def export_png(pptx_path: Path, out_dir: Path):
    import win32com.client

    out_dir.mkdir(parents=True, exist_ok=True)
    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
    powerpoint.Visible = True
    presentation = powerpoint.Presentations.Open(str(pptx_path.resolve()), WithWindow=False)
    presentation.SaveAs(str(out_dir.resolve()), 17)  # 17 = ppSaveAsPNG (exports all slides)
    presentation.Close()
    powerpoint.Quit()


def main():
    template_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    tmp_path = template_path.parent / f"_preview_{template_path.stem}.pptx"

    layout_names = build_preview_deck(template_path, tmp_path)
    for i, name in enumerate(layout_names, start=1):
        print(f"slide {i}: {name}")

    export_png(tmp_path, out_dir)
    print("exported to", out_dir)


if __name__ == "__main__":
    main()
