from pathlib import Path

from repo_triage.portfolio import load_portfolio
from repo_triage.rubric import FACTOR_KEYS, load_rubric
from repo_triage.scoring import emit_stubs


def test_emit_stubs_writes_one_per_repo(
    tmp_path: Path,
    min_portfolio_path: Path,
    rubric_path: Path,
) -> None:
    portfolio = load_portfolio(min_portfolio_path)
    rubric = load_rubric(rubric_path)
    out_dir = tmp_path / "scoring"
    written = emit_stubs(portfolio, rubric, month="2026-07", out_dir=out_dir)
    assert len(written) == len(portfolio.repos)
    names = {p.name for p in out_dir.iterdir()}
    assert names == {f"{r.slug}.md" for r in portfolio.repos}


def test_emit_stubs_contains_all_factor_keys(
    tmp_path: Path,
    min_portfolio_path: Path,
    rubric_path: Path,
) -> None:
    portfolio = load_portfolio(min_portfolio_path)
    rubric = load_rubric(rubric_path)
    out_dir = tmp_path / "scoring"
    emit_stubs(portfolio, rubric, month="2026-07", out_dir=out_dir)
    stub = (out_dir / "alpha.md").read_text(encoding="utf-8")
    for k in FACTOR_KEYS:
        assert k in stub


def test_emit_stubs_pins_rubric_version(
    tmp_path: Path,
    min_portfolio_path: Path,
    rubric_path: Path,
) -> None:
    portfolio = load_portfolio(min_portfolio_path)
    rubric = load_rubric(rubric_path)
    out_dir = tmp_path / "scoring"
    emit_stubs(portfolio, rubric, month="2026-07", out_dir=out_dir)
    stub = (out_dir / "alpha.md").read_text(encoding="utf-8")
    assert f"rubric_version: {rubric.version}" in stub


def test_emit_stubs_is_deterministic(
    tmp_path: Path,
    min_portfolio_path: Path,
    rubric_path: Path,
) -> None:
    portfolio = load_portfolio(min_portfolio_path)
    rubric = load_rubric(rubric_path)
    a = tmp_path / "a"
    b = tmp_path / "b"
    emit_stubs(portfolio, rubric, month="2026-07", out_dir=a)
    emit_stubs(portfolio, rubric, month="2026-07", out_dir=b)
    for r in portfolio.repos:
        assert (a / f"{r.slug}.md").read_text(encoding="utf-8") == (
            b / f"{r.slug}.md"
        ).read_text(encoding="utf-8")
