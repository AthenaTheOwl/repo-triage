from pathlib import Path

from click.testing import CliRunner

from repo_triage.cli import main


def test_rubric_pinned_cli_passes(
    m07_memo_path: Path,
    rubric_path: Path,
) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["rubric-pinned", str(m07_memo_path), "--rubric", str(rubric_path)],
    )
    assert result.exit_code == 0, result.output


def test_rubric_pinned_cli_fails_on_mismatch(
    m07_memo_path: Path,
    tmp_path: Path,
) -> None:
    fake = tmp_path / "v9.md"
    fake.write_text("---\nversion: v9\n---\n\n"
                    "### thesis_still_credible — x\n"
                    "### pull_from_outside — x\n"
                    "### shippable_next_step — x\n"
                    "### cost_of_freeze — x\n"
                    "### dependency_in_portfolio — x\n",
                    encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["rubric-pinned", str(m07_memo_path), "--rubric", str(fake)],
    )
    assert result.exit_code != 0
