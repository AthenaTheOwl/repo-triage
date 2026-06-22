# Product brief — Monthly Repo Triage

## What this is

A control-plane repo that scores, calibrates, and audits the active
portfolio of side-project repos once a month. The output is a single
markdown memo (`repo_triage/YYYY-MNN.md`) that names exactly:

- **2 ATTEND** repos — next month's shipping attention goes here
- **3 RETIRE** repos — archived; revival requires a written rationale
- **rest FREEZE** — alive, no attention this month

Plus a deltas-vs-prior section, a rubric pin, and four merge gates.

## Who it is for

- **The portfolio operator** (the author) as primary consumer. The
  memo is the artifact a future-self reads in 90 days to remember why
  attention landed where it did.
- **Anyone running 10+ active side-projects** who needs a written-down
  attention allocator instead of a feed-driven one.
- **The CDCP control-plane work** as a downstream consumer of the
  typed memo. Future: a machine-readable JSON sibling.

## Why it exists

Portfolio attention drifts to whichever repo emitted the most recent
emotionally salient signal — a green CI, a kind reply, a new idea at
breakfast. The result is a portfolio where the loudest repo wins
attention, not the one that most needs it.

This memo replaces feed-driven allocation with a written rule. The
forcing function is that the counts (2, 3, all-else) are
non-negotiable.

## What ships in v0.1

- A hand-scorable 5-factor thesis-alive rubric (`rules/v0.md`)
- A Python CLI `repo-triage` with six subcommands
- Four merge gates (enforce-counts, validate-schemas, rubric-pinned,
  voice-lint), each runnable locally and in CI
- The first calibration ledger row: `scoring/2026-M07/` (20
  hand-filled stubs) and `repo_triage/2026-M07.md` (the rendered memo)
- A machine-readable ledger entry at `data/ledger/runs.jsonl`

## What it is not

- Not a per-repo dashboard. No cards, no charts, no live feeds.
- Not LLM-judged. The rubric is hand-scorable; an LLM may help draft
  rationale paragraphs, but it does not assign the 0–3.
- Not a roadmap. ATTEND tells you which repo gets next month's
  shipping time, not what to ship.
- Not a graveyard catalogue. RETIRE is real archival with a written
  rationale, not "we might come back to it."

## Cadence

Monthly. Weekly is noise. Quarterly is too long to walk back a wrong
RETIRE.

## Success criteria for v0.1

1. The first memo (`repo_triage/2026-M07.md`) passes all four gates on
   CI without manual intervention.
2. The memo is readable cold by someone with no prior context — the
   rubric pin, the bucket lists, and the rationale lines stand alone.
3. The next factory run can pick up the "Next feature queue" in
   `STATUS.md` without further briefing.

## What revisits this

The brief is reread at the top of each monthly run. If after three
memos the rubric factors no longer match the operator's later judgment
of whether attention paid off, the rubric is bumped to `rules/v1.md`
and this brief gets a "v0.2" section explaining why.
