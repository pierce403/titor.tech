#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

# Preserve revision dates if a Git-aware plugin needs the complete history.
if [ "$(git rev-parse --is-shallow-repository)" = "true" ]; then
  git fetch --unshallow origin
fi

# Isolate the locked renderer from the build image's global Python packages.
python3 -m venv .venv
.venv/bin/python -m pip install --disable-pip-version-check -r requirements.lock
.venv/bin/python -m mkdocs build --clean --strict
test -f site/index.html
test -f site/404.html
test -f site/search/search_index.json

# Keep docs/CNAME in source for GitHub Pages recovery, outside Worker output.
rm -f site/CNAME
