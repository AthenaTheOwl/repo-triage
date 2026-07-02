from pathlib import Path

import pytest
import yaml

from repo_triage.memo import (
    ATTEND_COUNT,
    RETIRE_COUNT,
    Memo,
    _compute_deltas,
    load_memo,
    render_memo,
)
from repo_triage.portfolio import load_portfolio
from repo_triage.rubric import load_rubric


def _write_stub(
    out_dir: Path,
    slug: str,
    month: str,
    version: str,
    scores: dict[str, int],
) -> None:
    front = (
        "---\n"
        f"repo: {slug}\n"
        f"month: {month}\n"
        f"rubric_version: {version}\n"
        "scores:\n"
        + "".join(f"  {k}: {v}\n" for k, v in scores.items())
        + "evidence:\n"
        + "".join(f"  {k}: \"e\"\n" for k in scores)
        + "author: T\n"
        "---\n\n# x\n"
    )
    (out_dir / f"{slug}.md").write_text(front, encoding="utf-8")


def test_render_memo_against_fixture(
    tmp_path: Path,
    min_portfolio_path: Path,
    rubric_path: Path,
) -> None:
    portfolio = load_portfolio(min_portfolio_path)
    rubric = load_rubric(rubric_path)
    scoring = tmp_path / "scoring"
    scoring.mkdir()
    base = {
        "thesis_still_credible": 0,
        "pull_from_outside": 0,
        "shippable_next_step": 0,
        "cost_of_freeze": 0,
        "dependency_in_portfolio": 0,
    }
    _write_stub(scoring, "alpha", "2026-07", "v0", {**base, "thesis_still_credible": 3, "pull_from_outside": 3, "shippable_next_step": 3, "cost_of_freeze": 3, "dependency_in_portfolio": 3})
    _write_stub(scoring, "bravo", "2026-07", "v0", {**base, "thesis_still_credible": 3, "pull_from_outside": 3, "shippable_next_step": 3, "cost_of_freeze": 3, "dependency_in_portfolio": 2})
    _write_stub(scoring, "charlie", "2026-07", "v0", {**base, "thesis_still_credible": 2})
    _write_stub(scoring, "delta", "2026-07", "v0", {**base, "thesis_still_credible": 1})
    _write_stub(scoring, "echo", "2026-07", "v0", base)

    text = render_memo(
        scoring_dir=scoring,
        portfolio=portfolio,
        month="2026-07",
        rubric_version="v0",
    )
    assert text.startswith("---\n")
    end = text.find("\n---", 4)
    front = yaml.safe_load(text[4:end])
    assert front["month"] == "2026-07"
    assert front["rubric_version"] == "v0"
    assert front["attend"] == ["alpha", "bravo"]
    assert len(front["retire"]) == RETIRE_COUNT
    assert set(front["retire"]) == {"charlie", "delta", "echo"}
    assert front["freeze"] == []
    assert front["deltas"] == []


def test_render_memo_rejects_missing_stubs(
    tmp_path: Path,
    min_portfolio_path: Path,
) -> None:
    portfolio = load_portfolio(min_portfolio_path)
    scoring = tmp_path / "scoring"
    scoring.mkdir()
    _write_stub(scoring, "alpha", "2026-07", "v0", {
        "thesis_still_credible": 1,
        "pull_from_outside": 1,
        "shippable_next_step": 1,
        "cost_of_freeze": 1,
        "dependency_in_portfolio": 1,
    })
    with pytest.raises(ValueError, match="missing stubs"):
        render_memo(
            scoring_dir=scoring,
            portfolio=portfolio,
            month="2026-07",
            rubric_version="v0",
        )


def test_render_memo_rejects_stub_outside_portfolio(
    tmp_path: Path,
    min_portfolio_path: Path,
) -> None:
    portfolio = load_portfolio(min_portfolio_path)
    scoring = tmp_path / "scoring"
    scoring.mkdir()
    for slug in ("alpha", "bravo", "charlie", "delta", "echo", "intruder"):
        _write_stub(scoring, slug, "2026-07", "v0", {
            "thesis_still_credible": 1,
            "pull_from_outside": 1,
            "shippable_next_step": 1,
            "cost_of_freeze": 1,
            "dependency_in_portfolio": 1,
        })
    with pytest.raises(ValueError, match="not in portfolio"):
        render_memo(
            scoring_dir=scoring,
            portfolio=portfolio,
            month="2026-07",
            rubric_version="v0",
        )


def test_render_memo_rejects_rubric_version_mismatch(
    tmp_path: Path,
    min_portfolio_path: Path,
) -> None:
    portfolio = load_portfolio(min_portfolio_path)
    scoring = tmp_path / "scoring"
    scoring.mkdir()
    for slug in portfolio.slugs:
        _write_stub(scoring, slug, "2026-07", "v0", {
            "thesis_still_credible": 1,
            "pull_from_outside": 1,
            "shippable_next_step": 1,
            "cost_of_freeze": 1,
            "dependency_in_portfolio": 1,
        })
    with pytest.raises(ValueError, match="rubric"):
        render_memo(
            scoring_dir=scoring,
            portfolio=portfolio,
            month="2026-07",
            rubric_version="v1",
        )


def test_compute_deltas_prior_vs_current() -> None:
    # Golden-master lock on the prior-vs-current bucketing diff. Without a
    # non-None prior the whole path in _compute_deltas is unpinned, so this
    # pins the exact promoted/moved/dropped wording against a known prior.
    prior = Memo(
        month="2026-06",
        rubric_version="v0",
        attend=("alpha", "bravo"),
        retire=("charlie", "delta", "echo"),
        freeze=("foxtrot",),
        deltas=(),
    )
    # charlie: RETIRE -> ATTEND (promotion); foxtrot: FREEZE -> RETIRE;
    # alpha: ATTEND -> FREEZE (dropped); echo: RETIRE -> ATTEND (promotion).
    deltas = _compute_deltas(
        prior,
        attend=["charlie", "echo"],
        retire=("delta", "foxtrot", "bravo"),
        freeze=["alpha"],
    )
    assert deltas == [
        "promoted to ATTEND: charlie (was RETIRE)",
        "promoted to ATTEND: echo (was RETIRE)",
        "moved to RETIRE: foxtrot (was FREEZE)",
        "moved to RETIRE: bravo (was ATTEND)",
        "dropped from ATTEND to FREEZE: alpha",
    ]


def test_compute_deltas_no_prior_is_empty() -> None:
    assert _compute_deltas(None, ["a"], ["b"], ["c"]) == []


def test_checked_in_m07_memo_parses(m07_memo_path: Path) -> None:
    memo = load_memo(m07_memo_path)
    assert memo.month == "2026-07"
    assert memo.rubric_version == "v0"
    assert len(memo.attend) == ATTEND_COUNT
    assert len(memo.retire) == RETIRE_COUNT
    assert "grid-silicon" in memo.attend
    assert "dream-replay-cli" in memo.attend
