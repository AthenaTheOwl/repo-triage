#!/usr/bin/env python3
"""Validate memo (and optionally scoring stubs) against their JSON schemas.

Usage:

    python scripts/validate_schemas.py repo_triage/2026-M07.md \
        --memo-schema schemas/memo.schema.json \
        --scoring-schema schemas/scoring.schema.json \
        --scoring-dir scoring/2026-M07/
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from repo_triage.cli import validate_schemas_cmd

if __name__ == "__main__":
    validate_schemas_cmd()
