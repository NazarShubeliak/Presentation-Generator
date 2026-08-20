# PowerPoint Master Template (WP6)

**Status: in progress.** This document will end up recording, per the task
brief's WP6 step 7, which placeholder in which layout corresponds to which
field from `docs/04-fields.md`. That mapping is built one page type at a
time as `templates/master_v01.pptx` is built by hand in PowerPoint (Slide
Master view + Selection Pane) — python-pptx cannot create new slide layouts,
so the template itself has to be built in the desktop app, per the task
brief's own warning.

## Derived CI baseline — no official package exists

Per `docs/open-questions.md` #17: there is no separate CI/brand package.
Martin's answer (2026-08-18) was to build the template ourselves. The
fonts and colours below are **derived by measurement from the 5 reference
`.ai` files**, not supplied — documented here as a design decision per
ground rule 2, not something to re-derive or second-guess later.

Tooling: `src/extract_ai_measurements.py` (extended 2026-08-18 to also
capture text colour and vector fill/stroke colour, not just font/size/bbox)
and `src/aggregate_by_page_type.py`. Raw output in `docs/measurements/`
(gitignored). Counts below are span/fill occurrences across all 5 decks
combined.

### Fonts

| Font | Role | Observed sizes (most common) |
|---|---|---|
| `MyriadPro-Regular` | Body text | 8–14pt (8.34, 11.13, 11.87, 12, 14 most common) |
| `HelveticaNeue-CondensedB` | Headlines / bold labels | 24–29pt for headlines, 8.5–12pt for small bold labels (e.g. table headers, step numbers) |
| `CoreSerifN-75Black` | Accent / display | 20–36pt, used more sparingly — large emphasis text |

`HelveticaNeueBlackConden` also appears (31 spans) — this is the already-
documented font-substitution artifact in the Erzgebirgsdorf file (see
`docs/03-elements.md`, `PAGE_07_BESTSELLERS`), not a 4th real font. Treat
`HelveticaNeue-CondensedB` as canonical.

**Not yet mapped:** which font/size combination is used by which specific
text element per page type (e.g. exact headline vs. body vs. caption
sizes). Will be resolved page-type-by-page-type as the template is built,
cross-referencing `docs/03-elements.md`'s per-element character counts
against `docs/measurements/by_page_type.json`.

### Colours

| Hex | Role | Basis |
|---|---|---|
| `#f2eae0` | **Slide background** (all content page types) | Confirmed: full-page (720×540pt) fill on every measured `PAGE_02`–`PAGE_10` instance across all 5 decks, no exceptions. |
| `#231f20` | **Primary text colour** | Dominant text colour, 603 of ~700 measured text spans. |
| `#c5923b` | **Primary accent** (gold) | Dominant fill colour on non-background shapes, 598 occurrences — used for numbered circles, table header bars, underlines/highlights. |
| `#fcb657` | Secondary accent (lighter gold) | Minor use (6 occurrences), likely a hover/variant shade of the primary accent. |
| `#0d1216` / `#001319` | Dark accent panels | 312 / 145 fill occurrences — near-black/navy, used for smaller dark panel fills, not the page background. |
| `#ffffff` | Text/elements on dark fills | 9 text spans, 14 shape fills. |
| `#000000` | Pure black, minor use | 9 text spans — likely a specific small element, not the primary text colour (`#231f20` is warmer/softer black, dominant). |

**Not part of the fixed palette — varies per deck:** `PAGE_01_TITLE`'s
title slide has a colour-tinted rectangle behind the headline (bbox
≈[15–20, 20–25, 475–500, 145–165], area ≈55–75k) that differs per deck:
`#5d9fd6` (Basel), `#90a6c5` (Freiburg), `#040d31` (Halle), `#1c66b0`
(Magdeburg). Reads as a photo-matched overlay tint for text legibility,
not a brand colour — do not standardize this into the fixed palette;
treat as photo-dependent, likely something the generator or template
computes/samples per hero photo rather than a fixed value. Flag for the
designer if a fixed treatment is actually wanted here instead.

### Logo

**No standalone logo image found** in any of the 5 reference `.ai` files —
checked for a raster image at a consistent position/size repeated across
a deck's slides (the usual signature of a corner logo/watermark) and found
none. "cosmoproducts GmbH" on `PAGE_10_CONTACT` appears to be styled text,
not an embedded logo graphic. **Open question for Martin/designer, not yet
asked:** is there a logo mark that should appear on the master template
(e.g. slide master footer, title slide), given none is visible in the
source decks? Needs answering before the slide master step (WP6 step 2) is
fully complete — can proceed with layouts/placeholders in the meantime
since this only affects the master, not per-layout placeholder mapping.

### Slide dimensions

Source artboards: 720×540pt (4:3). New template: 16:9 (WP6 step 1) —
standard PowerPoint 16:9 is 960×540pt (13.333″×7.5″). None of the source
frame ratios measured in `docs/03-elements.md` transfer 1:1 — they're a
starting reference for what the source used, to be re-checked once each
layout is actually laid out in 16:9.

---

## Per-page-type placeholder mapping

To be filled in as each layout is built in PowerPoint, one page type at a
time. Format per page type: layout name (= page type ID, per WP6 step 3),
then a table of placeholder name (= WP5 field name, set via the Selection
Pane) → placeholder type → notes, plus the fixed content to fill in
directly (verbatim from `docs/03-elements.md`).

### PAGE_01_TITLE

Reference: `docs/02-page-types.md` (purpose), `docs/03-elements.md`
(measurements), `docs/04-fields.md` (field definitions).

**Fixed content — type directly into the layout, not a placeholder:**

| Element | Content |
|---|---|
| Headline (text box) | "Wir machen Ihre Besucher zu einem Teil Ihrer Geschichte." |

**Placeholders — name exactly as shown, via Selection Pane:**

| Placeholder name | Type | Notes |
|---|---|---|
| `IMG_THEME_WORLD_PHOTO` | Picture Placeholder | Full-bleed, behind all other content — covers the entire 16:9 slide. Source decks used a 4:3 photo cropped/bled to fill a 4:3 canvas (`docs/03-elements.md`); for 16:9 this will need a wider crop or a blurred/extended edge treatment — flag for the designer if a hard crop looks wrong once real photos are tested. |
| `TXT_TITLE_SUBLINE` | Text Placeholder | Max 95 characters (`docs/04-fields.md`). Sits below/over the headline. |
| `TXT_THEME_WORLD_NAME` | Text Placeholder | **Optional** — per `docs/03-elements.md`, only 3 of 5 source decks have this caption at all (present only when the deck has >2 theme worlds; computed by the generator, not authored — `docs/open-questions.md` #12). Build the placeholder anyway so WP8 can choose to fill or skip it; do not treat its absence in 2 of 5 decks as "delete this placeholder from the layout." Max 25 characters. |

**Not yet resolved before this layout can be called final:**
- Photo crop treatment for 4:3 source → 16:9 full-bleed target (above).
- Logo placement, if any (`docs/open-questions.md` #18) — likely a slide
  master element rather than something specific to this layout, but
  affects every layout including this one.

---

### PAGE_02_SERVICE

Reference: `docs/02-page-types.md` (purpose), `docs/03-elements.md`
(measurements), `docs/04-fields.md` (field definitions). Exact wording and
per-run formatting below re-verified directly against
`docs/measurements/by_page_type.json` (all 5 decks byte-identical except
Erzgebirgsdorf's headline, already resolved as an outlier).

**Fixed content — type directly into the layout, not a placeholder:**

| Element | Content | Formatting note |
|---|---|---|
| Headline (text box) | "Ihr Erlebnispartner —\nvon Konzept bis\nBetreuung vor Ort." | `HelveticaNeue-CondensedB`, 29.2pt, `#231f20`. 3 manual line breaks as shown. |
| Body paragraph (text box) | "Wir entwickeln individuelle KI- & AR-Erlebniswelten für Weihnachtsmärkte — und schaffen dabei mehrere vernetzte Erlebnisstationen auf dem gesamten Markt." | `MyriadPro-Regular`, 11.87pt, `#231f20`. |
| Bullet 1 (text box) | "**Erlebniskonzept und 3D-Masken** werden individuell für den jeweiligen Markt entwickelt." | Lead-in run bold (`HelveticaNeue-CondensedB` 12pt), rest regular (`MyriadPro-Regular` 12pt) — same pattern all 3 bullets, both colours `#231f20`. |
| Bullet 2 (text box) | "**Hüttendesign, Technik und Aufbau** werden vollständig durch uns realisiert." | Same bold-lead-in pattern as bullet 1. |
| Bullet 3 (text box) | "**Wir stellen eigenes Personal vor Ort** - der Marktleiter kümmert sich um nichts." | Same bold-lead-in pattern as bullet 1. |

**Placeholders — name exactly as shown, via Selection Pane:**

| Placeholder name | Type | Notes |
|---|---|---|
| `IMG_THEME_WORLD_PHOTO` | Picture Placeholder | Booth photo, right ~55-60% of the slide (text column occupies the left ~40%, x≈25-300 of 720pt source canvas). Source frame ratio 4:3 in the two decks not using an oversized bleed source (Basel, Freiburg); **target 4:3**, same field/ratio as `PAGE_01_TITLE`. |
| `TXT_THEME_WORLD_NAME` | Text Placeholder | Same field as `PAGE_01_TITLE`'s caption — **optional**, present only when the deck has >2 theme worlds (2 of 5 source decks: Halle "Märchen- und Familienwelt", Magdeburg "Märchengasse"). Overlaid on the photo, bottom-right corner (observed bbox roughly x 410-685, y 424-443 of the 720×540 source canvas — right-edge-anchored, grows leftward with caption length). Max 25 characters. Build the placeholder regardless of source-deck presence, same rule as `PAGE_01_TITLE`. |

**Not yet resolved before this layout can be called final:**
- Photo crop treatment for 4:3 source → 16:9 target (same open item as
  `PAGE_01_TITLE`, applies here too since it's the same field/ratio).
- Logo placement, if any (`docs/open-questions.md` #18) — slide-master-level,
  affects every layout.

---

### PAGE_03_THEME_SHOWCASE

Reference: `docs/02-page-types.md` (purpose, the "overflow slot" rule),
`docs/03-elements.md` (measurements), `docs/04-fields.md` (field
definitions). Confirmed schema shape: array of 1–2 theme entries, layout
(single vs. 2-up) picked automatically by array length
(`docs/open-questions.md` #11).

**Fixed content:** none — this page type has no headline or body copy, only
a full-bleed photo (or 2-up photo pair) and per-theme caption(s).

**Placeholders — name exactly as shown, via Selection Pane:**

| Placeholder name | Type | Notes |
|---|---|---|
| `IMG_THEME_WORLD_PHOTO_1` | Picture Placeholder | Full-bleed (or left half of a 2-up pair). Source frame ratio 4:3 for the single-photo layout. |
| `IMG_THEME_WORLD_PHOTO_2` | Picture Placeholder | **Optional** — present only when the array has 2 entries (2-up layout, right half). |
| `TXT_THEME_WORLD_NAME_1` | Text Placeholder | Mandatory. Max 25 characters. |
| `TXT_THEME_WORLD_NAME_2` | Text Placeholder | **Optional** — present only on a 2-up slide, matching `IMG_THEME_WORLD_PHOTO_2`. Max 25 characters (max 55 if the template ends up rendering both names as one combined caption instead of two separate ones — see below). |

**Not yet resolved before this layout can be called final — do not guess a
value for either of these, both need a designer decision:**
- **Caption styling has no consistent precedent to copy.** Measured across
  the 3 decks that have this page type, no two instances share the same
  font, colour, or position (top-left large headline-style in Basel vs.
  bottom small caption-style in Halle/Magdeburg, and Halle vs. Magdeburg's
  2-up captions don't even match each other) — logged as
  `docs/open-questions.md` #19. Needs a designer decision on the canonical
  treatment before this layout's text placeholder can be styled.
- **2-up photo split.** Source `.ai` files render the 2-up pair as a single
  flattened bleed image per slide, not two independently-placed photo
  frames — the actual left/right split ratio isn't measurable from the
  source and needs to be decided directly in the PowerPoint layout (e.g. an
  even 50/50 vertical split is the natural default, but confirm once this
  layout is actually laid out, per `docs/03-elements.md`'s existing note on
  this page type).
- Photo crop treatment for 4:3 source → 16:9 target (same open item carried
  from `PAGE_01_TITLE`/`PAGE_02_SERVICE`).
- Logo placement, if any (`docs/open-questions.md` #18) — slide-master-level.

---

### PAGE_04_REFERENCES

Reference: `docs/02-page-types.md` (purpose), `docs/03-elements.md`
(measurements, incl. a 2026-08-19 data-quality note on Halle's footer),
`docs/04-fields.md` ("Fields not included here" section — this page type
deliberately has zero WP5 fields). Confirmed byte-identical across 4 of 5
decks (Halle's footer is a one-off bug, not a variant — see
`docs/03-elements.md`); this is the most boilerplate page type measured so
far.

**Fixed content — type directly into the layout, not a placeholder:**

| Element | Content | Formatting note |
|---|---|---|
| Headline (text box) | "Jeder Markt bekommt seine eigene Welt." | `HelveticaNeue-CondensedB`, 29.2pt, `#231f20`. |
| Intro line (text box) | "Wir entwickeln Hüttendesign, Masken und Erlebniswelt individuell — passend zur Identität Ihres Markts." | `MyriadPro-Regular`, 11.87pt, `#231f20`. |
| Caption row 1 (text box) | "**Historischer Markt** — Mozart · Komponist · Hofmusiker.\n**Märchenmarkt** — Das tapfere Schneiderlein · Prinzessin · König." | Same bold-lead-in pattern as `PAGE_02_SERVICE`'s bullets: theme name bold (`HelveticaNeue-CondensedB` 8.5pt), "— description" regular (`MyriadPro-Regular` 8.5pt). Both colour `#231f20`. |
| Caption row 2 (text box) | "**Barock & Schloss** — Markgraf · Hofdame · Venezianische Maskenfigur.\n**Regionale Identität** — Erzgebirgsmännchen · Bergmann · Winzermeister." | Same bold-lead-in pattern. Canonical full-suffix version confirmed by designer (`docs/open-questions.md` #4) — do not use the shorter "Barock & Schloss" alone seen in 3/5 source decks. |
| 4 example-theme photos + background collage photo | Cross-client portfolio images (Salzburg/Kassel/Charlottenburg/Erzgebirge-themed), explicitly not location-specific per the task brief | Fixed, boilerplate — bake directly into the layout as static pictures, no picture placeholders. (Source `.ai` files are inconsistent about whether this is 1 flattened montage image or up to 5 separate images per deck — irrelevant here since either way the content is identical and static, unlike `PAGE_06_LOCAL_MOTIFS`'s flattened-vs-per-cell question which mattered because that content is per-market.) |

**Placeholders — name exactly as shown, via Selection Pane:**

| Placeholder name | Type | Notes |
|---|---|---|
| `TXT_REFERENCES_FOOTER` | Text Placeholder | **Not a WP5 field** (deliberately excluded, see `docs/04-fields.md`) — this text is never authored in the input JSON, it's computed by the WP8 generator as the fixed client list minus the current deck's own market name (`docs/03-elements.md`). Still needs a named placeholder here so WP8 has somewhere to write the computed string. `MyriadPro-Regular`, 10.83pt, `#231f20`. |

**Not yet resolved before this layout can be called final:**
- Logo placement, if any (`docs/open-questions.md` #18) — slide-master-level.
- None of this page type's own content is blocked — it's fully fixed except
  the computed footer, which has a settled generation rule.

---

### PAGE_05_USER_FLOW

Reference: `docs/02-page-types.md` (purpose), `docs/03-elements.md`
(measurements), `docs/04-fields.md` (field definitions). Canonical text
below is "Variant B" (`docs/open-questions.md` #6) — pulled from Halle's
instance specifically (not Erzgebirgsdorf's, which has the already-
documented `HelveticaNeueBlackConden` font-substitution artifact for the
same wording).

**Fixed content — type directly into the layout, not a placeholder:**

| Element | Content | Formatting note |
|---|---|---|
| Headline (text box) | "Für Ihre Besucher:\ndrei Schritte — ein\nunvergesslicher Moment." | `HelveticaNeue-CondensedB`, 29.2pt, `#231f20`. |
| Step number "1" / "2" / "3" (3 text boxes) | "1", "2", "3" | `CoreSerifN-75Black`, 36.05pt, `#c5923b` (gold accent) — large display numerals, not part of the step label text box. |
| Step 1 label (text box) | "**Maske wählen —** aus den Erlebniswelten Ihres Markts." | Bold-lead-in pattern (same as `PAGE_02_SERVICE`/`PAGE_04_REFERENCES`): lead-in bold (`HelveticaNeue-CondensedB` 12pt), rest regular (`MyriadPro-Regular` 12pt), both `#231f20`. |
| Step 2 label (text box) | "**Hintergrund wählen —** Ihre Stadt, Ihr Markt, Ihre Atmosphäre." | Same bold-lead-in pattern. |
| Step 3 label (text box) | "**Foto machen —** fertig. Das Erlebnis-Souvenir ist sofort da." | Same bold-lead-in pattern. |
| Disclaimer (text box) | "Keine Einweisung, keine Wartezeit, keine Technik für Ihr Team — Ihre Besucher stehen davor und verstehen es sofort." | `MyriadPro-Regular`, 11.34pt, `#231f20`, no bold lead-in (whole line regular). |

**Placeholders — name exactly as shown, via Selection Pane:**

| Placeholder name | Type | Notes |
|---|---|---|
| `IMG_KIOSK_SCREENSHOT` | Picture Placeholder | Market-specific kiosk-interface screenshot — must show the deck's own market backgrounds (QC rule 4.4, `docs/02-page-types.md`). Frame ratio target **1.45**. Top-right area of the slide. |
| `IMG_USER_FLOW_CARD_1` | Picture Placeholder | **Provisional — see `docs/open-questions.md` #20.** Built as 2 separate placeholders to match the current WP5 field catalogue, but the source `.ai` files (Basel/Freiburg/Magdeburg, the confirmed 2-card layout) actually contain **one single flattened image** covering both cards (native ratio 1.78), not two independent photos — same architecture question already resolved for `PAGE_06_LOCAL_MOTIFS` (`docs/open-questions.md` #9), not yet asked here. Bottom-right area of the slide, below the kiosk screenshot. |
| `IMG_USER_FLOW_CARD_2` | Picture Placeholder | Same caveat as `IMG_USER_FLOW_CARD_1` — may need to collapse into a single `IMG_USER_FLOW_CARDS` field instead once #20 is answered. |

**Not yet resolved before this layout can be called final:**
- **`IMG_USER_FLOW_CARD_1`/`_2` vs. one combined field** —
  `docs/open-questions.md` #20, new. Don't build WP8 image-insertion logic
  against 2 independent card placeholders until this is confirmed, same
  caution already applied to `PAGE_06_LOCAL_MOTIFS`.
- **`TXT_KIOSK_BACKGROUND_LABEL`** — re-confirmed baked into
  `IMG_KIOSK_SCREENSHOT` in all 5 decks, no standalone text object found;
  not yet formally asked, `docs/open-questions.md` #21. Not built as a
  placeholder here (treated as part of the image, not a text field) —
  revisit if the designer says otherwise.
- Logo placement, if any (`docs/open-questions.md` #18) — slide-master-level.

---

### PAGE_06_LOCAL_MOTIFS

Reference: `docs/02-page-types.md` (purpose), `docs/03-elements.md`
(measurements, extended 2026-08-19 with typography for every element on this
page type and a re-measurement of all 5 decks' rotating text), `docs/04-fields.md`
(field definitions — `TXT_MOTIF_INTRO` removed 2026-08-19, reclassified as
fixed/computed, see below). Structure (row limit, image architecture,
headline rotation mechanism) is settled; **exact wording for 3 of this page
type's fixed text elements is provisional**, pending `docs/open-questions.md`
#22 and #23 — do not treat the wording below as final.

**Fixed content — type directly into the layout, not a placeholder, EXCEPT
where noted provisional:**

| Element | Content | Formatting note |
|---|---|---|
| Headline, position 1 | "Jede Karte ist ein Unikat — und ein Grund zum Teilen." | `HelveticaNeue-CondensedB`, 24.87pt, `#231f20`. Always paired with the stats callout below — non-negotiable per the designer (`docs/open-questions.md` #10). |
| Headline, position 2 | "Das nehmen Ihre Besucher mit — personalisiert, sofort, teilbar." | Same formatting. |
| Headline, position 3 | "Ihre Charaktere. Ihre Geschichte." | Same formatting. |
| Headline, position 4+ | Plain theme-name heading (reuses `TXT_THEME_WORLD_NAME`'s value as the heading text, no separate fixed string) | Same formatting — not yet confirmed which weight/size applies here specifically, assume same as positions 1–3 until built. |
| Intro paragraph, position 1 **(provisional — `docs/open-questions.md` #22)** | "Jedes Motiv wird individuell passend zu Ihrem Event gestaltet — Ihre Besucher werden Teil Ihrer Erlebniswelt. Das teilen sie." | `MyriadPro-Regular`, 11.13pt, `#231f20`. Majority wording (3 of 5 decks) — Halle and Erzgebirgsdorf each use a different text, not yet resolved which is canonical. |
| Intro paragraph, position 2 **(provisional — `docs/open-questions.md` #22)** | "Ein Event. Mehrere Erlebniswelten. Jedes Motiv erzählt eine eigene Geschichte – perfekt abgestimmt auf Ihre Veranstaltung." | Same formatting. Majority wording, same caveat as position 1. |
| Intro paragraph, position 3 | "Gemeinsam mit Ihnen entwickeln wir die Charaktere, die perfekt zu Ihrem Markt passen." | Same formatting. **Not provisional** — confirmed by direct measurement, both decks that reach position 3 agree exactly. |
| Intro paragraph, position 4+ | Not present (no text block found at this position in any deck) | — |
| 70%-stats callout **(provisional — `docs/open-questions.md` #23)** | "70 % der Besucher teilen ihr Motiv aktiv auf Facebook, Instagram oder TikTok — mit Ihrem Markt als Kontext." | `MyriadPro-Regular`, 11.87pt — "70 %" in `#c5923b` (gold), rest in `#efe7de` (cream), set inside a dark panel (`#001518` fill, `#c5923b` stroke). Only present on the position-1 table, together with that headline. Using the already-"resolved" `docs/open-questions.md` #7 wording here as the working draft, but a majority of decks (3 of 5) actually use a different, longer text — re-confirm before finalizing. |
| Column headers, first table of a sequence | "Fotokarte", "Hintergrund", "AR-Maske" | `MyriadPro-Regular`, 11.87pt, `#231f20`. One combined text run across all 3 columns. |
| Column headers, continuation table | "Fotokarte" (unchanged) + "Hintergrund", "AR-Maske" | Same formatting, but measured as two separate text boxes on continuation slides — "Fotokarte" stays in place, "Hintergrund"/"AR-Maske" repeat. Build as 2 separate text boxes to match. |
| Row-number circles | "1"/"2"/"3" on a table's first appearance; "4"/"5"/"6" if a theme continues onto a second slide | `CoreSerifN-75Black`, 22.37pt, `#c5923b`. Structural, not a content field — WP8 writes the number, not the input JSON. |

**Placeholders — name exactly as shown, via Selection Pane:**

| Placeholder name | Type | Notes |
|---|---|---|
| `TXT_THEME_WORLD_NAME` | Text Placeholder | Same field as `PAGE_01_TITLE`/`PAGE_02_SERVICE`/`PAGE_08_TRANSITION` — mandatory here (unlike its optional use on TITLE/SERVICE). Max 55 characters (higher than the 25-char limit used elsewhere — this page type's caption runs longer, e.g. Erzgebirgsdorf's 47-char instance). `HelveticaNeue-CondensedB`, 14.26pt, `#231f20`, top-left, above the headline. Build on every table position (1 through 4+), matching what positions 1–3 actually show in the majority of decks — Freiburg's LOCAL_MOTIFS slides are missing this caption entirely, but per the established 100%-mandatory rule (`docs/open-questions.md` #8) that's a deck bug, not a valid caption-less layout to replicate. |
| `TXT_MOTIF_1_NAME` / `TXT_MOTIF_2_NAME` / `TXT_MOTIF_3_NAME` | Text Placeholder | `_1` mandatory, `_2`/`_3` optional (1–3 motif rows per table). Max 30 characters. `MyriadPro-Regular`, 8.34pt, `#231f20`. |
| `IMG_MOTIF_1_PHOTO` / `IMG_MOTIF_1_BACKGROUND` / `IMG_MOTIF_1_MASK` | Picture Placeholder ×3 | Per-cell images per the designer's resolved architecture (`docs/open-questions.md` #9) — generator composes the 3×3 grid, template does not receive one flattened table image. Aspect ratio **not measurable from source** (source files flatten the whole table into one image) — decide directly in PowerPoint when this layout is laid out, same treatment as `PAGE_03_THEME_SHOWCASE`'s 2-up split. |
| `IMG_MOTIF_2_*` / `IMG_MOTIF_3_*` (same 3 sub-fields each) | Picture Placeholder ×6 | Optional, matching `TXT_MOTIF_2_NAME`/`TXT_MOTIF_3_NAME`. Same aspect-ratio caveat. |

**Not yet resolved before this layout can be called final:**
- **Intro paragraph wording for positions 1 and 2** — `docs/open-questions.md`
  #22, new. Majority text used above as a working draft only.
- **Stats callout wording** — `docs/open-questions.md` #23, new. The
  previously-"resolved" #7 answer turns out to be the minority wording by
  deck count; re-confirm before finalizing.
- Per-cell motif image aspect ratios (photo/background/mask) — not
  measurable from the flattened source, decide directly in PowerPoint.
- Row-limit continuation mechanics (reusing the 3-row structure with
  circles 4/5/6, and the column-header split into 2 boxes) are documented
  above from measurement, but haven't been built/tested in an actual 16:9
  layout yet — re-verify once this layout exists in PowerPoint.
- Logo placement, if any (`docs/open-questions.md` #18) — slide-master-level.

---

### PAGE_07_BESTSELLERS

Reference: `docs/02-page-types.md` (purpose), `docs/03-elements.md`
(measurements — 100% fixed, no open questions), `docs/04-fields.md`
("Fields not included here" — this page type has zero WP5 fields).
Re-verified 2026-08-20 directly against `docs/measurements/by_page_type.json`
for all 5 decks: Basel/Freiburg/Halle/Magdeburg are byte-identical and
bbox-identical (sub-pixel) on every text element; Erzgebirgsdorf matches
content-for-content and differs only in the already-documented
`HelveticaNeueBlackConden` font-substitution artifact and a few pixels of
bbox drift. No new findings, no open questions — the simplest page type
built so far along with `PAGE_04_REFERENCES`.

**Fixed content — type directly into the layout, not a placeholder. The
motif photos are boilerplate best-sellers, not market-specific, so the
table graphic is baked in as a static picture too, same as
`PAGE_04_REFERENCES`'s portfolio photos — this page type needs zero
placeholders:**

| Element | Content | Formatting note |
|---|---|---|
| Headline (text box) | "Best-Seller der \nSaison 2025" | `HelveticaNeue-CondensedB`, 29.2pt, `#231f20`. 1 manual line break as shown. |
| Intro line (text box) | "Die beliebtesten Motive auf Deutschlands Weihnachtsmärkten" | `MyriadPro-Regular`, 11.87pt, `#231f20`. |
| Motif caption 1 | "Weihnachtsrentier" | `MyriadPro-Regular`, 7.96pt, `#231f20`. |
| Motif caption 2 | "Santa mit \nSonnenbrille" | Same formatting, 1 manual line break. |
| Motif caption 3 | "Glühwein-Santa" | Same formatting. |
| Column headers (text box) | "Fotokarte / Hintergrund / AR-Maske" | `MyriadPro-Regular`, 11.32pt, `#231f20`. One combined text run. |
| Row-number circles | "1" / "2" / "3" | `CoreSerifN-75Black`, 21.35pt, `#c5923b`. |
| Motif table graphic (3×3 Fotokarte/Hintergrund/AR-Maske grid, boilerplate photos) | Fixed, static picture, not a placeholder | Same "identical content regardless of flattening" reasoning as `PAGE_04_REFERENCES`'s portfolio photos — this content never varies per market, so how it's composed in the source doesn't matter for WP6/WP8. Frame ratio 1.94 (Erzgebirgsdorf) to 2.00 (other 4, exact match) — insert at whatever size fits the layout, no crop decision needed since it's one fixed asset. |

**Placeholders:** none — this page type is selected/included per deck (a
boolean in the input JSON, per `docs/02-page-types.md`'s "mandatory, once"),
but has no per-market content to fill in.

**Not yet resolved before this layout can be called final:**
- Logo placement, if any (`docs/open-questions.md` #18) — slide-master-level,
  the only open item shared with every other layout.

---

### PAGE_08_TRANSITION

Reference: `docs/02-page-types.md` (purpose), `docs/03-elements.md`
(measurements, incl. the designer's resolution that the overlay caption is
the theme-world name, not market-name branding — `docs/open-questions.md`
#8), `docs/04-fields.md` (field definitions). Re-measured 2026-08-20 against
all 5 decks' `docs/measurements/by_page_type.json` data — the 2-card
structure and frame ratio are confirmed clean, but the caption's *content*
doesn't match what #8's resolution described. Logged as a new open question
rather than assumed away.

**Fixed content:** none — this page type has no headline or body copy, only
2 output-card photos and, per the mandatory-caption rule, an overlay
caption.

**Placeholders — name exactly as shown, via Selection Pane:**

| Placeholder name | Type | Notes |
|---|---|---|
| `IMG_OUTPUT_CARD_1` | Picture Placeholder | Left card. Frame ratio consistently 1.54–1.57 across Basel/Erzgebirgsdorf/Freiburg/Magdeburg — **target 1.55**. Halle's is a wider range (1.41–1.63), not treated as the model per `docs/03-elements.md`. |
| `IMG_OUTPUT_CARD_2` | Picture Placeholder | Right card. Same ratio target. |
| `TXT_TRANSITION_CAPTION` **(new field, provisional — see open question below)** | Text Placeholder | Overlay caption on each card, present in all 5 decks per the mandatory rule (`docs/open-questions.md` #8) but only actually visible in Halle's source file — the other 4 are missing it (deck bugs, not valid caption-less examples, per the existing resolution). `HelveticaNeue-Medium`, 14.19pt — measured as a fill/stroke pair (`#ffffff` fill, `#000000` stroke, for legibility over a photo), same duplicate-instance pattern already noted for this element. This is a font not seen anywhere else in the 5 decks; since Halle is the only surviving example, treat it as canonical for this element specifically rather than folding it into the 3-font baseline. |

**Not yet resolved before this layout can be called final:**
- **The caption's field identity is now in question.** `docs/open-questions.md`
  #8 concluded this caption is "the theme-world name," reusing the same
  mechanism as `PAGE_03_THEME_SHOWCASE`/`PAGE_06_LOCAL_MOTIFS`'s
  `TXT_THEME_WORLD_NAME`. But the only measured instance (Halle) reads
  "Hallescher Weihnachtsmarkt" — the **market's own name**, not any of
  Halle's actual theme-world names (which are "Historisches Halle",
  "Händelstadt Halle", "Hallmarkt & Salzstadt", "Märchen- und Familienwelt",
  "Luther & Reformation" — none of them match). This reads more like the
  same "market name alone" pattern WP5 already resolved for
  `PAGE_09_SOCIAL_REACH` (reuse the top-level `city` field, not a per-page
  field) than like `TXT_THEME_WORLD_NAME`. Built above as a new
  provisional field name (`TXT_TRANSITION_CAPTION`) rather than reusing
  either existing field, specifically so this doesn't get wired to the
  wrong source by default — **needs a designer/Martin confirmation: is this
  caption the market name, or a specific theme-world name that just happens
  to coincide with the market name in this one example?** Logged as new
  `docs/open-questions.md` #24.
- Logo placement, if any (`docs/open-questions.md` #18) — slide-master-level.

---

### PAGE_09_SOCIAL_REACH

Reference: `docs/02-page-types.md` (purpose), `docs/03-elements.md`
(measurements), `docs/04-fields.md` (field definitions). Re-verified
2026-08-20 against all 5 decks — headline/stats/bullets/closing paragraph
are byte-identical everywhere (Erzgebirgsdorf's font-substitution artifact
aside), confirming the existing doc. One correction found: the Instagram
mockup's "captioned with market name" claim in `docs/03-elements.md` was
never actually measured — checked now, and **no separate caption text
object exists in any of the 5 decks**, so it's reclassified below.

**Fixed content — type directly into the layout, not a placeholder:**

| Element | Content | Formatting note |
|---|---|---|
| Headline (text box) | "Organische Reichweite die \nkein Werbebudget kaufen kann." | `HelveticaNeue-CondensedB`, 27.98pt, `#231f20`. 1 manual line break. (Halle's copy has a comma after "die" — minor punctuation drift, not meaningful.) |
| Stat numbers (text box, 2 lines) | "90%\n70%" | `HelveticaNeue-CondensedB`, 56.9pt, `#231f20`. Large display numerals. |
| 90% label (text box) | "der Besucher hinterlassen \nfreiwillig ihre Kontaktdaten" | `MyriadPro-Regular`, 11.13pt, `#231f20`. |
| 70% label (text box) | "teilen ihr Motiv aktiv auf \nFacebook, Instagram oder TikTok — \nmit Ihrem Markt als Kontext." | Same formatting. **Note:** byte-identical to `PAGE_06_LOCAL_MOTIFS`'s "Kontext" stats-callout wording (`docs/open-questions.md` #7) and confirmed consistent across all 5 decks here — useful corroborating evidence for #23, but not by itself a resolution of which PAGE_06 wording is canonical. |
| Bullet 1 (text box) | "Ihre Besucher werden zu \nMarkenbotschaftern Ihres Markts." | Same formatting, no bold lead-in on this page type. |
| Bullet 2 (text box) | "Organischer Content, den kein \nWerbebudget ersetzen kann." | Same formatting. |
| Bullet 3 (text box) | "Jedes geteilte Motiv trägt Ihren \nMarktnamen in die sozialen Netzwerke." | Same formatting. |
| Closing paragraph (text box) | "Nach der Saison erhalten Sie von uns eine vollständige Auswertung — welche Motive am häufigsten geteilt wurden, welche Masken am besten ankamen, und wie wir das Erlebnis für die nächste Saison gemeinsam weiterentwickeln." | Same formatting, 223 chars — confirmed via Erzgebirgsdorf/Halle's unbroken extraction; Basel/Freiburg/Magdeburg's extraction splits this across 2 text-flow reads (a PDF-extraction artifact, not a real content difference, per `docs/03-elements.md`). |

**Placeholders — name exactly as shown, via Selection Pane:**

| Placeholder name | Type | Notes |
|---|---|---|
| `IMG_INSTAGRAM_MOCKUP` | Picture Placeholder | Instagram-style mockup photo. Frame ratio standardized to **1.33** per the designer (`docs/open-questions.md` #13) — Halle's 1.03 source crop was a mistake, not intentional. |

**Not built as a placeholder — reclassified 2026-08-20:** `docs/03-elements.md`
originally described this mockup as "captioned with market name," treated in
`docs/04-fields.md` as reusing the top-level `city` field rather than a
dedicated one. Re-checked directly against all 5 decks' measurement data:
**no separate caption text object exists next to the mockup image in any of
them.** If a market-name caption is wanted here, it's either baked into the
`IMG_INSTAGRAM_MOCKUP` photo asset itself (same pattern as
`IMG_KIOSK_SCREENSHOT`'s baked-in labels, `docs/open-questions.md` #21) or
was never actually part of the source decks' design. Not building a text
placeholder for it — if this turns out to be wrong, it's a small addition
later, safer than shipping a placeholder with no confirmed source of truth.

**Not yet resolved before this layout can be called final:**
- Whether an Instagram-caption market-name element belongs here at all
  (above) — worth folding into the next batch of designer questions
  alongside `docs/open-questions.md` #21, not urgent enough to number
  separately since nothing in the source decks currently supports it.
- Logo placement, if any (`docs/open-questions.md` #18) — slide-master-level.

---

### PAGE_10_CONTACT

Reference: `docs/02-page-types.md` (purpose), `docs/03-elements.md`
(measurements), `docs/04-fields.md` (field definitions). Re-verified
2026-08-20 against all 5 decks — headline, company contact block, and
intro/closing paragraph are byte-identical everywhere (Erzgebirgsdorf's
font-substitution artifact aside), confirming the existing doc with no new
findings. Last of the 10 page types — WP6's placeholder mapping is now
drafted for all of them, modulo the open items below.

**Fixed content — type directly into the layout, not a placeholder:**

| Element | Content | Formatting note |
|---|---|---|
| Headline (text box) | "Lassen Sie uns gemeinsam \nIhre Erlebniswelt entwickeln." | `HelveticaNeue-CondensedB`, 27.98pt, `#231f20`. 1 manual line break. |
| Intro/closing paragraph (text box) | "Interesse geweckt? \nGerne besprechen wir in einem persönlichen Gespräch, welche \nErlebniswelten, KI-/AR-Szenarien und Vermarktungsmöglichkeiten zu \nIhrem Standort passen.\n\nWir freuen uns darauf, Ihre Ideen kennenzulernen und gemeinsam \nMöglichkeiten für eine erfolgreiche Umsetzung zu entwickeln." | `MyriadPro-Regular`, 11.0pt, `#231f20`. Confirmed 294–295 chars total across all 5 decks (Basel/Freiburg/Magdeburg extract it as 2 separate text boxes — 170 + 124 chars — Erzgebirgsdorf/Halle as one unbroken block; same content either way, per `docs/03-elements.md`). Build as one text box with a blank line between the two sentences, matching Erzgebirgsdorf/Halle's structure. |
| Company block (text box) | "cosmoproducts GmbH\nMartin Baack\nBruno-Bürgel-Weg 69–81\nHaus 6\n12439 Berlin\nTelefon: +49 (0)30 – 26 36 71 70\nE-Mail: martinbaack@cosmoproducts.de\nWeb.: www.cosmoproducts.de" | Company name + contact name: `HelveticaNeue-CondensedB`, 14.68pt, `#231f20`. Address/phone/email/web lines: `MyriadPro-Regular`, 14.01pt, `#231f20`. Confirmed byte-identical across all 5 decks — this is cosmoproducts' own contact info, not market-specific, so it's fixed regardless of which deck/market the template is used for. |

**Placeholders — name exactly as shown, via Selection Pane:**

| Placeholder name | Type | Notes |
|---|---|---|
| `IMG_LANDMARK_PHOTO` | Picture Placeholder | Market landmark hero photo, right side of the slide, full-bleed to the edge. Frame ratio standardized to **0.559** (portrait) per the designer (`docs/open-questions.md` #14) — Erzgebirgsdorf's 0.75 and Halle's 0.684 crops were not intentional per-market discretion. |

**Not yet resolved before this layout can be called final:**
- Logo placement, if any (`docs/open-questions.md` #18) — slide-master-level,
  the only item still open across every layout in this template.

---

## Status: all 10 page types drafted (2026-08-20)

Every page type in `docs/02-page-types.md`'s catalogue now has a section
above. **Several are explicitly provisional, not ready to build as final in
PowerPoint yet** — don't skip straight to WP6 steps 4–7 (building the actual
`templates/master_v01.pptx`) without checking which:

- `PAGE_03_THEME_SHOWCASE` — caption styling unresolved (`docs/open-questions.md` #19).
- `PAGE_05_USER_FLOW` — 1-vs-2 output-card image fields unresolved (#20).
- `PAGE_06_LOCAL_MOTIFS` — intro-paragraph wording (#22) and stats-callout
  wording (#23) both unresolved; per-cell motif image aspect ratios need a
  PowerPoint-time decision, not a designer answer.
- `PAGE_08_TRANSITION` — overlay caption's field identity unresolved (#24).
- `PAGE_09_SOCIAL_REACH` — possible missing market-name caption element,
  informal, not yet a numbered question.
- Every layout — logo placement (#18) is still open and affects the slide
  master.

`PAGE_01_TITLE`, `PAGE_02_SERVICE`, `PAGE_04_REFERENCES`,
`PAGE_07_BESTSELLERS`, `PAGE_10_CONTACT` have no open items and can be built
as final now. Next session: send the newly-logged questions (#19–#24, plus
#18/#21) to the designer/Martin as a consolidated batch (matching how the
first two rounds of `docs/open-questions.md` were sent), then start WP6
steps 1–2 (slide master: 16:9 dimensions, background fill, fonts — none of
which are blocked) while answers are pending.
