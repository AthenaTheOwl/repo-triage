"""Machine-readable ledger of monthly scoring runs.

Each monthly memo also writes a single JSON object to
``data/ledger/runs.jsonl``. The markdown memo at
``repo_triage/<month>.md`` is the human artifact; the JSONL row is
what the downstream CDCP control-plane consumer reads.

Row schema (one JSON object per line):

    {
      "month": "2026-07",
      "rubric_version": "v0",
      "attend": ["grid-silicon", "dream-replay-cli"],
      "retire": ["baz-experiment", "foo-bar-old", "quux-prototype"],
      "freeze": ["cdcp-control-plane", ...],
      "composite_scores": {"grid-silicon": 15, ...},
      "memo_path": "repo_triage/2026-M07.md",
      "generated_at": "2026-06-22T00:00:00Z"
    }

This file is the documented entry point for that schema; the writer
implementation will live in ``src/repo_triage/`` when the
``repo-triage ledger-append`` subcommand lands. Until then,
``data/ledger/runs.jsonl`` is updated by hand at memo render time.
"""
