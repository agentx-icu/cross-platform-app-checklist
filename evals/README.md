# Reproducible review evaluations

These three synthetic cases exercise review decisions without an app build,
account or hardware. They do not establish production readiness. Run each in a
fresh agent context with only `SKILL.md`, the case, and this report format. Let
the agent read relevant references; keep `rubrics.json`, examples and past results
out of its context. Record agent/model, date, skill revision and loaded files.

Prompt: “Use the cross-platform-app-checklist skill in this checkout to review
`evals/cases/<case>.md`. Follow its requested mode, stay read-only and write a JSON
report using the format below. Read references on demand. Do not read the rubric,
examples or previous results.” Use an output file outside the checkout.

## Report format

JSON object with these fields (no Markdown fence):
- `scope`: object with `mode` (`change` or `release`), `project`, `change`,
  `framework`, `platforms` (array) and `channels` (array).
- `selected_ids`: array of stable IDs reviewed. Full release: all 65.
- `excluded_areas`: array of `{area, reason}` for areas outside a change review;
  an empty array is allowed for full release. Outside scope is not N/A.
- `references_loaded`: array of repository-relative reference paths actually read.
- `rows`: array of `{id, platform, priority, status, evidence, next_step,
  reason, release_blocker}`. Use one shipped platform per row (`Android`,
  `Windows`, `Linux`); split proven and outstanding cases when needed.
  `evidence`, `next_step`, `reason` are strings; `release_blocker` is boolean.
  Status is `verified`, `to do`, `needs device` or `not applicable`.
  For these wholly unexecuted fixtures use one unique row per ID/platform;
  combine multiple outstanding observations in that row. General app reviews can
  split genuinely different proven/outstanding cases as the skill describes.
- `device_plan`: array of concrete hardware scenarios with expected observations
  (strings or structured objects; semantic completeness is reviewed separately).
- `release_blockers`: array of outstanding shipping conditions (strings or objects).
- `limitations`: array of unverified claims and access limits.

## Three separate kinds of check

1. Documentation/CI structure tests check IDs, links and metadata. They cannot
   measure agent behavior.
2. `tools/evaluate_review.py CASE REPORT.json` grades observable report contracts:
   missing IDs/platforms, unsupported verified claims, missing device/blocker
   records, and excessive or contradictory N/A. The synthetic cases supply no
   executed evidence, so no whole-item `verified` is defensible. The N/A threshold
   is specific to these feature-rich fixtures, not a universal product rule.
3. A human/independent reviewer reads the actual findings against raw artifacts:
   did Flutter review find OS-based layout, fixed text height and inactive/audio
   mistakes on both targets; did Electron review find unsafe paths, off-screen
   bounds, quit ownership and mislabeled payloads without Flutter advice; did full
   release preserve all IDs and separate source, runtime, device and store evidence?
   A report can pass the script and still fail this semantic review.

Run the deterministic positive examples and mutation negatives with:
```bash
python3 -B -m unittest discover -s tools -p 'test_*.py' -v
python3 tools/evaluate_review.py --examples
```

Files under `examples/` are hand-authored contract examples, never agent results.
Actual agent runs and qualified conclusions are recorded separately under
`results/`. To repeat an agent run, use the prompt above and then grade its output;
the repository deliberately does not install an agent CLI, select paid models,
or send project files to a service. No hardware, real store or acceptance test is
performed by this harness.
