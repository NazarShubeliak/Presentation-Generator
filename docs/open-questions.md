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
2. The Erzgebirgsdorf motif-table subheading **"Märchenwelt Schwerin"** —
   the general cross-market-contamination principle is confirmed (designer's
   QC rule 4.4, `docs/02-page-types.md`), but this specific instance hasn't
   been confirmed by name: mislabeled market, or an intentional theme name?

## B. Copy — recurring "two versions" pattern

The same shape keeps showing up: a shorter/older-looking version of a fixed
text in some decks, a fuller/newer-looking version in others, split roughly
along the same deck lines (Erzgebirgsdorf and/or Halle vs. Basel/Freiburg/
Magdeburg). Reads like an in-progress copy revision that wasn't back-applied
everywhere, not 5 independent choices — one combined question rather than 5:

3. `PAGE_02_SERVICE` headline: "...bis Betreuung **vor Ort**." vs. "...bis
   Betreuung" (missing those two words).
4. `PAGE_04_REFERENCES` caption: "Barock & Schloss — Markgraf · Hofdame ·
   Venezianische Maskenfigur." vs. just "Barock & Schloss" (no description).
5. `PAGE_04_REFERENCES` client-list footer: with or without "Striezelmarkt
   Dresden".
6. All 4 fixed `PAGE_05_USER_FLOW` text fields (3 step labels + disclaimer)
   exist in two complete variants.
7. `PAGE_06_LOCAL_MOTIFS` stats callout ("70 % der Besucher...") also has 2
   phrasing variants.
8. `PAGE_08_TRANSITION`: only Halle has an overlay caption with the market
   name on the output-card photos; the other 4 decks don't.

**Question: which version is current?** Should the other decks be updated
to match?

## C. Schema architecture (blocks WP5/WP7/WP8 — highest priority)

9. **The `PAGE_06_LOCAL_MOTIFS` table is one flattened image per theme in
   the source, not 9 separate per-cell images.** Will the generator receive
   one pre-composed table image per theme (simple, but the row layout can't
   be built programmatically), or 9 separate motif images that the
   generator composes into the 3×3 grid itself (matches the schema's
   implied per-field structure)? This decision blocks the WP5 field
   catalogue for this page type.
10. **The headline-rotation rule doesn't match measurement.** Stated rule:
    world 1 → "Jede Karte ist ein Unikat...", world 2 → "Das nehmen Ihre
    Besucher mit...". Measured: in Basel, Halle, and Magdeburg, the
    *first* standalone motif table always uses "Das nehmen..." and the
    *second* always uses "Jede Karte..." — consistently the reverse of the
    stated rule. Raw per-deck order is recorded in `docs/03-elements.md`
    under `PAGE_06_LOCAL_MOTIFS`, open question 1.
11. `PAGE_03_THEME_SHOWCASE` sometimes shows 1 photo+caption, sometimes 2
    (side by side). Should the schema represent this as an array of 1–2
    theme entries, with layout picked automatically by array length?
12. The optional theme-world caption on `PAGE_01_TITLE`/`PAGE_02_SERVICE`
    (only present when a deck has >2 theme worlds) — should this be
    authored explicitly in the JSON, or computed by the generator from a
    `theme_worlds` list?

## D. Aspect ratios needing a design call

13. Instagram mockup on `PAGE_09_SOCIAL_REACH`: Halle's frame ratio is 1.03
    (near-square) vs. 1.33 in the other 4 decks — intentional different
    crop, or a mistake?
14. Hero photo on `PAGE_10_CONTACT`: ratio ranges 0.56–0.75 across the 5
    decks — should the template enforce one fixed portrait ratio, or is
    per-market crop discretion intended?
