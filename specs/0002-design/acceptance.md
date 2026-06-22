# Spec 0002 — Acceptance

v0.1 is done when:

```bash
python -m uv sync
python -m uv run pytest -v
python -m uv run repo-triage score-template \
    --portfolio config/portfolio.yaml \
    --rubric rules/v0.md \
    --month 2026-07 \
    --out scratch/scoring-test/
python -m uv run repo-triage render-memo \
    --scoring scoring/2026-M07/ \
    --portfolio config/portfolio.yaml \
    --rubric rules/v0.md \
    --month 2026-07 \
    --out scratch/2026-M07.md
python -m uv run repo-triage enforce-counts repo_triage/2026-M07.md \
    --portfolio config/portfolio.yaml
python -m uv run repo-triage validate-schemas repo_triage/2026-M07.md \
    --memo-schema schemas/memo.schema.json \
    --scoring-schema schemas/scoring.schema.json \
    --scoring-dir scoring/2026-M07/
python -m uv run repo-triage rubric-pinned repo_triage/2026-M07.md \
    --rubric rules/v0.md
python -m uv run repo-triage voice-lint repo_triage/2026-M07.md
```

And:

- `pytest` exits 0
- `score-template` writes 20 stubs into `scratch/scoring-test/`, one
  per portfolio repo
- The checked-in `repo_triage/2026-M07.md`:
  - pins `rubric_version: v0`
  - has exactly 2 ATTEND, exactly 3 RETIRE, and 15 FREEZE
  - has an empty deltas section (no prior memo)
  - passes all four gates above
- The checked-in `scoring/2026-M07/<slug>.md` files validate against
  `schemas/scoring.schema.json` (integer 0–3 scores, no nulls, all
  five factors present)
- `STATUS.md` has H2 sections `## Current state`, `## Known limits`,
  `## Next feature queue`
- `PRODUCT_BRIEF.md` and `SYSTEM_MAP.md` exist at the repo root
- `docs/METHODOLOGY.md` exists and has a `## What revisits this` H2
  section
- `data/ledger/runs.jsonl` contains a single JSON row for `month:
  2026-07` recording the rubric version, bucket assignments, and
  per-repo composite scores
- `decisions/DEC-0001-bundled-v0.1-release.md` exists and explains
  why v0.1 collapses three planned PRs into one
- `.github/workflows/ci.yml` runs the same gate sequence as above on
  every push and PR
