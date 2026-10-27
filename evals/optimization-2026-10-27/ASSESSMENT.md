# SKILL.md purpose-first optimization assessment

The change follows the user's request to foreground what this skill does, using
[the project README](../../README.md) as the capability source. It updates master
only. The published GitHub tag/Release and ClawHub 0.1.0 remain separate snapshots;
no version bump, tag rewrite or upload belongs to this optimization.

## Concrete changes and rationale

- Replace the abstract opening and immediate permission rules with purpose,
  actual target platforms, review outputs and limits. Explain that framework-
  independent platform rules also apply to native implementations; Flutter notes
  are supplementary and do not prove all frameworks/targets tested.
- Present the existing nine capability areas and their reference routes before
  workflow details. Make release work concrete: identity, privacy/content,
  listing/review access, signed artifacts, tracks and safe updates under existing
  P4/P8/P9/W4/X6, without a new checklist.
- Retain change and full-release modes, with explicit narrow-mode precedence and
  complete 65-ID per-shipped-target release coverage. Limit selective loading to
  change mode; release reads each area's applicable rules and chosen-channel detail.
- Distinguish consequential missing inputs from harmless unknowns. Continue useful
  provisional review without invented shipping scope or completed coverage.
- Preserve statuses, parity, physical-device, native/package/signature and final-head
  CI evidence boundaries. Add README's distinction between required/conditional/
  recommended rules, issue priority and verification status when deriving blockers.
- Exclude unrelated API explanations and prose edits while retaining distribution
  text such as privacy disclosures. Keep existing user authorization and read-only
  defaults; omit repository installation, contribution and publication history
  from the skill's operating instructions.

Independent draft review found two wording problems: an overly broad prose-edit
exclusion and an unqualified affected-sections rule. Both were corrected before
fresh final forward tests. Draft test agents were interrupted without assessed
output; they were replaced with fresh final-context agents. Source review then
approved the final entrypoint. No existing rubric, scorer, case, reference,
README, CI workflow, license or version metadata was changed.

## File comparison

| Item | Before | After |
|---|---|---|
| SKILL.md | 7,141 bytes; 110 lines; 944 whitespace-delimited words | 8,350 bytes; 129 lines; 1,081 words |
| References | 14 existing files | Byte-for-byte unchanged; all 65 stable IDs preserved |
| Existing tools, fixtures, rubric and saved runs | Existing validation baseline | Unchanged |
| New optimization directory | Absent | Raw boundary cases, protocol, manifest and actual evaluation evidence |

The entrypoint grows **1,209 bytes (16.9%)** to make purpose/capabilities explicit.
This is not a context-size optimization or a claimed speed improvement. Size is
reported alongside clarity and preserved behavior. [The manifest](input-manifest.json)
records final hash `027674af80136f15bd95879fe5cffa777c9e86d35983e974dd34a5a441286c48`
and hashes for 27 unchanged files. The original entrypoint remains accessible at
`fc3d246` / `v0.1.0`.

## Actual agent observations

Before change/release reports are historical actual runs of the exact before
entrypoint and the same raw cases. The after reports come from fresh independent
contexts using the final hash. Exact model identities are unavailable. Existing
contract rules were kept fixed; the raw findings were separately read against the
cases rather than treating a contract score as semantic proof.

| Case | Before | After | Observable result |
|---|---|---|---|
| Flutter change | 21 IDs / 42 rows; 0 verified | [20 IDs / 40 rows](results/flutter-change-after.json); 0 verified | Both flag the OS-based layout pattern, fixed height, inactive-recording, Windows denial and route/device evidence gaps; both retain Android/Windows parity |
| Full release | 65 IDs / 130 rows; 0 verified | [65 IDs / 130 rows](results/release-review-after.json); 0 verified | Both retain migration, privacy/billing, architecture/package/install, final-head CI and diagnostic ownership/chronology gaps |
| A: typo only | No checklist review | No checklist review | Both correct; no demonstrated baseline over-trigger |
| B: incomplete evidence | Provisional release; no verified/N/A | Provisional release; no verified/N/A | Both correct; after uses unresolved-target placeholders rather than provisional platform columns |
| C: explicit change | Scoped MSI review | Scoped MSI review | Both correct; after excludes unrelated Linux review rather than using the baseline's scoped Linux N/A row |
| D: disclosure text | Not run | P4 change review | After-only regression probe catches the conflicting data statements without claiming observed SDK traffic |

The existing grader reports **0 contract problems** for both after change/release
reports. Release statuses remain 108 to do, 20 needs device and 2 N/A (M8 only).
Change statuses are 33 to do, 6 needs device and 1 channel-backed N/A. No whole-item
verified claim is supported by these wholly unexecuted fixtures, and none was made.
The complete [before](results/boundaries-before.json) and
[after](results/boundaries-after.json) boundary responses are retained. Only local
checkout prefixes were normalized to `.`; no decisions or findings were edited.

Independent semantic review of A–D found no substantive defect. A–C already
satisfied the fixed criteria before editing; D was introduced after draft review
and before the final tests, so it cannot establish a before/after improvement.
Reference-list recording also differs: after boundary metadata includes the
entrypoint/case paths, while before lists only area references. Counts are not
comparable measures of context efficiency.

Independent semantic review of the two realistic after reports found no important
failure and confirmed the critical evidence boundaries. Two reading limits remain:
the fixture's `compact` variable has no shown consumer, so the OS-based pattern is
not proof of a runtime layout effect; framework/plugin support warnings for Windows
are informational risks, not evidence that this app chose an unsupported purchase
or camera plugin. The reports must not be read as establishing those app facts.

## Validation and limits

Existing full regressions, positive/negative fixtures, documentation/frontmatter/
ID/link checks, quick skill validation, saved baseline report grading and both new
report grades are run for this change. CI still checks structural contracts and
saved reports; it does not run fresh agents. Boundary semantic criteria and repeat
instructions are in [README](README.md).

These are single synthetic observations, not a controlled model comparison,
statistical reliability result or host automatic-routing evaluation. No real app,
build, package, physical hardware, SDK configuration, policy console or store
submission was tested. App policy/version facts were not refreshed in the
network-free probes. The observations support preserving the existing review
boundaries and clearer purpose/scope expression; they do not establish new
platform support, automatic verification or acceptance by any store.
