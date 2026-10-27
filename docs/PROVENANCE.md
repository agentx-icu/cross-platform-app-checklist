# License and provenance review — 2026-10-27

Scope: the complete tracked tree and 13 commits reachable from default branch
`master` at `0a64c0fdc93fd43e56aea23eadafe587ab9bff5a`, before this preparation.
The repository owner explicitly requested MIT-0 relicensing on 2026-10-27.

## Evidence inspected

- `git log --all`, `git shortlog -sne --all`, file history, tracked file modes,
  license/copyright notices, external-source links and code fences.
- [GitHub commit attribution](https://api.github.com/repos/agentx-icu/cross-platform-app-checklist/commits?per_page=100):
  every substantive author (local name `anonymoussoft`) and initial/merge author
  (`agentx.icu`) resolves to GitHub login `agentx-icu`. GitHub's `web-flow`
  committer is the merge service, not an additional content author. Names alone
  were not treated as evidence of two independent rights holders.
- Initial commit `77dcba8` contains the standard GPL-3.0 license and a one-line
  README. `b1a4dab` adds the checklist/references/tools as original project work;
  later commits extend that work. No vendored library, image, third-party code
  block, imported checklist, additional copyright holder or third-party GPL
  notice was identified in the reviewed tree/history.
- [Sources](../references/sources.md) and store guides contain links and project
  explanations of platform rules. Related-project links (including BSD and
  CC BY resources) are reading suggestions; their files are not bundled here.
  A link does not relicense the linked work. This change claims no rights over
  external documents, platform marks, framework APIs or future contributions.

## Conclusion and limit

No third-party relicensing obstacle was identified in this bounded review.
Together with the owner's explicit instruction, the single-account contribution
history supports replacing this project's GPL-3.0 license with **MIT-0**, including
its original documentation, tools and new synthetic examples. This is a repository
provenance check, not proof about undisclosed off-repository origins. Newly
identified copied/restricted material or another rights holder requires a fresh
review and must not be silently relicensed.

[LICENSE](../LICENSE) follows the [SPDX MIT-0 text](https://spdx.org/licenses/MIT-0.html),
with `Copyright 2026 agentx-icu`. The ordinary MIT attribution condition is absent.
The copyright line identifies this project's holder; preserving attribution is
not a condition of MIT-0. README and skill metadata agree. Earlier GPL-3.0
snapshots retain the permissions already granted under their original license;
this preparation does not rewrite history or withdraw those permissions.

This review does not accept ClawHub terms, create an account or publish anything.
