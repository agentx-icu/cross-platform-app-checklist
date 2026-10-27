# Actual independent agent runs — 2026-10-27

These are actual Codex subagent outputs from fresh contexts, separate from the
hand-authored contract examples. Exact runtime model identifier was not exposed;
no model name or statistical reliability is inferred. App execution, builds,
network, accounts, secrets and source fixes were outside the evaluation scope.
Agents were given the case, skill and report-format instructions, and were told
not to read rubrics, examples or other results. Reported loaded references were
checked against the reports. Full prompts are reproducible from the parent
[evaluation instructions](../README.md).

Prepared entrypoint SHA-256:
`790b241119818f43b12deba831d5aff3110c349aec9e127f9b9a0e03bd6941bd`.
The [input manifest](input-manifest.json) records base `0a64c0f`, the original
entrypoint hash and final prepared source hashes. Only workstation-specific
checkout prefixes in saved reports were normalized to `.`; decisions, selection,
status and evidence claims were preserved. Report-format clarification in the
testing reference was added during the evaluation session; the entrypoint and
raw case content were fixed before the three forward tests began.

| Run / actual output | IDs / rows | verified | to do | needs device | N/A | Final contract grade |
|---|---|---|---|---|---|---|
| [Original-skill Flutter baseline](baseline-flutter.json) | 35 / 73 | 0 | 67 | 5 | 1 | Four format/scope diagnostics; see qualification below |
| [Flutter change](flutter-change.json) | 21 / 42 | 0 | 35 | 6 | 1 | 0 problems |
| [Electron change](electron-change.json) | 14 / 28 | 0 | 26 | 2 | 0 | 0 problems |
| [Full release](release-review.json) | 65 / 130 | 0 | 108 | 20 | 2 | 0 problems |

## Semantic review

- Flutter: identified OS-based breakpoint choice, fixed text height/unwrapped
  content, indiscriminate inactive-state recording stops, missing Windows denial
  handling, and absent route/device/OS-resize evidence. Both shipped targets were
  retained; unchanged areas were excluded with scope reasons.
- Electron: identified mutable data beside the executable, unchecked saved window
  bounds, quit ownership and an uncancelled flush after timeout, plus ARM64 package
  labeling versus x64 payload and uninspected SQLite addon. The agent loaded no
  Flutter reference and did not treat desktop lifecycle as inapplicable.
- Release: covered all 65 IDs on both targets. Explicitly retained migration and
  newer-data safety gaps, stale privacy/billing evidence, final native payload
  versus package metadata versus machine-load distinctions, and X9 retained real
  directories/writer identity/chronology across timestamp ties. Hardware plans,
  owner materials and store evidence remained separate. Only absent screen/system
  audio capture (M8) was N/A. No claim of runtime success or store acceptance.

The independent code reviewer also confirmed exact catalog migration and no new
visible licensing obstacle. They reproduced and verified fixes for duplicate-row
N/A padding and malformed JSON crashes. Those are grader regressions, not proof
of real app behavior.

## Calibration and limits

The baseline used the original skill at `0a64c0f`; it found the important defects
and made zero unsupported verified claims. Its 35 selected IDs exceed the
fixture-specific daily cap of 30. It also split three ID/platform pairs into
separate cases; the unique-row clarification was added after the baseline. The
four current diagnostics are therefore not four demonstrated safety failures,
and baseline/forward scores are not a controlled performance benchmark.

Initial grading also rejected valid descriptive framework/channel labels and
structured device plans. These were grader mistakes: positive regressions now
accept equivalent scope information and structured records. An initial rubric
required I3/input.md for the Flutter case although the snippet changed no Enter,
composition, paste or submission handling. Independent review concluded that the
reasoned exclusion was appropriate to change mode; I3 is now optional for this
case. The agent report was not rewritten to match the rubric, and this correction
is not reported as a skill defect fixed.

Entrypoint bytes fell from **22,148 to 7,141** while all 65 original catalog rules
were retained verbatim apart from relative link roots. This measures file size,
not actual token cost, latency or model effectiveness. These are one run per
synthetic case with one narrow baseline, not broad or repeated reliability data.
No runnable Flutter/Electron app, physical hardware, binary package, real store
console or actual submission was tested. Application platform/store policies were
not reopened in the network-free cases. ClawHub documentation was separately
checked for preparation; no upload/registry scan/dry-run was executed.

To regrade these saved outputs (this does not run a new agent):
```bash
python3 tools/evaluate_review.py flutter-change evals/results/flutter-change.json
python3 tools/evaluate_review.py electron-change evals/results/electron-change.json
python3 tools/evaluate_review.py release-review evals/results/release-review.json
```
