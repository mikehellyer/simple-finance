import json
import urllib.error
from unittest.mock import MagicMock, patch

import pytest

from simplefinance.updater import (
    ReleaseAsset,
    check_for_update,
    fetch_latest_release,
    is_update_available,
    parse_version,
    pick_asset_for_platform,
)


@pytest.mark.parametrize(
    "text,expected",
    [
        ("1.2.3", (1, 2, 3)),
        ("v1.2.3", (1, 2, 3)),
        ("v2.0", (2, 0)),
        ("v1.2.3-beta", (1, 2, 3)),
        ("", (0,)),
    ],
)
def test_parse_version(text, expected):
    assert parse_version(text) == expected


@pytest.mark.parametrize(
    "current,latest,expected",
    [
        ("0.10.6", "0.10.7", True),
        ("0.10.6", "v0.11.0", True),
        ("0.10.6", "0.10.6", False),
        ("0.10.6", "0.9.9", False),
        ("1.0.0", "0.9.9", False),
    ],
)
def test_is_update_available(current, latest, expected):
    assert is_update_available(current, latest) is expected


def _mock_response(payload):
    response = MagicMock()
    response.read.return_value = json.dumps(payload).encode("utf-8")
    response.__enter__.return_value = response
    response.__exit__.return_value = False
    return response


def test_fetch_latest_release_parses_assets():
    payload = {
        "tag_name": "v1.2.3",
        "html_url": "https://github.com/mikehellyer/finance/releases/tag/v1.2.3",
        "assets": [
            {"name": "SimpleFinance-Setup.exe", "browser_download_url": "https://example.com/a.exe"},
            {"name": "SimpleFinance.dmg", "browser_download_url": "https://example.com/a.dmg"},
        ],
    }
    with patch("simplefinance.updater.urllib.request.urlopen", return_value=_mock_response(payload)):
        release = fetch_latest_release("mikehellyer/finance")

    assert release.tag == "v1.2.3"
    assert len(release.assets) == 2
    assert release.assets[0].name == "SimpleFinance-Setup.exe"


def test_fetch_latest_release_returns_none_on_network_error():
    with patch(
        "simplefinance.updater.urllib.request.urlopen",
        side_effect=urllib.error.URLError("no network"),
    ):
        assert fetch_latest_release("mikehellyer/finance") is None


def test_fetch_latest_release_returns_none_when_no_releases_yet():
    with patch(
        "simplefinance.updater.urllib.request.urlopen",
        side_effect=urllib.error.HTTPError("url", 404, "Not Found", {}, None),
    ):
        assert fetch_latest_release("mikehellyer/finance") is None


def test_check_for_update_none_when_up_to_date():
    payload = {"tag_name": "0.10.6", "html_url": "", "assets": []}
    with patch("simplefinance.updater.urllib.request.urlopen", return_value=_mock_response(payload)):
        assert check_for_update("mikehellyer/finance", "0.10.6") is None


def test_check_for_update_returns_release_when_newer():
    payload = {"tag_name": "0.11.0", "html_url": "", "assets": []}
    with patch("simplefinance.updater.urllib.request.urlopen", return_value=_mock_response(payload)):
        release = check_for_update("mikehellyer/finance", "0.10.6")
    assert release is not None
    assert release.tag == "0.11.0"


def test_pick_asset_for_platform():
    assets = [
        ReleaseAsset("SimpleFinance-Setup.exe", "https://example.com/a.exe"),
        ReleaseAsset("SimpleFinance.dmg", "https://example.com/a.dmg"),
        ReleaseAsset("simplefinance.deb", "https://example.com/a.deb"),
    ]
    assert pick_asset_for_platform(assets, platform="win32").name.endswith(".exe")
    assert pick_asset_for_platform(assets, platform="darwin").name.endswith(".dmg")
    assert pick_asset_for_platform(assets, platform="linux").name.endswith(".deb")
    assert pick_asset_for_platform([], platform="win32") is None
