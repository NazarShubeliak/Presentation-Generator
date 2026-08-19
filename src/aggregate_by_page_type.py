"""Group the per-deck measurement JSONs (docs/measurements/*.json, produced by
extract_ai_measurements.py) by page type, using the slide-to-page-type mapping
derived from docs/01-slide-inventory.md and docs/02-page-types.md.

Used for Work Package 4 (separating fixed from variable elements). Output is
raw material for docs/03-elements.md, not the deliverable itself.
"""

import json
from pathlib import Path

MEASUREMENTS_DIR = Path(__file__).resolve().parent.parent / "docs" / "measurements"
OUTPUT_PATH = MEASUREMENTS_DIR / "by_page_type.json"

# slide number (1-based) -> page_type, per deck. Derived from
# docs/01-slide-inventory.md (re-reviewed 2026-08-17 for Magdeburg).
SLIDE_MAP = {
    "basel_2026": {
        1: "PAGE_01_TITLE",
        2: "PAGE_02_SERVICE",
        3: "PAGE_03_THEME_SHOWCASE",
        4: "PAGE_04_REFERENCES",
        5: "PAGE_05_USER_FLOW",
        6: "PAGE_06_LOCAL_MOTIFS",
        7: "PAGE_06_LOCAL_MOTIFS",
        8: "PAGE_06_LOCAL_MOTIFS",
        9: "PAGE_07_BESTSELLERS",
        10: "PAGE_08_TRANSITION",
        11: "PAGE_09_SOCIAL_REACH",
        12: "PAGE_10_CONTACT",
    },
    "erzgebirgsdorf_auf_dem_düsseldorfer_platz_2026": {
        1: "PAGE_01_TITLE",
        2: "PAGE_02_SERVICE",
        3: "PAGE_04_REFERENCES",
        4: "PAGE_05_USER_FLOW",
        5: "PAGE_06_LOCAL_MOTIFS",
        6: "PAGE_07_BESTSELLERS",
        7: "PAGE_08_TRANSITION",
        8: "PAGE_09_SOCIAL_REACH",
        9: "PAGE_10_CONTACT",
    },
    "freiburger_weihnachtsmarkt_2026": {
        1: "PAGE_01_TITLE",
        2: "PAGE_02_SERVICE",
        3: "PAGE_04_REFERENCES",
        4: "PAGE_05_USER_FLOW",
        5: "PAGE_06_LOCAL_MOTIFS",
        6: "PAGE_06_LOCAL_MOTIFS",
        7: "PAGE_07_BESTSELLERS",
        8: "PAGE_08_TRANSITION",
        9: "PAGE_09_SOCIAL_REACH",
        10: "PAGE_10_CONTACT",
    },
    "helle_hallescher_weihnachtsmarkt_2026": {
        1: "PAGE_01_TITLE",
        2: "PAGE_03_THEME_SHOWCASE",
        3: "PAGE_02_SERVICE",
        4: "PAGE_03_THEME_SHOWCASE",
        5: "PAGE_04_REFERENCES",
        6: "PAGE_05_USER_FLOW",
        7: "PAGE_06_LOCAL_MOTIFS",
        8: "PAGE_06_LOCAL_MOTIFS",
        9: "PAGE_06_LOCAL_MOTIFS",
        10: "PAGE_06_LOCAL_MOTIFS",
        11: "PAGE_06_LOCAL_MOTIFS",
        12: "PAGE_08_TRANSITION",
        13: "PAGE_07_BESTSELLERS",
        14: "PAGE_09_SOCIAL_REACH",
        15: "PAGE_10_CONTACT",
    },
    "magdeburger_weihnachtsmarkt_2026": {
        1: "PAGE_01_TITLE",
        2: "PAGE_02_SERVICE",
        3: "PAGE_03_THEME_SHOWCASE",
        4: "PAGE_03_THEME_SHOWCASE",
        5: "PAGE_04_REFERENCES",
        6: "PAGE_05_USER_FLOW",
        7: "PAGE_06_LOCAL_MOTIFS",
        8: "PAGE_06_LOCAL_MOTIFS",
        9: "PAGE_06_LOCAL_MOTIFS",
        10: "PAGE_06_LOCAL_MOTIFS",
        11: "PAGE_06_LOCAL_MOTIFS",
        12: "PAGE_06_LOCAL_MOTIFS",
        13: "PAGE_07_BESTSELLERS",
        14: "PAGE_08_TRANSITION",
        15: "PAGE_09_SOCIAL_REACH",
        16: "PAGE_10_CONTACT",
    },
}


def main() -> None:
    by_page_type = {}

    for deck_name, slide_to_type in SLIDE_MAP.items():
        deck_path = MEASUREMENTS_DIR / f"{deck_name}.json"
        deck_data = json.loads(deck_path.read_text(encoding="utf-8"))
        pages_by_slide = {p["slide"]: p for p in deck_data["pages"]}

        for slide_num, page_type in slide_to_type.items():
            page = pages_by_slide[slide_num]
            entry = {
                "deck": deck_name,
                "slide": slide_num,
                "page_size": page["page_size"],
                "text_blocks": page["text_blocks"],
                "images": page["images"],
                "fills": page.get("fills", []),
            }
            by_page_type.setdefault(page_type, []).append(entry)

    OUTPUT_PATH.write_text(
        json.dumps(by_page_type, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    for page_type, entries in sorted(by_page_type.items()):
        print(f"{page_type}: {len(entries)} instances "
              f"across {len(set(e['deck'] for e in entries))} decks")
    print(f"\nWritten to {OUTPUT_PATH.relative_to(OUTPUT_PATH.parent.parent.parent)}")


if __name__ == "__main__":
    main()
