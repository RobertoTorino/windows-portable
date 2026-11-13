<!-- SPDX-License-Identifier: GPL-3.0-or-later -->

# CLAUDE.md (Windows Portable Suite)

The rules of the **Windows Portable Suite**, in its own repository, `github.com/RobertoTorino/windows-portable`
(branch `main`; owner, 13-11-2026: one repository per suite). Nexus's CLAUDE.md (`../CLAUDE.md` in the checkout
described below) holds what is Nexus's (git, releases, the CHANGELOG format and kinds, line endings, the checks) and
applies here too. Status and plans: [MIGRATION.md](MIGRATION.md). Paths below are written from this repository's
root unless they start with `../`, which is the Nexus checkout.

## Inside a Nexus checkout

The suite keeps no copy of core or of the Nexus tools. It is worked on **inside a checkout of Nexus**
(`github.com/RobertoTorino/nexus`), cloned there as the folder `windows-portable/`, which Nexus's `.gitignore`
lists:

```bash
git clone https://github.com/RobertoTorino/nexus.git Nexus
git clone https://github.com/RobertoTorino/windows-portable.git Nexus/windows-portable
```

So `../core/`, `../tools/` and `../dev/` are Nexus's, every Nexus tool finds the suite as before
(`--suite windows-portable`), and `../test.sh` runs its tests. The venv is the Nexus checkout's, with the suite's
packages added: `pip install -r windows-portable/requirements-dev.txt` after Nexus's own. The two are separate git checkouts: git in this folder
is the suite's (its commits, its tags, its CI), git in `..` is Nexus's, and a change to both is two commits. Cloned
on its own, outside a Nexus checkout, the suite's tests and tools do not run. `NEXUS_REF` names the Nexus commit the
suite's workflows use (a branch such as `main`, or a commit to hold the suite on a tested Nexus): every job starts
with Nexus's action `RobertoTorino/nexus/.github/actions/suite`, which checks out that Nexus and this repository
inside it.

## What this is

The **Windows Portable Suite** (exactly that name): tools for Windows 10/11 on portable gaming devices, any Windows
handheld, first the owner's ASUS ROG XBOX Ally X. Its `SYSTEM` is `windows` and its `TAG_PREFIX` `wp-` (owner,
26-10-2026): tags are `wp-<app>-v<x.y.z>` and `wp-portal-v<x.y.z>`. A **portal** installs and starts the apps listed
in its manifest. **test** (Windows Portable Test) is always installed and always listed first; every other listed
app is an optional tile. The wiki is at robertotorino.github.io/nexus/windows-portable-suite/.

- `apps/<name>/`: one folder per app, each with its own VERSION, CHANGELOG, LICENSE and .gitignore. Every app has a
  `category` in `portal/apps.toml`: sustainable, graphics, gaming or utilities (owner, 27-10-2026: the BC250
  suite's without development), the portal's tab for it. No `[checkout.*]` apps and no Development tab: the portal
  lists only released apps.
- `portal/`: the portal (`portable_portal/`), `apps.toml` (one pinned release per app), its `install.ps1` and
  `run.ps1`, its images and the intro's sound.
- `tools/`: `build_release.py` (an app's or the portal's release zip, on Windows), `check_manifest.py`,
  `suite_release.py` and `publish_release.sh` (the release workflow's plan, pin and publish steps),
  `check-release.ps1` (the release checks on the handheld, from the Nexus Release Tool's test buttons; `draft`: the
  device test of a Nexus release), `cec_probe.py` (can the handheld reach the TV's HDMI-CEC through its USB-C to
  HDMI adapter: AMD's AUX channel to the adapter's CEC tunneling, `--ping` asks the TV), `portal_tour.py` and
  `record-tour.sh` (the portal's video tour, the same tour as the BC250 suite's on this portal, recorded on the
  handheld from Git Bash; `--wiki` writes the wiki's Portal Tour copy; owner, 02-11-2026), `record-app-tour.sh`
  (one app's tour, through the Nexus `tools/app_tour.py`), `mkdocs/`
  (the wiki's overrides), their tests in `tools/tests/`, and `tools/installer-tests/<name>.ps1` (an installer test
  per app and per manifest entry, and the Nexus apps' `nrt.ps1` and `dash.ps1`).
- `docs/` and `mkdocs.yml`: the wiki; `icons/`: the suite's pictures and the category icons
  (`icons/<category>/<category>-<size>.png`), the PNG sources of their copies: every optional app takes its
  category's icon (`../tools/make_icons.py` writes the copies and lists them in `ICONS.md`). `icons/categories.toml`
  says so for `../tools/sync_icons.py` (the dashboard's Convert icons): PNG at every size, Gaming 2:1, the apps
  from the portal's `apps.toml`.
- `../core/bc250_core/`: shared Python code, every suite's, **bundled per app** in its release. The portable window
  (`portable.py`: `PortableWindow`, `Card`, `Pane`, `Pill`, `InfoPill`, `Legend`, `PortableHeader`), the
  controller (`gamepad.py`), the battery (`power.py`) and the Windows folders and shortcuts (`platform.py`) are
  this suite's base.

## Rules from the owner

- **Each suite stands apart** (owner, 27-10-2026; a repository each, 13-11-2026): a change here never edits another
  suite, and a change two suites want is two changes, one per suite, each with its own release. This suite's
  workflows are in `.github/workflows/`: its CI `ci.yml`, its releases `release.yml` (never GitHub's Latest), its
  weekly emulator check `upstream.yml`. Its wiki is built and published by Nexus's `docs.yml`, at the address it
  always had.
- **An emulator moves only with its app** (owner, 29-10-2026: a new emulator release can break things): each app
  pins one tested release in its `emulator.py` (`REPO`, `VERSION`, `ASSET`, `SHA256`), and a newer one reaches the
  device only with a new release of the app, tried first. Every Monday `tools/check_upstream.py` compares each pin
  with the newest stable release and with the file GitHub publishes, and keeps the "Upstream review (Windows
  Portable Suite)" issue up to date; a new emulator app's `emulator.py` with those constants is checked by itself.
  **The suite follows the emulators' release cycle** (owner, 31-10-2026): the pin is always the newest stable
  release, so a new one is taken up in the working tree as soon as it is out. Check it against the source the app
  relies on (`emulator.py` and the other modules name the upstream files), the asset's layout and checksum, and say
  in the handover that the app needs a release.
- **Worked on and tested on Windows** (owner, 26-10-2026): the suite's tests, installer tests and release builds
  run on Windows (`./test.sh` runs them only there, unless `NEXUS_SYSTEM=windows`).
- **A design of its own, with the weight on UX and UI** (owner, 25-10-2026): the portable design (direction D, B's
  amber on C's cards; `../DESIGN.md`), never the Bazzite design. A small screen held in the hands, touch and a
  controller, often without a keyboard:
  - Every action is reachable with the controller and by touch: the d-pad moves an amber focus between cards and
    rows, A acts, B goes back (a pane to its card, a page to where it came from; nothing on a card; in a pane
    the d-pad stays in it, never jumping to the cards at a list's end: core's `move_focus()`), View (⧉)
    exits the app and Menu (☰) opens the information of the pane that shows (owner, 29-10-2026: "Close" on B was
    not clear; core's `PortableWindow`, the legend ending with `common_items()`: ☰ Info, B Back, ⧉ Exit, owner 31-10-2026). **The
    legend at the bottom is the row of actions** (owner, 29-10-2026:
    "use that bottom row for actions"; then "one way everywhere"): **every action is a button and a legend entry,
    A too (A Install, A Read, A Steam mark, A View log), and a pane holds no pill** (no Install, Remove, Save or
    Open the log pill); a tap on the entry does the same (core's `Legend`, through `PortableWindow.act()`, A
    beside a card or row through `bind("accept")`). An action without a button of its own takes a free one on its
    pane (Remove BIOS on LB, Remove game on RB). A tap on a pane may do its A where that is
    safe (the Log pane shows the log). Pills stay only inside a popup, as its choices (the stick lights). The
    information icon is touch only: the d-pad never lands on it, Menu (☰) opens it.
  - No dialogs: an action that needs care asks for a second press within five seconds (Remove; View while a
    download or an install runs), and the legend's entry and the status line say so meanwhile. **Nothing is grayed
    out** (owner, 29-10-2026): pressed when its action cannot run now, a button says why on the pane's status
    line. Never `setEnabled(False)` on a `Pill` or a row.
  - Windows' own windows are not used: they cannot be used with the controller (owner, 29-10-2026: a folder could
    not be chosen). A folder or a file is chosen in core's browser (`browse.Browser`: the places, then folders,
    A opens, B goes up, X adds the folder, A on a file picks it); a long text (the log) is read in a `TextView` in
    the pane, the d-pad scrolling it, never in Notepad.
  - The emulator apps never start a game (owner, 29-10-2026): the games are played from Steam, and A on a game is
    its Steam mark.
  - The window fits the Ally's screen: 1280 x 720 logical pixels at 150 %, the size every page is laid out for
    (`portable.px()` scales it to a larger screen). Text that does not fit goes behind an information icon
    (`InfoPill`, at the top right of its pane) that shows it over the window (owner, 28-10-2026). Where space is
    short, an icon at the pane's top right opens a popup with the rest (text or controls), owner 29-10-2026.
  - The portal's pane under the tiles is the title and two lines, the versions and the summary (owner, 31-10-2026):
    an app's `summary` in `portal/apps.toml` fits one line at 1280 x 720, short words over a second line
    (`portal/tests/test_main_window.py` measures every one).
  - The wallpaper is the suite's (owner, 29-10-2026): every window shows it behind see-through cards (core's
    `PortableWindow`), on or off for every app at once on the portal's Settings page
    (`%APPDATA%\windows-portable-suite\suite.ini`).
  - Nothing runs before it is asked for: a card that reads the device reads on A (owner, 28-10-2026).
  - **No user name on the screen or in a log** (owner, 29-10-2026: the privacy rule): a path is shown through core's
    `platform.private()` (`%LOCALAPPDATA%\...`, `%USERPROFILE%\...`), and every app logs with
    `applog.setup(..., private=True)`.
  - The header's status line: the date, the time and the battery, `Wednesday 28/10/2026 | 17:04 | 82%` (owner,
    28-10-2026: no space before %; 30-10-2026: the battery last); Windows Portable Test shows the date and the time, and under them
    the temperatures, the power draw, the screen's refresh rate and the battery, `CPU 47° GPU 45° | 18 W | 120 Hz |
    82%` (owner, 29-10-2026). No icon in the
    test app's header (the screen is too small for it).
- **Not limited to the owner's handheld.** The Ally X is one case, not the target: an app reads what Windows
  reports, works on another Windows handheld, and says so where something does not apply (no AMD driver, no Wi-Fi,
  no back buttons). **No hardcoded names of hardware** (owner, 07-11-2026: hardware can change): no screen, audio
  device or other device is found by a name written in the code; an app asks Windows what is there (the monitor a
  window is on, its size and scaling) and works with whatever it finds.
- **For your own user; administrator per use case.** The installers refuse an administrator's window; everything goes
  in `%LOCALAPPDATA%\windows-portable-suite\` (programs, logs, reports, the portal's state) and
  `%APPDATA%\windows-portable-suite\` (one `.ini` per app); nothing in the registry (tests must not write to it
  either). An app the portal installs gets a Start-menu entry in the Windows Portable Suite folder and no Desktop
  shortcut (owner, 28-10-2026); one installed by hand gets both. An action that needs an administrator is the
  owner's to approve, one use case at a time (owner, 01-11-2026: no rule against it, each case assessed on its own):
  ask before building one, and keep it to one Windows prompt for that action only, never the whole app running as
  administrator. Approved so far. The first (owner, 31-10-2026): the
  portal's Operating Mode helper on the ROG XBOX Ally X, a scheduled task that writes the watt limits as SYSTEM,
  installed with one administrator prompt, its script in `C:\Program Files\windows-portable-suite\` so the user
  cannot change what it runs, and its request (one letter the user may write), result and log in
  `C:\ProgramData\windows-portable-suite\`. The second (owner, 31-10-2026): USB HD Cam's Allow access, which binds
  Microsoft's in-box WinUSB driver (winusb.inf, section WINUSB) to the PS5 HD Camera's boot loader (05a9:0580) with
  one administrator prompt per USB port: the app starts its own program again with `--bind <instance ID>`, which
  binds only that device and ends (`apps/hdcam/usb_hd_cam/driver.py`). No certificate, no driver of anyone else's.
  The third (owner, 01-11-2026): BIOS Reader's Read the settings, the device's UEFI variables read by the app's own
  program started again with `--read-variables <request> <result>` (Windows' firmware variable calls need an
  administrator's privilege; `apps/bios/bios_reader/device.py`): only GetFirmwareEnvironmentVariableExW, never a
  write, and never a variable that may hold personal data (`device.PRIVATE`).
- **Personal data is never read out**: no serial numbers, MAC addresses, network names (SSID) or access point
  addresses, no paired Bluetooth devices (they carry their owner's name).
- **The user decides what to keep before anything is deleted** (owner, 01-11-2026): an app never deletes a game, a
  package, a BIOS file or anything else of the user's on its own; it shows a page of what would go (core's
  `keep.py`: a row each with its size, every row marked Delete at first, A turns one to Keep and back, X deletes the
  rows still marked Delete, B deletes nothing). The game managers use it for Remove game, for the packages a clean
  install leaves, and for PCSX2's Remove BIOS.
- **Unsigned** (code signing and an MSIX for XBOX mode's home app were dropped, owner 04-11-2026).

## How an app is built

Every app is built the same way; Windows Portable Test is the model:

- `apps/<name>/<package>/` (`__init__.py` with `APP_NAME`, `APP_ID` = `windows-portable-<name>`, `EXE_NAME`, `SUITE`,
  `__version__` and an `AppInfo` with `settings_org=SUITE, settings_ini=True`; `__main__.py`; `main_window.py` on
  `PortableWindow`), `images/` (`<app id>.webp` and `-128.png`), `tests/` (with a conftest that keeps settings out of
  the registry), `install.ps1`, `run.ps1` (from the checkout, full screen or `--windowed`), `requirements.txt`,
  `requirements-dev.txt`, README.md and the four files.
- Its chapter in the wiki is `docs/apps/<name>.md` with a nav line in `mkdocs.yml`; the release carries it as
  MANUAL.md.
- Its release is `wp-<name>-v<x.y.z>.zip` from `tools/build_release.py`: `program/` (PyInstaller one-folder,
  `<EXE_NAME>.exe` beside `_internal/`), `install.ps1`, LICENSE, THIRD-PARTY-NOTICES.txt and MANUAL.md, with
  SHA256SUMS and notes.md.
- What Windows reports is read through its own APIs (ctypes) or one CIM or PowerShell query that returns JSON, never
  the text of a tool such as netsh or powercfg, which is in Windows' language. Slow reads run off the window's
  thread.
- A new app adds its `portal/apps.toml` entry and its installer test `tools/installer-tests/<name>.ps1`;
  `../tools/new_app.py --suite windows-portable` does all of it. The suite's CI needs no edit: its pytest matrix
  (every folder with `tests/`) and its `installers` matrix (a job per app: the installer test, the release built
  and installed) are read from the folders by its plan job (`../tools/ci_matrix.py`; `../tools/tests/test_layout.py`
  and `tools/tests/` check them). The suite's CI runs on every push to this repository;
  a change to core or the Nexus tools reaches it with its next run (`NEXUS_REF`).

## Checks of the suite

From PowerShell at the root of the Nexus checkout, as Nexus's `.claude/checks.md` lists them:

```powershell
.venv-windows\Scripts\python.exe tools\check_versions.py --suite windows-portable
.venv-windows\Scripts\python.exe windows-portable\tools\check_manifest.py --base origin/main
Get-ChildItem windows-portable\tools\installer-tests\*.ps1 | ForEach-Object { powershell -NoProfile -ExecutionPolicy Bypass -File $_.FullName }
.venv-windows\Scripts\python.exe windows-portable\tools\build_release.py wp-test-v<VERSION> <folder>
powershell -NoProfile -ExecutionPolicy Bypass -File windows-portable\tools\installer-tests\test.ps1 -Release <folder>\wp-test-v<VERSION>.zip
.venv-windows\Scripts\mkdocs.exe build --strict -f windows-portable\mkdocs.yml   # then remove windows-portable\site
```

`./test.sh` (Git Bash, at the root of the Nexus checkout) runs every test suite of this system, this suite's among them. A window's layout is checked
at 1280 x 720 offscreen (its minimum height at most 720), and looked at on the Ally by the owner.

## Releases

Everything about releases is the owner's (Nexus's CLAUDE.md): the version bumps, the tags (`wp-` first), the
release zips and the pins in `portal/apps.toml`. When finished work needs a release, the handover says which app
and why.

The manual (`docs/`, built with MkDocs) is called **the wiki** in user-facing text.
