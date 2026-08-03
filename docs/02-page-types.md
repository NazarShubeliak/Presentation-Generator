# Page Type Catalogue (WP3) — DRAFT for designer review

Derived by comparing the five slide inventories in `docs/01-slide-inventory.md`
and grouping slides that fulfil the same purpose, even where their content
differs. IDs follow the task brief's format (`PAGE_NN_NAME`, English, upper
snake case) but the list itself is **not** the brief's example list — it
reflects what was actually found across the 5 decks, including two groupings
(`PAGE_03_THEME_SHOWCASE`, splitting `LOCAL_MOTIFS` from `BESTSELLERS`) that
the brief's example doesn't spell out.

**This is a draft.** Flagged with an ⚠️ open question anywhere the grouping
is a judgment call rather than an obvious match — please correct at the
review meeting, per WP3 step 5.

---

## PAGE_01_TITLE

**Purpose:** Opening hero slide — headline "Wir machen Ihre Besucher zu einem
Teil Ihrer Geschichte.", subline naming the market, full-bleed photo of the
market's primary AR-Photobooth hut.

- Appears in: **all 5 presentations**
- Mandatory or optional: **Mandatory**
- Occurs once or repeats: **Once**
- Representative screenshot: `docs/slides/basel_2026/slide_01.png`

![PAGE_01_TITLE](slides/basel_2026/slide_01.png)

---

## PAGE_02_SERVICE

**Purpose:** "Ihr Erlebnispartner — von Konzept bis Betreuung [vor Ort]" —
3-bullet value proposition (concept & masks / hut design-tech-setup / on-site
staff), next to a booth photo. Bullet copy is fixed/reusable; the booth photo
and (in Magdeburg's case) the intro sentence vary slightly per deck.

- Appears in: **all 5 presentations**
- Mandatory or optional: **Mandatory**
- Occurs once or repeats: **Once**
- Representative screenshot: `docs/slides/basel_2026/slide_02.png`

![PAGE_02_SERVICE](slides/basel_2026/slide_02.png)

---

## PAGE_03_THEME_SHOWCASE ⚠️

**Purpose:** Full-bleed photo (or 2-up photo pair) of a themed booth variant,
captioned with the theme name only — no bullet copy, no motif table. Reads
as a "preview" for a theme world that gets its own `LOCAL_MOTIFS` table
later in the deck.

- Appears in: **2 of 5** (Basel — 1 instance; Halle — 2 instances)
- Mandatory or optional: **Optional**
- Occurs once or repeats: **Repeats** (0–2 times seen; Halle uses it for 2 of
  its 4 theme-world booths, 1 theme-world booth photo is folded into
  `PAGE_02_SERVICE` instead, and 1 theme world — Halle's
  "Märchen- und Familienwelt" — has no showcase/booth photo at all, only a
  `LOCAL_MOTIFS` table)
- Representative screenshot: `docs/slides/helle_hallescher_weihnachtsmarkt_2026/slide_02.png`

![PAGE_03_THEME_SHOWCASE](slides/helle_hallescher_weihnachtsmarkt_2026/slide_02.png)

⚠️ **Open question for the designer:** is this really a distinct page type,
or is it a variant of `PAGE_02_SERVICE` / an optional lead-in to
`PAGE_06_LOCAL_MOTIFS` that shouldn't get its own ID? It's structurally
simple (one photo + caption) compared to every other page type, and only 2 of
5 decks use it — worth confirming this is meant to stay separate rather than
being one of a small deck's "skipped" optional slides.

---

## PAGE_04_REFERENCES

**Purpose:** Cross-client portfolio grid — "Jeder Markt bekommt seine eigene
Welt.", 4 example booth themes from other markets (Salzburg, Kassel,
Charlottenburg, Erzgebirge) plus a footer list of past clients. Not
location-specific to the deck's own market — same content reused near-
verbatim across decks (Magdeburg's footer list has one extra market name;
otherwise byte-identical).

- Appears in: **all 5 presentations**
- Mandatory or optional: **Mandatory**
- Occurs once or repeats: **Once**
- Representative screenshot: `docs/slides/basel_2026/slide_04.png`

![PAGE_04_REFERENCES](slides/basel_2026/slide_04.png)

---

## PAGE_05_USER_FLOW

**Purpose:** "Für Ihre Besucher: drei Schritte" — numbered 3-step visitor
process (choose mask / choose background/scene / take photo), with a kiosk
UI screenshot and 1–2 output-card examples.

- Appears in: **all 5 presentations**
- Mandatory or optional: **Mandatory**
- Occurs once or repeats: **Once**
- Representative screenshot: `docs/slides/freiburger_weihnachtsmarkt_2026/slide_04.png`

![PAGE_05_USER_FLOW](slides/freiburger_weihnachtsmarkt_2026/slide_04.png)

⚠️ **Open question for the designer:** in 2 of 5 decks (Erzgebirgsdorf,
Magdeburg), the kiosk-screenshot photo shows a different market's
backgrounds (Duisburg) than the deck's own — same stock image reused in
both. Is the kiosk screenshot meant to be genuinely location-specific
artwork per market, or is it acceptable/intended as a fixed generic asset?
This affects whether WP4 should classify it as a "fixed" or "variable"
element.

---

## PAGE_06_LOCAL_MOTIFS

**Purpose:** 3-column table (Fotokarte / Hintergrund / AR-Maske) presenting
the market's own themed photo motifs, one row per motif. The main
location-specific content block of each deck; can span multiple slides when
a market has several theme worlds or more than 3 motifs.

- Appears in: **all 5 presentations**
- Mandatory or optional: **Mandatory**
- Occurs once or repeats: **Repeats** — count varies a lot per deck:
  - Basel: 3 tables / 3 themes (1 slide each) — includes one table themed to
    Switzerland generally rather than Basel specifically (see note below)
  - Erzgebirgsdorf: 1 table (subheading names a mismatched market, "Märchenwelt Schwerin" — see `docs/01-slide-inventory.md`)
  - Freiburg: 2 slides / 5 motifs (continuation across slides, not a new
    theme per slide)
  - Magdeburg: 2 slides / 6 motifs (continuation)
  - Halle: 5 tables / 5 theme worlds (1 slide each) — the deck's structural
    outlier, see `docs/01-slide-inventory.md` cross-deck notes
- Representative screenshot: `docs/slides/helle_hallescher_weihnachtsmarkt_2026/slide_07.png`

![PAGE_06_LOCAL_MOTIFS](slides/helle_hallescher_weihnachtsmarkt_2026/slide_07.png)

⚠️ **Open question for the designer:** should "table with 3 motifs" and
"table spanning 2 slides with 5–6 motifs, continuing the same headline" be
the same page type with a variable row count, or two different page types
(one for single-slide theme tables, one for a multi-slide continuation
layout with a different headline pattern — "Das nehmen Ihre Besucher mit"
vs. "Jede Karte ist ein Unikat")? Currently modeled as one type with
variable length; flagging since the continuation slides do use a visibly
different headline/intro-text pattern.

---

## PAGE_07_BESTSELLERS

**Purpose:** "Best-Seller der Saison 2025" — same 3-column motif table
format as `PAGE_06_LOCAL_MOTIFS`, but fixed, generic, nationwide content
(Weihnachtsrentier, Santa mit Sonnenbrille, Glühwein-Santa) — identical
across all 5 decks, not location-specific.

- Appears in: **all 5 presentations**
- Mandatory or optional: **Mandatory**
- Occurs once or repeats: **Once**
- Representative screenshot: `docs/slides/basel_2026/slide_09.png`

![PAGE_07_BESTSELLERS](slides/basel_2026/slide_09.png)

---

## PAGE_08_TRANSITION

**Purpose:** Two large output photo-card examples, full-bleed, no headline
or body copy — a visual "palate cleanser" between the motif tables and the
closing sections. Correctly branded to the deck's own market in 3 of 5
decks; mismatched to a different city in 1 (Erzgebirgsdorf).

- Appears in: **all 5 presentations**
- Mandatory or optional: **Mandatory**
- Occurs once or repeats: **Once**
- Representative screenshot: `docs/slides/freiburger_weihnachtsmarkt_2026/slide_08.png`

![PAGE_08_TRANSITION](slides/freiburger_weihnachtsmarkt_2026/slide_08.png)

---

## PAGE_09_SOCIAL_REACH

**Purpose:** "Organische Reichweite..." — 90%/70% stat callouts, Instagram
mockup photo captioned with the deck's own market name, 3 bullet points,
social-platform icons.

- Appears in: **all 5 presentations**
- Mandatory or optional: **Mandatory**
- Occurs once or repeats: **Once**
- Representative screenshot: `docs/slides/magdeburger_weihnachtsmarkt_2026/slide_09.png`

![PAGE_09_SOCIAL_REACH](slides/magdeburger_weihnachtsmarkt_2026/slide_09.png)

---

## PAGE_10_CONTACT

**Purpose:** Closing slide — "Lassen Sie uns gemeinsam..." message,
cosmoproducts GmbH contact block (Martin Baack, address, phone, email,
website), hero photo of the market's landmark.

- Appears in: **all 5 presentations**
- Mandatory or optional: **Mandatory**
- Occurs once or repeats: **Once**
- Representative screenshot: `docs/slides/magdeburger_weihnachtsmarkt_2026/slide_10.png`

![PAGE_10_CONTACT](slides/magdeburger_weihnachtsmarkt_2026/slide_10.png)

---

## Summary table

| ID | Appears in | Mandatory? | Repeats? |
|---|---|---|---|
| PAGE_01_TITLE | 5/5 | Mandatory | Once |
| PAGE_02_SERVICE | 5/5 | Mandatory | Once |
| PAGE_03_THEME_SHOWCASE ⚠️ | 2/5 | Optional | Repeats (0–2) |
| PAGE_04_REFERENCES | 5/5 | Mandatory | Once |
| PAGE_05_USER_FLOW | 5/5 | Mandatory | Once |
| PAGE_06_LOCAL_MOTIFS | 5/5 | Mandatory | Repeats (1–5 slides) |
| PAGE_07_BESTSELLERS | 5/5 | Mandatory | Once |
| PAGE_08_TRANSITION | 5/5 | Mandatory | Once |
| PAGE_09_SOCIAL_REACH | 5/5 | Mandatory | Once |
| PAGE_10_CONTACT | 5/5 | Mandatory | Once |

Total page types: **10** (brief's example list had 8; 2 extra found —
`PAGE_03_THEME_SHOWCASE` and the `LOCAL_MOTIFS`/`BESTSELLERS` split, which
the brief's example already implied but is worth confirming explicitly).

## Open questions for the designer meeting

1. Should `PAGE_03_THEME_SHOWCASE` stay a separate type, or fold into
   `PAGE_02_SERVICE` / `PAGE_06_LOCAL_MOTIFS`?
2. Should `PAGE_06_LOCAL_MOTIFS` single-theme tables and multi-slide
   continuation tables (different headline pattern) be split into two types?
3. Data-quality flag (not a page-type question, but relevant context): the
   Erzgebirgsdorf deck has several slides referencing the wrong market
   (Schwerin, Chemnitz, Duisburg-background kiosk photo), and Magdeburg
   reuses the same mismatched Duisburg kiosk photo. Worth asking Martin
   whether these are known copy-paste artifacts before WP4 treats their
   content as a reliable example of "variable" location content.
