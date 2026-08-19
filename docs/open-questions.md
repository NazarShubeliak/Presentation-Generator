# Open Questions for Martin / the Designer

Consolidated from WP3 (`docs/02-page-types.md`) and WP4 (`docs/03-elements.md`).
Per ground rule 3 ("feedback from the designer is written down"), answers
should be recorded back into the relevant source doc once received, not just
here.

## A. Files and data

1. Is there a newer `.ai`/PDF for **Erzgebirgsdorf**, the way Magdeburg's PDF
   turned out to be outdated (10 slides vs. the correct 16 — see
   `docs/01-slide-inventory.md`)? Specifically: has the Duisburg-background
   kiosk-screenshot bug (`PAGE_05_USER_FLOW`) already been fixed there too?
   **Resolved (2026-08-18): no newer file — the Erzgebirgsdorf presentation
   itself is current/fine.** The Duisburg-background kiosk screenshot is a
   standalone content mistake (a QC-rule-4.4 cross-market-contamination
   violation, same category as the Magdeburg instance), not a symptom of
   using a stale file version. Treat it as a one-off error to flag/fix, not
   as a file-freshness problem.
2. The Erzgebirgsdorf motif-table subheading **"Märchenwelt Schwerin"** —
   the general cross-market-contamination principle is confirmed (designer's
   QC rule 4.4, `docs/02-page-types.md`), but this specific instance hasn't
   been confirmed by name: mislabeled market, or an intentional theme name?
   **Resolved (2026-08-18): it's a mistake** — leftover from copy-pasting
   another market's slide/table, same QC-rule-4.4 violation category as
   question 1's kiosk background. Not an intentional theme name.

## B. Copy — recurring "two versions" pattern

The same shape keeps showing up: a shorter/older-looking version of a fixed
text in some decks, a fuller/newer-looking version in others, split roughly
along the same deck lines (Erzgebirgsdorf and/or Halle vs. Basel/Freiburg/
Magdeburg). Reads like an in-progress copy revision that wasn't back-applied
everywhere, not 5 independent choices — one combined question rather than 5:

3. `PAGE_02_SERVICE` headline: "...bis Betreuung **vor Ort**." vs. "...bis
   Betreuung" (missing those two words). **Resolved (2026-08-18):** "...bis
   Betreuung vor Ort." is the canonical/current text. Erzgebirgsdorf's
   shorter version is the outdated one.
4. `PAGE_04_REFERENCES` caption: "Barock & Schloss — Markgraf · Hofdame ·
   Venezianische Maskenfigur." vs. just "Barock & Schloss" (no description).
   **Resolved (2026-08-18):** the full version with the "— Markgraf ·
   Hofdame · Venezianische Maskenfigur." suffix is canonical.
5. `PAGE_04_REFERENCES` client-list footer: with or without "Striezelmarkt
   Dresden". **Resolved (2026-08-18) — and the premise was wrong.** This
   isn't a "two versions, pick one" question: it's a standing rule. A
   market's own reference list must never include itself. "Striezelmarkt
   Dresden" appears in the footer of every deck *except* the deck built
   for Striezelmarkt Dresden itself. So the footer content is effectively
   **variable** (fixed list minus the current deck's own market), not
   fixed-with-a-variant as originally framed — update
   `docs/03-elements.md`'s `PAGE_04_REFERENCES` row to reflect this
   generation rule, not a copy-version ambiguity.
6. All 4 fixed `PAGE_05_USER_FLOW` text fields (3 step labels + disclaimer)
   exist in two complete variants. **Resolved (2026-08-18):** the
   designer-confirmed canonical text is what `docs/03-elements.md` already
   recorded as **"Variant B"** (the Erzgebirgsdorf/Halle wording) —
   step 1 "Maske wählen — aus den Erlebniswelten Ihres Markts.", step 2
   "Hintergrund wählen — Ihre Stadt, Ihr Markt, Ihre Atmosphäre.", step 3
   "Foto machen — fertig. Das Erlebnis-Souvenir ist sofort da.", disclaimer
   "Keine Einweisung, keine Wartezeit, keine Technik für Ihr Team — Ihre
   Besucher stehen davor und verstehen es sofort." Basel/Freiburg/
   Magdeburg's "Variant A" is the outdated one — note this is the minority
   deck-count winning, not the majority.
7. `PAGE_06_LOCAL_MOTIFS` stats callout ("70 % der Besucher...") also has 2
   phrasing variants. **Resolved (2026-08-18):** canonical text is "70 %
   der Besucher teilen ihr Motiv aktiv auf Facebook, Instagram oder TikTok
   — mit Ihrem Markt als Kontext." This callout must always appear on the
   **first** motif table (theme 1) — see question 10 below, same answer.
8. `PAGE_08_TRANSITION`: only Halle has an overlay caption with the market
   name on the output-card photos; the other 4 decks don't. **Resolved
   (2026-08-18) — and the premise was wrong.** It's not market-name
   branding, it's the **theme-world name**, and per the designer it must
   be present 100% of the time in both places it can appear: next to the
   theme-world photo (huts, `PAGE_03_THEME_SHOWCASE`) *and* on the output
   cards (`PAGE_08_TRANSITION`). The other 4 decks are missing a caption
   they should have, not showing a valid caption-less alternative — ties
   together with `PAGE_06_LOCAL_MOTIFS`'s already-confirmed "mandatory
   theme-world-name caption" rule (`docs/02-page-types.md`).

**Question: which version is current? Should the other decks be updated
to match?** All answered above — see per-item resolutions.

## C. Schema architecture (blocks WP5/WP7/WP8 — highest priority)

9. **The `PAGE_06_LOCAL_MOTIFS` table is one flattened image per theme in
   the source, not 9 separate per-cell images.** Will the generator receive
   one pre-composed table image per theme (simple, but the row layout can't
   be built programmatically), or 9 separate motif images that the
   generator composes into the 3×3 grid itself (matches the schema's
   implied per-field structure)? This decision blocks the WP5 field
   catalogue for this page type. **Resolved (2026-08-18):** prefer 9
   separate per-cell motif images that the generator composes into the
   3×3 grid itself, where feasible. WP5's field catalogue for this page
   type should use per-cell fields (e.g. `IMG_MOTIF_1_PHOTO`,
   `IMG_MOTIF_1_BACKGROUND`, `IMG_MOTIF_1_MASK`, ×3 rows), not one
   pre-composed table image.
10. **The headline-rotation rule doesn't match measurement.** Stated rule:
    world 1 → "Jede Karte ist ein Unikat...", world 2 → "Das nehmen Ihre
    Besucher mit...". Measured: in Basel, Halle, and Magdeburg, the
    *first* standalone motif table always uses "Das nehmen..." and the
    *second* always uses "Jede Karte..." — consistently the reverse of the
    stated rule. Raw per-deck order is recorded in `docs/03-elements.md`
    under `PAGE_06_LOCAL_MOTIFS`, open question 1. **Resolved (2026-08-18)
    — the stated rule stands, the reference decks are the ones with the
    bug.** Theme 1 → "Jede Karte ist ein Unikat..." headline, and theme 1
    must **always** carry the 70%-stats callout (question 7 above) —
    that pairing is the important, non-negotiable part. Theme 2 → "Das
    nehmen Ihre Besucher mit...". Which exact headline wording lands on
    which theme is otherwise a minor detail per the designer — the
    stats-callout-stays-with-theme-1 rule is what matters. The 3
    reference decks measured (Basel, Halle, Magdeburg) all have this
    backwards and should not be treated as the model to replicate.
11. `PAGE_03_THEME_SHOWCASE` sometimes shows 1 photo+caption, sometimes 2
    (side by side). Should the schema represent this as an array of 1–2
    theme entries, with layout picked automatically by array length?
    **Resolved (2026-08-18): yes**, confirmed as-is — more themes → 2 huts
    on one photo, fewer → 1, automatic layout by array length is fine.
12. The optional theme-world caption on `PAGE_01_TITLE`/`PAGE_02_SERVICE`
    (only present when a deck has >2 theme worlds) — should this be
    authored explicitly in the JSON, or computed by the generator from a
    `theme_worlds` list? **Resolved (2026-08-18): computed by the
    generator from `theme_worlds`.** This overturns `docs/03-elements.md`'s
    original recommendation (it had suggested authoring explicitly, for
    generator simplicity) — designer prefers the automatic/computed
    approach, consistent with question 11's answer.

## D. Aspect ratios needing a design call

13. Instagram mockup on `PAGE_09_SOCIAL_REACH`: Halle's frame ratio is 1.03
    (near-square) vs. 1.33 in the other 4 decks — intentional different
    crop, or a mistake? **Resolved (2026-08-18):** standardize — one fixed
    ratio everywhere (1.33, the majority value). Halle's 1.03 crop was not
    intentional.
14. Hero photo on `PAGE_10_CONTACT`: ratio ranges 0.56–0.75 across the 5
    decks — should the template enforce one fixed portrait ratio, or is
    per-market crop discretion intended? **Resolved (2026-08-18):** same
    answer — standardize to one fixed ratio everywhere (0.559, the
    majority value already recommended in `docs/03-elements.md`), not
    per-market crop discretion.

## F. Blocking WP6 — for Martin specifically (new, 2026-08-18)

17. **Is there an official CI package** (fonts, colours, logo files) for
    the new master template, as the task assignment's own placeholder list
    asks ("Official CI template available? — to be provided by Martin")?
    Or should the template's fonts/colours/logo be derived from what's
    actually measured in the 5 reference `.ai` files (already have the
    tooling from WP4 — `src/extract_ai_measurements.py` pulls real font
    data)? **Resolved (2026-08-18): no official CI package — Martin said
    to build it ourselves.** Fonts/colours/logo for the master template
    are derived from what's actually measured across the 5 reference
    `.ai` files. WP6 is now unblocked.
18. **Is there a logo mark that should appear on the master template**
    (e.g. slide master footer, title slide)? No standalone logo image was
    found in any of the 5 reference `.ai` files — "cosmoproducts GmbH" on
    `PAGE_10_CONTACT` appears to be styled text, not an embedded graphic.
    Not yet asked. Doesn't block starting the layouts/placeholders, but
    needs an answer before the slide master step (WP6 step 2) is
    complete — see `docs/05-template.md`.
19. **`PAGE_03_THEME_SHOWCASE`'s theme-world caption styling is inconsistent
    across all 3 decks that have it, in both position and typography, not
    just the already-resolved 1-vs-2-up array question (question 11):**
    - Basel's single-theme instance ("Die Schweiz erleben"): top-left,
      `HelveticaNeue-CondensedB` 27.41pt, `#f2f0ee` (near-white) — large and
      headline-like.
    - Halle's single-theme instance ("Hallmarkt & Salzstadt"): bottom,
      right-of-centre, `MyriadPro-Regular` 15.08pt, `#fcb657` (gold) — small
      and caption-like.
    - Halle's 2-up instance ("Luther & Reformation" / "Händelstadt Halle"):
      bottom, side-by-side over each photo half, `MyriadPro-Regular`
      15.08pt, `#fcb657`.
    - Magdeburg's 2-up instances: bottom, side-by-side, `HelveticaNeue-
      CondensedB` 16.45pt, `#f2f0ee`.
    No two instances share the same font+colour+position combination, and
    it doesn't split cleanly by single-vs-2-up either (Halle's single and
    2-up match each other; Magdeburg's 2-up doesn't match Halle's 2-up).
    Needs a designer decision on the canonical caption treatment for this
    page type — not guessing one from majority count since there's no
    majority (3 different combinations across 4 measured instances).
    Blocks finalizing `PAGE_03_THEME_SHOWCASE` in `docs/05-template.md`.
20. **`PAGE_05_USER_FLOW`'s 2-card output example may have the same
    flattened-image problem already found and resolved for
    `PAGE_06_LOCAL_MOTIFS` (question 9).** `docs/04-fields.md` currently
    lists `IMG_USER_FLOW_CARD_1`/`IMG_USER_FLOW_CARD_2` as two separate
    fields with a "combined frame ratio ≈1.78". Re-checked directly against
    the source `.ai` files while building `docs/05-template.md`
    (2026-08-19): in all 3 canonical decks (Basel, Freiburg, Magdeburg —
    the confirmed 2-card layout, `docs/open-questions.md` #2 resolution),
    the slide has exactly **one** image XObject in that region (native
    pixel dims e.g. 1672×941, ratio 1.78 — matching the "combined" ratio
    exactly), not two. Same open question as #9: is the generator meant to
    receive one pre-composed "both cards side by side" photo (matches what
    the source files actually contain, but the two output-card examples
    can no longer be chosen independently), or should this become two
    separate per-card image fields that the template composes side by side
    (matches the schema's current per-field assumption, but doesn't match
    any of the 5 source decks)? Blocks finalizing `PAGE_05_USER_FLOW`'s
    image placeholders in `docs/05-template.md` — built with 2 separate
    placeholders for now (matching the existing WP5 field catalogue) but
    flagged as provisional pending this answer, same treatment as
    `TXT_KIOSK_BACKGROUND_LABEL` below.
21. **`TXT_KIOSK_BACKGROUND_LABEL`, re-checked while building WP6
    (2026-08-19):** confirmed baked into the `IMG_KIOSK_SCREENSHOT` image
    in all 5 source decks — no separate overlay text object found at that
    position in any deck. Leaning toward "not a real separate field, purely
    part of the image asset" (matching `PAGE_08_TRANSITION`'s already-
    resolved market-name-watermark precedent, `docs/open-questions.md` #8),
    but still not formally asked — carry into the next batch of designer
    questions alongside #19 and #20.

## E. Found while building the WP5 field catalogue (new, 2026-08-18)

15. `PAGE_06_LOCAL_MOTIFS` headline, table position 3 and beyond: the
    stated rule says "Ihre Charaktere. Ihre Geschichte." but measurement
    shows position-3+ tables actually use a plain theme-name heading
    instead (Magdeburg tables 3–6, Halle tables 4–5). The designer's
    2026-08-18 answer (question 10) only confirmed positions 1 and 2 —
    which is correct for position 3+: the stated fixed text, or the
    plain theme-name heading actually seen in the decks? **Resolved
    (2026-08-18):** position 3 → fixed text "Ihre Charaktere. Ihre
    Geschichte." (as originally stated); position 4 and beyond → plain
    theme-name heading, matching what's actually seen in the decks. So
    the full rotation is now: 1st="Jede Karte..."+stats, 2nd="Das
    nehmen...", 3rd="Ihre Charaktere...", 4th+ = plain theme name.
16. `PAGE_06_LOCAL_MOTIFS` intro paragraph (below the headline) has 2
    known phrasing variants plus an "absent from the 3rd table onward"
    pattern — this is the same "2 versions" shape as the items in section
    B, but it wasn't included in that batch of questions and so wasn't
    answered. Which version is canonical, and does it stay absent from
    the 3rd table onward or should it be present with a value?
    **Partially resolved (2026-08-18):** canonical wording confirmed as
    "Jedes Motiv wird individuell passend zu Ihrem Event gestaltet — Ihre
    Besucher werden Teil Ihrer Erlebniswelt. Das teilen sie." (120 chars).
    **Still open:** whether it should now appear on position-3+ tables
    too (question 15's answer means position 3 gets a real headline
    again, unlike what was measured) — not explicitly confirmed, don't
    assume either way.
