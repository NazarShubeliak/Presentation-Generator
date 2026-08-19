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

**Resolved by designer (2026-08-18, see `docs/open-questions.md` #12):** computed by the generator from a `theme_worlds` list, not authored explicitly in the JSON — overturns this doc's original recommendation (explicit authoring, for WP8 simplicity). Designer prefers the automatic approach.

---

## PAGE_02_SERVICE

| Element | Fixed / Variable | Detail |
|---|---|---|
| Headline ("Ihr Erlebnispartner — von Konzept bis Betreuung vor Ort.") | **Fixed** | 4 of 5 decks identical (56–57 chars); Erzgebirgsdorf is missing "vor Ort." (48 chars) — looks like an incomplete edit, not an intentional per-market variant. Flagged below. |
| Body paragraph ("Wir entwickeln individuelle KI-...") | **Fixed** | Word-for-word identical across all 5 (154–155 chars, only line-wrap position differs). |
| 3 bullet items (concept/masks, hut design, on-site staff) | **Fixed** | Word-for-word identical across all 5 (73–85 chars each). |
| Theme-world caption (e.g. "Märchengasse") | **Variable, optional** | Same mechanism as `PAGE_01_TITLE`'s caption — present only in Halle (25 chars) and Magdeburg (12 chars). **Limit: 25 characters** (shared with title's caption field — same field, reused). |
| Booth photo | **Variable** | Market-specific booth photo. On-canvas frame ratio 4:3 (Basel/Freiburg) up to 1.5 in decks using a larger bleed source; **frame ratio to target: 4:3**, consistent with `PAGE_01_TITLE`. |

**Resolved by designer (2026-08-18, see `docs/open-questions.md` #3):** "...bis Betreuung vor Ort." (57 chars) is confirmed canonical. Erzgebirgsdorf's shortened instance is the outlier/artifact, as suspected.

---

## PAGE_03_THEME_SHOWCASE

| Element | Fixed / Variable | Detail |
|---|---|---|
| Theme-world caption(s) | **Variable** | 1 caption (Basel, Halle-slide4: 19–21 chars) or 2 captions joined with a line break when the slide covers a 2-up pair (Halle-slide2: 38 chars, Magdeburg: 46–47 chars). **Limit for a single caption: 25 characters. Limit for a combined 2-up caption: 55 characters.** |
| Booth photo(s) | **Variable** | 1 photo (single layout) or 2 photos side by side (2-up layout) — this is a **structural** variant of the same page type, not just a text difference. Frame ratio ≈ 4:3 per booth photo (full-bleed canvas for single; each half of a 2-up pair is narrower — exact split not independently measurable from the flattened bleed image, needs confirming against the actual PowerPoint template once built in WP6). |

**Resolved by designer (2026-08-18, see `docs/open-questions.md` #11):** yes — array of 1–2 theme entries, layout (single vs. 2-up) picked automatically by array length. Confirmed as-is.

---

## PAGE_04_REFERENCES

| Element | Fixed / Variable | Detail |
|---|---|---|
| Headline ("Jeder Markt bekommt seine eigene Welt.") | **Fixed** | Identical across all 5 (except OCR line-break differences), 39 chars. |
| Intro line ("Wir entwickeln Hüttendesign...") | **Fixed** | Byte-identical across all 5, 92 chars. |
| 4 example-theme captions (Historischer Markt, Märchenmarkt, Barock & Schloss, Regionale Identität) | **Fixed** | Full version confirmed canonical (designer, 2026-08-18): "Barock & Schloss — Markgraf · Hofdame · Venezianische Maskenfigur." Basel/Freiburg/Magdeburg's shorter line (missing the suffix) is the outdated instance, matching Erzgebirgsdorf/Halle's full version. Longest observed combined 2-line block: 138 chars. |
| Client-list footer | **Variable** (not fixed-with-a-variant, see below) | **Resolved by designer (2026-08-18, see `docs/open-questions.md` #5) — the premise was wrong.** This is a standing generation rule, not a copy-version question: a market's own reference list must never include itself. "Striezelmarkt Dresden" belongs in the footer of every deck *except* the one built for Striezelmarkt Dresden. WP5/WP7: model the footer as the fixed client list **minus the current deck's own market name**, computed per-generation, not a static fixed string. Full list (Basel/Erzgebirgsdorf/Freiburg/Magdeburg, byte-identical, 217 chars): "Striezelmarkt Dresden␣␣␣␣␣Salzburger Christkindlmarkt␣␣␣␣␣Berliner Weihnachtszeit␣␣␣␣␣Weihnachtsmarkt Wiesbaden␣␣␣\nKölner Dom␣␣␣␣␣Tower Bridge London␣␣␣␣␣Checkpoint Charlie Berlin␣␣␣␣␣Wiener Prater␣␣␣␣␣und viele mehr." (8 named clients + generic tail, `␣␣␣␣␣` = 5-space separator). **Data-quality flag, re-checked 2026-08-19 while building WP6:** Halle's footer (191 chars) is missing "Striezelmarkt Dresden" — but Halle is *not* Striezelmarkt Dresden, so this isn't an instance of the confirmed self-exclusion rule (none of the 8 names in this boilerplate list matches any of the 5 reference decks' own market anyway, so the rule was never actually exercised by these 5 examples). Treat Halle's omission as a one-off content bug in that reference file (same category as the other confirmed reference-deck bugs, e.g. Erzgebirgsdorf's missing "vor Ort."), not as a second exclusion case to explain — the generator should always compute the footer as fixed-list-minus-current-market and disregard Halle's specific wording as a bug, not a pattern. |
| 4 example-theme photos + background market photo | **Fixed** | Cross-client portfolio, explicitly not location-specific per the task brief and confirmed identical content across decks. Not worth an aspect-ratio measurement — this whole page type is boilerplate, no per-location fields at all. |

**No open question remaining** — both items resolved by the designer, 2026-08-18 (see `docs/open-questions.md` #4–5).

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
1. ~~Steps 1–3 and the disclaimer form two complete, consistent variant sets — which is current?~~ **Resolved by designer (2026-08-18, see `docs/open-questions.md` #6): Variant B is canonical** (the Erzgebirgsdorf/Halle wording, minority by deck count) — step 1 "Maske wählen — aus den Erlebniswelten Ihres Markts.", step 2 "Hintergrund wählen — Ihre Stadt, Ihr Markt, Ihre Atmosphäre.", step 3 "Foto machen — fertig. Das Erlebnis-Souvenir ist sofort da.", disclaimer "Keine Einweisung, keine Wartezeit, keine Technik für Ihr Team — Ihre Besucher stehen davor und verstehen es sofort." Basel/Freiburg/Magdeburg's "Variant A" is outdated.
2. The output-card example area's inconsistent image count/layout (2 vs. several small vs. 4) is a real structural difference the master template will have to pick one canonical layout for — needs a designer decision on the intended layout, not a measurement problem. **Resolved (2026-08-18): 2 cards is correct** — the Basel/Freiburg/Magdeburg pattern (ratio ≈1.78 combined) is the target layout; Erzgebirgsdorf's several-small-thumbnails and Halle's 4-medium-cards layouts are the outliers.

---

## PAGE_06_LOCAL_MOTIFS

| Element | Fixed / Variable | Detail |
|---|---|---|
| Headline (one of 3 rotating patterns, or none) | **Fixed, computed by table position — not a WP5 field** | Full rotation confirmed by designer, 2026-08-18 (`docs/open-questions.md` #15): position 1 → "Jede Karte ist ein Unikat — und ein Grund zum Teilen." + the stats callout above; position 2 → "Das nehmen Ihre Besucher mit — personalisiert, sofort, teilbar."; position 3 → "Ihre Charaktere. Ihre Geschichte." (33 chars, as originally stated); position 4 and beyond → plain theme-name heading (no fixed rotating text), matching what's actually seen in Magdeburg/Halle. |
| Intro paragraph (below headline) | **Fixed, conditional — not a WP5 field** | Canonical wording confirmed by designer, 2026-08-18 (`docs/open-questions.md` #16): "Jedes Motiv wird individuell passend zu Ihrem Event gestaltet — Ihre Besucher werden Teil Ihrer Erlebniswelt. Das teilen sie." (120 chars). **Still open:** whether it now also appears on position-3+ tables (which get a real headline again per the row above) or stays absent there as measured — not yet confirmed. |
| Theme-world name (small caption, above or beside the table) | **Variable** | 15–47 chars observed (Erzgebirgsdorf's "Märchenwelt Schwerin" included — see the data-quality flag in `docs/02-page-types.md`, do not treat as a clean example). **Limit: 55 characters.** |
| Motif row: photo caption/name | **Variable**, 1–3 rows per table | 6–23 chars observed (e.g. "Rudolph" to "Adalbert von Magdeburg"). **Limit: 30 characters.** |
| Column headers ("Fotokarte", "Hintergrund", "AR-Maske") | **Fixed** | Identical everywhere, only present in full on the first table of a sequence — continuation/later tables sometimes show only "Hintergrund / AR-Maske" (Freiburg's continuation slide) because "Fotokarte" is shown once and implied. |
| 70%-share stat callout ("70 % der Besucher teilen...") | **Fixed, conditional — not a WP5 field** | Designer confirmed one canonical text (`docs/open-questions.md` #7): "70 % der Besucher teilen ihr Motiv aktiv auf Facebook, Instagram oder TikTok — mit Ihrem Markt als Kontext." (108 chars). Not per-market content — it's boilerplate that the generator includes only on the theme-position-1 table (see headline row below), same mechanism as `PAGE_07_BESTSELLERS`'s fully-fixed content. |
| Row-limit ("1/2/3" numbered circle) | **Fixed structural**, not a content field | Table has exactly 3 row-slots. A theme with more than 3 motifs continues onto a second slide reusing the same 3-row structure with circles numbered 4/5/6 (confirmed via Freiburg: 5 motifs = 3 + 2). This resolves the WP4 follow-up flagged earlier in `docs/02-page-types.md` — **the row limit is 3.** |
| Motif table graphic (Fotokarte + Hintergrund + AR-Maske columns, all rows) | **Variable — 9 separate per-cell images, not 1** | Every instance measured in the reference decks has exactly **one** flattened image object covering the whole table area, but the designer's resolved architecture decision (below) is to build this from 9 separate images going forward, not replicate the source's flattening. Reference-deck frame ratio 1.78–1.91 was measured against the flattened source image and is not directly meaningful once the table is composed from 9 separate images in WP6/WP8. |

**Open questions:**
1. **The headline-rotation rule doesn't match measurement.** The designer's stated rule (`docs/02-page-types.md`) is: world 1 → "Jede Karte ist ein Unikat" + stats, world 2 → "Das nehmen Ihre Besucher mit", world 3+ → "Ihre Charaktere." But the *first* standalone motif table in **every** multi-theme deck measured (Basel, Halle, Magdeburg) actually uses "Das nehmen..." (the stated world-2 pattern), and the *second* table uses "Jede Karte..." (the stated world-1 pattern) — consistently reversed from what was described, across all 3 decks. Raw observed order:
   - Basel: table1="Das nehmen"+stats, table2="Jede Karte", table3="Ihre Charaktere"
   - Halle: table1(Historisches Halle)="Das nehmen", table2(Händelstadt Halle)="Jede Karte", table3(Hallmarkt&Salzstadt)="Ihre Charaktere"+stats, table4–5=plain theme-name heading, no rotating headline
   - Magdeburg: table1(Kaiser-Otto-Pfalz)="Das nehmen", table2(Märchengasse)="Jede Karte"+stats, table3–6=plain theme-name heading, no rotating headline
   - Freiburg (continuation, not separate themes): slide1(rows1-3)="Das nehmen", slide2(rows4-5, continuation)="Jede Karte"+stats

   **Resolved by designer (2026-08-18, see `docs/open-questions.md` #10) — the stated rule stands; the reference decks have the bug, not the rule.** Theme 1 → "Jede Karte ist ein Unikat — und ein Grund zum Teilen." headline, and theme 1 must **always** carry the 70%-stats callout (canonical text confirmed, see `docs/open-questions.md` #7: "70 % der Besucher teilen ihr Motiv aktiv auf Facebook, Instagram oder TikTok — mit Ihrem Markt als Kontext.") — that pairing is the important, non-negotiable part. Theme 2 → "Das nehmen Ihre Besucher mit — personalisiert, sofort, teilbar." Exact headline wording per theme position is a minor detail per the designer; the stats-stays-with-theme-1 rule is what matters. Do not model the 3 measured reference decks' (reversed) order as correct.
2. **The motif table is one flattened image per slide in the source, not 9 separate cell images.** This is a real architecture question for WP6/WP7/WP8, not just a WP4 measurement note: will the generator receive one pre-composed table image per theme (simplest, but means table layout/rows can't be built programmatically — contradicts the brief's "insert every image" language which implies per-field images), or will it need to compose the 3×3 grid itself from 9 separate motif images per table (matching the JSON schema's implied per-field structure, e.g. `IMG_MOTIF_1_PHOTO`, `IMG_MOTIF_1_BACKGROUND`, `IMG_MOTIF_1_MASK`)? **Resolved by designer (2026-08-18, see `docs/open-questions.md` #9): prefer 9 separate per-cell images, composed into the 3×3 grid by the generator, where feasible.** WP5's field catalogue for this page type should use per-cell fields (`IMG_MOTIF_{n}_PHOTO`, `IMG_MOTIF_{n}_BACKGROUND`, `IMG_MOTIF_{n}_MASK`, ×3 rows per table).
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
| Theme-world-name caption (e.g. "Hallescher Weihnachtsmarkt") | **Variable, mandatory — not "Halle-only"** | Halle has visible overlay caption text (appearing twice per card — likely a stroke+fill duplicate in the source, not 2 real instances) that no other deck has. Frame ratio also differs more (1.41–1.63) than the other 4. |

**Resolved by designer (2026-08-18, see `docs/open-questions.md` #8) — the premise was wrong.** This isn't market-name branding, it's the **theme-world name**, and it must be present 100% of the time in both places it can appear: next to the theme-world photo (`PAGE_03_THEME_SHOWCASE`) *and* on the output cards here. The other 4 decks are each missing a caption they should have — Halle is the correct/current version, not an outlier extra treatment. Ties together with `PAGE_06_LOCAL_MOTIFS`'s already-confirmed mandatory theme-world-name caption rule.

---

## PAGE_09_SOCIAL_REACH

| Element | Fixed / Variable | Detail |
|---|---|---|
| Headline, 90%/70% stat labels, 3 bullet points | **Fixed** | Byte-identical across all 5 (headline 56–57 chars; minor comma difference in Halle's headline, not meaningful). |
| Closing paragraph ("Nach der Saison erhalten Sie...") | **Fixed** | Byte-identical content, 223 chars, confirmed via Erzgebirgsdorf/Halle's unbroken version — Basel/Freiburg/Magdeburg's extraction shows this text split oddly with a chunk apparently missing, which on inspection is a text-flow/line-order extraction artifact (multi-line-wrap reading order), **not a real content difference**. Treat 223 characters as the authoritative fixed length. |
| Instagram mockup photo, captioned with market name | **Variable** | Caption = market name (reuses the same field as `PAGE_01_TITLE`'s subline market name, just the city, not the full sentence — needs its own shorter field, not measured separately here since the visible caption is the market name alone judging from `docs/01-slide-inventory.md`'s descriptions). Frame ratio: 1.33 in 3/5 decks, 1.31 (Erzgebirgsdorf), 1.03 (Halle, notably square-ish, an outlier). **Target 1.33; flag Halle's crop as a designer question below.** |

**Resolved by designer (2026-08-18, see `docs/open-questions.md` #13):** standardize to one fixed ratio everywhere — **1.33** (the majority value). Halle's 1.03 crop was not intentional.

---

## PAGE_10_CONTACT

| Element | Fixed / Variable | Detail |
|---|---|---|
| Headline ("Lassen Sie uns gemeinsam...") | **Fixed** | Byte-identical across all 5, 55 chars. |
| Company block (cosmoproducts GmbH, Martin Baack, address, phone, email, website) | **Fixed** | Byte-identical across all 5 — same company contact info regardless of market, confirmed. Combined block length 167 chars across the 5 lines. |
| Intro/closing paragraph ("Interesse geweckt?...") | **Fixed** | Byte-identical content (≈294–295 chars total) across all 5 — the apparent 170+124 vs. one-block-of-295 split is just a text-block-boundary rendering difference, not a real content variant (confirmed: 170+124=294 ≈ the single-block versions' 295). |
| Hero photo (market landmark) | **Variable** | Market-specific. Frame ratio varies more than any other page type's photo: 0.559 (3/5 decks), 0.750 (Erzgebirgsdorf), 0.684 (Halle) — all portrait orientation but a real spread, not measurement noise (bbox is clean/on-canvas in all 5). **Flagged below rather than picking one target.** |

**Resolved by designer (2026-08-18, see `docs/open-questions.md` #14):** standardize to one fixed portrait ratio everywhere — **0.559** (the majority value, matching this doc's original recommendation), not per-market crop discretion.

---

## Cross-cutting open questions (not specific to one page type)

1. ~~Recurring "2 known variants" pattern~~ **Resolved by designer, 2026-08-18** — see `docs/open-questions.md` section B for the consolidated answer set (items #3–8). `PAGE_08_TRANSITION`'s caption in particular turned out not to be a copy-version question at all — see that page type's section above.
2. ~~The motif-table-as-one-flattened-image finding~~ **Resolved by designer, 2026-08-18** — see `docs/open-questions.md` #9 and `PAGE_06_LOCAL_MOTIFS` open question 2 above. 9 separate per-cell images, generator composes the grid. WP5 can now proceed on this page type.
3. Source artboards are 4:3; new template is 16:9 (per WP6). None of the frame ratios measured here transfer directly — they're a documented starting reference for "what the source used", to compare against once layouts are redrawn for 16:9 in WP6, not values to hard-code into the new template.

**Remaining open items before WP5, none blocking:** `docs/open-questions.md`
section A (Erzgebirgsdorf file freshness, "Märchenwelt Schwerin" naming) and
`PAGE_05_USER_FLOW` open question 2 (output-card layout) above are still
unanswered as of 2026-08-18.
