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
SKILL.md                    entry point: when to use, how to answer, the checklist
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
tools/check_skill.py        consistency check (IDs, all README / reference links and anchors, YAML frontmatter, basic leak patterns; needs PyYAML)
tools/test_check_skill.py   isolated positive / negative validator regressions
README.zh-CN.md             Chinese project documentation
```

## Install

Clone the repository and link it into your agent's skills directory:

```bash
git clone https://github.com/agentx-icu/cross-platform-app-checklist.git
# Claude Code (user level)
mkdir -p ~/.claude/skills
ln -s "$PWD/cross-platform-app-checklist" ~/.claude/skills/cross-platform-app-checklist
# Agents that read ~/.agents/skills
mkdir -p ~/.agents/skills
ln -s "$PWD/cross-platform-app-checklist" ~/.agents/skills/cross-platform-app-checklist
```

To make a project apply it on every UI or platform change, add a line to the
project's `CLAUDE.md` / `AGENTS.md`, for example:

> UI, lifecycle, permission, media and packaging changes are checked against
> the `cross-platform-app-checklist` skill; the answers (verified / to do /
> not applicable with reason) go into the PR description.

## Using it

The agent loads the skill when a change touches UI or platform behaviour.
It scopes the platforms and form factors the change reaches, answers every
checklist item as **verified** (with evidence), **to do** or **not
applicable** (with a reason), opens the matching reference before writing
code, and reports the answers as a table. Items that need real hardware are
marked "needs device", never "verified" from a simulator.

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

## Contributing

Add a rule when a real defect shows a gap: the rule, the failure it
prevents, and how to verify it. Give new checklist items an ID in the
reference file (`## L8 ...`) and list it in `SKILL.md`. Prefer deepening an
existing item when the same acceptance rule covers the issue. Keep the
English and Chinese project / store documentation in sync. For a store
rule, link the current official source, date, exact channel / territory /
feature trigger, rule level and observable evidence; do not turn fees,
SDK deadlines or one store's rules into universal constants.

## Validation

Install PyYAML in the Python environment used for these commands, then run:

```bash
python3 -B -m unittest discover -s tools -p 'test_*.py' -v
python3 tools/check_skill.py
git diff --check
```

The [CI workflow](.github/workflows/check.yml) runs the validator regressions
and consistency check on pushes and pull requests. It checks frontmatter,
checklist / reference ID correspondence, local links and heading anchors
in every README and reference, line endings and selected leak patterns.
Negative fixtures prove a broken translated README link / reference anchor
is rejected. It does **not** validate remote policy freshness, agent
compliance, an app's binaries or a real store submission. Capture those
separately using the [release evidence template](references/stores.md#report-record).

## License

GPL-3.0, see [LICENSE](LICENSE).
