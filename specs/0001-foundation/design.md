# Spec 0001 — Design (Repo Triage)

## Monthly cadence

```
day 1 of month   ─► run score_template.py
                    ┌─────────────────────────────┐
                    │ scoring/YYYY-MNN/<repo>.md  │  (one stub per active repo)
                    └─────────────────────────────┘
day 2-4          ─► author fills stubs by hand
day 5            ─► run render_memo.py
                    ┌──────────────────────────┐
                    │ repo_triage/YYYY-MNN.md  │
                    └──────────────────────────┘
                          │
                          ▼
day 5 PR         ─► gates run: voice_lint, validate_schemas,
                    enforce_counts, rubric_pinned
day 5+           ─► merged; ATTEND list drives next month's shipping
```

## Rubric shape (rules/v0.md)

Five factors, each 0-3:

1. **Thesis still credible.** The why-it-matters statement in the
   repo's README would survive a five-minute hostile read today.
2. **Pull from outside.** At least one external signal in the last 30
   days (citation, issue, inbound, real user).
3. **Shippable next step.** A concrete next PR exists and is bounded
   to one to three weeks of work.
4. **Cost of freeze.** Freezing for a month does not foreclose a
   timely opportunity.
5. **Dependency in the portfolio.** Another repo in the portfolio
   depends on this one shipping a particular thing in the next 90
   days.

Composite = sum of the five. Top 2 by composite go ATTEND, bottom 3 go
RETIRE. Ties broken by author judgment with a written one-line
rationale.

## Module map

```
rules/
  v0.md                        # the rubric
config/
  portfolio.yaml               # active portfolio repos
scoring/
  YYYY-MNN/                    # one .md stub per repo, hand-filled
repo_triage/
  YYYY-MNN.md                  # the monthly memo
scripts/
  score_template.py            # emits stubs from config/portfolio.yaml
  render_memo.py               # builds the memo from the stub directory
  enforce_counts.py            # asserts 2/3/rest
  rubric_pinned.py             # asserts memo references existing rubric
schemas/
  scoring.schema.json
  memo.schema.json
```

## Memo shape

```markdown
---
month: 2026-07
rubric_version: v0
attend: [grid-silicon, dream-replay-cli]
retire: [foo-bar-old, baz-experiment, quux-prototype]
freeze: [<remaining active repos>]
---

# Repo Triage — 2026-M07

## ATTEND
- grid-silicon: <one paragraph why>
- dream-replay-cli: <one paragraph why>

## RETIRE
- foo-bar-old: <one paragraph why>
- baz-experiment: <one paragraph why>
- quux-prototype: <one paragraph why>

## FREEZE
- <one line per repo>

## Deltas vs 2026-M06
- promoted to ATTEND: dream-replay-cli (was FREEZE)
- moved to RETIRE: quux-prototype (was FREEZE)
- no movement: <remaining>
```

## Determinism

- `score_template.py` is deterministic given the same portfolio file
- `render_memo.py` is deterministic given the same stub directory
- The hand-filled scoring is not deterministic by design — a person's
  judgment is the input
