# Spec 0001 — Tasks (Repo Triage)

First PR (the scaffold — this commit):

- [x] R-RTG-001 scaffold: README + LICENSE + AGENTS.md + .gitignore
- [x] R-RTG-001 specs/0001-foundation/{requirements,design,tasks,acceptance}.md
- [x] R-RTG-001 docs/first-pr.md

Second PR (rubric + scoring template):

- [ ] R-RTG-002 `rules/v0.md` — 5-factor rubric, 0-3 bands, definitions
- [ ] R-RTG-011 `config/portfolio.yaml` — list of active portfolio repos
- [ ] R-RTG-003 `schemas/scoring.schema.json`
- [ ] R-RTG-006 `scripts/score_template.py` emits stubs
- [ ] tests for the template emitter

Third PR (first memo + count enforcement):

- [ ] First hand-scored pass: `scoring/2026-M07/<repo>.md` for all 20 repos
- [ ] R-RTG-004 `schemas/memo.schema.json`
- [ ] R-RTG-007 `scripts/render_memo.py`
- [ ] R-RTG-005 `scripts/enforce_counts.py`
- [ ] `scripts/rubric_pinned.py`
- [ ] `scripts/voice_lint.py`
- [ ] `scripts/validate_schemas.py`
- [ ] R-RTG-008 first memo `repo_triage/2026-M07.md` with deltas section
      (deltas-vs-prior empty for the first memo; full from M08)
- [ ] CI workflow running all four gates
- [ ] R-RTG-009 archival rationale linked from the first memo's
      RETIRE entries

Fourth PR (deltas working from M08 onward):

- [ ] `scoring/2026-M08/` hand-filled
- [ ] `repo_triage/2026-M08.md` with real deltas-vs-M07 section
