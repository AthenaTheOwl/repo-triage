import json
from pathlib import Path

import yaml
from click.testing import CliRunner
from jsonschema import Draft202012Validator

from repo_triage.cli import main
from repo_triage.scoring import parse_stub


def test_memo_schema_validates_canonical_memo(
    m07_memo_path: Path,
    memo_schema_path: Path,
) -> None:
    text = m07_memo_path.read_text(encoding="utf-8")
    end = text.find("\n---", 4)
    front = yaml.safe_load(text[4:end])
    schema = json.loads(memo_schema_path.read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(schema).iter_errors(front))
    assert errors == [], [e.message for e in errors]


def test_scoring_schema_validates_every_m07_stub(
    m07_scoring_dir: Path,
    scoring_schema_path: Path,
) -> None:
    schema = json.loads(scoring_schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    for stub_path in sorted(m07_scoring_dir.glob("*.md")):
        text = stub_path.read_text(encoding="utf-8")
        assert text.startswith("---\n")
        end = text.find("\n---", 4)
        front = yaml.safe_load(text[4:end])
        errors = list(validator.iter_errors(front))
        assert errors == [], (stub_path.name, [e.message for e in errors])


def test_every_m07_stub_parses(m07_scoring_dir: Path) -> None:
    for stub_path in sorted(m07_scoring_dir.glob("*.md")):
        stub = parse_stub(stub_path)
        assert 0 <= stub.composite <= 15


def test_validate_schemas_cli_passes(
    m07_memo_path: Path,
    memo_schema_path: Path,
    scoring_schema_path: Path,
    m07_scoring_dir: Path,
) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "validate-schemas",
            str(m07_memo_path),
            "--memo-schema",
            str(memo_schema_path),
            "--scoring-schema",
            str(scoring_schema_path),
            "--scoring-dir",
            str(m07_scoring_dir),
        ],
    )
    assert result.exit_code == 0, result.output
