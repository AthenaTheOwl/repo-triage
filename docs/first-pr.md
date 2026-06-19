# First PR after the scaffold

This file describes the literal next PR after the v0 scaffold lands.
Spec 0002 is the work plan; this file is the file-level changeset.

## Goal

A hand-scorable rubric plus a script that emits one scoring stub per
active portfolio repo for a given month. The author then fills in the
stubs by hand during the first week of the month.

No memo is rendered yet; that lands in spec 0003. The point of this
PR is to lock in the rubric and the per-repo scoring shape before any
forcing-function output gets written.

## Files changed

New:

- `pyproject.toml` — Python 3.11, `uv`, `pyyaml`, `pydantic`,
  `jsonschema`, `click`
- `rules/v0.md` — the 5-factor rubric, definitions, 0-3 bands
- `config/portfolio.yaml` — initial list of active portfolio repos
  (cross-referenced against `user_repo_portfolio.md` in the user's
  memory)
- `schemas/scoring.schema.json`
- `scripts/score_template.py` — emits one stub per repo into
  `scoring/<month>/<repo>.md`
- `scoring/.gitkeep`
- `tests/fixtures/portfolio_min.yaml` — small fixture
- `tests/test_score_template.py`
- `tests/test_rubric_referenced.py` — asserts every factor in v0.md is
  referenced in the scoring schema

Modified:

- `README.md` — replace placeholder "How to run" with the real command
- `specs/0001-foundation/tasks.md` — check off spec-0002 rows
- `AGENTS.md` — point Gates section at real scripts

## Verification

```bash
uv sync
uv run pytest -v
uv run python scripts/score_template.py \
    --portfolio tests/fixtures/portfolio_min.yaml \
    --rubric rules/v0.md \
    --month 2026-07 \
    --out scratch/scoring-test/
ls scratch/scoring-test/   # one .md per repo in the fixture
```

## Out of scope for this PR

- `render_memo.py` (spec 0003)
- `enforce_counts.py` (spec 0003)
- `voice_lint.py` and the rest of the gate scripts (spec 0003)
- The first real memo `repo_triage/2026-M07.md` (spec 0003)
- A CI workflow (spec 0003)
