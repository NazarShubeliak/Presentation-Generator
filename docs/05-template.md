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

*(remaining 5 page types not yet built — continue here next session)*
