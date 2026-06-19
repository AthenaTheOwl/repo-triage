# Spec 0001 — Foundation (Repo Triage)

## R-RTG-001 — repo scaffold
Repo lives at `e:/claude_code/random-apps/repo-triage`. MIT license,
copyright Vignesh Gopalakrishnan. README, AGENTS.md, .gitignore, and
`specs/0001-foundation/` exist before any rubric or memo lands.

## R-RTG-002 — rubric file
`rules/v0.md` is the hand-scorable 5-factor thesis-alive rubric. Each
factor is named, defined, and given a 0-3 scoring band. The rubric is
versioned (`v0`, `v1`, ...) and every memo pins the version it scored
against.

## R-RTG-003 — scoring stub schema
`schemas/scoring.schema.json` defines the per-repo scoring stub: repo
slug, rubric version, per-factor score, per-factor one-line evidence,
composite score, author signature.

## R-RTG-004 — memo schema
`schemas/memo.schema.json` defines the monthly memo front-matter:
month, rubric version, ATTEND list (exactly 2), RETIRE list (exactly
3), FREEZE list (everything else), deltas vs prior month.

## R-RTG-005 — count enforcement
`scripts/enforce_counts.py` asserts every memo has exactly 2 ATTEND
items, exactly 3 RETIRE items, and that every active portfolio repo
appears in exactly one of ATTEND / RETIRE / FREEZE. Fails CI otherwise.

## R-RTG-006 — scoring template script
`scripts/score_template.py` emits one scoring stub per active portfolio
repo into `scoring/YYYY-MNN/<repo>.md`. The author then fills in the
stubs by hand.

## R-RTG-007 — memo renderer
`scripts/render_memo.py` reads a `scoring/YYYY-MNN/` directory, applies
the rubric, and writes `repo_triage/YYYY-MNN.md` with the front-matter
block plus the prose sections.

## R-RTG-008 — deltas vs prior month
Every memo (from M02 onward) contains a deltas section: which repos
moved between ATTEND / RETIRE / FREEZE since the prior month, and the
one-line reason.

## R-RTG-009 — RETIRE archival rule
A repo placed in RETIRE is moved to an `archived/` registry in the
portfolio manifest (separate repo). Revival requires a new written
rationale in a subsequent memo.

## R-RTG-010 — gates
Four gates run in CI and locally: `voice_lint`, `validate_schemas`,
`enforce_counts`, `rubric_pinned`. A memo that fails any gate is not
merged.

## R-RTG-011 — portfolio source of truth
`config/portfolio.yaml` is the canonical list of active portfolio
repos this memo scores against. Adding a repo to the portfolio = a
PR to this file plus a one-line rationale.
