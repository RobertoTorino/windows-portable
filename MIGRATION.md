<!-- SPDX-License-Identifier: GPL-3.0-or-later -->

# Migration status

Working notes of the Windows Portable Suite. Not part of the wiki or the READMEs, which describe only what exists.

## The suite on hold (owner, 09-11-2026: from 10-11-2026)

**Development of the Windows Portable Suite is on hold from 10-11-2026** (owner, 09-11-2026: the last day with the
ROG XBOX Ally X). The released apps and wp-portal-v10.3.0 stay as they are; no new features or releases until the
owner takes it up again. The wiki carries a banner saying so on every page (`tools/mkdocs/overrides/main.html`,
Material's announce bar; take it out when work resumes).

## A repository of its own (owner, 13-11-2026)

The suite left Nexus on 13-11-2026 (owner: one repository per suite) and is `github.com/RobertoTorino/windows-portable`.
The code moved as it was: no app and no portal changed. The history and the `wp-` tags stayed in Nexus, as its
releases did.

**The first release from this repository is on hold** (owner's decisions, not made yet, 13-11-2026). Before it:

- **Where installed portals look.** wp-portal-v10.3.0 and every released app look for releases in
  `github.com/RobertoTorino/nexus` (core's `SUITE_REPO_URL`), and the portal reads a release's manifest from
  `windows-portable/portal/apps.toml` at its tag (`portal/portable_portal/portal_update.py`, `RAW_URL`). A release
  published here is not seen by them. The portal and the apps need this repository's address and path, and the
  installed portals need a way to it (a last portal release in Nexus that points here, or installing anew).
- **The earlier releases.** The `wp-` tags and their releases are in Nexus. `release.yml` builds a portal only when
  every pinned tag exists here, and bundles the pinned Windows Portable Test from this repository's releases. CI's
  portal job takes that release from Nexus while this repository has none.
- **`release.yml` has not run here yet.** It is Nexus's `release-windows-portable.yml` with this repository for git
  and GitHub; `tools/check-release.ps1` still downloads from Nexus.
- **The Nexus Release Tool** does not release a suite in a repository of its own yet (Nexus's MIGRATION.md).
