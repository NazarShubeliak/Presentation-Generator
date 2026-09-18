"""Renders one slide from the GUI's in-progress form data to a PNG, so a
market can see roughly what a slide will look like without running a full
generation and opening the download in PowerPoint.

Reuses build_presentation.build_slide() for the actual content-filling —
same function main() calls in its per-slide loop — so the preview can never
drift from what a real `Generate` would produce; only the final PNG
rasterisation step is preview-specific, done via PowerPoint COM automation
(the same proven method already used for this project's QA screenshots, see
src/_preview_layouts.py).

Safety note: uses DispatchEx (not plain Dispatch) to force a *new* PowerPoint
process rather than possibly attaching to one the user already has open on
their desktop — Dispatch() can silently reuse a running instance via the
Running Object Table, and this module's own .Quit() at the end would then
close whatever the user had open, unsaved work included. DispatchEx forces
a fresh process, so .Quit() only ever closes the instance this module
started.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
import build_presentation as bp  # noqa: E402 (sys.path must be set up first)

from pptx import Presentation  # noqa: E402

PREVIEW_TMP_DIR = PROJECT_ROOT / "output" / "_gui_preview_tmp"


class PreviewError(Exception):
    pass


def render_slide_png(template_path: Path, data: dict, page_index: int):
    """Returns (png_path, log_lines) for data['pages'][page_index], built
    against template_path exactly as build_presentation.py would build that
    same slide as part of a full deck."""
    pages = data.get("pages", [])
    if not (0 <= page_index < len(pages)):
        raise PreviewError(f"page_index {page_index} out of range (deck has {len(pages)} slides)")

    page = pages[page_index]
    page_type = page["page_type"]
    fields = page.get("fields", {})

    # PAGE_06_LOCAL_MOTIFS's computed headline/subheadline/stats depend on
    # which occurrence *within the whole deck* this is (see MOTIF_POSITION_
    # CONTENT in build_presentation.py) — derive it the same way main()'s
    # running counter would, from every PAGE_06 entry up to and including
    # this one, not just this single page in isolation.
    motif_position = None
    if page_type == "PAGE_06_LOCAL_MOTIFS":
        motif_position = sum(
            1 for p in pages[: page_index + 1] if p.get("page_type") == "PAGE_06_LOCAL_MOTIFS"
        )

    tmp_dir = PREVIEW_TMP_DIR
    tmp_dir.mkdir(parents=True, exist_ok=True)
    export_dir = tmp_dir / "export"
    export_dir.mkdir(exist_ok=True)
    for old in export_dir.glob("*"):
        old.unlink()

    prs = Presentation(str(template_path))
    log_lines = []
    bp.build_slide(
        prs, page_type, fields, base_dir=PROJECT_ROOT, tmp_dir=tmp_dir, log=log_lines.append,
        city=data.get("city"), theme_worlds=data.get("theme_worlds"), motif_position=motif_position,
    )
    if len(prs.slides) == 0:
        raise PreviewError(f"template has no layout named {page_type}")

    pptx_path = tmp_dir / "preview.pptx"
    prs.save(str(pptx_path))

    _export_first_slide_png(pptx_path, export_dir)
    # PowerPoint names the exported file after its own UI language (e.g.
    # "Слайд1.PNG" on Ukrainian-locale PowerPoint, not "Slide1.PNG") — don't
    # assume an English name, just take whatever single file export_dir now
    # has (it was emptied right before SaveAs, and the source has exactly
    # one slide).
    exported = list(export_dir.glob("*"))
    if not exported:
        raise PreviewError("PowerPoint export did not produce an image")
    png_path = exported[0]

    log_text = f"Slide 1: {page_type}\n" + "\n".join(log_lines)
    return png_path, log_text


def _powerpoint_already_running() -> bool:
    import subprocess

    out = subprocess.run(
        ["tasklist", "/FI", "IMAGENAME eq POWERPNT.EXE"],
        capture_output=True, text=True,
    ).stdout
    return "POWERPNT.EXE" in out


def _export_first_slide_png(pptx_path: Path, export_dir: Path):
    import pythoncom
    import win32com.client

    # Measured empirically (see git history around this line): tried
    # DispatchEx() to force a separate process from any PowerPoint the user
    # already has open, expecting .Quit() below to then only ever affect our
    # own instance. It doesn't work — PowerPoint enforces single-instance
    # regardless of the dispatch method, so DispatchEx silently attached to
    # the user's already-running PowerPoint anyway, and .Quit() closed their
    # real window, unsaved work and all. The only safe policy: check whether
    # PowerPoint was already running *before* we touch it, and only call
    # .Quit() if we're the ones who started it — otherwise leave the shared
    # instance alone and just close the one presentation we opened.
    was_running = _powerpoint_already_running()

    pythoncom.CoInitialize()
    try:
        powerpoint = win32com.client.Dispatch("PowerPoint.Application")
        powerpoint.Visible = True
        try:
            presentation = powerpoint.Presentations.Open(str(pptx_path.resolve()), WithWindow=False)
            try:
                presentation.SaveAs(str(export_dir.resolve()), 18)  # 18 = ppSaveAsPNG (17 is ppSaveAsJPG)
            finally:
                presentation.Close()
        finally:
            if not was_running:
                powerpoint.Quit()
    finally:
        pythoncom.CoUninitialize()
