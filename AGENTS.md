# AGENTS.md — repo-triage

Operating contract for AI agents (Claude, Codex, Cursor) working in
this repo. Conventions match the rest of the AthenaTheOwl portfolio.

## What this repo is

A monthly single-file memo across the active portfolio repos. The memo
forces a top-2 ATTEND list, a bottom-3 RETIRE list, and a FREEZE list
against a hand-scorable 5-factor thesis-alive rubric. The memo, not a
dashboard, is the artifact.

## Roles you may see in tasks

| Role | What they do |
|---|---|
| `rubric-author` | Maintains `rules/v0.md`; proposes revisions in PR form |
| `repo-scorer` | Fills in `scoring/YYYY-MNN/<repo>.md` by hand against the rubric |
| `memo-renderer` | Runs `render_memo.py` to assemble the monthly memo |
| `count-enforcer` | Runs `enforce_counts.py` to assert exactly 2 ATTEND + 3 RETIRE |
| `retrospective-author` | Maintains the deltas-vs-last-month section |

These roles exist in the spec ledger; v0 does not implement them.

## Voice constraints

- No marketing words. The memo is a forcing function; reading it
  should feel like reading a fund manager's allocation note, not a
  product launch.
- No antithetical reversals as a structural device.
- Plain assertions. The rubric is the discipline; the prose is
  scaffolding.

## Gates (shipped in v0.1; spec 0002)

All four gates are subcommands of the `repo-triage` CLI. The
`scripts/*.py` files are thin shims that re-export them.

- `repo-triage voice-lint <memo>` — rejects banned marketing /
  antithetical-reversal phrases (see `src/repo_triage/cli.py`).
- `repo-triage enforce-counts <memo> --portfolio config/portfolio.yaml`
  — exactly 2 ATTEND, exactly 3 RETIRE per memo; every other active
  repo in FREEZE; fails otherwise.
- `repo-triage validate-schemas <memo> --memo-schema schemas/memo.schema.json
  --scoring-schema schemas/scoring.schema.json --scoring-dir scoring/<month>/`
  — JSON-schema validation of memo front-matter and every scoring stub.
- `repo-triage rubric-pinned <memo> --rubric rules/v0.md` — memo's
  front-matter pins a rubric version matching the file on disk.

CI runs all four on every push and PR; see `.github/workflows/ci.yml`.

## Out of scope

- A live dashboard. No web UI, no per-repo cards, no charts.
- LLM-assigned scores. An LLM may help draft rationale; the score
  comes from a person reading the repo.
- Cross-portfolio comparisons. This memo is scoped to the author's
  portfolio.
- Weekly cadence. The whole point is monthly; weekly is noise.
