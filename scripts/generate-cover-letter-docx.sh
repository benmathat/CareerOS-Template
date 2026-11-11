#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! python3 -c "import docx, fontTools, pypdf" 2>/dev/null; then
  echo "Installing DOCX generation dependencies (python-docx, fonttools, pypdf, cffi)..."
  python3 -m pip install -q -r "${SCRIPT_DIR}/resume_docx/requirements.txt"
fi

if ! command -v soffice >/dev/null 2>&1 \
   && ! command -v libreoffice >/dev/null 2>&1 \
   && [[ -z "${RESUME_DOCX_SOFFICE_BIN:-}" ]] \
   && [[ ! -x "/Applications/LibreOffice.app/Contents/MacOS/soffice" ]] \
   && [[ ! -x "/usr/bin/soffice" ]] \
   && [[ ! -x "/opt/libreoffice/program/soffice" ]]; then
  echo "WARNING: LibreOffice ('soffice') was not found on PATH or in the usual install locations." >&2
  echo "         PDF conversion and page-count validation will fail; pass --no-pdf to skip them," >&2
  echo "         or set RESUME_DOCX_SOFFICE_BIN to the full path of the soffice executable." >&2
fi

exec python3 "${SCRIPT_DIR}/resume_docx/cover_letter_docx.py" "$@"
