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
        "show",
    ):
        assert sub in result.output


def test_show_subcommand_no_args() -> None:
    """`show` reads the committed memo and prints a ranked table, no args."""
    runner = CliRunner()
    result = runner.invoke(main, ["show"])
    assert result.exit_code == 0, result.output
    out = result.output
    # header + forcing-function note
    assert "repo triage - 2026-07" in out
    assert "ATTEND" in out and "RETIRE" in out and "FREEZE" in out
    # the top-ranked repo and its forced bucket
    assert "grid-silicon" in out
    assert "15/15" in out
    # the bottom-ranked retire repo
    assert "quux-prototype" in out
    # ranked order: grid-silicon (rank 1) appears before a freeze repo
    assert out.index("grid-silicon") < out.index("cdcp-control-plane")
    # attention summary line
    assert "this month's shipping attention: grid-silicon, dream-replay-cli" in out


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
