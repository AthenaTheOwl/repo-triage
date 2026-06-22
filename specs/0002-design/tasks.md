# Spec 0002 — Tasks

This PR (v0.1):

- [x] R-RTG-020 `pyproject.toml` with `[tool.uv] package = true` and `[dependency-groups]`
- [x] R-RTG-020 `src/repo_triage/{__init__,portfolio,rubric,scoring,memo,cli,__main__}.py`
- [x] R-RTG-021 `rules/v0.md`
- [x] R-RTG-022 `config/portfolio.yaml` with 20 active portfolio repos
- [x] R-RTG-023 `schemas/scoring.schema.json` + `schemas/memo.schema.json`
- [x] R-RTG-024 `repo-triage score-template` subcommand + `scripts/score_template.py` shim
- [x] R-RTG-025 `repo-triage render-memo` subcommand + `scripts/render_memo.py` shim
- [x] R-RTG-026 `repo-triage enforce-counts` subcommand + `scripts/enforce_counts.py` shim
- [x] R-RTG-027 `repo-triage validate-schemas` subcommand + `scripts/validate_schemas.py` shim
- [x] R-RTG-028 `repo-triage rubric-pinned` subcommand + `scripts/rubric_pinned.py` shim
- [x] R-RTG-029 `repo-triage voice-lint` subcommand + `scripts/voice_lint.py` shim
- [x] R-RTG-030 first calibration ledger row: `scoring/2026-M07/*.md` + `repo_triage/2026-M07.md` + `data/ledger/runs.jsonl`
- [x] R-RTG-031 `.github/workflows/ci.yml`
- [x] R-RTG-032 `docs/METHODOLOGY.md`, `SYSTEM_MAP.md`, and `PRODUCT_BRIEF.md`
- [x] R-RTG-033 `STATUS.md` with the three required H2 sections
- [x] R-RTG-034 `decisions/DEC-0001-bundled-v0.1-release.md`
- [x] root-level entry-point shims: `repo_triage/{cli,score,ledger,report}.py`
- [x] tests covering portfolio, rubric, scoring, memo, gates, and the CLI surface

Next PR (M08 deltas):

- [ ] `scoring/2026-M08/` hand-filled
- [ ] `repo_triage/2026-M08.md` rendered with `--prior repo_triage/2026-M07.md`
- [ ] First real deltas-vs-prior section
- [ ] Append the M08 row to `data/ledger/runs.jsonl`
- [ ] Lift the placeholder M08 entry in `STATUS.md` Next feature queue
