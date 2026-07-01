from pathlib import Path

import pytest
from click.testing import CliRunner

from repo_triage.cli import _BANNED_PHRASES, main, voice_lint


def test_voice_lint_passes_on_canonical_memo(m07_memo_path: Path) -> None:
    text = m07_memo_path.read_text(encoding="utf-8")
    assert voice_lint(text) == []


def test_voice_lint_flags_banned_phrase() -> None:
    assert voice_lint("this is revolutionary") != []
    assert voice_lint("Not just a CLI — a way of life") != []


@pytest.mark.parametrize("phrase", _BANNED_PHRASES)
def test_voice_lint_flags_every_banned_phrase(phrase: str) -> None:
    # Pins the whole banned list: dropping any phrase from _BANNED_PHRASES
    # drops its case here, so no single entry can be deleted undetected.
    hits = voice_lint(f"prefix {phrase} suffix")
    assert f"banned phrase: {phrase!r}" in hits, hits


def test_voice_lint_banned_list_is_expected() -> None:
    # Lock the exact set so a silent removal fails even before the
    # parametrized cases run.
    assert _BANNED_PHRASES == (
        "revolutionary",
        "game-changing",
        "world-class",
        "best-in-class",
        "delightful",
        "seamless",
        "blazing fast",
        "blazingly fast",
        "unlocks",
        "leverages",
        "empowers",
        "supercharges",
        "not just",
        "it's not just",
        "this isn't just",
        "this is not just",
    )


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


def test_voice_lint_cli_rejects_directory(tmp_path: Path) -> None:
    # A directory where a memo file is expected must be a clean usage error
    # (exit 2), not an uncaught OSError from read_text().
    runner = CliRunner()
    result = runner.invoke(main, ["voice-lint", str(tmp_path)])
    assert result.exit_code == 2, result.output
    assert "is a directory" in result.output
