# Field Catalogue and Naming Convention (WP5)

Every piece of variable content from `docs/03-elements.md`, collected into one
list and given a single, unambiguous name — merged wherever two page types
turned out to need the same kind of value, per the task brief's own example
("the market name is one field, not eight").

## Naming convention

- English, upper snake case, prefixed by type: `TXT_` for text, `IMG_` for
  images.
- A field used **once per page occurrence** keeps a bare name (e.g.
  `TXT_THEME_WORLD_NAME`). A field that can occur **more than once within a
  single page occurrence** gets a `_N` suffix, `N` starting at 1 (e.g.
  `IMG_MOTIF_1_PHOTO`, `IMG_MOTIF_2_PHOTO`). This is the same convention
  already used for `PAGE_06_LOCAL_MOTIFS`'s motif rows.
- The same field name is reused across every page type where it means the
  same thing, even though each page *occurrence* carries its own value —
  this is what makes the merge real rather than cosmetic. Page types that
  repeat (`PAGE_03_THEME_SHOWCASE`, `PAGE_06_LOCAL_MOTIFS`) get a fresh set
  of field values per occurrence in the `pages` array (per the WP7 JSON
  shape), so reusing a name across occurrences never collides.

## Fields not included here, and why

Three elements that `docs/03-elements.md` originally listed as "variable"
turned out, after the designer's 2026-08-18 answers, not to need a WP5 field
at all. Documented here per ground rule 2 (decisions recorded even when they
seem obvious):

- **Market name standing alone** (`PAGE_09_SOCIAL_REACH`'s Instagram
  caption). The brief's own JSON shape already carries a top-level `city`
  field (see the WP7 example in the task assignment). Reusing that instead
  of adding a duplicate per-page `TXT_MARKET_NAME` field avoids exactly the
  kind of duplication WP5 step 3 warns against. The generator fills this
  caption from `city`, not from a page-level field.
- **`PAGE_04_REFERENCES` client-list footer.** Per the designer's
  2026-08-18 answer (`docs/open-questions.md` #5), the footer is the fixed
  client list minus the current deck's own market — computed by the
  generator from the fixed list (baked into the template) and top-level
  `city`/`location_name`, not an authored field.
- **`PAGE_06_LOCAL_MOTIFS`'s 70%-stats callout and rotating headline.**
  The designer's 2026-08-18 answers turned both into fixed boilerplate
  text, conditionally shown by the generator based on a table's position
  among its deck's motif tables (position 1 gets the stats callout +
  "Jede Karte..." headline; position 2 gets "Das nehmen..."). Not
  per-market content, so not a field — see `docs/03-elements.md`'s
  `PAGE_06_LOCAL_MOTIFS` section for the exact conditional text.
  **Position 3+ is unresolved** (`docs/open-questions.md` #15) — the
  generator's placeholder behaviour there is provisional until answered.
- **`PAGE_06_LOCAL_MOTIFS`'s intro paragraph (`TXT_MOTIF_INTRO`), reclassified
  2026-08-19.** Previously catalogued below as an authored field, but
  `docs/03-elements.md` already classified it as fixed/computed-by-position
  (same mechanism as the headline and stats callout above), and re-measuring
  all 5 decks confirms it: the wording is tied to table position, not chosen
  per market. Removed from the field table below. Exact per-position text is
  provisional pending `docs/open-questions.md` #22 (positions 1–2's wording
  disagrees across decks; position 3's is already confirmed by measurement).

## Text fields (`TXT_`)

| Field | Constraint | Mandatory | Used in | Example value |
|---|---|---|---|---|
| `TXT_TITLE_SUBLINE` | max. 95 characters | Yes | `PAGE_01_TITLE` | "KI- & AR-Erlebnisinstallationen für den Weihnachtsmarkt Magdeburg" |
| `TXT_THEME_WORLD_NAME` | max. 25 characters | Optional in `PAGE_01_TITLE`/`PAGE_02_SERVICE` (present only when the deck has >2 theme worlds, computed by the generator — see `docs/03-elements.md`); mandatory in `PAGE_06_LOCAL_MOTIFS`/`PAGE_08_TRANSITION` | `PAGE_01_TITLE`, `PAGE_02_SERVICE`, `PAGE_06_LOCAL_MOTIFS`, `PAGE_08_TRANSITION` | "Kaiser-Otto-Pfalz" |
| `TXT_THEME_WORLD_NAME_1` | max. 25 characters | Yes | `PAGE_03_THEME_SHOWCASE` | "Luther & Reformation" |
| `TXT_THEME_WORLD_NAME_2` | max. 25 characters | Optional — present only on a 2-up slide | `PAGE_03_THEME_SHOWCASE` | "Händelstadt Halle" |
| `TXT_MOTIF_1_NAME` | max. 30 characters | Yes | `PAGE_06_LOCAL_MOTIFS` | "Rudolph" |
| `TXT_MOTIF_2_NAME` | max. 30 characters | Optional — a table can have 1–3 motif rows | `PAGE_06_LOCAL_MOTIFS` | "Adalbert von Magdeburg" |
| `TXT_MOTIF_3_NAME` | max. 30 characters | Optional | `PAGE_06_LOCAL_MOTIFS` | "Schneekönigin" |
| `TXT_KIOSK_BACKGROUND_LABEL` | max. 30 characters (provisional — not separately measured in WP4) | Yes | `PAGE_05_USER_FLOW` | "Kaiser-Otto-Pfalz" |

`TXT_KIOSK_BACKGROUND_LABEL` note: `docs/02-page-types.md`'s QC rule 4.4
lists "background-choice labels shown in the kiosk-interface screenshot" as
a per-market-variable element distinct from the screenshot image itself.
**Confirmed by the designer 2026-08-20** (`docs/open-questions.md` #21):
this is a real, separate text field, not baked into `IMG_KIOSK_SCREENSHOT`
(the source decks just never showed it as its own text object). Filled from
a brief listing characters, places, and defined landmarks per market,
supplied in advance of generation — not authored freehand per field.

## Image fields (`IMG_`)

| Field | Constraint | Mandatory | Used in | Example value |
|---|---|---|---|---|
| `IMG_THEME_WORLD_PHOTO` | `PAGE_01_TITLE`: full-bleed 16:9 (source was 4:3, see `docs/03-elements.md`). `PAGE_02_SERVICE`: 4:3, frame ratio 1.33 | Yes | `PAGE_01_TITLE`, `PAGE_02_SERVICE` | `images/magdeburg_kaiser_otto_pfalz.jpg` |
| `IMG_THEME_WORLD_PHOTO_1` | 4:3, frame ratio 1.33 | Yes | `PAGE_03_THEME_SHOWCASE` | `images/halle_luther_reformation.jpg` |
| `IMG_THEME_WORLD_PHOTO_2` | 4:3, frame ratio 1.33 | Optional — present only on a 2-up slide | `PAGE_03_THEME_SHOWCASE` | `images/halle_haendelstadt.jpg` |
| `IMG_MOTIF_1_PHOTO` / `IMG_MOTIF_1_BACKGROUND` / `IMG_MOTIF_1_MASK` | Aspect ratio **not yet measured** — see open question | Yes | `PAGE_06_LOCAL_MOTIFS` | `images/magdeburg_rudolph_photo.jpg` |
| `IMG_MOTIF_2_*` / `IMG_MOTIF_3_*` (same 3 sub-fields each) | Same as above | Optional, matching `TXT_MOTIF_2_NAME`/`TXT_MOTIF_3_NAME` | `PAGE_06_LOCAL_MOTIFS` | — |
| `IMG_KIOSK_SCREENSHOT` | Frame ratio 1.45 | Yes | `PAGE_05_USER_FLOW` | `images/magdeburg_kiosk.png` |
| `IMG_USER_FLOW_CARD_1` / `IMG_USER_FLOW_CARD_2` | Individual aspect ratio not yet determined — see note below | Yes | `PAGE_05_USER_FLOW` | `images/magdeburg_card_example_1.jpg` |
| `IMG_OUTPUT_CARD_1` / `IMG_OUTPUT_CARD_2` | Frame ratio 1.55 | Yes | `PAGE_08_TRANSITION` | `images/magdeburg_output_card_1.jpg` |
| `IMG_INSTAGRAM_MOCKUP` | Frame ratio 1.33 | Yes | `PAGE_09_SOCIAL_REACH` | `images/magdeburg_instagram_mockup.jpg` |
| `IMG_LANDMARK_PHOTO` | Frame ratio 0.559 (portrait) | Yes | `PAGE_10_CONTACT` | `images/magdeburg_dom.jpg` |

**Correction (2026-08-18, made while starting WP6):** an earlier draft of
this table had a separate `IMG_HERO_PHOTO` field for `PAGE_01_TITLE`,
reasoning it was conceptually different from `IMG_THEME_WORLD_PHOTO`. That
was wrong — `docs/02-page-types.md`'s own Halle worked example shows
theme world #1's photo *is* the title slide's cover photo, the same
image, not two separate assets ("1. Historisches Halle → `PAGE_01_TITLE`
cover photo"). Removed the duplicate field; `IMG_THEME_WORLD_PHOTO` alone
covers `PAGE_01_TITLE` (full-bleed frame), `PAGE_02_SERVICE` (booth-photo
frame) and `PAGE_03_THEME_SHOWCASE` (booth-photo frame, ×1–2) — same
field, different frame per page type, consistent with how every other
reused field in this catalogue already works.

## Open items carried from WP4, still unresolved

**Status 2026-08-20: all designer-side questions for this catalogue are
now answered** (`docs/open-questions.md` #18–#25). What's left is
PowerPoint-layout-time work, not something the designer needs to weigh in
on again — see `docs/open-questions.md` for full context, not repeated
here:

- `IMG_MOTIF_1/2/3_PHOTO`/`_BACKGROUND`/`_MASK` aspect ratios — the source
  decks only measured the flattened 3×3 table image, which no longer
  applies once the table is composed from 9 separate images (designer's
  resolved architecture, `docs/open-questions.md` #9). Real per-cell ratios
  need measuring once WP6's template defines the actual cell frames.
- `IMG_USER_FLOW_CARD_1`/`_2` individual aspect ratio — count (2) and
  arrangement (vertical stack) are confirmed (`docs/open-questions.md`
  #20), but the only ratio ever measured (1.78) was for the old
  side-by-side flattened image and doesn't transfer to a vertical stack.
  Decide once this layout is laid out in PowerPoint.

**Resolved 2026-08-18/2026-08-20, no longer open:** `IMG_USER_FLOW_CARD_1`/`_2`
count (2 cards) and arrangement (vertical stack, `docs/open-questions.md`
#20); `TXT_KIOSK_BACKGROUND_LABEL` confirmed as a real field (#21);
`PAGE_06_LOCAL_MOTIFS`'s headline/subheadline rotation entirely rewritten
and finalized (#22) — see `docs/03-elements.md`/`docs/05-template.md` for
the new wording, the old "position 3+" question this file used to track no
longer applies since the whole rotation scheme it referred to was replaced.

None of the remaining items block starting WP6/WP7 — they only affect the
exact schema shape for `PAGE_06_LOCAL_MOTIFS`'s per-cell images and
`PAGE_05_USER_FLOW`'s card images, both PowerPoint-layout decisions.
