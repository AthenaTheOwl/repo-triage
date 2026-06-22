from pathlib import Path

import pytest

from repo_triage.rubric import FACTOR_KEYS, load_rubric


def test_load_v0_rubric(rubric_path: Path) -> None:
    r = load_rubric(rubric_path)
    assert r.version == "v0"
    assert r.keys == FACTOR_KEYS
    assert len(r.factors) == 5


def test_rubric_referenced_by_scoring_schema(rubric_path: Path, scoring_schema_path: Path) -> None:
    """Every rubric factor key is required by scoring.schema.json."""
    import json

    schema = json.loads(scoring_schema_path.read_text(encoding="utf-8"))
    score_props = set(schema["properties"]["scores"]["required"])
    assert score_props == set(FACTOR_KEYS)
    ev_props = set(schema["properties"]["evidence"]["required"])
    assert ev_props == set(FACTOR_KEYS)


def test_rubric_rejects_missing_version(tmp_path: Path) -> None:
    bad = tmp_path / "v.md"
    bad.write_text("# no front matter\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_rubric(bad)


def test_rubric_rejects_wrong_factor_order(tmp_path: Path) -> None:
    bad = tmp_path / "v.md"
    bad.write_text(
        "---\nversion: v9\n---\n\n"
        "### pull_from_outside — x\n"
        "### thesis_still_credible — x\n"
        "### shippable_next_step — x\n"
        "### cost_of_freeze — x\n"
        "### dependency_in_portfolio — x\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="factors"):
        load_rubric(bad)
