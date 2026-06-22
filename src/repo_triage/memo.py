"""Memo model and renderer.

A memo is a single markdown file per month. The header is YAML
front-matter pinning the rubric version, the ATTEND / RETIRE / FREEZE
bucketing, and the deltas-vs-prior list. The body is one short section
per bucket plus a deltas section.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence

import yaml

from repo_triage.portfolio import Portfolio
from repo_triage.scoring import ScoringStub, parse_stub

ATTEND_COUNT = 2
RETIRE_COUNT = 3


@dataclass(frozen=True)
class Memo:
    month: str
    rubric_version: str
    attend: tuple[str, ...]
    retire: tuple[str, ...]
    freeze: tuple[str, ...]
    deltas: tuple[str, ...]
    rationale: dict[str, str] = field(default_factory=dict)


def _load_stubs(scoring_dir: Path) -> list[ScoringStub]:
    return [parse_stub(p) for p in sorted(scoring_dir.glob("*.md"))]


def _bucket(stubs: Sequence[ScoringStub]) -> tuple[list[str], list[str], list[str]]:
    """Bucket stubs by composite score: top 2 ATTEND, bottom 3 RETIRE, rest FREEZE.

    Ties broken by slug for determinism. The author is expected to
    override the bucketing in their hand-edit of the memo if they
    disagree with the tie-break, with a one-line written rationale.
    """
    ranked = sorted(stubs, key=lambda s: (-s.composite, s.repo))
    attend = [s.repo for s in ranked[:ATTEND_COUNT]]
    retire = [s.repo for s in ranked[-RETIRE_COUNT:]]
    middle = [s.repo for s in ranked[ATTEND_COUNT:-RETIRE_COUNT]]
    freeze = sorted(middle)
    return attend, sorted(retire), freeze


def render_memo(
    scoring_dir: str | Path,
    portfolio: Portfolio,
    month: str,
    rubric_version: str,
    prior_memo: "Memo | None" = None,
) -> str:
    """Render a memo markdown file from a directory of hand-filled stubs."""
    stubs = _load_stubs(Path(scoring_dir))
    stub_slugs = {s.repo for s in stubs}
    portfolio_slugs = set(portfolio.slugs)
    missing = portfolio_slugs - stub_slugs
    extra = stub_slugs - portfolio_slugs
    if missing:
        raise ValueError(f"scoring directory missing stubs for: {sorted(missing)}")
    if extra:
        raise ValueError(f"scoring directory has stubs not in portfolio: {sorted(extra)}")

    for s in stubs:
        if s.rubric_version != rubric_version:
            raise ValueError(
                f"stub {s.repo} pins rubric {s.rubric_version!r}; "
                f"memo pins {rubric_version!r}"
            )

    attend, retire, freeze = _bucket(stubs)
    rationale = {s.repo: _rationale(s) for s in stubs}

    deltas = _compute_deltas(prior_memo, attend, retire, freeze)

    return _format_memo(
        month=month,
        rubric_version=rubric_version,
        attend=attend,
        retire=retire,
        freeze=freeze,
        deltas=deltas,
        rationale=rationale,
    )


def _rationale(stub: ScoringStub) -> str:
    parts = []
    for k, v in stub.scores.items():
        ev = stub.evidence.get(k, "").strip()
        parts.append(f"{k}={v}" + (f" ({ev})" if ev else ""))
    return f"composite {stub.composite}/15. " + "; ".join(parts) + "."


def _compute_deltas(
    prior: "Memo | None",
    attend: Sequence[str],
    retire: Sequence[str],
    freeze: Sequence[str],
) -> list[str]:
    if prior is None:
        return []
    prior_bucket: dict[str, str] = {}
    for slug in prior.attend:
        prior_bucket[slug] = "ATTEND"
    for slug in prior.retire:
        prior_bucket[slug] = "RETIRE"
    for slug in prior.freeze:
        prior_bucket[slug] = "FREEZE"

    deltas: list[str] = []
    for slug in attend:
        prev = prior_bucket.get(slug)
        if prev and prev != "ATTEND":
            deltas.append(f"promoted to ATTEND: {slug} (was {prev})")
    for slug in retire:
        prev = prior_bucket.get(slug)
        if prev and prev != "RETIRE":
            deltas.append(f"moved to RETIRE: {slug} (was {prev})")
    for slug in freeze:
        prev = prior_bucket.get(slug)
        if prev == "ATTEND":
            deltas.append(f"dropped from ATTEND to FREEZE: {slug}")
    return deltas


def _format_memo(
    *,
    month: str,
    rubric_version: str,
    attend: Sequence[str],
    retire: Sequence[str],
    freeze: Sequence[str],
    deltas: Sequence[str],
    rationale: dict[str, str],
) -> str:
    front = {
        "month": month,
        "rubric_version": rubric_version,
        "attend": list(attend),
        "retire": list(retire),
        "freeze": list(freeze),
        "deltas": list(deltas),
    }
    fm = yaml.safe_dump(front, sort_keys=False, default_flow_style=False).strip()
    lines: list[str] = []
    lines.append("---")
    lines.append(fm)
    lines.append("---")
    lines.append("")
    lines.append(f"# Repo Triage — {month}")
    lines.append("")
    lines.append("## ATTEND")
    for slug in attend:
        lines.append(f"- {slug}: {rationale.get(slug, '')}")
    lines.append("")
    lines.append("## RETIRE")
    for slug in retire:
        lines.append(f"- {slug}: {rationale.get(slug, '')}")
    lines.append("")
    lines.append("## FREEZE")
    for slug in freeze:
        lines.append(f"- {slug}: {rationale.get(slug, '')}")
    lines.append("")
    lines.append(f"## Deltas vs prior month")
    if deltas:
        for d in deltas:
            lines.append(f"- {d}")
    else:
        lines.append("- (no prior memo)")
    lines.append("")
    return "\n".join(lines)


def load_memo(path: str | Path) -> Memo:
    """Parse an existing memo file back into a :class:`Memo` model."""
    text = Path(path).read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"memo missing front-matter: {path}")
    end = text.find("\n---", 4)
    if end < 0:
        raise ValueError(f"memo front-matter not terminated: {path}")
    fm = yaml.safe_load(text[4:end])
    if not isinstance(fm, dict):
        raise ValueError(f"memo front-matter must be a mapping: {path}")
    return Memo(
        month=str(fm["month"]),
        rubric_version=str(fm["rubric_version"]),
        attend=tuple(fm.get("attend") or ()),
        retire=tuple(fm.get("retire") or ()),
        freeze=tuple(fm.get("freeze") or ()),
        deltas=tuple(fm.get("deltas") or ()),
    )
