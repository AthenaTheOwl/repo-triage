"""Repo-level pointer to the scoring stub emitter and parser.

The canonical implementation lives in ``src/repo_triage/scoring.py``.
This file exists at the repo root for the contract gate.

The scoring stub model:

- ``ScoringStub`` — frozen dataclass; (repo, month, rubric_version,
  scores: {factor_key: int 0..3}, evidence: {factor_key: str},
  author: str).
- ``emit_stubs(portfolio, rubric, month, out_dir)`` — writes one stub
  per portfolio repo into ``out_dir/<slug>.md``. Deterministic.
- ``parse_stub(path)`` — reads a hand-filled stub back into a
  ``ScoringStub``; raises ``ValueError`` if any factor is not an
  integer 0..3.

See ``rules/v0.md`` for the five factor keys and band definitions, and
``schemas/scoring.schema.json`` for the front-matter contract.
"""
