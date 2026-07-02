from pathlib import Path

from click.testing import CliRunner

from repo_triage.cli import _enforce_counts, main
from repo_triage.memo import Memo, load_memo
from repo_triage.portfolio import load_portfolio


def test_enforce_counts_helper_passes_on_canonical_memo(
    m07_memo_path: Path,
    portfolio_path: Path,
) -> None:
    memo = load_memo(m07_memo_path)
    portfolio = load_portfolio(portfolio_path)
    errors = _enforce_counts(memo, portfolio.slugs)
    assert errors == [], errors


def test_enforce_counts_helper_rejects_wrong_attend() -> None:
    memo = Memo(
        month="2026-07",
        rubric_version="v0",
        attend=("a",),
        retire=("b", "c", "d"),
        freeze=("e",),
        deltas=(),
    )
    errors = _enforce_counts(memo, ("a", "b", "c", "d", "e"))
    assert any("ATTEND" in e for e in errors)


def test_enforce_counts_helper_rejects_overlap() -> None:
    memo = Memo(
        month="2026-07",
        rubric_version="v0",
        attend=("a", "b"),
        retire=("c", "d", "e"),
        freeze=("a",),  # overlap with ATTEND
        deltas=(),
    )
    errors = _enforce_counts(memo, ("a", "b", "c", "d", "e"))
    assert any("both" in e for e in errors)


def test_enforce_counts_helper_rejects_retire_freeze_overlap() -> None:
    # Pins the ('RETIRE', 'FREEZE') pair specifically: a slug in both retire
    # and freeze must be flagged, not only the ATTEND/FREEZE case above.
    memo = Memo(
        month="2026-07",
        rubric_version="v0",
        attend=("a", "b"),
        retire=("c", "d", "e"),
        freeze=("c",),  # overlap with RETIRE
        deltas=(),
    )
    errors = _enforce_counts(memo, ("a", "b", "c", "d", "e"))
    assert any("both RETIRE and FREEZE" in e for e in errors), errors


def test_enforce_counts_cli_passes(
    m07_memo_path: Path,
    portfolio_path: Path,
) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["enforce-counts", str(m07_memo_path), "--portfolio", str(portfolio_path)],
    )
    assert result.exit_code == 0, result.output
    assert "ok" in result.output
