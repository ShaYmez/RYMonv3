#!/bin/bash
# RYMonv3 — venv install (Debian/Ubuntu). Do not pip install into system Python.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if ! command -v python3 >/dev/null 2>&1; then
    echo "python3 not found" >&2
    exit 1
fi

echo "Installing OS packages (sudo)..."
sudo apt-get update -qq
sudo apt-get install -y \
    python3 \
    python3-venv \
    python3-dev \
    libffi-dev \
    libssl-dev \
    build-essential

if [[ ! -d .venv ]]; then
    echo "Creating .venv..."
    python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

mkdir -p log data

if [[ ! -f rymon.cfg ]]; then
    cp rymon_SAMPLE.cfg rymon.cfg
    echo "Created rymon.cfg from sample — edit [FDMR CONNECTION] before starting."
fi

echo ""
echo "Done. Start with:"
echo "  cd $ROOT"
echo "  source .venv/bin/activate"
echo "  python monitor.py"
echo ""
echo "Or: ./run.sh"