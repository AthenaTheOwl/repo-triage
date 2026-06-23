"""``repo-triage`` Click CLI.

Subcommands:

- ``score-template`` emits one hand-fill stub per portfolio repo
- ``render-memo`` builds the monthly memo from a directory of stubs
- ``enforce-counts`` asserts the 2-ATTEND / 3-RETIRE / rest-FREEZE shape
- ``validate-schemas`` validates a memo and (optionally) its scoring stubs
- ``rubric-pinned`` asserts the memo pins an existing rubric version
- ``voice-lint`` runs the banned-phrase lint over a memo
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click

from repo_triage.memo import (
    ATTEND_COUNT,
    RETIRE_COUNT,
    Memo,
    load_memo,
    render_memo,
)
from repo_triage.portfolio import load_portfolio
from repo_triage.rubric import load_rubric
from repo_triage.scoring import emit_stubs


@click.group()
@click.version_option()
def main() -> None:
    """Monthly forcing-function memo across an active side-project portfolio."""


@main.command("score-template")
@click.option("--portfolio", "portfolio_path", required=True, type=click.Path(exists=True))
@click.option("--rubric", "rubric_path", required=True, type=click.Path(exists=True))
@click.option("--month", required=True, help="e.g. 2026-07")
@click.option("--out", "out_dir", required=True, type=click.Path())
def score_template(portfolio_path: str, rubric_path: str, month: str, out_dir: str) -> None:
    """Emit one hand-fill scoring stub per portfolio repo."""
    portfolio = load_portfolio(portfolio_path)
    rubric = load_rubric(rubric_path)
    written = emit_stubs(portfolio, rubric, month=month, out_dir=out_dir)
    click.echo(f"emitted {len(written)} stubs into {out_dir}")


@main.command("render-memo")
@click.option("--scoring", "scoring_dir", required=True, type=click.Path(exists=True))
@click.option("--portfolio", "portfolio_path", required=True, type=click.Path(exists=True))
@click.option("--rubric", "rubric_path", required=True, type=click.Path(exists=True))
@click.option("--month", required=True)
@click.option("--prior", "prior_memo_path", type=click.Path(exists=True), default=None)
@click.option("--out", "out_path", required=True, type=click.Path())
def render_memo_cmd(
    scoring_dir: str,
    portfolio_path: str,
    rubric_path: str,
    month: str,
    prior_memo_path: str | None,
    out_path: str,
) -> None:
    """Render a monthly memo from a directory of hand-filled stubs."""
    portfolio = load_portfolio(portfolio_path)
    rubric = load_rubric(rubric_path)
    prior = load_memo(prior_memo_path) if prior_memo_path else None
    text = render_memo(
        scoring_dir=scoring_dir,
        portfolio=portfolio,
        month=month,
        rubric_version=rubric.version,
        prior_memo=prior,
    )
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    click.echo(f"wrote {out_path}")


@main.command("enforce-counts")
@click.argument("memo_path", type=click.Path(exists=True))
@click.option("--portfolio", "portfolio_path", required=True, type=click.Path(exists=True))
def enforce_counts_cmd(memo_path: str, portfolio_path: str) -> None:
    """Assert the memo has exactly 2 ATTEND, 3 RETIRE, and rest FREEZE."""
    memo = load_memo(memo_path)
    portfolio = load_portfolio(portfolio_path)
    errors = _enforce_counts(memo, portfolio.slugs)
    if errors:
        for e in errors:
            click.echo(f"enforce_counts: {e}", err=True)
        sys.exit(1)
    click.echo("enforce_counts: ok")


def _enforce_counts(memo: Memo, portfolio_slugs: tuple[str, ...]) -> list[str]:
    errors: list[str] = []
    if len(memo.attend) != ATTEND_COUNT:
        errors.append(f"ATTEND must have exactly {ATTEND_COUNT} entries, got {len(memo.attend)}")
    if len(memo.retire) != RETIRE_COUNT:
        errors.append(f"RETIRE must have exactly {RETIRE_COUNT} entries, got {len(memo.retire)}")
    buckets = {
        "ATTEND": set(memo.attend),
        "RETIRE": set(memo.retire),
        "FREEZE": set(memo.freeze),
    }
    all_listed = buckets["ATTEND"] | buckets["RETIRE"] | buckets["FREEZE"]
    portfolio_set = set(portfolio_slugs)
    if all_listed != portfolio_set:
        missing = portfolio_set - all_listed
        extra = all_listed - portfolio_set
        if missing:
            errors.append(f"portfolio repos missing from memo: {sorted(missing)}")
        if extra:
            errors.append(f"memo lists repos not in portfolio: {sorted(extra)}")
    pairs = [("ATTEND", "RETIRE"), ("ATTEND", "FREEZE"), ("RETIRE", "FREEZE")]
    for a, b in pairs:
        overlap = buckets[a] & buckets[b]
        if overlap:
            errors.append(f"repos appear in both {a} and {b}: {sorted(overlap)}")
    return errors


@main.command("validate-schemas")
@click.argument("memo_path", type=click.Path(exists=True))
@click.option("--memo-schema", "memo_schema", required=True, type=click.Path(exists=True))
@click.option("--scoring-schema", "scoring_schema", type=click.Path(exists=True))
@click.option("--scoring-dir", "scoring_dir", type=click.Path(exists=True))
def validate_schemas_cmd(
    memo_path: str,
    memo_schema: str,
    scoring_schema: str | None,
    scoring_dir: str | None,
) -> None:
    """Validate memo front-matter (and optionally scoring stubs) against JSON schemas."""
    errors = _validate_schemas(
        memo_path=Path(memo_path),
        memo_schema=Path(memo_schema),
        scoring_schema=Path(scoring_schema) if scoring_schema else None,
        scoring_dir=Path(scoring_dir) if scoring_dir else None,
    )
    if errors:
        for e in errors:
            click.echo(e, err=True)
        sys.exit(1)
    click.echo("validate_schemas: ok")


def _validate_schemas(
    *,
    memo_path: Path,
    memo_schema: Path,
    scoring_schema: Path | None,
    scoring_dir: Path | None,
) -> list[str]:
    """Return a list of schema violations. Empty list = pass."""
    import yaml
    from jsonschema import Draft202012Validator

    errors: list[str] = []

    text = memo_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return ["validate_schemas: memo missing front-matter"]
    end = text.find("\n---", 4)
    front = yaml.safe_load(text[4:end])

    schema = json.loads(memo_schema.read_text(encoding="utf-8"))
    for e in Draft202012Validator(schema).iter_errors(front):
        errors.append(f"validate_schemas[memo]: {e.message}")

    if scoring_dir and scoring_schema:
        sc_schema = json.loads(scoring_schema.read_text(encoding="utf-8"))
        validator = Draft202012Validator(sc_schema)
        for stub_path in sorted(scoring_dir.glob("*.md")):
            stub_text = stub_path.read_text(encoding="utf-8")
            if not stub_text.startswith("---\n"):
                errors.append(f"validate_schemas[stub:{stub_path.name}]: missing front-matter")
                continue
            stub_end = stub_text.find("\n---", 4)
            stub_front = yaml.safe_load(stub_text[4:stub_end])
            for e in validator.iter_errors(stub_front):
                errors.append(f"validate_schemas[stub:{stub_path.name}]: {e.message}")

    return errors


# repo root is two parents up from this file: src/repo_triage/cli.py
_REPO_ROOT = Path(__file__).resolve().parents[2]


@main.command("validate")
def validate_cmd() -> None:
    """Validate the bundled committed memo and scoring stubs against the schemas.

    This is the canonical no-arg sanity check: it reads only committed
    artifacts (the latest monthly memo, its scoring stubs, and the bundled
    schemas) and exits 0 when they are schema-valid. No network, no writes.
    """
    memos = sorted(_REPO_ROOT.glob("repo_triage/[0-9][0-9][0-9][0-9]-M[0-9][0-9].md"))
    if not memos:
        click.echo("validate: no committed memo found under repo_triage/", err=True)
        sys.exit(1)
    memo_path = memos[-1]
    month = memo_path.stem  # e.g. 2026-M07

    errors = _validate_schemas(
        memo_path=memo_path,
        memo_schema=_REPO_ROOT / "schemas" / "memo.schema.json",
        scoring_schema=_REPO_ROOT / "schemas" / "scoring.schema.json",
        scoring_dir=_REPO_ROOT / "scoring" / month,
    )
    if errors:
        for e in errors:
            click.echo(e, err=True)
        sys.exit(1)
    click.echo(f"validate: ok ({memo_path.name} and its scoring stubs are schema-valid)")


@main.command("show")
def show_cmd() -> None:
    """Print the latest committed memo as a ranked attention table.

    Reads only committed artifacts (the latest monthly memo and its
    scoring stubs) and prints every portfolio repo ranked by composite
    rubric score, with its ATTEND / RETIRE / FREEZE bucket and the
    binding reason. No network, no writes. This is the no-arg view of
    "where does next month's attention go, and why".
    """
    from repo_triage.scoring import parse_stub

    memos = sorted(_REPO_ROOT.glob("repo_triage/[0-9][0-9][0-9][0-9]-M[0-9][0-9].md"))
    if not memos:
        click.echo("show: no committed memo found under repo_triage/", err=True)
        sys.exit(1)
    memo_path = memos[-1]
    month = memo_path.stem  # e.g. 2026-M07
    memo = load_memo(memo_path)

    bucket_of: dict[str, str] = {}
    for slug in memo.attend:
        bucket_of[slug] = "ATTEND"
    for slug in memo.retire:
        bucket_of[slug] = "RETIRE"
    for slug in memo.freeze:
        bucket_of[slug] = "FREEZE"

    scoring_dir = _REPO_ROOT / "scoring" / month
    rows: list[tuple[int, str, str]] = []
    for stub_path in sorted(scoring_dir.glob("*.md")):
        stub = parse_stub(stub_path)
        rows.append((stub.composite, stub.repo, bucket_of.get(stub.repo, "?")))

    # Rank: highest composite first, ties by slug. Bucket as secondary key
    # so the forced top-2 / bottom-3 ordering reads correctly even on ties.
    order = {"ATTEND": 0, "FREEZE": 1, "RETIRE": 2, "?": 3}
    rows.sort(key=lambda r: (order[r[2]], -r[0], r[1]))

    click.echo(f"repo triage - {memo.month}  (rubric {memo.rubric_version})")
    click.echo("ranked by composite thesis-alive score (0-15); attention is forced:")
    click.echo("  2 ATTEND  /  3 RETIRE  /  rest FREEZE")
    click.echo("")
    click.echo(f"  {'rank':>4}  {'score':>5}  {'bucket':<7}  repo")
    click.echo(f"  {'-' * 4}  {'-' * 5}  {'-' * 7}  {'-' * 24}")
    for i, (composite, slug, bucket) in enumerate(rows, start=1):
        click.echo(f"  {i:>4}  {composite:>2}/15  {bucket:<7}  {slug}")
    click.echo("")
    click.echo(f"this month's shipping attention: {', '.join(memo.attend)}")
    click.echo(f"archived (needs a written revival rationale): {', '.join(memo.retire)}")
    click.echo(
        f"held without attention: {len(memo.freeze)} repos "
        f"(see {memo_path.relative_to(_REPO_ROOT).as_posix()})"
    )


@main.command("rubric-pinned")
@click.argument("memo_path", type=click.Path(exists=True))
@click.option("--rubric", "rubric_path", required=True, type=click.Path(exists=True))
def rubric_pinned_cmd(memo_path: str, rubric_path: str) -> None:
    """Assert the memo pins a rubric version that matches ``rubric_path``."""
    memo = load_memo(memo_path)
    rubric = load_rubric(rubric_path)
    if memo.rubric_version != rubric.version:
        click.echo(
            f"rubric_pinned: memo pins {memo.rubric_version!r}, rubric on disk is {rubric.version!r}",
            err=True,
        )
        sys.exit(1)
    click.echo("rubric_pinned: ok")


_BANNED_PHRASES: tuple[str, ...] = (
    "revolutionary",
    "game-changing",
    "world-class",
    "best-in-class",
    "delightful",
    "seamless",
    "blazing fast",
    "blazingly fast",
    "unlocks",
    "leverages",
    "empowers",
    "supercharges",
    "not just",
    "it's not just",
    "this isn't just",
    "this is not just",
)


@main.command("voice-lint")
@click.argument("memo_path", type=click.Path(exists=True))
def voice_lint_cmd(memo_path: str) -> None:
    """Reject the memo if it contains banned marketing or antithetical-reversal phrases."""
    text = Path(memo_path).read_text(encoding="utf-8")
    errors = voice_lint(text)
    if errors:
        for e in errors:
            click.echo(f"voice_lint: {e}", err=True)
        sys.exit(1)
    click.echo("voice_lint: ok")


def voice_lint(text: str) -> list[str]:
    """Return a list of violations. Empty list = pass."""
    lower = text.lower()
    hits: list[str] = []
    for phrase in _BANNED_PHRASES:
        if phrase in lower:
            hits.append(f"banned phrase: {phrase!r}")
    return hits


if __name__ == "__main__":
    main()
