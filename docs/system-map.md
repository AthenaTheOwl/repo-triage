# System map — Monthly Repo Triage

This is the read-once orientation for someone who has just cloned the
repo and needs to know what file does what.

## Data flow

```
config/portfolio.yaml   ──┐
                          │
rules/v0.md ──────────────┼─► repo-triage score-template ──► scoring/YYYY-MNN/<slug>.md
                          │                                       │
                          │                                       ▼
                          │                                  (hand-filled)
                          │                                       │
                          ├──────────────────────────────────────┘
                          │
                          ▼
                    repo-triage render-memo ──► repo_triage/YYYY-MNN.md
                                                       │
                                                       ▼
                                          ┌────────────┴────────────┐
                                          │                         │
                                  enforce_counts            validate_schemas
                                  rubric_pinned             voice_lint
                                          │                         │
                                          └────────────┬────────────┘
                                                       │
                                                       ▼
                                                   merged
                                                       │
                                                       ▼
                                       ATTEND list drives next-month attention
                                       RETIRE list drives portfolio archival
```

## Module map

```
src/repo_triage/
  portfolio.py   Load config/portfolio.yaml into a Portfolio model.
  rubric.py      Load rules/v<N>.md, extract version and factor keys.
  scoring.py     Emit and parse per-repo scoring stubs.
  memo.py        Render the monthly memo from a stub directory.
  cli.py         Click CLI entrypoints (the `repo-triage` script).

scripts/
  score_template.py     Thin shim around `repo-triage score-template`.
  render_memo.py        Thin shim around `repo-triage render-memo`.
  enforce_counts.py     Gate: 2-ATTEND / 3-RETIRE / rest-FREEZE.
  validate_schemas.py   Gate: memo + scoring stub JSON-schema validation.
  rubric_pinned.py      Gate: memo pins an existing rubric version.
  voice_lint.py         Gate: banned marketing/antithetical-reversal phrases.

schemas/
  scoring.schema.json   JSON schema for a scoring stub front-matter block.
  memo.schema.json      JSON schema for a memo front-matter block.

rules/
  v0.md                 The hand-scorable 5-factor rubric.

config/
  portfolio.yaml        The 20 active portfolio repos this memo scores.

scoring/
  YYYY-MNN/<slug>.md    One hand-filled stub per repo per month.

repo_triage/
  YYYY-MNN.md           The monthly memo. The artifact.

specs/
  0001-foundation/      Scaffold spec ledger.
  0002-rubric-and-first-memo/   This v0.1 spec ledger.

docs/
  methodology.md        Why the discipline looks the way it does.
  system-map.md         This file.
  first-pr.md           The original scaffold-to-v0.1 changeset.

STATUS.md               Three-section state file consumed by the factory.
```

## Where the four gates run

- Locally, via the `scripts/*.py` shims, before commit.
- In CI, via `.github/workflows/ci.yml` on every PR that touches
  `repo_triage/`, `scoring/`, `rules/`, `config/`, or the `src/` tree.

## What the CLI is not

The CLI does not assign scores. It emits empty stubs (with the 0-3
placeholders) and assembles a memo from hand-filled stubs. The operator
is the model. The CLI is the scaffolding.
