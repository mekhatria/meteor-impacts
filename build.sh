#!/usr/bin/env bash
# Rebuild the four dashboard pages from src/template.html and data/.
#   ./build.sh            rebuild from the saved data
#   ./build.sh --refresh  re-download the NASA/JPL fireball feed first
set -euo pipefail
cd "$(dirname "$0")"
if [ "${1:-}" = "--refresh" ]; then
  curl -sf "https://ssd-api.jpl.nasa.gov/fireball.api" -o data/cneos_fireballs_raw.json
  echo "Fetched NASA/JPL fireball feed. Update the 'retrieved' date in src/split.py."
fi
python3 -I src/prep.py src data
python3 -I src/split.py src .
