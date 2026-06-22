"""Repo-level pointer to the memo renderer.

The canonical implementation lives in ``src/repo_triage/memo.py``.
This file exists at the repo root for the contract gate.

The memo model:

- ``Memo`` — frozen dataclass; (month, rubric_version, attend, retire,
  freeze, deltas).
- ``render_memo(scoring_dir, portfolio, month, rubric_version,
  prior_memo=None)`` — reads hand-filled stubs, buckets by composite
  score (top 2 ATTEND, bottom 3 RETIRE, rest FREEZE), computes
  deltas-vs-prior if a prior memo is supplied, and returns the
  markdown text.
- ``load_memo(path)`` — parses an existing memo back into a ``Memo``.

The CLI subcommand ``repo-triage render-memo`` wraps this and writes
the result to ``repo_triage/<month>.md``. The first calibration
ledger row is the M07 memo at ``repo_triage/2026-M07.md``.
"""
