#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ $# -ne 1 ]]; then
  echo "Usage: scripts/run_command_gate.sh <runtime-io-file>"
  exit 2
fi

runtime_io_file="$1"

if [[ ! -f "$runtime_io_file" ]]; then
  echo "FAIL: runtime IO file not found: $runtime_io_file"
  exit 2
fi

if ! python3 -c "import yaml" 2>/dev/null; then
  echo "Installing PyYAML (required for YAML-structure validation)..."
  python3 -m pip install -q -r "${SCRIPT_DIR}/requirements-runtime-validator.txt"
fi

python3 "${SCRIPT_DIR}/validate_runtime_io.py" "$runtime_io_file"
