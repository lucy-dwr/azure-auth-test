#!/usr/bin/env bash
set -euo pipefail

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

.venv/bin/python -m pip install --upgrade pip

if [ -f "requirements.txt" ]; then
  .venv/bin/python -m pip install -r requirements.txt
else
  echo "requirements.txt not found; skipping dependency install."
fi

echo "Setup complete."
echo "Run scripts with: .venv/bin/python <script.py>"
echo "Optional activation: source .venv/bin/activate"
