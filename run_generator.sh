#!/usr/bin/env bash
# Run the WP8 presentation generator (src/build_presentation.py).
#
# Usage:
#   ./run_generator.sh [input.json] [template.pptx] [output_dir]
#
# All three arguments are optional and default to the paths used for the
# Basel demo run.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

INPUT="${1:-data/example_01.json}"
TEMPLATE="${2:-templates/master_v02.pptx}"
OUTPUT="${3:-output/}"

source .venv/Scripts/activate

python src/build_presentation.py \
  --input "$INPUT" \
  --template "$TEMPLATE" \
  --output "$OUTPUT"
