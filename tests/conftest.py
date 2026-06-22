from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def portfolio_path(repo_root: Path) -> Path:
    return repo_root / "config" / "portfolio.yaml"


@pytest.fixture(scope="session")
def rubric_path(repo_root: Path) -> Path:
    return repo_root / "rules" / "v0.md"


@pytest.fixture(scope="session")
def memo_schema_path(repo_root: Path) -> Path:
    return repo_root / "schemas" / "memo.schema.json"


@pytest.fixture(scope="session")
def scoring_schema_path(repo_root: Path) -> Path:
    return repo_root / "schemas" / "scoring.schema.json"


@pytest.fixture(scope="session")
def m07_memo_path(repo_root: Path) -> Path:
    return repo_root / "repo_triage" / "2026-M07.md"


@pytest.fixture(scope="session")
def m07_scoring_dir(repo_root: Path) -> Path:
    return repo_root / "scoring" / "2026-M07"


@pytest.fixture(scope="session")
def min_portfolio_path(repo_root: Path) -> Path:
    return repo_root / "tests" / "fixtures" / "portfolio_min.yaml"
