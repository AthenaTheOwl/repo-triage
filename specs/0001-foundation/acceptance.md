# Spec 0001 — Acceptance (Repo Triage)

v0 (this scaffold PR) is done when:

- `README.md`, `LICENSE`, `AGENTS.md`, `.gitignore` exist
- `specs/0001-foundation/{requirements,design,tasks,acceptance}.md` exist
- `docs/first-pr.md` describes the second PR
- README status checkboxes show the scaffold rows checked
- No memo or rubric exists yet

Spec 0002 (rubric + scoring template) is done when:

```bash
python scripts/score_template.py \
    --portfolio config/portfolio.yaml \
    --rubric rules/v0.md \
    --month 2026-07 \
    --out scoring/2026-M07/
```

emits one schema-valid stub per active portfolio repo.

Spec 0003 (first memo) is done when:

```bash
# author has hand-filled scoring/2026-M07/
python scripts/render_memo.py \
    --scoring scoring/2026-M07/ \
    --out repo_triage/2026-M07.md
python scripts/voice_lint.py repo_triage/2026-M07.md
python scripts/validate_schemas.py repo_triage/2026-M07.md
python scripts/enforce_counts.py repo_triage/2026-M07.md
python scripts/rubric_pinned.py repo_triage/2026-M07.md
```

And:

- The memo has exactly 2 ATTEND, exactly 3 RETIRE, and every other
  active portfolio repo in FREEZE
- The memo front-matter pins `rubric_version: v0`
- The deltas section is present (empty for M07; full from M08)
- All gates pass

Gates: `voice_lint`, `validate_schemas`, `enforce_counts`,
`rubric_pinned`. A memo that fails any gate is not merged.
