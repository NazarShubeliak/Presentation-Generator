# Presentation Generator

A system that turns a small set of location data into a complete, individualised
PowerPoint presentation. This repository covers **Step 1**: analysing the existing
manually-built presentations, deriving a page type catalogue, building a PowerPoint
master template, defining a JSON data structure, and writing a script that turns a
JSON file into a finished `.pptx` file.

Location research, AI-generated content and any user interface are out of scope for
this step — see `docs/` for the full task assignment and analysis documents.

## Project structure

```
presentation-generator/
    src/                 # Python code
    templates/           # the PowerPoint master template
    schema/              # JSON schema
    data/                # example JSON files
    docs/                # all analysis documents
    output/              # generated files (git-ignored)
    reference/           # the 5 source presentations (git-ignored, confidential)
    .venv/               # Python virtual environment (git-ignored)
```

`output/` and `reference/` are excluded from Git: generated files are build
artefacts, and the reference presentations are large, confidential customer
material.

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

## Usage

Once the template and schema exist (Work Packages 6–7), a presentation is
generated with:

```
python src/build_presentation.py --input data/example_01.json --template templates/master_v01.pptx --output output/
```

This is not yet implemented — see `docs/` for progress.
