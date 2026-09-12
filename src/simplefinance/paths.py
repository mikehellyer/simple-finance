"""Cross-platform per-user data directory.

Keeps the leaf folder name "simple-finance" on every OS so a database created
by the original Linux-only build keeps working unmodified after this migration.
"""

import sys
from pathlib import Path

_APP_DIR_NAME = "simple-finance"


def data_dir() -> Path:
    if sys.platform == "win32":
        import os

        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path.home() / ".local" / "share"

    path = base / _APP_DIR_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path
