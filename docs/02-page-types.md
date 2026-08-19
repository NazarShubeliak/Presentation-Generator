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

## PAGE_03_THEME_SHOWCASE

**Purpose:** Full-bleed photo (or 2-up photo pair) of a themed booth variant,
captioned with the theme name only — no bullet copy, no motif table. Reads
as a "preview" for a theme world that gets its own `LOCAL_MOTIFS` table
later in the deck.

**Confirmed by designer (review meeting, see below):** this is a genuine,
separate page type, not a variant of `PAGE_02_SERVICE`. It functions as an
**overflow slot** for theme worlds beyond the two that `PAGE_01_TITLE` and
`PAGE_02_SERVICE` already carry a booth photo for. Every deck's title slide
and service slide each showcase one theme world "for free" via their own
photo; any theme world beyond those first two needs a `PAGE_03` slide to get
a photo of its own (themes can be doubled up 2-per-slide, e.g. as a 2-up
pair). Designer's worked example, Halle (5 theme worlds):

| Theme world | Where its photo appears |
|---|---|
| 1. Historisches Halle | `PAGE_01_TITLE` cover photo |
| 2. Luther & Reformation | `PAGE_03_THEME_SHOWCASE` slide 2 (2-up with #3) |
| 3. Händelstadt Halle | `PAGE_03_THEME_SHOWCASE` slide 2 (2-up with #2) |
| 4. Märchen- und Familienwelt | `PAGE_02_SERVICE` booth photo |
| 5. Hallmarkt & Salzstadt | `PAGE_03_THEME_SHOWCASE` slide 4 (single) |

Basel (3 theme worlds) fits the same rule: 2 absorbed by title+service, 1
left over → exactly the 1 `PAGE_03` instance seen there. Magdeburg (6 theme
worlds, re-reviewed 2026-08-17 after its reference file was updated — see
`docs/01-slide-inventory.md`) also fits: 2 absorbed by title+service, 4 left
over → exactly 2 `PAGE_03` slides (2-up pairs), same shape as Halle.

**Open follow-up for WP4:** this rule was confirmed against Basel and Halle,
both of which structure `LOCAL_MOTIFS` as one table per theme world. It's
not yet clear how (or whether) the rule applies to the continuation-style
decks (Freiburg, Magdeburg, Erzgebirgsdorf), where `LOCAL_MOTIFS` lists
several motifs per table rather than one theme per table — carry this into
open question #2 below.

- Appears in: **3 of 5** (Basel — 1 instance; Halle — 2 instances; Magdeburg — 2 instances)
- Mandatory or optional: **Optional** — activates only when a deck's theme
  count exceeds 2 (the number already absorbed by `PAGE_01_TITLE` +
  `PAGE_02_SERVICE`)
- Occurs once or repeats: **Repeats**, one slide per 1–2 overflow themes
- Representative screenshot: `docs/slides/helle_hallescher_weihnachtsmarkt_2026/slide_02.png`

![PAGE_03_THEME_SHOWCASE](slides/helle_hallescher_weihnachtsmarkt_2026/slide_02.png)

---

## PAGE_04_REFERENCES

**Purpose:** Cross-client portfolio grid — "Jeder Markt bekommt seine eigene
Welt.", 4 example booth themes from other markets (Salzburg, Kassel,
Charlottenburg, Erzgebirge) plus a footer list of past clients.

**Resolved by designer (2026-08-18, see `docs/open-questions.md` #5):** the
footer list is **not** simply reused verbatim — it must always exclude the
deck's own market. "Striezelmarkt Dresden" appears in every deck's footer
except the one built for Striezelmarkt Dresden itself. So the footer is a
fixed list, filtered per-generation by the current market, not a fully
fixed/reused block.

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

**Resolved by designer (review meeting, see below):** the kiosk-screenshot
must show location-specific artwork for each market — it is a `variable`
element for WP4, not a fixed generic asset. The 2 instances found
(Erzgebirgsdorf and Magdeburg both showing Duisburg backgrounds) are
**not** acceptable/intended reuse — they are a **QC violation** in the
reference decks and should be escalated (to Mathias/Martin, per the weekly
status note in the ground rules), not modeled as normal behaviour.

---

## PAGE_06_LOCAL_MOTIFS

**Purpose:** 3-column table (Fotokarte / Hintergrund / AR-Maske) presenting
the market's own themed photo motifs, one row per motif. The main
location-specific content block of each deck; can span multiple slides when
a market has several theme worlds or more than 3 motifs.

**Resolved by designer (review meeting, see below):** stays **one page
type**, but the draft's original theory for why headlines differ was wrong.
It is not "different headline = continuation table." There are actually
**two separate, unrelated mechanisms**, both producing multi-slide
`PAGE_06` sequences, which the draft had conflated into one open question:

1. **Headline rotates by the theme-world's ordinal position in the deck**
   (only relevant to decks like Halle that give each theme world its own
   table):

   | World position in deck | Headline |
   |---|---|
   | 1st world | *"Jede Karte ist ein Unikat — und ein Grund zum Teilen."* + a social-share stats block (FB/Insta/TikTok %) |
   | 2nd world | *"Das nehmen Ihre Besucher mit — personalisiert, sofort, teilbar."* |
   | 3rd world and beyond | *"Ihre Charaktere. Ihre Geschichte."* |

   **Designer-confirmed (2026-08-18, see `docs/open-questions.md` #10):**
   this rule stands as-is — the reference decks (Basel, Halle, Magdeburg)
   were all measured with the 1st/2nd world order reversed from this
   table, which is a bug in those decks, not the rule. The important,
   non-negotiable part is that the social-share stats block always stays
   with the 1st world's headline; exact headline wording per position
   matters less.

   Plus a **mandatory** rule not previously captured: every such slide must
   be captioned with its own theme world's name (e.g. "Händelstadt Halle")
   — and per the designer, this same theme-world-name captioning is
   mandatory on `PAGE_08_TRANSITION`'s output-card photos too, not just
   here (see that page type's entry below).

2. **Row-limit continuation** (Freiburg: 2 slides/5 motifs; Magdeburg: 2
   slides/6 motifs) — a *single* theme's motif table overflowing its row
   limit onto a second slide. Same headline repeats/continues across both
   slides; this is unrelated to mechanism 1 and must not be modeled with the
   same headline-rotation logic.

For WP4 this means `PAGE_06_LOCAL_MOTIFS` gets two new variable elements on
top of the motif table itself: a **headline**, selected by a lookup keyed on
theme-world position (not free text — fixed set of 3 strings), and a
**mandatory theme-world-name caption**. The row-limit continuation mechanism
(2) still needs its own row-limit number derived in WP4 (how many motif rows
trigger a continuation slide) — not yet measured.

- Appears in: **all 5 presentations**
- Mandatory or optional: **Mandatory**
- Occurs once or repeats: **Repeats** — count varies a lot per deck:
  - Basel: 3 tables / 3 themes (1 slide each) — includes one table themed to
    Switzerland generally rather than Basel specifically (see note below)
  - Erzgebirgsdorf: 1 table (subheading names a mismatched market, "Märchenwelt Schwerin" — see `docs/01-slide-inventory.md`)
  - Freiburg: 2 slides / 5 motifs (mechanism 2: row-limit continuation, not
    a new theme per slide)
  - Magdeburg: 6 tables / 6 theme worlds (1 slide each, mechanism 1:
    headline-by-position) — re-reviewed 2026-08-17 after its reference file
    was found outdated and replaced, see `docs/01-slide-inventory.md`;
    previously (incorrectly) recorded as 2 slides/6 motifs continuation
  - Halle: 5 tables / 5 theme worlds (1 slide each, mechanism 1:
    headline-by-position) — structurally near-identical to the corrected
    Magdeburg, see `docs/01-slide-inventory.md` cross-deck notes
- Representative screenshot: `docs/slides/helle_hallescher_weihnachtsmarkt_2026/slide_07.png`

![PAGE_06_LOCAL_MOTIFS](slides/helle_hallescher_weihnachtsmarkt_2026/slide_07.png)

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
| PAGE_03_THEME_SHOWCASE | 3/5 | Optional (activates if themes > 2) | Repeats (0–2) |
| PAGE_04_REFERENCES | 5/5 | Mandatory | Once |
| PAGE_05_USER_FLOW | 5/5 | Mandatory | Once |
| PAGE_06_LOCAL_MOTIFS | 5/5 | Mandatory | Repeats (1–6 slides) |
| PAGE_07_BESTSELLERS | 5/5 | Mandatory | Once |
| PAGE_08_TRANSITION | 5/5 | Mandatory | Once |
| PAGE_09_SOCIAL_REACH | 5/5 | Mandatory | Once |
| PAGE_10_CONTACT | 5/5 | Mandatory | Once |

Total page types: **10** (brief's example list had 8; 2 extra found —
`PAGE_03_THEME_SHOWCASE` and the `LOCAL_MOTIFS`/`BESTSELLERS` split, which
the brief's example already implied but is worth confirming explicitly).

## Open questions for the designer meeting

1. ~~Should `PAGE_03_THEME_SHOWCASE` stay a separate type, or fold into
   `PAGE_02_SERVICE` / `PAGE_06_LOCAL_MOTIFS`?~~ **Resolved.** Confirmed as
   a separate type — see the designer's note and the Halle worked example
   under `PAGE_03_THEME_SHOWCASE` above.
2. ~~Should `PAGE_06_LOCAL_MOTIFS` single-theme tables and multi-slide
   continuation tables (different headline pattern) be split into two
   types?~~ **Resolved — and the premise was wrong.** Stays one type. The
   draft conflated two unrelated mechanisms (headline-rotation-by-world-
   position vs. row-limit continuation within one theme); see the
   designer's note and table under `PAGE_06_LOCAL_MOTIFS` above. Follow-up
   for WP4: measure the actual row-limit trigger for mechanism 2, not yet
   done.
3. ~~Data-quality flag (not a page-type question, but relevant context): the
   Erzgebirgsdorf deck has several slides referencing the wrong market
   (Schwerin, Chemnitz, Duisburg-background kiosk photo), and Magdeburg
   reuses the same mismatched Duisburg kiosk photo.~~ **Resolved.** Designer
   confirmed all instances (kiosk-photo backgrounds, theme-world-name
   captions, and any other cross-market trace) are genuine QC violations,
   not intended reuse — none of it should be modeled as normal/acceptable
   behaviour in WP4/WP5. Designer has formalized this into a new mandatory
   step in their own pre-delivery QC checklist, **4.4 "Cross-Market
   Contamination Check"**, added alongside their existing 4. Personalization
   Rules — recorded here for context, not something this project builds,
   but directly relevant to which fields WP4/WP5 must treat as
   per-market-variable:
   - theme-world-name captions under motif tables (e.g. `PAGE_06_LOCAL_MOTIFS`)
   - background-choice labels shown in the kiosk-interface screenshot (`PAGE_05_USER_FLOW`)
   - logos/stamps baked directly into output photo cards (`PAGE_08_TRANSITION`, `PAGE_09_SOCIAL_REACH` mockup)
   - any other text visible inside an image or screenshot, not just on-slide text

   Designer's rationale: this is the worst failure mode for the client —
   visible proof the deck was reused from another market's template without
   proofreading, which damages trust more than any formatting error. Worth
   carrying into WP8: the generator script's "missing field" warning
   mechanism (`<<MISSING: ...>>`) should have an equivalent guard against
   *wrong* per-market values being silently left in, not just missing ones —
   flag as a WP8 consideration, not yet a decision.
