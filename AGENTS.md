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

## Gates (will land in spec 0002)

- `voice_lint` on every memo and every rubric revision
- `enforce_counts.py` — exactly 2 ATTEND, exactly 3 RETIRE per memo;
  every other active repo in FREEZE; fails otherwise
- `validate_schemas.py` — `memo.schema.json` validates every
  `repo_triage/*.md` front-matter block
- `rubric_pinned.py` — every memo's front-matter pins the rubric
  version it scored against

## Out of scope

- A live dashboard. No web UI, no per-repo cards, no charts.
- LLM-assigned scores. An LLM may help draft rationale; the score
  comes from a person reading the repo.
- Cross-portfolio comparisons. This memo is scoped to the author's
  portfolio.
- Weekly cadence. The whole point is monthly; weekly is noise.
