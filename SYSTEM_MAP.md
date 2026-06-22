# System map — Monthly Repo Triage

Read-once orientation for someone who has just cloned the repo and
needs to know what file does what.

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
                                                  data/ledger/runs.jsonl
                                                       │
                                                       ▼
                                       ATTEND list drives next-month attention
                                       RETIRE list drives portfolio archival
```

## Top-level layout

```
PRODUCT_BRIEF.md            What this is, who it is for, why it exists.
SYSTEM_MAP.md               This file.
STATUS.md                   Three-section state file consumed by the factory.
AGENTS.md                   Operating contract for AI agents working in this repo.
README.md                   Quickstart.
LICENSE                     MIT.
pyproject.toml              Package + dev deps under [dependency-groups]; [tool.uv] package = true.

specs/0001-foundation/      Scaffold spec ledger (original PRs A/B/C).
specs/0002-design/          v0.1 spec ledger — rubric, CLI, gates, first memo.
decisions/DEC-*.md          Architectural decision records.

src/repo_triage/            The installable Python package.
repo_triage/                Re-export shims + the monthly memo files (YYYY-MNN.md).
scripts/                    Thin shims over the CLI; one per gate.
tests/                      Pytest suite — package and gates.

rules/v0.md                 The hand-scorable 5-factor rubric.
config/portfolio.yaml       The 20 active portfolio repos this memo scores.
schemas/                    JSON schemas for scoring stubs and memos.
scoring/YYYY-MNN/           One hand-filled stub per repo per month.
data/ledger/runs.jsonl      Machine-readable record of each scoring run.

docs/METHODOLOGY.md         Why the discipline looks the way it does.
docs/methodology.md         Long-form companion to METHODOLOGY.md (historical).
docs/system-map.md          Long-form companion to SYSTEM_MAP.md (historical).
docs/first-pr.md            The original scaffold-to-v0.1 changeset.

.github/workflows/ci.yml    Runs `uv sync`, pytest, and the four gates.
```

## Module map (src/repo_triage)

```
src/repo_triage/
  portfolio.py   Load config/portfolio.yaml into a Portfolio model.
  rubric.py      Load rules/v<N>.md, extract version and factor keys.
  scoring.py     Emit and parse per-repo scoring stubs.
  memo.py        Render the monthly memo from a stub directory.
  cli.py         Click CLI entrypoints (the `repo-triage` script).
  __main__.py    `python -m repo_triage` entrypoint.
```

## Where the four gates run

- Locally, via the `scripts/*.py` shims, before commit.
- In CI, via `.github/workflows/ci.yml` on every push and PR.

## Ledger

`data/ledger/runs.jsonl` is the machine-readable record of each
scoring run. One JSON object per line; fields: `month`,
`rubric_version`, `attend`, `retire`, `freeze`, `composite_scores`,
`generated_at`. The markdown memo at `repo_triage/<month>.md` remains
the human artifact; the JSONL row is what the downstream CDCP
control-plane consumer reads.

## What the CLI is not

The CLI does not assign scores. It emits empty stubs (with 0–3
placeholders) and assembles a memo from hand-filled stubs. The operator
is the model. The CLI is the scaffolding.
