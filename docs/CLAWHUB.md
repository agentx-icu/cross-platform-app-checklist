# ClawHub release checklist — 0.1.1

Version **0.1.1** packages the purpose-first SKILL.md optimization from `17cb681`.
Only its version metadata changes for this release; the reviewed instruction body,
65 IDs and detailed references remain intact. Existing `v0.1.0` GitHub and ClawHub
artifacts must be preserved. Publication requires the owner's authorization;
this document does not authorize future uploads, accounts or new access grants.
The skill itself continues to default to read-only app review.

## Format and identity

Checked **2026-10-27** against official docs at ClawHub commit
`eb65c6c1af089d8947d2d62ebd60a8b26cbc6eeb`:
[skill format](https://github.com/openclaw/clawhub/blob/eb65c6c1af089d8947d2d62ebd60a8b26cbc6eeb/docs/skill-format.md),
[publishing](https://github.com/openclaw/clawhub/blob/eb65c6c1af089d8947d2d62ebd60a8b26cbc6eeb/docs/publishing.md),
[CLI](https://github.com/openclaw/clawhub/blob/eb65c6c1af089d8947d2d62ebd60a8b26cbc6eeb/docs/cli.md).
Recheck current requirements before a later release. CLI 0.23.3 supports the
commands below; the earlier 0.8.0 CLI lacks the preview/catalog/source flags.

The portable folder name and frontmatter name are `cross-platform-app-checklist`.
`VERSION` and `metadata.version` agree; pass `--version 0.1.1` explicitly rather
than relying on automatic version selection. The project uses **MIT-0**, required
by ClawHub with no per-skill override; see [provenance](PROVENANCE.md).
Review needs no service credential, required environment variable or installer.
Optional repository validators use Python 3/PyYAML.

Publisher: `agentx-icu`; slug: `cross-platform-app-checklist`; display name:
`Cross-platform App Checklist`; category: `development`; topics:
`cross-platform,release-review,flutter,desktop,quality`. Verify existing publisher
access with `clawhub whoami`. Do not print tokens. If login, a new persistent grant
or acceptance of new platform terms is required, stop and obtain the appropriate
user confirmation; do not create access as part of file preparation.

## Validate and stage

Before committing, then confirm the final commit and CI:
```bash
python3 -B -m unittest discover -s tools -p 'test_*.py' -v
python3 tools/check_skill.py
python3 tools/evaluate_review.py --examples
python3 tools/evaluate_review.py flutter-change evals/optimization-2026-10-27/results/flutter-change-after.json
python3 tools/evaluate_review.py release-review evals/optimization-2026-10-27/results/release-review-after.json
git diff --check
```

Inspect existing tags, Releases and hosted versions first. Never overwrite an
existing release version or force-rewrite a tag. Stage from the reviewed commit
outside the checkout, including only **17 regular files**: `SKILL.md`, `LICENSE`,
`VERSION` and `references/*.md`. Verify paths, bytes, local links and SHA-256
hashes against that commit. `.clawhubignore` excludes development CI, docs,
evaluations, tools, READMEs and caches if publishing from a checkout; a separate
whitelist stage is easier to audit. Do not package symlinks, working projects,
local reports, private paths or credentials. The bundle cap is 50 MB.

Create the authorized GitHub tag/Release at the exact successful final commit.
From the parent of the staged folder, preview with that source commit:
```bash
clawhub skill publish ./cross-platform-app-checklist --dry-run --json \
  --owner agentx-icu --slug cross-platform-app-checklist \
  --name "Cross-platform App Checklist" --version 0.1.1 \
  --categories development \
  --topics cross-platform,release-review,flutter,desktop,quality \
  --source-repo agentx-icu/cross-platform-app-checklist \
  --source-commit "$RELEASE_COMMIT" --source-ref refs/tags/v0.1.1 --source-path .
```
Set `RELEASE_COMMIT` to the verified tag's commit. Preview may contact the registry
and does not check all server-side catalog rules. After the explicit publication
authorization, publish that same bundle without `--dry-run`, with a concise
`--changelog`. No automatic publishing workflow or `sync` batch is needed.

## Verify the result

Save the upload receipt/version/attempt IDs. A successful command with
`pending-publication` is not public availability. Follow the existing submission
with read-only owner/public checks; do not upload again merely because review is
pending. Stop for a concrete rejection, failure or access requirement rather than
changing review state or bypassing it.

Confirm public owner/version/latest, security state and anonymous archive
availability. Compare all 17 project-file hashes with the release commit; the
registry may add its own `_meta.json`. Verify normal CLI installation in a
disposable directory with telemetry disabled, without `--force` or
`--force-install`, and without activating the skill in a user's agent.
`clawhub skill verify @agentx-icu/cross-platform-app-checklist --version 0.1.1`
provides a separate verification envelope: report `card.missing`, unsigned or
other limitations exactly rather than calling complete verification passed.
A missing platform-generated Skill Card is not a reason to invent or upload one.

Keep receipts and hash evidence; clean regenerable CLI/cache/install staging once
finished. See [installation/invocation](../README.md#install) and the
[synthetic evaluation assessment](../evals/optimization-2026-10-27/ASSESSMENT.md).
Repository tests, agent probes and registry scans do not establish real app,
physical-device or store acceptance.
