"""Smoke tests for the top-level Click CLI surface."""

from pathlib import Path

from click.testing import CliRunner

from repo_triage.cli import main


def test_cli_help_lists_subcommands() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    for sub in (
        "score-template",
        "render-memo",
        "enforce-counts",
        "validate-schemas",
        "rubric-pinned",
        "voice-lint",
    ):
        assert sub in result.output


def test_score_template_subcommand(
    tmp_path: Path,
    min_portfolio_path: Path,
    rubric_path: Path,
) -> None:
    runner = CliRunner()
    out = tmp_path / "scoring"
    result = runner.invoke(
        main,
        [
            "score-template",
            "--portfolio", str(min_portfolio_path),
            "--rubric", str(rubric_path),
            "--month", "2026-07",
            "--out", str(out),
        ],
    )
    assert result.exit_code == 0, result.output
    assert len(list(out.glob("*.md"))) == 5
