#!/usr/bin/env bash
# Wraps the PyInstaller .app bundle into a .dmg using create-dmg.
# Run from the repo root after:
#   ./packaging/macos/make_icon.sh
#   pyinstaller packaging/pyinstaller/simplefinance.spec
#
#   ./packaging/macos/build_dmg.sh 1.2.3
set -euo pipefail

VERSION="${1:-0.0.0}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
APP_PATH="$ROOT_DIR/dist/SimpleFinance.app"
OUT_DIR="$ROOT_DIR/dist/installers"
OUT_DMG="$OUT_DIR/SimpleFinance-$VERSION.dmg"

if [ ! -d "$APP_PATH" ]; then
    echo "Expected $APP_PATH - run PyInstaller first." >&2
    exit 1
fi

mkdir -p "$OUT_DIR"
rm -f "$OUT_DMG"

if ! command -v create-dmg >/dev/null 2>&1; then
    echo "create-dmg not found. Install it with: brew install create-dmg" >&2
    exit 1
fi

create-dmg \
    --volname "Simple Finance" \
    --app-drop-link 450 150 \
    --icon "SimpleFinance.app" 150 150 \
    --window-size 600 300 \
    "$OUT_DMG" \
    "$APP_PATH"

echo "Wrote $OUT_DMG"
