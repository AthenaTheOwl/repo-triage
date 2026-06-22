#!/usr/bin/env python3
"""Emit one hand-fill scoring stub per portfolio repo.

Usage:

    python scripts/score_template.py \
        --portfolio config/portfolio.yaml \
        --rubric rules/v0.md \
        --month 2026-07 \
        --out scoring/2026-M07/
"""

from repo_triage.cli import score_template

if __name__ == "__main__":
    score_template()
