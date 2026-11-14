# SPDX-License-Identifier: GPL-3.0-or-later
"""Shared fixtures: an offscreen QApplication with bc250_core from the checkout, and the settings and the user's
folders in a temp folder (never Windows' registry or the user's own %LOCALAPPDATA%)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
PORTAL = Path(__file__).resolve().parents[1]
CORE = PORTAL.parents[1] / "core"
for path in (CORE, PORTAL):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))       # bc250_core from the checkout, as a release bundles it


@pytest.fixture(scope="session")
def qapp():
    from PyQt6.QtCore import QSettings
    from PyQt6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])
    from bc250_core import portable
    portable.pin_scale((1280, 720))     # the Ally's screen, not the offscreen one (800 x 800): the windows fit-tested
    yield app
    QSettings.setDefaultFormat(QSettings.Format.IniFormat)


@pytest.fixture(autouse=True)
def settings_in_tmp(tmp_path, monkeypatch):
    from PyQt6.QtCore import QSettings
    QSettings.setDefaultFormat(QSettings.Format.IniFormat)
    QSettings.setPath(QSettings.Format.IniFormat, QSettings.Scope.UserScope, str(tmp_path / "settings"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "Local"))
    monkeypatch.setenv("APPDATA", str(tmp_path / "Roaming"))
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "data"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))


class SilentPlayer:
    """Stands in for the music's player: it records what the portal asked and plays nothing."""

    def __init__(self):
        self.path = None
        self.playing = False
        self.calls: list[str] = []

    def set_track(self, path) -> None:
        self.path = path
        self.calls.append("track")

    def play(self) -> None:
        self.playing = True
        self.calls.append("play")

    def pause(self) -> None:
        self.playing = False
        self.calls.append("pause")

    def stop(self) -> None:
        self.playing = False
        self.calls.append("stop")


@pytest.fixture(autouse=True)
def silent_music(monkeypatch):
    """No test plays the portal's music on the machine the tests run on: a window's player is a SilentPlayer. A test
    of the player itself makes one from the class this returns."""
    from portable_portal import music
    real = music.Player
    monkeypatch.setattr(music, "Player", SilentPlayer)
    return real
