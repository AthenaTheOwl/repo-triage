# DEC-0001 — Bundle rubric, CLI, gates, and first memo into v0.1

- **Status**: Accepted
- **Date**: 2026-06-22
- **Spec**: [0002-design](../specs/0002-design/requirements.md)

## Context

Spec 0001 sketched the v0 work as three sequential PRs:

1. PR A — `rules/v0.md` plus the scoring-stub template emitter.
2. PR B — the memo renderer plus the four merge gates.
3. PR C — the first hand-filled month and the rendered memo.

Each PR was supposed to be independently mergeable. The intent was
that PR A could be reviewed without committing to a specific
schema-cardinality or factor-key shape, then PR B would lock those in,
then PR C would calibrate.

## Problem

Reviewing PR A in isolation has no falsifiable referent. Without a
first memo on disk, there is no way to ask "does the factor key for
'cost of freezing' actually produce different rationales across 20
real repos, or does every repo land at 2?" The reviewer would either
(a) approve on vibes, or (b) ask for sample memos that the spec
defers to PR C. Either way, PR A would harden a rubric shape that may
not survive contact with the first real scoring pass.

The same critique applies to PR B: the gate cardinalities (ATTEND=2,
RETIRE=3) are testable only against a real memo. Mocked test memos
satisfy the gate, but they don't pressure-test whether 2 ATTEND is
the right number for a 20-repo portfolio.

## Decision

v0.1 ships all three pieces in one PR. The first memo
(`repo_triage/2026-M07.md`) is what calibrates the rubric and the
gates. If the first hand-filled pass had surfaced a factor that
collapsed to the same value across all 20 repos, that factor would
have been removed before v0.1 landed — not in a follow-up.

The atomic-shipped pieces:

- `rules/v0.md` — the 5-factor rubric
- `src/repo_triage/` — the Python package with CLI subcommands
- `schemas/{scoring,memo}.schema.json` — front-matter contracts
- `scoring/2026-M07/` — 20 hand-filled stubs
- `repo_triage/2026-M07.md` — the rendered memo
- `data/ledger/runs.jsonl` — machine-readable record of the run
- `.github/workflows/ci.yml` — CI runs all four gates on the M07 memo

## Consequences

**Positive.** The rubric is now empirically calibrated against 20
real repos. The gate cardinalities have a falsifiable referent. Future
rubric bumps (v0 → v1) have a clear comparison point: "did this factor
shift the ATTEND list, or did it just shuffle the FREEZE order?"

**Negative.** The v0.1 diff is larger than three smaller PRs would
have been. The reviewer needs to hold the rubric, the schema, and the
first scored memo in their head at once. This is mitigated by the
spec ledger at `specs/0002-design/`, which keeps the rationale for
each piece self-contained.

**Followups locked in by this decision.** The "Next feature queue"
section of `STATUS.md` lists the items deferred to v0.2 — the
`repo-triage diff` subcommand, the pluggable voice-lint rules file,
and the `repo-triage ledger-append` automation. These were considered
in scope for v0.1 and explicitly deferred.

## Alternatives considered

- **Three separate PRs as originally specced**: rejected for the
  falsifiable-referent reason above.
- **PR A + a synthetic first memo, PR B + the real first memo**: this
  was the closest runner-up. It was rejected because a synthetic memo
  is a worse test of the rubric than a real one, and the cost of
  doing both was higher than just doing the real one once.
