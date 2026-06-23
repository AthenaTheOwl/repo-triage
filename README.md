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

v0.1. Rubric, CLI, gates, and the first calibration ledger row
(`repo_triage/2026-M07.md`) are all checked in. Live state lives in
`STATUS.md`.

- [x] Repo scaffold + LICENSE + AGENTS.md
- [x] Spec 0001 (foundation) — requirements, design, tasks, acceptance
- [x] First-PR plan in `docs/first-pr.md`
- [x] Rubric `rules/v0.md` checked in
- [x] First hand-scored pass of all 20 repos (`scoring/2026-M07/`)
- [x] First monthly memo `repo_triage/2026-M07.md`
- [x] Four gates: `enforce_counts`, `validate_schemas`, `rubric_pinned`, `voice_lint`
- [x] CI workflow running all gates on every PR

## How to run

```bash
python -m uv sync

# day 1 of the month — emit one hand-fill stub per portfolio repo
python -m uv run repo-triage score-template \
    --portfolio config/portfolio.yaml \
    --rubric rules/v0.md \
    --month 2026-07 \
    --out scoring/2026-M07/

# days 2-4 — the operator fills in each stub by hand

# day 5 — render the memo and run the four gates
python -m uv run repo-triage render-memo \
    --scoring scoring/2026-M07/ \
    --portfolio config/portfolio.yaml \
    --rubric rules/v0.md \
    --month 2026-07 \
    --out repo_triage/2026-M07.md

python -m uv run repo-triage enforce-counts repo_triage/2026-M07.md --portfolio config/portfolio.yaml
python -m uv run repo-triage validate-schemas repo_triage/2026-M07.md --memo-schema schemas/memo.schema.json --scoring-schema schemas/scoring.schema.json --scoring-dir scoring/2026-M07/
python -m uv run repo-triage rubric-pinned repo_triage/2026-M07.md --rubric rules/v0.md
python -m uv run repo-triage voice-lint repo_triage/2026-M07.md
```

See `docs/methodology.md` for why the discipline looks this way, and
`docs/system-map.md` for the file-level orientation.

## try it

No arguments. Reads the committed memo (`repo_triage/2026-M07.md`) and
its scoring stubs, then prints every portfolio repo ranked by composite
score with its forced bucket:

```bash
python -m uv run repo-triage show
```

```
repo triage - 2026-07  (rubric v0)
ranked by composite thesis-alive score (0-15); attention is forced:
  2 ATTEND  /  3 RETIRE  /  rest FREEZE

  rank  score  bucket   repo
     1  15/15  ATTEND   grid-silicon
     2  14/15  ATTEND   dream-replay-cli
     3  12/15  FREEZE   cdcp-control-plane
    ...
    20   0/15  RETIRE   quux-prototype

this month's shipping attention: grid-silicon, dream-replay-cli
```

The ranked list is the point: it shows where next month's shipping
attention goes and which repos the rubric forces you to archive, rather
than letting the loudest repo win.

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

Shipped in v0.1:

```
  STATUS.md
  pyproject.toml
  src/repo_triage/                   # the Python package
    __init__.py
    portfolio.py
    rubric.py
    scoring.py
    memo.py
    cli.py
    __main__.py
  rules/
    v0.md                            # the 5-factor rubric
  config/
    portfolio.yaml                   # 20 active portfolio repos
  schemas/
    scoring.schema.json
    memo.schema.json
  scoring/
    2026-M07/<repo>.md               # one hand-filled stub per repo
  repo_triage/
    2026-M07.md                      # first monthly memo
  scripts/                           # thin shims over the CLI
    score_template.py
    render_memo.py
    enforce_counts.py
    validate_schemas.py
    rubric_pinned.py
    voice_lint.py
  tests/
  docs/
    methodology.md
    system-map.md
  .github/workflows/ci.yml
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
