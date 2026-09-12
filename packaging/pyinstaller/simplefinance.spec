# PyInstaller spec used on all three platforms:
#   pyinstaller packaging/pyinstaller/simplefinance.spec
# Can be run from anywhere - all paths are resolved from SPECPATH, which
# PyInstaller sets to this file's own directory.
import os
import sys

ROOT = os.path.abspath(os.path.join(SPECPATH, "..", ".."))
SRC = os.path.join(ROOT, "src")
ICON_PNG = os.path.join(SRC, "simplefinance", "icon.png")
ICON_ICO = os.path.join(ROOT, "packaging", "windows", "icon.ico")
ICON_ICNS = os.path.join(ROOT, "packaging", "macos", "icon.icns")

block_cipher = None

a = Analysis(
    [os.path.join(SRC, "simplefinance", "__main__.py")],
    pathex=[SRC],
    binaries=[],
    datas=[(ICON_PNG, "simplefinance")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

windows_icon = ICON_ICO if sys.platform == "win32" and os.path.exists(ICON_ICO) else None

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="SimpleFinance",
    debug=False,
    strip=False,
    upx=False,
    console=False,
    icon=windows_icon,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="SimpleFinance",
)

if sys.platform == "darwin":
    mac_icon = ICON_ICNS if os.path.exists(ICON_ICNS) else None
    app = BUNDLE(
        coll,
        name="SimpleFinance.app",
        icon=mac_icon,
        bundle_identifier="com.mikehellyer.simplefinance",
        info_plist={
            "NSHighResolutionCapable": True,
        },
    )
