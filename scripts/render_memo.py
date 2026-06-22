#!/usr/bin/env python3
"""Render a monthly memo from a directory of hand-filled scoring stubs.

Usage:

    python scripts/render_memo.py \
        --scoring scoring/2026-M07/ \
        --portfolio config/portfolio.yaml \
        --rubric rules/v0.md \
        --month 2026-07 \
        --out repo_triage/2026-M07.md
"""

from repo_triage.cli import render_memo_cmd

if __name__ == "__main__":
    render_memo_cmd()
