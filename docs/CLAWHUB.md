# ClawHub publication preparation — 0.1.0

Prepared on **2026-10-27**; no ClawHub upload, account/credential setup, acceptance
of new terms, GitHub tag or Release is part of this change. The owner must
separately authorize publication. The default skill operation is read-only review.

## Official format checked

Official docs at ClawHub commit `5e73cd713330fec7b33c3e56921bfed42190df33`:
[skill format](https://github.com/openclaw/clawhub/blob/5e73cd713330fec7b33c3e56921bfed42190df33/docs/skill-format.md),
[publishing](https://github.com/openclaw/clawhub/blob/5e73cd713330fec7b33c3e56921bfed42190df33/docs/publishing.md),
[CLI](https://github.com/openclaw/clawhub/blob/5e73cd713330fec7b33c3e56921bfed42190df33/docs/cli.md).
Recheck the current versions before a future upload.

The folder has the required `SKILL.md`, lowercase portable name, description,
MIT-0 license and relative references. Version `0.1.0` is the first explicitly
versioned preparation, recorded in `VERSION` and `metadata.version` for portable
Agent Skills. An eventual CLI invocation must select `--version 0.1.0`; ClawHub's
new-skill default is otherwise `1.0.0`. No per-skill license override exists:
ClawHub requires MIT-0 without attribution. See the [provenance review](PROVENANCE.md).

No service, secret, required environment variable or automatic installer is
needed for the review. Optional local validators use Python 3 and PyYAML; the
skill can be read without running them. Do not declare credentials or `always`.

Suggested catalog fields: slug `cross-platform-app-checklist`, display name
`Cross-platform App Checklist`, category `development`, topics
`cross-platform,release-review,flutter,desktop,quality`. All five are ordinary
labels; none implies platform endorsement or security certification. Choose the
actual publisher handle at publication time; repository ownership does not
establish a ClawHub account or namespace.

## Local preparation and bundle review

From a clean checkout:
```bash
python3 -B -m unittest discover -s tools -p 'test_*.py' -v
python3 tools/check_skill.py
python3 tools/evaluate_review.py --examples
git diff --check
```

`.clawhubignore` excludes development CI, documentation, evals, tools and caches.
The intended bundle is `SKILL.md`, `LICENSE`, `VERSION` and `references/*.md`.
Inspect the file inventory and size before uploading; regular supporting files
are accepted subject to ignore/hidden/symlink handling and the 50 MB bundle cap.
Do not package local reports, credentials, working projects or symlinks. The
optional validators and evaluation instructions remain in the GitHub checkout.

After separate authorization and with a current installed CLI, a **preview only**
command is:
```bash
clawhub skill publish . --dry-run --version 0.1.0 \
  --slug cross-platform-app-checklist \
  --name "Cross-platform App Checklist" \
  --categories development \
  --topics cross-platform,release-review,flutter,desktop,quality
```
This command has **not** been executed in this preparation. CLI preview may
contact the registry and does not check all server-side catalog constraints.
Do not remove `--dry-run`, run `sync`, log in, accept terms, or add a publishing
workflow as part of preparation. A future uploader must inspect exact contents,
confirm publisher rights and terms, and await the registry's security result;
pending status is not published or discoverable status.

## Installation and invocation

Today: use the Git clone/link instructions in [README](../README.md#install).
After a separately completed public upload, verify the real owner/slug with
`clawhub inspect @OWNER/cross-platform-app-checklist --files`, then install that
qualified identifier with `clawhub install @OWNER/cross-platform-app-checklist`.
`OWNER` is a placeholder; these commands do not claim a listing exists. The CLI
installs into its configured workdir/skills directory; agent discovery varies.

Invoke with project/revision or diff, targets, framework, channels and mode; the
[three review cases](../evals/README.md) provide repeatable prompts. Never treat a
passing repository validator, an agent report or a registry scan as proof that
an application works on real hardware or will pass any store review.
