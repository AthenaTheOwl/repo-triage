# Spec 0002 — Design

## Why one PR instead of three

The original spec 0001 staged this as three PRs: (a) rubric + scoring
template, (b) memo renderer + gates, (c) first memo. Shipping (a)
alone would have locked in the rubric file shape without a falsifiable
referent — there would be no memo against which to check whether the
factor keys, the band definitions, or the schema cardinalities held
up. So v0.1 ships all three at once and uses the first memo to
pressure test the design. The rationale is also recorded as a formal
decision record in ``decisions/DEC-0001-bundled-v0.1-release.md``.

## Module layout

```
src/repo_triage/
  portfolio.py    Portfolio loader. Dataclass model; YAML parse.
  rubric.py       Rubric loader. Front-matter regex + factor-key regex.
  scoring.py      ScoringStub dataclass; emit_stubs; parse_stub.
  memo.py         Memo dataclass; render_memo; load_memo; _bucket; _compute_deltas.
  cli.py          Click group with six subcommands. All gates are
                  subcommands of the same CLI; the scripts/ shims just
                  re-export them so the operator can invoke them as
                  bare scripts too.
```

A second copy of the entry-point filenames lives at the repo root
under ``repo_triage/`` (``cli.py``, ``score.py``, ``ledger.py``,
``report.py``). These are documentation shims — they do not contain
business logic. They exist because:

1. The factory contract gate expects those filenames at the repo
   root.
2. The ``repo_triage/`` directory is also where the monthly memo
   files (``YYYY-MNN.md``) live, so a tree-down reader looking for the
   CLI entry point lands on the shim instead of "no python file here."

The scripts/ directory is intentionally thin. The CLI is the
canonical entry point; the scripts/ files exist because the original
spec 0001 referred to them by path and changing those references
would have been churn. Each script is a 3-line import + invoke of the
matching CLI subcommand.

## Bucketing algorithm

```
ranked = sorted(stubs, key=lambda s: (-s.composite, s.repo))
attend = ranked[:2]
retire = ranked[-3:]
middle = ranked[2:-3]
freeze = sorted(middle by slug)
```

Ties broken by slug for determinism. The operator is expected to
hand-edit the rendered memo to override the tie-break when they have
a real preference; the override lives in the memo body as a
one-sentence rationale. The bucket lists in the front-matter are the
source of truth for the gates.

## Deltas computation

The renderer takes an optional ``--prior`` memo path. If supplied:

- Walk the new ATTEND list; if a slug was not in the prior ATTEND,
  emit ``promoted to ATTEND: <slug> (was <prior bucket>)``.
- Walk the new RETIRE list; same idea for moves into RETIRE.
- Walk the new FREEZE list; if a slug was in the prior ATTEND, emit
  ``dropped from ATTEND to FREEZE: <slug>``.

For M07 there is no prior memo, so the deltas list is empty and the
memo body reads ``(no prior memo)``. M08 will be the first memo with
a real deltas-vs-prior section.

## Gate matrix

| Gate            | Reads                                      | Asserts                                                            |
|-----------------|--------------------------------------------|--------------------------------------------------------------------|
| enforce_counts  | memo front-matter, portfolio.yaml          | ATTEND=2, RETIRE=3, union==portfolio, no overlap                   |
| validate_schemas| memo front-matter (+ optional stubs)       | front-matter matches JSON schema                                   |
| rubric_pinned   | memo front-matter, rules/v<N>.md           | memo rubric_version == rubric on disk                              |
| voice_lint      | memo body                                  | no banned phrase substring present                                 |

Every gate is a CLI subcommand of the same ``repo-triage`` binary so
that the CI workflow is a flat list of ``python -m repo_triage ...``
invocations rather than a mix of subprocess shapes.

## Ledger row

After ``render-memo`` succeeds, a JSON object is appended to
``data/ledger/runs.jsonl``. Schema:

```
{
  "month":            "YYYY-MM",
  "rubric_version":   "v<N>",
  "attend":           ["slug", ...],   // length 2
  "retire":           ["slug", ...],   // length 3
  "freeze":           ["slug", ...],   // length len(portfolio) - 5
  "composite_scores": {"slug": int, ...},
  "memo_path":        "repo_triage/<month>.md",
  "prior_month":      "YYYY-MM" | null,
  "generated_at":     "<ISO 8601 UTC>"
}
```

The markdown memo remains the human artifact; the JSONL row is the
machine-readable consumer surface for the CDCP control-plane work.

## What is not in v0.1

- A ``repo-triage diff`` subcommand that prints the bucketing delta
  between two memos. Listed in ``STATUS.md`` under Next feature
  queue; M08 is when this starts paying off.
- A pluggable voice_lint rules file. The current implementation is a
  hard-coded list inside ``cli.py``. Replacing it with a YAML file is
  also in Next feature queue.
- A ``repo-triage ledger-append`` CLI subcommand. The JSONL row is
  written by hand at memo render time in v0.1; automating it lands in
  v0.2.

## Determinism

- ``emit_stubs`` writes stubs in portfolio order; each stub's contents
  depend only on ``(slug, month, rubric.version)``.
- ``render_memo`` is deterministic given the same stub directory; the
  bucketing is sorted by ``(-composite, slug)``; the YAML
  front-matter is dumped with ``sort_keys=False`` so the ordering is
  the one the renderer chose, not alphabetical.
- The hand-filled scoring is not deterministic — a person's judgment
  is the input by design.
