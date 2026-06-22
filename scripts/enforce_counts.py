#!/usr/bin/env python3
"""Assert a memo has exactly 2 ATTEND, 3 RETIRE, and rest FREEZE.

Usage:

    python scripts/enforce_counts.py repo_triage/2026-M07.md \
        --portfolio config/portfolio.yaml
"""

from repo_triage.cli import enforce_counts_cmd

if __name__ == "__main__":
    enforce_counts_cmd()
