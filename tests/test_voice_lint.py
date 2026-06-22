from pathlib import Path

from click.testing import CliRunner

from repo_triage.cli import main, voice_lint


def test_voice_lint_passes_on_canonical_memo(m07_memo_path: Path) -> None:
    text = m07_memo_path.read_text(encoding="utf-8")
    assert voice_lint(text) == []


def test_voice_lint_flags_banned_phrase() -> None:
    assert voice_lint("this is revolutionary") != []
    assert voice_lint("Not just a CLI — a way of life") != []


def test_voice_lint_cli_passes_on_canonical_memo(m07_memo_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["voice-lint", str(m07_memo_path)])
    assert result.exit_code == 0, result.output


def test_voice_lint_cli_fails_on_banned_phrase(tmp_path: Path) -> None:
    bad = tmp_path / "memo.md"
    bad.write_text("# bad\nThis tool is revolutionary.\n", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(main, ["voice-lint", str(bad)])
    assert result.exit_code != 0
