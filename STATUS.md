# STATUS — Monthly Repo Triage

Last updated: 2026-06-22

## Current state

- Archived 2026-07-01. The forced ATTEND/FREEZE/RETIRE count enforcement is the idea carried over into portfolio-thesis-plane, so work continues there instead of here.
- v0.1 ships the rubric, scoring template emitter, memo renderer, four
  gate scripts, schemas, a runnable Python CLI (`repo-triage`), and the
  first calibration ledger row (`scoring/2026-M07/` + `repo_triage/2026-M07.md`
  + `data/ledger/runs.jsonl`).
- `rules/v0.md` defines the 5-factor thesis-alive rubric with 0-3 bands.
- `config/portfolio.yaml` enumerates the 20 active portfolio repos.
- The first memo `repo_triage/2026-M07.md` has 2 ATTEND, 3 RETIRE,
  15 FREEZE, pins `rubric_version: v0`, and passes all four gates.
- `PRODUCT_BRIEF.md` and `SYSTEM_MAP.md` at the repo root, plus
  `docs/METHODOLOGY.md`, give a tree-down reader the why / what / how.
- `decisions/DEC-0001-bundled-v0.1-release.md` records why v0.1
  collapses three planned PRs into one.
- Tests cover the CLI, the renderer, the count enforcer, the schema
  validator, the rubric-pin gate, and the voice lint.

## Known limits

- The deltas section is empty for M07 by design (no prior month). M08
  is the first memo with a real deltas-vs-prior block.
- `voice_lint` is a banned-phrase list, not a model. It catches the
  obvious marketing/antithetical-reversal patterns and nothing else.
- `validate_schemas` validates the memo front-matter and scoring stubs
  against the two JSON schemas, but does not cross-check that every
  repo listed in the memo appears in `config/portfolio.yaml` — that
  cross-check lives in `enforce_counts`.
- The portfolio file is the canonical source; there is no auto-sync
  from a GitHub org list. Adding/removing a repo is a manual PR.
- Scoring is hand-filled. The CLI emits stubs and renders the memo;
  it does not assign scores.

## Next feature queue

- 2026-M08 memo: first real deltas-vs-prior section against M07.
- `scripts/voice_lint.py` v0.2: pluggable rules file instead of a
  hard-coded banned-phrase list.
- `scripts/render_memo.py`: emit a machine-readable
  `repo_triage/YYYY-MNN.json` sibling alongside the markdown for the
  CDCP control-plane consumer.
- `config/portfolio.yaml`: add a per-repo `archived_at` field so
  RETIRE moves can write back to the canonical portfolio file rather
  than only being recorded in the memo.
- A `repo-triage diff` CLI subcommand that prints the ATTEND/RETIRE/FREEZE
  delta between two memo files (used to generate the deltas section
  semi-automatically from M08 onward).
- A `repo-triage ledger-append` subcommand that writes the
  `data/ledger/runs.jsonl` row automatically as part of `render-memo`,
  instead of by hand.

- Resolve factory defect: missing PRODUCT_BRIEF.md,SYSTEM_MAP.md
- Resolve factory defect: missing data/ledger/*.jsonl
- Resolve factory defect: METHODOLOGY.md missing revisit section
- Resolve factory defect: PRODUCT_BRIEF.md is required for active repos
- Resolve factory defect: SYSTEM_MAP.md is required for active repos
- Resolve factory defect: expected file 'PRODUCT_BRIEF.md' is missing
- Resolve factory defect: expected file 'SYSTEM_MAP.md' is missing
- Resolve factory defect: expected file 'specs/0002-design/requirements.md' is missing
- Resolve factory defect: expected file 'specs/0002-design/design.md' is missing
- Resolve factory defect: expected file 'specs/0002-design/tasks.md' is missing
- Resolve factory defect: expected file 'specs/0002-design/acceptance.md' is missing
- Resolve factory defect: expected file 'repo_triage/cli.py' is missing
- Resolve factory defect: expected file 'repo_triage/score.py' is missing
- Resolve factory defect: expected file 'repo_triage/ledger.py' is missing
- Resolve factory defect: expected glob 'data/ledger/*.jsonl' matched no files
- Resolve factory defect: expected glob 'decisions/DEC-*.md' matched no files
- Resolve factory defect: module 'cli' declares source 'repo_triage/cli.py', but it is missing
- Resolve factory defect: module 'score' declares source 'repo_triage/score.py', but it is missing
- Resolve factory defect: module 'ledger' declares source 'repo_triage/ledger.py', but it is missing
- Resolve factory defect: module 'report' declares source 'repo_triage/report.py', but it is missing
- Resolve factory defect: claude_code review requested patch; inspect defect log
