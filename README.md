# Monthly Repo Triage

A single-file monthly memo across the ~20 active repos in the
portfolio. Each month forces a top-2 ATTEND list, a bottom-3 RETIRE
list, and a FREEZE list. No per-repo dashboard cards. No weekly
noise. The memo is the artifact; the discipline is the forcing
function.

## What this is

Portfolio attention drifts to whichever repo emitted the most recent
emotionally salient signal (a green CI, a kind reply, a new idea at
breakfast). The result is a portfolio where the loudest repo wins
attention, not the one that most needs it.

This repo replaces that with a written rule:

- Every month, every active repo is scored against a 5-factor
  thesis-alive rubric
- The top 2 by composite score get ATTEND (the next month's shipping
  attention goes here)
- The bottom 3 get RETIRE (archived; revived only on a new written
  rationale)
- Everything else gets FREEZE (still alive, no attention this month)

The rubric is not LLM vibes. It is a hand-scorable checklist a person
fills in once per repo per month. The forcing function is that the
counts (2, 3, all-else) are non-negotiable.

## Status

v0 scaffold. No memo published yet — only the spec ledger and the
rubric design below. First memo lands in spec 0002.

- [x] Repo scaffold + LICENSE + AGENTS.md
- [x] Spec 0001 (foundation) — requirements, design, tasks, acceptance
- [x] First-PR plan in `docs/first-pr.md`
- [ ] Rubric `rules/v0.md` checked in
- [ ] First hand-scored pass of all 20 repos
- [ ] First monthly memo `repo_triage/2026-M07.md`

## How to run

Placeholder. Writing the first memo is a manual editorial pass against
the rubric in `rules/v0.md`. A small script `scripts/score_template.py`
will emit a per-repo scoring stub from the rubric. The runnable shape
lands in spec 0002.

```bash
# After spec 0002 lands:
python scripts/score_template.py --rubric rules/v0.md --out scratch/2026-M07-scoring/
# fill in the stubs by hand, then:
python scripts/render_memo.py --scoring scratch/2026-M07-scoring/ --out repo_triage/2026-M07.md
```

Until spec 0002 lands, this is a scaffold.

## Layout

```
repo-triage/
  README.md
  LICENSE
  AGENTS.md
  .gitignore
  specs/
    0001-foundation/
      requirements.md
      design.md
      tasks.md
      acceptance.md
  docs/
    first-pr.md
```

Planned but not yet present:

```
  rules/
    v0.md                            # the 5-factor rubric
  repo_triage/
    2026-M07.md                      # first monthly memo
    2026-M08.md
  scoring/
    2026-M07/                        # per-repo hand-scored stubs
  scripts/
    score_template.py
    render_memo.py
    enforce_counts.py
  schemas/
    scoring.schema.json
    memo.schema.json
```

## Who this is for

- The portfolio operator (the author) as the primary consumer
- Anyone running 10+ active side-projects who needs a written-down
  attention allocator instead of a feed-driven one
- The CDCP control-plane work as a downstream consumer of the typed
  memo

## What this is not

- Not a per-repo dashboard. There are no cards, no charts, no live
  feeds. One file per month.
- Not LLM-judged. The rubric is hand-scorable. An LLM may help draft
  the rationale; it does not assign the score.
- Not a roadmap. ATTEND tells you which repo gets the next month's
  shipping time, not what to ship.
- Not a graveyard catalogue. RETIRE is real archival, with a written
  rationale, not "we might come back to it."

## License

MIT. See `LICENSE`.
