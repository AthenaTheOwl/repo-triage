# Spec 0001 — Tasks (Repo Triage)

First PR (the scaffold — this commit):

- [x] R-RTG-001 scaffold: README + LICENSE + AGENTS.md + .gitignore
- [x] R-RTG-001 specs/0001-foundation/{requirements,design,tasks,acceptance}.md
- [x] R-RTG-001 docs/first-pr.md

Second + third PRs (collapsed into v0.1; see `specs/0002-rubric-and-first-memo/`):

- [x] R-RTG-002 `rules/v0.md` — 5-factor rubric, 0-3 bands, definitions
- [x] R-RTG-011 `config/portfolio.yaml` — list of active portfolio repos
- [x] R-RTG-003 `schemas/scoring.schema.json`
- [x] R-RTG-006 `scripts/score_template.py` emits stubs
- [x] tests for the template emitter
- [x] First hand-scored pass: `scoring/2026-M07/<repo>.md` for all 20 repos
- [x] R-RTG-004 `schemas/memo.schema.json`
- [x] R-RTG-007 `scripts/render_memo.py`
- [x] R-RTG-005 `scripts/enforce_counts.py`
- [x] `scripts/rubric_pinned.py`
- [x] `scripts/voice_lint.py`
- [x] `scripts/validate_schemas.py`
- [x] R-RTG-008 first memo `repo_triage/2026-M07.md` with deltas section
      (empty for M07 by design; full from M08)
- [x] CI workflow running all four gates
- [x] R-RTG-009 archival rationale inline in the first memo's RETIRE
      entries

Fourth PR (deltas working from M08 onward):

- [ ] `scoring/2026-M08/` hand-filled
- [ ] `repo_triage/2026-M08.md` with real deltas-vs-M07 section
