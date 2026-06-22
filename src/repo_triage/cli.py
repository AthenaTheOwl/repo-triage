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
    import yaml
    from jsonschema import Draft202012Validator

    text = Path(memo_path).read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        click.echo("validate_schemas: memo missing front-matter", err=True)
        sys.exit(1)
    end = text.find("\n---", 4)
    front = yaml.safe_load(text[4:end])

    schema = json.loads(Path(memo_schema).read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(schema).iter_errors(front))
    if errors:
        for e in errors:
            click.echo(f"validate_schemas[memo]: {e.message}", err=True)
        sys.exit(1)

    if scoring_dir and scoring_schema:
        sc_schema = json.loads(Path(scoring_schema).read_text(encoding="utf-8"))
        validator = Draft202012Validator(sc_schema)
        any_failed = False
        for stub_path in sorted(Path(scoring_dir).glob("*.md")):
            stub_text = stub_path.read_text(encoding="utf-8")
            if not stub_text.startswith("---\n"):
                click.echo(f"validate_schemas[stub:{stub_path.name}]: missing front-matter", err=True)
                any_failed = True
                continue
            stub_end = stub_text.find("\n---", 4)
            stub_front = yaml.safe_load(stub_text[4:stub_end])
            stub_errors = list(validator.iter_errors(stub_front))
            for e in stub_errors:
                click.echo(f"validate_schemas[stub:{stub_path.name}]: {e.message}", err=True)
                any_failed = True
        if any_failed:
            sys.exit(1)

    click.echo("validate_schemas: ok")


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
