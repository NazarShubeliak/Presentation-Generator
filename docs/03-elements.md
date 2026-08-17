# Fixed vs. Variable Elements (WP4)

One table per page type, listing every visible element and whether it is
**fixed** (identical in every generated deck) or **variable** (filled per
location). Character limits and image aspect ratios are measured directly
from the 5 reference decks (native `.ai` files, PDF-compatible — see
`src/extract_ai_measurements.py` and `src/aggregate_by_page_type.py`;
raw measurements in `docs/measurements/`, gitignored, not this file).

**Margin policy** (so every limit below is reproducible, not invented):
`limit = longest observed length, rounded up to the nearest 5, plus 15%
of that value, rounded up to the nearest 5 again`. Applied uniformly;
noted per-field only where a different judgment call was made.

**Frame vs. file, confirmed:** for every image element below, the ratio
comes from the placement bounding box in the source file (the frame), not
from the embedded raster's native pixel dimensions — per the task brief's
instruction. Source artboards are 4:3 (720×540pt); the new master template
is 16:9 (WP6) — these frame ratios are a starting reference for what the
*source* used, not a target to copy 1:1 into the new template.

---

## PAGE_01_TITLE

| Element | Fixed / Variable | Detail |
|---|---|---|
| Headline ("Wir machen Ihre Besucher zu einem Teil Ihrer Geschichte.") | **Fixed** | Byte-identical across all 5 decks. 56 characters. |
| Subline (market name sentence) | **Variable** | Pattern "KI- & AR-Erlebnisinstallationen für den/das {market}". Observed 63–81 chars (Erzgebirgsdorf longest: "...für das Erzgebirgsdorf auf dem Düsseldorfer Platz"). **Limit: 95 characters.** |
| Theme-world caption (e.g. "Kaiser-Otto-Pfalz") | **Variable, optional** | Only present when the deck has >2 theme worlds (see `PAGE_03_THEME_SHOWCASE` rule in `docs/02-page-types.md`) — 3 of 5 decks (Halle, Magdeburg) have it, 2 don't have it at all. Observed 17–18 chars. **Limit: 25 characters.** Not present → field must be optional/nullable in the schema, not empty-string. |
| Hero photo | **Variable** | Full-bleed background, market-specific. Frame = full page bleed. Source ratio 4:3 in 2/5 decks (Basel, Freiburg) where the image isn't overscaled; the other 3 use a larger, off-canvas-cropped source image for a bleed effect — **frame ratio to target: 4:3** (the canvas), not the raw image ratio. |

**Open question:** the theme-world caption is optional depending on a computed condition (theme count > 2), not a simple per-deck yes/no choice — WP5/WP7 need to decide whether this is authored directly in the JSON (include the field or omit it) or computed by the generator from a `theme_worlds` list. Recommend the former (explicit) to keep WP8 simple, per the schema's own philosophy of not inventing logic — flagging for the designer/Mathias to confirm.

---

## PAGE_02_SERVICE

| Element | Fixed / Variable | Detail |
|---|---|---|
| Headline ("Ihr Erlebnispartner — von Konzept bis Betreuung vor Ort.") | **Fixed** | 4 of 5 decks identical (56–57 chars); Erzgebirgsdorf is missing "vor Ort." (48 chars) — looks like an incomplete edit, not an intentional per-market variant. Flagged below. |
| Body paragraph ("Wir entwickeln individuelle KI-...") | **Fixed** | Word-for-word identical across all 5 (154–155 chars, only line-wrap position differs). |
| 3 bullet items (concept/masks, hut design, on-site staff) | **Fixed** | Word-for-word identical across all 5 (73–85 chars each). |
| Theme-world caption (e.g. "Märchengasse") | **Variable, optional** | Same mechanism as `PAGE_01_TITLE`'s caption — present only in Halle (25 chars) and Magdeburg (12 chars). **Limit: 25 characters** (shared with title's caption field — same field, reused). |
| Booth photo | **Variable** | Market-specific booth photo. On-canvas frame ratio 4:3 (Basel/Freiburg) up to 1.5 in decks using a larger bleed source; **frame ratio to target: 4:3**, consistent with `PAGE_01_TITLE`. |

**Open question:** is Erzgebirgsdorf's shortened headline ("...bis Betreuung", missing "vor Ort.") an intentional shorter variant, or a copy-paste/edit artifact like the other data-quality issues already flagged for that deck? Given the deck is already flagged for several cross-market contamination issues (see `docs/01-slide-inventory.md`), treating this headline as **fixed, 57-char canonical text** and the Erzgebirgsdorf instance as the outlier — but this should be confirmed with Martin/the designer, not assumed.

---

## PAGE_03_THEME_SHOWCASE

| Element | Fixed / Variable | Detail |
|---|---|---|
| Theme-world caption(s) | **Variable** | 1 caption (Basel, Halle-slide4: 19–21 chars) or 2 captions joined with a line break when the slide covers a 2-up pair (Halle-slide2: 38 chars, Magdeburg: 46–47 chars). **Limit for a single caption: 25 characters. Limit for a combined 2-up caption: 55 characters.** |
| Booth photo(s) | **Variable** | 1 photo (single layout) or 2 photos side by side (2-up layout) — this is a **structural** variant of the same page type, not just a text difference. Frame ratio ≈ 4:3 per booth photo (full-bleed canvas for single; each half of a 2-up pair is narrower — exact split not independently measurable from the flattened bleed image, needs confirming against the actual PowerPoint template once built in WP6). |

**Open question:** WP5/WP7 need a decision on how the single-vs-2-up variant is represented in the schema — e.g. always an array of 1–2 theme entries, with the layout picked automatically by array length? This page type already has more layout variance than any other (see also the "activates if themes > 2" rule in `docs/02-page-types.md`) and deserves explicit designer sign-off on the schema shape, not an assumption.

---

## PAGE_04_REFERENCES

| Element | Fixed / Variable | Detail |
|---|---|---|
| Headline ("Jeder Markt bekommt seine eigene Welt.") | **Fixed** | Identical across all 5 (except OCR line-break differences), 39 chars. |
| Intro line ("Wir entwickeln Hüttendesign...") | **Fixed** | Byte-identical across all 5, 92 chars. |
| 4 example-theme captions (Historischer Markt, Märchenmarkt, Barock & Schloss, Regionale Identität) | **Fixed** | Byte-identical across 4/5 decks. Basel/Freiburg/Magdeburg have a slightly shorter "Barock & Schloss" line missing its "— Markgraf · Hofdame · Venezianische Maskenfigur." suffix (compare to Erzgebirgsdorf/Halle, which have it in full) — same "looks like an incomplete edit" pattern as `PAGE_02_SERVICE`'s headline. Longest observed combined 2-line block: 138 chars. |
| Client-list footer | **Fixed, with one confirmed variant** | 4 of 5 decks (Basel, Erzgebirgsdorf, Freiburg, Magdeburg) include "Striezelmarkt Dresden" as the first item; Halle's list omits it. 214 vs. ~196 chars. |
| 4 example-theme photos + background market photo | **Fixed** | Cross-client portfolio, explicitly not location-specific per the task brief and confirmed identical content across decks. Not worth an aspect-ratio measurement — this whole page type is boilerplate, no per-location fields at all. |

**Open question:** the "Barock & Schloss" truncation (3 of 5 decks) and the missing "Striezelmarkt Dresden" (Halle) are the *same category* of question raised for `PAGE_02_SERVICE`'s headline — is there a single canonical/current version of this fixed copy that the shorter instances simply haven't been updated to match? Recommend bundling all three into one question to Martin/the designer rather than guessing which version is "correct."

---

## PAGE_05_USER_FLOW

| Element | Fixed / Variable | Detail |
|---|---|---|
| Headline ("Für Ihre Besucher: drei Schritte — ein unvergesslicher Moment.") | **Fixed** | Byte-identical across all 5, 63 chars. |
| Step 1 label ("Maske wählen —...") | **Fixed, 2 known variants** | Variant A (Basel/Freiburg/Magdeburg): "...aus verschiedenen Stilen und Erlebniswelten." (59 chars). Variant B (Erzgebirgsdorf/Halle): "...aus den Erlebniswelten Ihres Markts." (52 chars). |
| Step 2 label ("Szene wählen" / "Hintergrund wählen") | **Fixed, 2 known variants** | Variant A: "Szene wählen — passend zu Ihrem Event, Ihrer Location, Ihrer Atmosphäre." (72 chars). Variant B: "Hintergrund wählen — Ihre Stadt, Ihr Markt, Ihre Atmosphäre." (61 chars). Note the step *name itself* differs (Szene vs. Hintergrund), not just phrasing — same split as step 1. |
| Step 3 label ("Foto machen —...") | **Fixed, 2 known variants** | Variant A: "...fertig. Das persönliche Erinnerungsstück ist sofort da." (69 chars). Variant B: "...fertig. Das Erlebnis-Souvenir ist sofort da." (59 chars). |
| Disclaimer ("Keine Einweisung...") | **Fixed, 2 known variants** | Variant A: 124 chars. Variant B: 117 chars. |
| Kiosk-interface screenshot | **Variable** — **confirmed QC-relevant, see `docs/02-page-types.md`** | Must show the deck's own market backgrounds (designer-confirmed rule). Frame ratio ≈ 1.43–1.50 across all 5 (tight range) — **target 1.45**. |
| Output-card example photo(s) | **Variable** | Count/arrangement is **not consistent**: 2 large cards (Basel/Freiburg/Magdeburg, ratio ≈1.78 combined), several small thumbnails (Erzgebirgsdorf), 4 medium cards (Halle). Flagged below — this is a real structural inconsistency, not just a copy variant. |

**Open questions:**
1. Steps 1–3 and the disclaimer form **two complete, consistent variant sets** ("Variant A" everywhere or "Variant B" everywhere, never mixed within one deck) — this reads like an intentional copy revision (v1 → v2) applied to only 2 of 5 decks, not random drift. Worth asking Martin/designer which variant is current and whether the other 3 decks should be updated, or both are meant to coexist as valid options (unlikely, but per ground rules — ask, don't assume).
2. The output-card example area's inconsistent image count/layout (2 vs. several small vs. 4) is a real structural difference the master template will have to pick one canonical layout for — needs a designer decision on the intended layout, not a measurement problem.

---

## PAGE_06_LOCAL_MOTIFS

| Element | Fixed / Variable | Detail |
|---|---|---|
| Headline (one of 3 rotating patterns, or none) | **Variable, but see open question below** | "Das nehmen Ihre Besucher mit — personalisiert, sofort, teilbar." (63–65 chars) / "Jede Karte ist ein Unikat — und ein Grund zum Teilen." (53 chars) / "Ihre Charaktere. Ihre Geschichte." (33 chars) / no headline at all (theme name used directly as a plain heading instead, 15–31 chars, seen from the 3rd table onward in Magdeburg). **Limit: 75 characters** for the longest rotating headline. |
| Intro paragraph (below headline) | **Fixed-ish, 2 known variants, optional** | "Jedes Motiv wird individuell passend zu Ihrem Event gestaltet — Ihre Besucher werden Teil Ihrer Erlebniswelt. Das teilen sie." pattern (120–125 chars) vs. "Ein Event. Mehrere Erlebniswelten. Jedes Motiv erzählt eine eigene Geschichte – perfekt abgestimmt auf Ihre Veranstaltung." pattern (123–125 chars) vs. absent entirely (tables from the 3rd onward in Magdeburg/Halle). **Limit: 140 characters.** |
| Theme-world name (small caption, above or beside the table) | **Variable** | 15–47 chars observed (Erzgebirgsdorf's "Märchenwelt Schwerin" included — see the data-quality flag in `docs/02-page-types.md`, do not treat as a clean example). **Limit: 55 characters.** |
| Motif row: photo caption/name | **Variable**, 1–3 rows per table | 6–23 chars observed (e.g. "Rudolph" to "Adalbert von Magdeburg"). **Limit: 30 characters.** |
| Column headers ("Fotokarte", "Hintergrund", "AR-Maske") | **Fixed** | Identical everywhere, only present in full on the first table of a sequence — continuation/later tables sometimes show only "Hintergrund / AR-Maske" (Freiburg's continuation slide) because "Fotokarte" is shown once and implied. |
| 70%-share stat callout ("70 % der Besucher teilen...") | **Variable, optional** | 108–157 chars depending on phrasing variant (2 known variants, same "Variant A/B" split pattern as `PAGE_05_USER_FLOW`). Appears on exactly one table per deck — the one carrying the row-limit overflow (see below) or, in single-table decks, the only table. **Limit: 175 characters.** |
| Row-limit ("1/2/3" numbered circle) | **Fixed structural**, not a content field | Table has exactly 3 row-slots. A theme with more than 3 motifs continues onto a second slide reusing the same 3-row structure with circles numbered 4/5/6 (confirmed via Freiburg: 5 motifs = 3 + 2). This resolves the WP4 follow-up flagged earlier in `docs/02-page-types.md` — **the row limit is 3.** |
| Motif table graphic (Fotokarte + Hintergrund + AR-Maske columns, all rows) | **Variable — but flattened as ONE image in the source, not 9** | Every instance measured has exactly **one** image object covering the whole table area (not one image per cell). Frame ratio 1.78–1.91 (close to but not exactly 16:9) across all 17 instances. **This is a structural finding, not just a measurement — see open question below.** |

**Open questions:**
1. **The headline-rotation rule doesn't match measurement.** The designer's stated rule (`docs/02-page-types.md`) is: world 1 → "Jede Karte ist ein Unikat" + stats, world 2 → "Das nehmen Ihre Besucher mit", world 3+ → "Ihre Charaktere." But the *first* standalone motif table in **every** multi-theme deck measured (Basel, Halle, Magdeburg) actually uses "Das nehmen..." (the stated world-2 pattern), and the *second* table uses "Jede Karte..." (the stated world-1 pattern) — consistently reversed from what was described, across all 3 decks. The stats callout also doesn't consistently pair with "Jede Karte" as described — in Basel it's paired with "Das nehmen" (table 1) instead. **Not resolving this myself — presenting the raw observed order below for the designer to reconcile with their own rule:**
   - Basel: table1="Das nehmen"+stats, table2="Jede Karte", table3="Ihre Charaktere"
   - Halle: table1(Historisches Halle)="Das nehmen", table2(Händelstadt Halle)="Jede Karte", table3(Hallmarkt&Salzstadt)="Ihre Charaktere"+stats, table4–5=plain theme-name heading, no rotating headline
   - Magdeburg: table1(Kaiser-Otto-Pfalz)="Das nehmen", table2(Märchengasse)="Jede Karte"+stats, table3–6=plain theme-name heading, no rotating headline
   - Freiburg (continuation, not separate themes): slide1(rows1-3)="Das nehmen", slide2(rows4-5, continuation)="Jede Karte"+stats
2. **The motif table is one flattened image per slide in the source, not 9 separate cell images.** This is a real architecture question for WP6/WP7/WP8, not just a WP4 measurement note: will the generator receive one pre-composed table image per theme (simplest, but means table layout/rows can't be built programmatically — contradicts the brief's "insert every image" language which implies per-field images), or will it need to compose the 3×3 grid itself from 9 separate motif images per table (matching the JSON schema's implied per-field structure, e.g. `IMG_MOTIF_1_PHOTO`, `IMG_MOTIF_1_BACKGROUND`, `IMG_MOTIF_1_MASK`)? This decision blocks WP5's field catalogue for this page type and should be raised with Mathias, not assumed.
3. Not every theme-world's motifs are location-specific even within a single deck — see the note already added to `docs/01-slide-inventory.md`'s cross-deck observations (Magdeburg's "Märchengasse", "Weihnachtsmannhaus & Kinderdorf", "Magdeburger Lichterwelt" read as generic/universal, same as Halle's "Märchen- und Familienwelt"). Worth confirming whether generic theme-worlds like these should be modeled as reusable schema building blocks rather than one-off per-market content.

---

## PAGE_07_BESTSELLERS

| Element | Fixed / Variable | Detail |
|---|---|---|
| Everything on this slide (headline, intro, 3 motif rows, column headers, table graphic) | **100% Fixed** | Confirmed byte-identical (down to sub-pixel bbox coordinates) across 4 of 5 decks. Erzgebirgsdorf differs only in font name (`HelveticaNeueBlackConden` vs `HelveticaNeue-CondensedB` — a font-substitution artifact in that one file, not a real design difference) and a few pixels of bbox drift. Table image frame ratio 1.94–2.00 across all 5. |

**No open questions.** This page type has no variable content at all — it should be built as fully fixed content in the master template (WP6), with no schema fields required for it beyond selecting that it's included (WP4 step 1's "mandatory, once" from `docs/02-page-types.md` already covers this).

---

## PAGE_08_TRANSITION

| Element | Fixed / Variable | Detail |
|---|---|---|
| 2 output-card photos | **Variable** | Market-specific, no text on this page type at all in 4 of 5 decks. Frame ratio consistently 1.54–1.57 (tight range) across Basel/Erzgebirgsdorf/Freiburg/Magdeburg — **target 1.55**. |
| Market-name watermark/branding on the cards (e.g. "MAGDEBURGER WEIHNACHTSMARKT") baked into the photo | **Variable, but baked into the image, not a text field** | Confirmed by the designer as a **QC-relevant element** (`docs/02-page-types.md`, rule 4.4) — must match the deck's own market. Not a separate schema text field since it's part of the image asset itself, not overlaid text. |
| Halle-only caption text ("Hallescher Weihnachtsmarkt") | **Inconsistent with the other 4 decks** | Halle has visible overlay caption text (appearing twice per card — likely a stroke+fill duplicate in the source, not 2 real instances) that no other deck has. Frame ratio also differs more (1.41–1.63) than the other 4. |

**Open question:** is Halle's overlay caption text an intentional extra treatment for this one deck, or should the other 4 decks' transition slides also have it (i.e., is Halle the "correct"/current version and the other 4 outdated, similar to the `PAGE_02_SERVICE`/`PAGE_04_REFERENCES` copy-version questions above)? Recommend bundling with those into one combined question to Martin/the designer about which decks reflect the current template version.

---

## PAGE_09_SOCIAL_REACH

| Element | Fixed / Variable | Detail |
|---|---|---|
| Headline, 90%/70% stat labels, 3 bullet points | **Fixed** | Byte-identical across all 5 (headline 56–57 chars; minor comma difference in Halle's headline, not meaningful). |
| Closing paragraph ("Nach der Saison erhalten Sie...") | **Fixed** | Byte-identical content, 223 chars, confirmed via Erzgebirgsdorf/Halle's unbroken version — Basel/Freiburg/Magdeburg's extraction shows this text split oddly with a chunk apparently missing, which on inspection is a text-flow/line-order extraction artifact (multi-line-wrap reading order), **not a real content difference**. Treat 223 characters as the authoritative fixed length. |
| Instagram mockup photo, captioned with market name | **Variable** | Caption = market name (reuses the same field as `PAGE_01_TITLE`'s subline market name, just the city, not the full sentence — needs its own shorter field, not measured separately here since the visible caption is the market name alone judging from `docs/01-slide-inventory.md`'s descriptions). Frame ratio: 1.33 in 3/5 decks, 1.31 (Erzgebirgsdorf), 1.03 (Halle, notably square-ish, an outlier). **Target 1.33; flag Halle's crop as a designer question below.** |

**Open question:** Halle's Instagram-mockup frame ratio (1.03, near-square) is a clear outlier against the other 4 decks (1.31–1.33) — is this an intentional different crop for that deck, or a mistake? Worth a quick visual check with the designer before fixing 1.33 as the template's hard target.

---

## PAGE_10_CONTACT

| Element | Fixed / Variable | Detail |
|---|---|---|
| Headline ("Lassen Sie uns gemeinsam...") | **Fixed** | Byte-identical across all 5, 55 chars. |
| Company block (cosmoproducts GmbH, Martin Baack, address, phone, email, website) | **Fixed** | Byte-identical across all 5 — same company contact info regardless of market, confirmed. Combined block length 167 chars across the 5 lines. |
| Intro/closing paragraph ("Interesse geweckt?...") | **Fixed** | Byte-identical content (≈294–295 chars total) across all 5 — the apparent 170+124 vs. one-block-of-295 split is just a text-block-boundary rendering difference, not a real content variant (confirmed: 170+124=294 ≈ the single-block versions' 295). |
| Hero photo (market landmark) | **Variable** | Market-specific. Frame ratio varies more than any other page type's photo: 0.559 (3/5 decks), 0.750 (Erzgebirgsdorf), 0.684 (Halle) — all portrait orientation but a real spread, not measurement noise (bbox is clean/on-canvas in all 5). **Flagged below rather than picking one target.** |

**Open question:** the hero photo's aspect ratio genuinely varies across decks (0.559–0.750, a ~34% spread) — is this intentional per-market cropping discretion, or should the master template enforce one fixed portrait ratio (recommend 0.559, the majority value, matching `PAGE_04_REFERENCES`'s Basel/Freiburg/Magdeburg image ratio at 0.559 too — possibly the "correct" shared frame ratio, with Erzgebirgsdorf/Halle being the outliers this time)? Needs the designer's call, not a guess — a wrong aspect-ratio target here means every future contact-slide photo either gets awkwardly cropped or requires custom resizing per location, defeating the point of a fixed template frame.

---

## Cross-cutting open questions (not specific to one page type)

1. **Recurring "2 known variants" pattern.** `PAGE_02_SERVICE`'s headline, `PAGE_04_REFERENCES`'s theme captions and client list, `PAGE_05_USER_FLOW`'s 4 fixed text fields, `PAGE_06_LOCAL_MOTIFS`'s stats callout, and `PAGE_08_TRANSITION`'s caption treatment all show the same shape: a shorter/older-looking version in some decks and a fuller/newer-looking version in others, split roughly along the same deck lines (Erzgebirgsdorf and/or Halle differing from Basel/Freiburg/Magdeburg, or vice versa). This reads like an in-progress copy revision that wasn't back-applied to every deck, not 5 independent design choices. **Recommend one consolidated question to Martin/the designer covering all of these at once**, asking which version is current, rather than treating each as a separate ambiguity.
2. **The motif-table-as-one-flattened-image finding (`PAGE_06_LOCAL_MOTIFS`, open question 2)** is the single highest-impact open item in this document — it affects the JSON schema shape (WP5/WP7) and the generator script's image-insertion logic (WP8), not just the template. Recommend resolving this before starting WP5.
3. Source artboards are 4:3; new template is 16:9 (per WP6). None of the frame ratios measured here transfer directly — they're a documented starting reference for "what the source used", to compare against once layouts are redrawn for 16:9 in WP6, not values to hard-code into the new template.
