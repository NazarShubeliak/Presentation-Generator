#!/usr/bin/env bash
# Run the local web GUI for authoring a presentation's input JSON
# (src/gui/app.py). Local-only tool: binds to 127.0.0.1, no auth.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

source .venv/Scripts/activate

python src/gui/app.py
