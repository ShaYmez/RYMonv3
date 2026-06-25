#!/bin/bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [[ ! -d .venv ]]; then
    echo "No .venv — run ./install.sh first" >&2
    exit 1
fi

if [[ ! -f rymon.cfg ]]; then
    echo "No rymon.cfg — copy rymon_SAMPLE.cfg and edit FDMR_IP / FDMR_PORT" >&2
    exit 1
fi

# shellcheck disable=SC1091
source .venv/bin/activate
exec python monitor.py