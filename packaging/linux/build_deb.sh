#!/usr/bin/env bash
# Builds a .deb from the PyInstaller onedir build.
# Run from the repo root after:
#   pyinstaller packaging/pyinstaller/simplefinance.spec
#
#   ./packaging/linux/build_deb.sh 1.2.3
set -euo pipefail

VERSION="${1:-0.0.0}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
BUILD_DIR="$ROOT_DIR/dist/SimpleFinance"
OUT_DIR="$ROOT_DIR/dist/installers"
PKG_ROOT="$ROOT_DIR/dist/deb-root"
PKG_NAME="simplefinance_${VERSION}_amd64"

if [ ! -d "$BUILD_DIR" ]; then
    echo "Expected $BUILD_DIR - run PyInstaller first." >&2
    exit 1
fi

rm -rf "$PKG_ROOT"
mkdir -p \
    "$PKG_ROOT/DEBIAN" \
    "$PKG_ROOT/opt/simple-finance" \
    "$PKG_ROOT/usr/share/applications" \
    "$PKG_ROOT/usr/share/icons/hicolor/512x512/apps" \
    "$OUT_DIR"

cp -r "$BUILD_DIR"/* "$PKG_ROOT/opt/simple-finance/"
cp "$ROOT_DIR/src/simplefinance/icon.png" "$PKG_ROOT/usr/share/icons/hicolor/512x512/apps/simple-finance.png"
cp "$SCRIPT_DIR/simple-finance.desktop" "$PKG_ROOT/usr/share/applications/simple-finance.desktop"

cat > "$PKG_ROOT/DEBIAN/control" <<EOF
Package: simplefinance
Version: $VERSION
Section: office
Priority: optional
Architecture: amd64
Maintainer: Mike Hellyer
Description: Personal finance, budgeting, forecasting and reconciliation
EOF

dpkg-deb --build --root-owner-group "$PKG_ROOT" "$OUT_DIR/${PKG_NAME}.deb"
echo "Wrote $OUT_DIR/${PKG_NAME}.deb"
