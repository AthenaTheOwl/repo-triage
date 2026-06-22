#!/usr/bin/env python3
"""Assert the memo pins a rubric version that matches the rubric on disk.

Usage:

    python scripts/rubric_pinned.py repo_triage/2026-M07.md \
        --rubric rules/v0.md
"""

from repo_triage.cli import rubric_pinned_cmd

if __name__ == "__main__":
    rubric_pinned_cmd()
