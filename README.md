# cross-platform-app-checklist

An agent skill (Claude Code, Codex and other `SKILL.md`-aware agents) that
walks a change through the places multi-platform apps break: screen sizes and
breakpoints, high-DPI and fractional scaling, rotation, split screen and
foldables, safe areas and keyboards, large text, permission declarations,
background limits, mobile device features (audio routes, camera, sensors),
and the differences between desktop and mobile.

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
tools/check_skill.py        consistency check (IDs, links and anchors, YAML frontmatter, basic leak patterns; needs PyYAML)
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

## Contributing

Add a rule when a real defect shows a gap: the rule, the failure it
prevents, and how to verify it. Give new checklist items an ID in the
reference file (`## L8 ...`) and list it in `SKILL.md`; run
`python3 tools/check_skill.py` before committing.

## License

GPL-3.0, see [LICENSE](LICENSE).
