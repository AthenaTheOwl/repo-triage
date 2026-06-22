"""Scoring stub model and emitter.

A scoring stub is one markdown file per repo per month. The header is
YAML front-matter; the body is one section per factor where the author
hand-writes their 0-3 score and a one-line piece of evidence.

This module owns:
- the in-memory model of a stub (``ScoringStub``)
- the deterministic emitter that writes one stub per portfolio repo
- the parser that reads a stub back for memo rendering
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping

import yaml

from repo_triage.portfolio import Portfolio
from repo_triage.rubric import FACTOR_KEYS, Rubric


@dataclass(frozen=True)
class ScoringStub:
    repo: str
    month: str
    rubric_version: str
    scores: Mapping[str, int]
    evidence: Mapping[str, str]
    author: str = ""

    @property
    def composite(self) -> int:
        return sum(self.scores.get(k, 0) for k in FACTOR_KEYS)


def emit_stubs(
    portfolio: Portfolio,
    rubric: Rubric,
    month: str,
    out_dir: str | Path,
) -> list[Path]:
    """Emit one stub per portfolio repo. Returns the list of paths written.

    Deterministic: stubs are written in portfolio order, contents only
    depend on (slug, month, rubric.version).
    """
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for repo in portfolio.repos:
        path = out / f"{repo.slug}.md"
        path.write_text(_render_stub(repo.slug, month, rubric), encoding="utf-8")
        written.append(path)
    return written


def emit_stub_for_repo(
    slug: str,
    month: str,
    rubric: Rubric,
    out_dir: str | Path,
) -> Path:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{slug}.md"
    path.write_text(_render_stub(slug, month, rubric), encoding="utf-8")
    return path


def _render_stub(slug: str, month: str, rubric: Rubric) -> str:
    factor_lines: list[str] = []
    for factor in rubric.factors:
        factor_lines.append(f"### {factor.key}")
        factor_lines.append("")
        factor_lines.append("score: <0-3>")
        factor_lines.append("evidence: <one line>")
        factor_lines.append("")
    body = "\n".join(factor_lines).rstrip() + "\n"
    front = (
        "---\n"
        f"repo: {slug}\n"
        f"month: {month}\n"
        f"rubric_version: {rubric.version}\n"
        "scores:\n"
        + "".join(f"  {k}: null\n" for k in FACTOR_KEYS)
        + "evidence:\n"
        + "".join(f"  {k}: \"\"\n" for k in FACTOR_KEYS)
        + "author: \"\"\n"
        "---\n\n"
        f"# {slug} — {month}\n\n"
        "Fill in each factor: a 0-3 integer score and one line of evidence.\n\n"
    )
    return front + body


_FRONTMATTER_RE = re.compile(r"^---\s*\n(?P<body>.*?)\n---\s*\n", re.DOTALL)


def parse_stub(path: str | Path) -> ScoringStub:
    text = Path(path).read_text(encoding="utf-8")
    m = _FRONTMATTER_RE.match(text)
    if not m:
        raise ValueError(f"scoring stub missing YAML front-matter: {path}")
    data = yaml.safe_load(m.group("body"))
    if not isinstance(data, dict):
        raise ValueError(f"scoring stub front-matter must be a mapping: {path}")
    scores_raw = data.get("scores") or {}
    evidence_raw = data.get("evidence") or {}
    if not isinstance(scores_raw, dict) or not isinstance(evidence_raw, dict):
        raise ValueError(f"scores and evidence must be mappings: {path}")

    scores: dict[str, int] = {}
    for k in FACTOR_KEYS:
        v = scores_raw.get(k)
        if not isinstance(v, int) or not (0 <= v <= 3):
            raise ValueError(
                f"scoring stub {path} factor {k!r} must be an integer in 0..3, got {v!r}"
            )
        scores[k] = v
    evidence: dict[str, str] = {}
    for k in FACTOR_KEYS:
        v = evidence_raw.get(k, "")
        if not isinstance(v, str):
            raise ValueError(f"scoring stub {path} evidence {k!r} must be a string")
        evidence[k] = v

    return ScoringStub(
        repo=str(data["repo"]),
        month=str(data["month"]),
        rubric_version=str(data["rubric_version"]),
        scores=scores,
        evidence=evidence,
        author=str(data.get("author", "")),
    )
