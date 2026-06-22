#!/usr/bin/env python3
"""Reject the memo if it contains banned marketing or antithetical-reversal phrases.

Usage:

    python scripts/voice_lint.py repo_triage/2026-M07.md
"""

from repo_triage.cli import voice_lint_cmd

if __name__ == "__main__":
    voice_lint_cmd()
