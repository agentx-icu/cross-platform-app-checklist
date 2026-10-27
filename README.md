# cross-platform-app-checklist

[简体中文](README.zh-CN.md)

An agent skill (Claude Code, Codex and other `SKILL.md`-aware agents) that
walks a change through the places multi-platform apps break: screen sizes and
breakpoints, high-DPI and fractional scaling, rotation, split screen and
foldables, safe areas and keyboards, large text, permission declarations,
background limits, mobile device features (audio routes, camera, sensors),
and the differences between desktop and mobile.
It also checks release readiness for the app's chosen software stores:
publisher / package identity, privacy and content declarations, listing and
review access, signed artifacts, release tracks and safe updates.

The rules come from defects found and fixed while shipping Flutter apps on
iOS, iPadOS, Android, macOS, Windows and Linux. Each item says what to do,
what fails without it, and how to verify it. Platform facts apply to any
framework; Flutter-specific notes are kept in one file.

## Layout

```
SKILL.md                    short entry point: modes, routing, evidence and output contract
references/checklist.md     complete catalog of 65 stable IDs (full release coverage)
references/layout.md        L1–L8  sizes, breakpoints, runtime resize, safe areas, keyboard, orientation, overlays, folds
references/display.md       D1–D7  large text, localisation, pixel density, runtime scale, icons, theme, motion
references/input.md         I1–I9  touch targets, pointer / keyboard, text input, back, assistive input, time, gestures, links, sharing
references/lifecycle.md     B1–B8  lifecycle states, persistence, process death, background limits, instances, transfers, migrations, sync
references/permissions.md   P1–P9  declarations, runtime flow, degraded paths, store privacy, data at rest, file grants, capture, purchases, store rules
references/media-devices.md M1–M8  audio session / routes, camera, formats, memory, notifications, optional hardware, capture
references/desktop.md       W1–W4  windows, close / quit / tray, file system, packaging and Apple compatibility surfaces
references/performance.md   F1–F3  frame pacing, size and startup, energy and thermal
references/testing.md       X1–X9  device matrix, layout sweep, rotation, real-device labelling, parity, release / CI, interruptions, networks, diagnostics
references/flutter.md       Flutter APIs and plugin traps for all of the above
references/sources.md       official guidelines mapped to IDs, dated version / store gates, related projects
references/stores.md        store-specific submission / release evidence under existing P4 / P8 / P9 / W4 / X6
references/stores.zh-CN.md  Chinese counterpart of the store release guide
tools/check_skill.py        consistency check (IDs, project Markdown links/anchors, metadata, hygiene; needs PyYAML)
tools/test_check_skill.py   isolated positive / negative validator regressions
evals/                     three reproducible review cases, contract examples and actual agent results
tools/evaluate_review.py    synthetic report-contract grader, not an app verifier
VERSION / CHANGELOG.md      first versioned preparation: 0.1.0
docs/CLAWHUB.md             publication preparation only; no upload
docs/PROVENANCE.md          bounded license/source audit
README.zh-CN.md             Chinese project documentation
```

## Install

Clone the repository and link it into your agent's skills directory:

```bash
git clone https://github.com/agentx-icu/cross-platform-app-checklist.git
# Codex (user level)
mkdir -p ~/.codex/skills
ln -s "$PWD/cross-platform-app-checklist" ~/.codex/skills/cross-platform-app-checklist
# Claude Code (user level)
mkdir -p ~/.claude/skills
ln -s "$PWD/cross-platform-app-checklist" ~/.claude/skills/cross-platform-app-checklist
# Agents that read ~/.agents/skills
mkdir -p ~/.agents/skills
ln -s "$PWD/cross-platform-app-checklist" ~/.agents/skills/cross-platform-app-checklist
```

To make a project apply it on every UI or platform change, add a line to the
project's `CLAUDE.md` / `AGENTS.md`, for example:

> Use `cross-platform-app-checklist` in change mode for UI/platform changes,
> and release mode before shipping. Keep reviews read-only unless fixes are
> requested; report scoped IDs, target-specific evidence, device plans and blockers.

## Using it

Default behavior is **read-only review**. Inputs are the project/path and revision,
changed files/diff or release candidate, framework, shipped platforms/form factors,
and channels/package models/territories. Unknowns are labelled. Shared changes
reach every shipped target; default store availability is checked as part of X1.

- **Change mode:** expand only affected areas and their reachable dependencies;
  consider X1/X4/X5 and X6 for artifact/distribution changes. Report selected IDs
  and excluded-area reasons, without 65 boilerplate rows or blanket N/A.
- **Release mode:** account for all **65 stable IDs** per shipped target using the
  [complete catalog](references/checklist.md), then load detailed area and chosen
  channel references as needed. Missing evidence stays outstanding.

Output starts with scope and assumptions, followed by
`priority | ID | platform | status | evidence / gap | next step`, then separate
physical-device plans, release blockers and limitations. Status is **verified**,
**to do**, **needs device**, or **not applicable with reason**. Split partial
coverage by case/target. Source, packaged-artifact, runtime, hardware and store
approval evidence remain distinct. Reading the skill does not authorize fixes,
signing, uploading, credential collection or acceptance of new terms.

Example invocations (replace project and revision with real inputs):
```text
Use $cross-platform-app-checklist in change mode for ./app, diff base..HEAD.
Framework Flutter; Android phones + Windows; Google Play + direct installer.
Review the shared editor and microphone change read-only; list selected IDs,
prioritized findings, physical-device plans and release blockers.

Use $cross-platform-app-checklist in change mode for ./ledger, diff base..HEAD.
Framework Electron; Windows + Linux; MSI + Flathub. Review persistence and quit.

Use $cross-platform-app-checklist in release mode for ./app, candidate RC1.
Framework Flutter; Android + Windows; Google Play + Microsoft Store, US.
Cover all 65 IDs per target; distinguish unavailable evidence from verification.
```

See [reproducible cases and evaluation boundaries](evals/README.md),
[0.1.0 changes](CHANGELOG.md) and [ClawHub preparation](docs/CLAWHUB.md).
The ClawHub listing is not published by this preparation; clone/link works today.

For submission or release work, open the [store release guide](references/stores.md)
([简体中文](references/stores.zh-CN.md)) and choose the actual channel,
package model, territory and app type. It covers App Store (iOS / iPadOS /
macOS), Google Play, Microsoft Store, Flathub and Snap Store, representative
mainland China Android routes (Huawei, Xiaomi, OPPO), and conditional
WinGet / Homebrew Cask / F-Droid or direct-download distribution. The
existing **65 checklist IDs** remain stable; store evidence extends P4,
P8, P9, W4 and X6 rather than creating another independent checklist.

The guide separates required, conditionally required and recommended checks
from verification status. Official-source checks are dated **2026-10-22**;
dynamic policies must be read again at release time. It records limited
public access to some vendor portals, so the account owner must check the
current detailed requirements. Console checks, physical-device tests and
actual review approval are distinct evidence. Preparing a checklist does
not authorize publication or prove acceptance by a store.

Release evidence must identify the final reviewed head, actual job / step
outcomes, executed tests, conditional skips and final artifact hashes (X6).
The references also cover binary / symbol pairing and diagnostic privacy
(X9), visible-edit checkpoints (B2), live motion preferences (D7), stale
native command ownership (I2), paste dispatch (I3), filesystem mechanisms
(W3) and bounded UI polling / exact size metrics (F2–F3). These deepen the
existing IDs; app-specific budgets and implementation choices remain local.
Separate outstanding code defects from product decisions, owner materials
and device qualification, and never collect secret values in the report.

## Contributing

Add a rule when a real defect shows a gap: the rule, the failure it
prevents, and how to verify it. Give new checklist items an ID in the
reference file (`## L8 ...`) and the complete catalog. Preserve existing IDs;
update the stable-set validator deliberately if an addition is justified.
Prefer deepening an existing item when the same acceptance rule covers the issue. Keep the
English and Chinese project / store documentation in sync. For a store
rule, link the current official source, date, exact channel / territory /
feature trigger, rule level and observable evidence; do not turn fees,
SDK deadlines or one store's rules into universal constants.

## Validation

Install PyYAML in the Python environment used for these commands, then run:

```bash
python3 -B -m unittest discover -s tools -p 'test_*.py' -v
python3 tools/check_skill.py
python3 tools/evaluate_review.py --examples
git diff --check
```

The [CI workflow](.github/workflows/check.yml) runs the validator regressions
and consistency check on pushes and pull requests. It checks frontmatter,
checklist / reference ID correspondence, local links and heading anchors
in project Markdown, line endings and selected leak patterns. Version/license
metadata and the complete stable ID set are checked as well.
CI also regrades the saved synthetic agent reports; it does not launch fresh agents.
Negative fixtures prove a broken translated README link / reference anchor
is rejected. It does **not** validate remote policy freshness, agent
compliance, an app's binaries or a real store submission. Capture those
separately using the [release evidence template](references/stores.md#report-record).

For native releases, [X6](references/testing.md#x6-packaged-release-verification--p0-for-release)
also requires an app / engine / plugin architecture inventory from final
binary headers, separate from host CPU, tool ABI and package labels. Retain
installer / package metadata and store-target comparisons as well as
target-machine smoke evidence; this repository's CI does not provide them.

## License

MIT-0 (MIT No Attribution), see [LICENSE](LICENSE) and the
[provenance review](docs/PROVENANCE.md). External linked resources retain their
own licenses; the change does not relicense those works or rewrite old snapshots.
