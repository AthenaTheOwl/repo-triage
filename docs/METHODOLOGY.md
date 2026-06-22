# Methodology — Monthly Repo Triage

This document is the written-down version of how the monthly memo is
produced. It exists so the operator (and any future replacement) can
reconstruct the discipline a year from now, when the rubric will have
been revised at least once and the muscle memory is gone.

## Why hand-scoring

The five-factor rubric is hand-scorable on purpose. An LLM can read
twenty READMEs and emit a number; the operator cannot reliably tell
whether the LLM was credibly engaging with the thesis or
pattern-matching on tone. The forcing function is the operator reading
the repo, not the LLM emitting a score. The author signature in every
scoring stub is a deliberate friction point: the operator's name on
the line where the score sits, so the score belongs to a person.

## Why monthly

Weekly is noise. The signals the rubric captures (thesis credibility,
inbound pull, shippable next step) move on a multi-week timescale. A
weekly memo would either repeat itself or reward whichever repo had
the loudest recent week, which is the failure mode this memo exists to
fix.

Quarterly was the alternative. It was rejected because a quarter is
too long to walk back a wrong RETIRE — three months of inattention is
enough for a repo to lose context that took weeks to build. Monthly is
the shortest cadence that does not generate noise.

## Why the exact counts (2, 3, rest)

The forcing function does not work if the counts are negotiable. If
the operator can decide on the day whether to ATTEND 3 or RETIRE 2,
the allocation reverts to whichever repo emitted the loudest recent
signal and the discipline is gone.

The specific numbers are:

- **2 ATTEND** — the operator can credibly carry shipping attention on
  two repos in a month. Three is a lie; one collapses to the loudest
  signal.
- **3 RETIRE** — the portfolio drifts upward over time. If retirements
  are a slower trickle than additions, the portfolio becomes
  unmanageable. Three per month keeps the rate honest.
- **The rest FREEZE** — a repo in FREEZE is alive. The thesis still
  holds. It just does not get attention this month. FREEZE is not
  failure.

## Scoring procedure

1. On day 1 of the month, run `repo-triage score-template` to emit a
   stub per portfolio repo into `scoring/YYYY-MNN/`.
2. Days 2–4, sit with each repo. Read the README. Look at issues.
   Check inbound signals. Write the 0–3 for each factor and one line
   of evidence. Sign the stub.
3. Day 5, run `repo-triage render-memo`. The renderer buckets by
   composite score (top 2 / bottom 3 / rest) and writes the memo.
4. The operator reads the rendered memo. If a tie-break feels wrong,
   the operator manually edits the memo and writes a one-line
   rationale in the relevant bucket section. The hand-edit is final;
   the automated bucketing is a default, not a verdict.
5. Run the four gates: `enforce_counts`, `validate_schemas`,
   `rubric_pinned`, `voice_lint`. Any failure blocks merge.
6. Append a row to `data/ledger/runs.jsonl` recording the scored
   month, rubric version, bucket assignments, and composite scores.
7. Merge. The ATTEND list drives the next month's shipping attention.

## Tie-break policy

The renderer breaks composite ties by slug for determinism. The
operator is expected to override this whenever they have a real
preference. The override lives in the memo body — a one-sentence
rationale in the ATTEND/RETIRE bullet for the affected repo. The
override does not mutate the scoring stubs; the stubs remain the
historical record of the score, and the memo records the human
decision.

## When the rubric is wrong

A factor stops being useful when (a) every repo scores 3 on it or (b)
the score does not correlate with the operator's later judgment of
whether attention paid off. Rubric revisions are a new file
`rules/v<N+1>.md` with a written changelog at the top. Past memos
remain pinned to the rubric version they were scored against; the
gates enforce this.

## Archival rule

A repo placed in RETIRE is archived: its GitHub repo is set to
archived, and the entry in `config/portfolio.yaml` is removed in a
follow-up PR. Revival requires a new written rationale in a subsequent
memo, citing what changed. This is to prevent silently un-retiring a
repo and reverting the discipline.

## Out of scope

- A live dashboard. The memo is the artifact. Dashboards become weekly
  noise; this work is monthly by design.
- LLM-assigned scores. An LLM may draft a rationale paragraph; the
  0–3 comes from a person reading the repo.
- Per-repo metrics (stars, commits, contributor count). These were
  considered and rejected — they reward activity, not thesis health.

## What revisits this

This methodology is reread at the top of each monthly run. Two
trigger conditions force a revision:

1. **After every third memo**, the operator runs a retrospective:
   did the prior ATTEND repos actually receive shipping attention? Did
   any RETIRE call need walking back? If either answer is "no" twice
   in a row, the rubric or the counts get revisited and this file gets
   the rationale.
2. **When a rubric bump lands** (`rules/v0.md` → `rules/v1.md`), this
   document gets a corresponding `## Rubric history` entry explaining
   what changed and which memo first used the new rubric.

The deltas-vs-prior section of each memo is the running audit trail
that feeds this revisit step. The `data/ledger/runs.jsonl` file is
the machine-readable companion: it lets the retrospective query "what
was the composite score for repo X across the last three memos"
without re-parsing markdown.
