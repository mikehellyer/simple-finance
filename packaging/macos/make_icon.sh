#!/usr/bin/env bash
# Build packaging/macos/icon.icns from the app's source PNG using the
# built-in macOS `sips` and `iconutil` tools (no extra dependency).
#
# Run before PyInstaller on the macOS CI job:
#   ./packaging/macos/make_icon.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
SOURCE_PNG="$ROOT_DIR/src/simplefinance/icon.png"
ICONSET_DIR="$SCRIPT_DIR/icon.iconset"
OUTPUT_ICNS="$SCRIPT_DIR/icon.icns"

rm -rf "$ICONSET_DIR"
mkdir -p "$ICONSET_DIR"

for size in 16 32 64 128 256 512; do
    sips -z "$size" "$size" "$SOURCE_PNG" --out "$ICONSET_DIR/icon_${size}x${size}.png" >/dev/null
    double=$((size * 2))
    sips -z "$double" "$double" "$SOURCE_PNG" --out "$ICONSET_DIR/icon_${size}x${size}@2x.png" >/dev/null
done

iconutil -c icns "$ICONSET_DIR" -o "$OUTPUT_ICNS"
rm -rf "$ICONSET_DIR"
echo "Wrote $OUTPUT_ICNS"
