# Presentation Generator

A system that turns a small set of location data into a complete, individualised
PowerPoint presentation. This repository covers **Step 1**: analysing the existing
manually-built presentations, deriving a page type catalogue, building a PowerPoint
master template, defining a JSON data structure, and writing a script that turns a
JSON file into a finished `.pptx` file.

Location research, AI-generated content and any user interface are out of scope for
this step — see `docs/` for the full task assignment and analysis documents.

**Status: the generator is implemented and working** (`src/build_presentation.py`,
10 page types, `templates/master_v02.pptx`). Known open issues and the WP9/10
validation writeup are tracked in `docs/06-comparison.md` (local only, not in
Git — see below).

## Project structure

```
presentation-generator/
    src/                 # Python code
    templates/           # the PowerPoint master template(s)
    schema/              # JSON schema
    data/                # example JSON files (git-ignored, real customer content)
    images/              # real per-market photos referenced by data files (git-ignored)
    docs/                # all analysis documents
    output/              # generated files (git-ignored)
    reference/           # the 5 source presentations (git-ignored, confidential)
    .venv/               # Python virtual environment (git-ignored)
```

`output/`, `reference/`, `data/example_01.json`, and `images/` are excluded from
Git: generated files are build artefacts, and the rest is large, confidential
customer material (real presentation text and market photos) — see `.gitignore`
for the full list and reasoning per entry.

## Setup

1. Install Python 3.12 or newer (with "Add Python to PATH" ticked during install).
2. Install Git for Windows and a code editor such as VS Code.
3. Install Microsoft PowerPoint (desktop version). LibreOffice is not suitable —
   it renders `.pptx` files differently in the areas this project depends on
   (text flow, placeholder positions, font metrics).
4. Clone this repository.
5. Create and activate a virtual environment, then install dependencies:

   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install python-pptx jsonschema Pillow
   ```

6. Place the five reference presentations (provided separately) into `reference/`.
   They are not tracked by Git.
7. Place your input JSON (with real market content, see
   `schema/presentation.schema.json` for the required shape) and its referenced
   photos wherever your `--input`/image paths point to — `data/` and `images/`
   are both git-ignored for exactly this content.

## Usage

Generate a presentation with:

```
python src/build_presentation.py --input data/example_01.json --template templates/master_v02.pptx --output output/
```

or, with the same defaults, via the convenience script:

```
./run_generator.sh [input.json] [template.pptx] [output_dir]
```

Each run validates the input against `schema/presentation.schema.json`, fills
every named placeholder it finds a matching field for, writes a
`<<MISSING: FIELD_NAME>>` marker for any required field that's absent (instead
of failing silently), and logs a `schema/template drift` warning for any field
that has no matching placeholder in the template. Output files are versioned
(`<project_id>_v<NN>.pptx`) and never overwritten.

See `docs/06-comparison.md` for the current validation writeup and a list of
known open issues (not tracked in Git — same confidentiality rule as
`reference/`, since it discusses real customer content).
