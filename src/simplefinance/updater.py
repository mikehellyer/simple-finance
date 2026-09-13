"""GitHub-release update checking.

Pure logic here has no Tkinter dependency so it can be unit tested directly.
The GUI layer (app.py) is responsible for running check_for_update() off the
main thread and marshalling the result back via Tk's .after().
"""

import json
import re
import shutil
import ssl
import subprocess
import sys
import tempfile
import threading
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import certifi

API_TIMEOUT_SECONDS = 5
DOWNLOAD_TIMEOUT_SECONDS = 30

# PyInstaller builds on some platforms/toolchains (notably macOS via
# actions/setup-python) don't carry a usable default CA bundle, so a frozen
# app's HTTPS requests can fail with a certificate verification error even
# though the same code works fine unfrozen. Pinning to certifi's bundled
# CA file sidesteps that regardless of what the build environment had.
_SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())

_ASSET_PATTERNS = {
    "win32": re.compile(r"\.exe$", re.IGNORECASE),
    "darwin": re.compile(r"\.dmg$", re.IGNORECASE),
    "linux": re.compile(r"\.deb$", re.IGNORECASE),
}


@dataclass
class ReleaseAsset:
    name: str
    download_url: str


@dataclass
class ReleaseInfo:
    tag: str
    html_url: str
    assets: list


def parse_version(text: str):
    """"v1.2.3" / "1.2.3" -> (1, 2, 3). Non-numeric parts sort as 0."""
    text = (text or "").strip()
    if text.lower().startswith("v"):
        text = text[1:]
    parts = []
    for chunk in text.split("."):
        match = re.match(r"\d+", chunk)
        parts.append(int(match.group()) if match else 0)
    return tuple(parts) if parts else (0,)


def is_update_available(current_version: str, latest_tag: str) -> bool:
    return parse_version(latest_tag) > parse_version(current_version)


def fetch_latest_release(repo: str, timeout: float = API_TIMEOUT_SECONDS) -> Optional[ReleaseInfo]:
    """Query GitHub's releases/latest endpoint. Returns None on any failure
    (no network, no releases yet, rate limited, malformed response) rather
    than raising, so a caller can fail silently."""
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    request = urllib.request.Request(
        url, headers={"Accept": "application/vnd.github+json", "User-Agent": "simplefinance-update-checker"}
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout, context=_SSL_CONTEXT) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, ValueError, OSError):
        return None

    tag = data.get("tag_name")
    if not tag:
        return None

    assets = [
        ReleaseAsset(name=a.get("name", ""), download_url=a.get("browser_download_url", ""))
        for a in data.get("assets", [])
        if a.get("browser_download_url")
    ]
    return ReleaseInfo(tag=tag, html_url=data.get("html_url", ""), assets=assets)


def pick_asset_for_platform(assets, platform: str = None) -> Optional[ReleaseAsset]:
    platform = platform or sys.platform
    pattern = _ASSET_PATTERNS.get(platform)
    if pattern is None:
        return None
    for asset in assets:
        if pattern.search(asset.name):
            return asset
    return None


def check_for_update(repo: str, current_version: str) -> Optional[ReleaseInfo]:
    """Returns the ReleaseInfo if a newer version is published, else None.
    Never raises - safe to call from a background thread on startup."""
    release = fetch_latest_release(repo)
    if release is None:
        return None
    if not is_update_available(current_version, release.tag):
        return None
    return release


def download_asset(asset: ReleaseAsset, dest_dir: Path = None) -> Path:
    dest_dir = Path(dest_dir) if dest_dir else Path(tempfile.mkdtemp(prefix="simplefinance-update-"))
    dest_path = dest_dir / asset.name
    request = urllib.request.Request(asset.download_url, headers={"User-Agent": "simplefinance-update-checker"})
    with urllib.request.urlopen(
        request, timeout=DOWNLOAD_TIMEOUT_SECONDS, context=_SSL_CONTEXT
    ) as response, open(dest_path, "wb") as f:
        f.write(response.read())
    return dest_path


class UpdateChecker:
    """Thin threading wrapper so the GUI never blocks on the network call.

    `on_result` runs on the background thread - callers that touch Tk widgets
    from it must hop back to the main thread themselves (e.g. via
    `root.after(0, ...)`).
    """

    def __init__(self, repo: str, current_version: str):
        self.repo = repo
        self.current_version = current_version

    def check_async(self, on_result) -> None:
        def worker():
            try:
                result = check_for_update(self.repo, self.current_version)
            except Exception:
                result = None
            on_result(result)

        threading.Thread(target=worker, daemon=True).start()


def open_installer(path: Path) -> Optional[subprocess.Popen]:
    """Hand off to the OS's normal action for the downloaded installer (runs
    the .exe, mounts the .dmg, installs the .deb). Never runs anything
    silently/unattended - a privilege prompt or installer window always
    appears for the user to complete.

    Returns the spawned process where there is one, so a caller on Linux can
    wait for it to finish before quitting - quitting immediately there can
    kill the pkexec authentication dialog before it's answered, since the
    desktop session ties a launched app's child processes to its own
    lifetime. os.startfile on Windows has no equivalent handle, hence None.
    """
    path = str(path)
    if sys.platform == "win32":
        import os

        os.startfile(path)
        return None
    elif sys.platform == "darwin":
        return subprocess.Popen(["open", path])
    else:
        # Handing a local .deb of an already-installed package to a desktop
        # "Software" GUI via xdg-open is unreliable across distros: several
        # (including GNOME Software / Pop!_Shop) show an "Uninstall" action
        # instead of "Install"/"Reinstall" for a package name already on the
        # system, regardless of the file's version - clicking it just removes
        # the current install and does nothing with the downloaded file.
        # Install directly via apt (through pkexec for a graphical privilege
        # prompt) instead, which correctly upgrades in place.
        if shutil.which("pkexec") and shutil.which("apt"):
            return subprocess.Popen(["pkexec", "apt", "install", "-y", path])
        else:
            return subprocess.Popen(["xdg-open", path])
