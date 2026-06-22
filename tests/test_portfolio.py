from pathlib import Path

import pytest

from repo_triage.portfolio import load_portfolio


def test_load_min_portfolio(min_portfolio_path: Path) -> None:
    p = load_portfolio(min_portfolio_path)
    assert p.version == "v0"
    assert p.slugs == ("alpha", "bravo", "charlie", "delta", "echo")
    assert p.get("alpha").thesis == "First fixture repo."


def test_canonical_portfolio_has_twenty_repos(portfolio_path: Path) -> None:
    p = load_portfolio(portfolio_path)
    assert len(p.slugs) == 20
    assert len(set(p.slugs)) == 20


def test_portfolio_rejects_duplicate_slug(tmp_path: Path) -> None:
    bad = tmp_path / "dup.yaml"
    bad.write_text(
        "version: v0\nrepos:\n  - slug: alpha\n    thesis: x\n  - slug: alpha\n    thesis: y\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="duplicate slugs"):
        load_portfolio(bad)


def test_portfolio_rejects_missing_slug(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text("version: v0\nrepos:\n  - thesis: x\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_portfolio(bad)
