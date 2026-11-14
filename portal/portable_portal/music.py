# SPDX-License-Identifier: GPL-3.0-or-later
"""The portal's background music (owner, 14-11-2026): a track that plays quietly, over and over, while the portal is
in front. The portal's own is sounds/background.ogg (BUILT_IN: the owner's remix of DAT Station's Sea Breeze, made in
Audacity, the suite's own, GPL-3.0-or-later as the rest). The user's own tracks go in the suite's music folder
(folder(): %LOCALAPPDATA%\\windows-portable-suite\\music, beside the wallpapers'), and the Settings page's Music row
steps through the choices (choices): Off, Built-in, then each track in the folder, by file name. The choice is the
portal's setting (MUSIC_KEY in portal.ini).

Off is the music's own switch, apart from the Sound row's: either can be off while the other plays. The music waits
while the intro plays and while another window has the focus (a game, an app), and plays on from where it was. It
plays through Qt Multimedia (the intro's and the buttons' sounds stay with winsound, which plays one sound at a
time); without it, or without an audio output, the portal plays none and says nothing."""

from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import QSettings, QUrl

from bc250_core.platform import suite_data

from . import ROOT, SUITE

BUILT_IN = ROOT / "sounds" / "background.ogg"
FOLDER = r"%LOCALAPPDATA%\windows-portable-suite\music"      # as the user finds it
SUFFIXES = (".ogg", ".oga", ".opus", ".mp3", ".flac", ".wav", ".m4a")
VOLUME = 0.35                           # under the buttons' sound
RULES = "Ogg, Opus, MP3, FLAC, WAV or M4A sound files"
MUSIC_KEY = "look/music"                # "" (the portal's own), OFF, or the name of a track in the folder
OFF, OFF_NAME, BUILT_IN_NAME = "off", "Off", "Built-in"


def folder() -> Path:
    """Where the user's own tracks are dropped."""
    return suite_data(SUITE) / "music"


def tracks() -> list[Path]:
    """The sound files in the music folder, by name. The folder is made when it is missing."""
    try:
        folder().mkdir(parents=True, exist_ok=True)
        return sorted((p for p in folder().iterdir() if p.is_file() and p.suffix.lower() in SUFFIXES),
                      key=lambda p: p.name.lower())
    except OSError:
        return []


def choices(built_in: Path = BUILT_IN) -> list[tuple[str, Path | None]]:
    """The Music row's choices in order, (name, track): Off, Built-in, then each track in the folder."""
    return [(OFF_NAME, None), (BUILT_IN_NAME, built_in), *((p.name, p) for p in tracks())]


def chosen(settings: QSettings, among: list[tuple[str, Path | None]]) -> str:
    """The name of the choice kept: Off, a track still in the folder, else Built-in."""
    kept = str(settings.value(MUSIC_KEY, "") or "")
    if kept == OFF:
        return OFF_NAME
    return kept if kept and kept in [name for name, _ in among[2:]] else BUILT_IN_NAME


def keep(settings: QSettings, name: str) -> None:
    settings.setValue(MUSIC_KEY, OFF if name == OFF_NAME else "" if name == BUILT_IN_NAME else name)
    settings.sync()


class Player:
    """Plays one track over and over through Qt Multimedia; silent, without complaint, when the module or the
    file is not there, or the file cannot be played."""

    def __init__(self):
        self.path: Path | None = None
        self.player = None
        self.output = None
        self.failed = False
        self.wanted = False                             # play() was the last word, not pause()

    def _ensure(self) -> bool:
        if self.player is not None:
            return True
        if self.failed:
            return False
        try:
            from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
            self.output = QAudioOutput()
            self.output.setVolume(VOLUME)
            self.player = QMediaPlayer()
            self.player.setAudioOutput(self.output)
            self.player.setLoops(QMediaPlayer.Loops.Infinite)
        except Exception:  # noqa: BLE001  (any failure of the multimedia stack: the portal plays no music)
            self.failed = True
            self.player = self.output = None
            return False
        return True

    def set_track(self, path: Path | None) -> None:
        """*path* as the track, from its start; it plays at once when the music was playing. The same path again
        is read again: the user's copy has one name, whatever was chosen."""
        self.path = path
        if self.player is None:
            return
        self.player.stop()
        self.player.setSource(QUrl.fromLocalFile(str(path)) if path is not None else QUrl())
        if self.wanted and path is not None:
            self.player.play()

    def play(self) -> None:
        """Play, or play on from where pause() left it."""
        self.wanted = True
        if self.path is None or not self.path.is_file():
            return
        fresh = self.player is None
        if not self._ensure():
            return
        if fresh:
            self.player.setSource(QUrl.fromLocalFile(str(self.path)))
        self.player.play()

    def pause(self) -> None:
        self.wanted = False
        if self.player is not None:
            self.player.pause()

    def stop(self) -> None:
        self.wanted = False
        if self.player is not None:
            self.player.stop()

    @property
    def playing(self) -> bool:
        if self.player is None:
            return False
        from PyQt6.QtMultimedia import QMediaPlayer
        return self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState


class Silent(Player):
    """A player that plays nothing, for the tools that draw the portal (the Portal Tour, the wiki's picture)."""

    def play(self) -> None:
        self.wanted = True
