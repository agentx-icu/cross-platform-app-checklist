---
name: cross-platform-app-checklist
description: Review cross-platform app changes or release readiness across iOS, iPadOS, Android, macOS, Windows and Linux. Use for UI, lifecycle, permission, media, performance, packaging or store changes in Flutter, React Native, Compose Multiplatform, .NET MAUI, Electron or native apps.
license: MIT-0
metadata:
  version: "0.1.0"
---

# Cross-platform app checklist

Review the places where shared app behavior diverges across platforms. Default
to a **read-only review**: inspect supplied project artifacts and report findings.
Code fixes, installing tools, builds that modify the project, signing, uploading,
account creation and accepting platform terms require their own user scope.
Do not request secret values; record missing owner-material names, purpose and
acquisition location. A review never guarantees store acceptance.

## Inputs and mode

Record the project/path and revision, changed files/diff or release candidate,
framework, shipped target platforms and form factors, and distribution channels
(including package model and territory for store rules). Infer these from supplied
artifacts where possible; label assumptions and unknowns. Missing inputs narrow
what can be verified; continue useful inspection and ask only about consequential
unknowns. Shared code reaches every shipped target. Default store availability
may add reachable surfaces: inspect X1 rather than assuming a build list excludes them.

- **Change review (`change`, default for daily work):** map changed behavior and
  reachable dependencies to the area table below. Read only those area references
  and the applicable sections in testing. Always consider X1 (reach), X4 (device
  evidence), X5 (parity); include X6 when artifacts, native dependencies, signing
  or distribution change. Expand adjacent areas when the change creates a risk
  there. Report selected IDs and excluded areas with a short scope reason; do
  not print all 65 rows or turn unreviewed areas into N/A. This is a scoped
  change review, not a release-readiness declaration.
- **Full release review (`release`, explicit release/submission/readiness work):**
  read the [complete catalog](references/checklist.md) and account for **all 65
  IDs** on every shipped target, with target-specific reasons for inapplicability.
  Open area details as each area is reviewed. Use the chosen-channel sections of
  the [store guide](references/stores.md) ([中文](references/stores.zh-CN.md)) for
  P4/P8/P9/W4/X6. Omitted evidence is a gap, never implicit success.

If a request combines both, retain scoped change findings and the full release
coverage record. A narrow diff alone does not establish release coverage.

## Load references on demand

| Changed behavior / review question | IDs | Read |
|---|---|---|
| Window sizes, breakpoints, resize, safe areas, keyboard, rotation, folds | L1–L8 | [layout](references/layout.md) |
| Text scale, locale, density, runtime scale, icons, theme, motion | D1–D7 | [display](references/display.md) |
| Touch, pointer, keyboard/IME, navigation, accessibility, time, links, sharing | I1–I9 | [input](references/input.md) |
| Lifecycle, persistence, process death, background, instances, transfers, migrations, sync | B1–B8 | [lifecycle](references/lifecycle.md) |
| Declarations, denial, privacy, backups, file grants, capture, billing, audience | P1–P9 | [permissions](references/permissions.md) |
| Audio sessions/routes, camera, formats, memory, notifications, hardware, capture | M1–M8 | [media/devices](references/media-devices.md) |
| Windows, close/quit/tray, filesystem, packaging, Apple compatibility surfaces | W1–W4 | [desktop](references/desktop.md) |
| Frame pacing, size/startup, energy/thermal | F1–F3 | [performance](references/performance.md) |
| Target matrix, sweeps, OS resize, evidence, parity, artifacts, interruptions, network, diagnostics | X1–X9 | [testing](references/testing.md) |

For Flutter, read only the affected sections of [Flutter notes](references/flutter.md)
after the platform rule. For other frameworks, use their native equivalents;
do not load Flutter notes by default. Load [sources](references/sources.md) when
checking a version gate or dynamic platform/store claim. Recheck current official
guidance and record URL/date; distinguish runtime OS, build SDK, target SDK,
deployment minimum and channel. Historical dates in references are not fresh
release evidence. Do not preload all references for daily work.

## Evidence and decisions

For each selected ID and target, use:
- **verified**: name the actual test/inspection, result and evidence artifact,
  revision/build, OS, window dimensions/scale and relevant settings. Limit the
  claim to the cases actually proved.
- **to do**: identify a defect, missing decision/material, absent test, or unknown
  scope and its next action. Not run means not verified.
- **needs device**: identify hardware-dependent behavior and a concrete physical
  device scenario, expected observation and evidence to retain.
- **not applicable**: give a feature/platform/channel reason backed by the scope.
  Lack of access, missing evidence, a desktop target or time pressure alone does
  not make a reachable rule inapplicable. Reconsider blanket or excessive N/A.

Split partly proven items into proven and outstanding cases/platforms. Source
inspection can establish a narrow code fact, not packaged declarations or runtime
behavior. Screenshot goldens do not prove native UI, OS resize or process-death
recovery; simulators do not prove physical hardware. App/engine/plugin binary
headers, package metadata and target-machine load tests are separate X6 evidence;
host CPU, tool ABI and filenames do not substitute for them. Preserve the detailed
verification boundaries in testing, including retained real diagnostics, writer
ownership and event chronology across timestamp ties (X9).

Priorities: **P0** core function or required platform/store rule fails; **P1** a
common scenario degrades; **P2** enhancement/niche. A priority is not a test status.
In a review, recommend fixes at their shared cause and check reach/parity (X5).
Perform fixes only when requested; this skill itself grants no mutation authority.

## Output contract

Start with mode, inspected revision/change, framework, targets/form factors,
channels, selected IDs, excluded areas and assumptions. List prioritized findings:

`Priority | ID | platform | status | evidence / gap | next step`

Then list **physical-device plan** and **release blockers** separately, even if
empty (say why). Separate code defects, product decisions, owner materials and
hardware qualification; an account gap does not block unrelated analysis or an
authorized code fix. For a change review, state release readiness was not assessed.
For a release review, summarize full coverage and unresolved blockers without
claiming approval. Record unrun checks, unavailable artifacts and stale policies.
Use the [testing evidence template](references/testing.md#report-template) and
[store record](references/stores.md#report-record) when their scope applies.
