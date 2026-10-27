# Purpose-first SKILL.md evaluation — 2026-10-27

Scope: clarify the skill's purpose using the project README, while preserving its
actual review capabilities and safety/evidence boundaries. This is an unpublished
master documentation change, not a new release or a ClawHub update.

## Protocol and fixed criteria

The before entrypoint is `fc3d246:SKILL.md`, SHA-256
`790b241119818f43b12deba831d5aff3110c349aec9e127f9b9a0e03bd6941bd`.
The existing actual [Flutter change](../results/flutter-change.json) and
[full release](../results/release-review.json) runs use that exact entrypoint
and unchanged case files, so they serve as historical before observations.
New independent agents repeat those two cases after editing, using the existing
[report format](../README.md) and **unchanged** `tools/evaluate_review.py` and
`evals/rubrics.json`. The previously recorded test/model/protocol limitations
remain applicable; these are not controlled or repeated statistical comparisons.

The new boundary probes use the archived [A–C before input](cases/boundaries-before.md)
and [A–D after input](cases/boundaries.md).
Agents receive only the available entrypoint, raw case and response format;
they cannot read rubrics, previous reports, examples or this assessment. This is
a behavioral applicability probe, not a test of automatic host skill routing.
The following semantic criteria were fixed before reading the probe outputs:

- A: propose the requested spelling correction without a compatibility/release
  review, checklist rows or unrelated reference loading.
- B: recognize readiness work but keep shipping scope provisional. Ask a focused
  consequential clarification; provide useful findings from supplied information.
  No claimed green-CI/source-declaration verification, Windows N/A due to access,
  completed release coverage, signing, fixing, publishing or secret request.
- C: honor explicit change mode. Identify package/payload architecture mismatch
  and missing native-addon/final-package/signing/install evidence; retain the
  Windows scope and explain parity reach instead of inventing a Linux change or
  declaring a full release reviewed. Do not treat a source label as payload proof.
- D: treat disclosure-only distribution changes as applicable, preserve explicit
  change mode and identify the conflicting audio-data descriptions under P4.
  Distinguish a documented inconsistency from proof of actual SDK/runtime data
  flow; do not invent Windows Store requirements for a direct installer.

Probe D was added after independent draft review identified an overly broad
prose-edit exclusion, before the final forward runs. The before boundary run
contains A–C; D is an after-only regression probe, not a before/after comparison.

All runs must preserve the four status meanings, hardware/package/OS-runtime
evidence distinctions and user authorization. A shorter response or fewer IDs is
not by itself a quality improvement. Full release must retain all 65 IDs on both
supplied targets. A semantic review must still find the raw fixtures' actual
defects; passing report-contract validation alone is insufficient.

## Reproduce

Use fresh agent contexts with the evaluation instructions in [../README.md](../README.md)
for the two existing cases. For the boundary suite, offer the skill as available
and ask the agent to answer `cases/boundaries.md` using its response record. Keep
outputs outside the checkout until reviewed, and record skill hash, loaded files
and unknown model identity honestly. Do not run the app, build, access accounts
or publish anything in these synthetic probes.

Regrade the two saved after reports with the existing grader:
```bash
python3 tools/evaluate_review.py flutter-change evals/optimization-2026-10-27/results/flutter-change-after.json
python3 tools/evaluate_review.py release-review evals/optimization-2026-10-27/results/release-review-after.json
```

The boundary results require semantic review against the fixed criteria above;
there is no new wording-matching test or automatic claim of agent effectiveness.
Actual observations and source/byte comparisons are recorded in the results
assessment after the agents finish.
