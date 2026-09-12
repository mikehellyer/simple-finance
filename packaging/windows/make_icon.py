"""Build packaging/windows/icon.ico from the app's source PNG.

Run before PyInstaller on the Windows CI job:
    python packaging/windows/make_icon.py
"""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SOURCE_PNG = ROOT / "src" / "simplefinance" / "icon.png"
OUTPUT_ICO = Path(__file__).resolve().with_name("icon.ico")

SIZES = [16, 24, 32, 48, 64, 128, 256]


def main():
    image = Image.open(SOURCE_PNG).convert("RGBA")
    image.save(OUTPUT_ICO, sizes=[(s, s) for s in SIZES])
    print(f"Wrote {OUTPUT_ICO}")


if __name__ == "__main__":
    main()
