# Spec 0002 — Rubric, CLI, gates, and the first memo

This spec collapses what spec 0001 sketched as three separate PRs
(rubric + scoring template, then memo renderer + gates, then first
memo) into one v0.1 release. The justification: until a first memo
actually exists, the rubric and the schemas have no falsifiable
referent, so shipping them in isolation invites premature lock-in.

## R-RTG-020 — Python package and CLI

A real Python package ``repo_triage`` lives under ``src/repo_triage/``
and is editable-installed via ``[tool.uv] package = true`` in
``pyproject.toml``. Dev deps (pytest, pytest-cov) live under
``[dependency-groups]`` so ``python -m uv sync`` installs them
without an explicit ``--extra`` flag. The CLI is registered as
``repo-triage = "repo_triage.cli:main"`` and is invocable as both
``repo-triage <subcommand>`` and ``python -m repo_triage <subcommand>``.

## R-RTG-021 — rubric file

``rules/v0.md`` defines the 5-factor thesis-alive rubric. Each factor
has a stable snake_case key (used in the schema and stub front-matter)
and 0–3 scoring bands with one-sentence definitions per band. The file
front-matter pins ``version: v0``.

## R-RTG-022 — portfolio file

``config/portfolio.yaml`` enumerates the 20 active portfolio repos as a
list of ``{slug, thesis}`` records. The loader rejects duplicate slugs
and slugs that do not match ``^[a-z0-9][a-z0-9-]*$``.

## R-RTG-023 — schemas

``schemas/scoring.schema.json`` validates a scoring stub front-matter
block. ``schemas/memo.schema.json`` validates a memo front-matter block.
Both schemas enforce: ISO month, ``v<N>`` rubric version pin,
filesystem-safe slugs, integer 0–3 scores, and exact ATTEND=2 /
RETIRE=3 cardinalities on the memo.

## R-RTG-024 — score-template subcommand

``repo-triage score-template --portfolio P --rubric R --month M --out O``
emits one stub per portfolio repo into ``O/``. The stub has a YAML
front-matter block matching ``scoring.schema.json`` (with ``null`` score
placeholders that the author fills in by hand) and a markdown body with
one section per factor.

## R-RTG-025 — render-memo subcommand

``repo-triage render-memo --scoring S --portfolio P --rubric R --month M
[--prior PRIOR] --out O`` reads hand-filled stubs from ``S/``, asserts
every portfolio repo has a stub and vice versa, asserts each stub pins
the same rubric version as the rubric on disk, then writes a memo to
``O`` with top-2 ATTEND, bottom-3 RETIRE, rest FREEZE, and a deltas
section computed against ``PRIOR`` if provided.

## R-RTG-026 — gate: enforce-counts

``repo-triage enforce-counts <memo> --portfolio P`` exits non-zero
unless the memo has exactly 2 ATTEND, exactly 3 RETIRE, and the union
of the three buckets equals the portfolio. Overlap between buckets is
also a failure.

## R-RTG-027 — gate: validate-schemas

``repo-triage validate-schemas <memo> --memo-schema M
[--scoring-schema S --scoring-dir D]`` validates the memo front-matter
against the memo schema, and (if provided) every stub in the scoring
directory against the scoring schema.

## R-RTG-028 — gate: rubric-pinned

``repo-triage rubric-pinned <memo> --rubric R`` exits non-zero unless
the rubric version in the memo's front-matter matches the version
extracted from the rubric file on disk.

## R-RTG-029 — gate: voice-lint

``repo-triage voice-lint <memo>`` exits non-zero if the memo body
contains any banned phrase from the in-CLI banned-phrase list. The
banned-phrase list captures the obvious marketing language and
antithetical-reversal patterns. Replacing the list with a pluggable
rules file is in the "Next feature queue" of ``STATUS.md``.

## R-RTG-030 — first calibration ledger row

``scoring/2026-M07/`` contains a hand-filled stub for each of the 20
portfolio repos, and ``repo_triage/2026-M07.md`` is the rendered memo.
The memo pins ``rubric_version: v0``, has 2 ATTEND, 3 RETIRE, 15
FREEZE, and passes all four gates. Its deltas section is empty because
M07 has no prior month. A machine-readable companion row is appended
to ``data/ledger/runs.jsonl``.

## R-RTG-031 — CI workflow

``.github/workflows/ci.yml`` runs ``python -m uv sync``, then
``pytest``, then the four gates against the checked-in 2026-M07 memo
on every push and PR.

## R-RTG-032 — methodology and system map

``docs/METHODOLOGY.md`` explains why the discipline looks the way it
does. ``SYSTEM_MAP.md`` at the repo root orients a reader to the file
layout and the data flow. ``PRODUCT_BRIEF.md`` at the repo root states
what this is, who it is for, and why it exists.

## R-RTG-033 — STATUS

``STATUS.md`` has the three required H2 sections (``Current state``,
``Known limits``, ``Next feature queue``) and accurately reflects what
v0.1 ships, what it does not, and what the next factory run should
pick up.

## R-RTG-034 — decisions ledger

``decisions/`` contains at least one ``DEC-*.md`` architectural
decision record for v0.1. The first record explains why v0.1 bundles
rubric + CLI + gates + first memo into one PR rather than the three
PRs originally sketched in spec 0001.
