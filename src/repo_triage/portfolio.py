"""Portfolio loader.

The portfolio is the canonical list of active repos the monthly memo
scores against. It lives in ``config/portfolio.yaml`` as a list of
``{slug, thesis}`` records.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml


@dataclass(frozen=True)
class PortfolioRepo:
    slug: str
    thesis: str


@dataclass(frozen=True)
class Portfolio:
    version: str
    repos: tuple[PortfolioRepo, ...]

    @property
    def slugs(self) -> tuple[str, ...]:
        return tuple(r.slug for r in self.repos)

    def get(self, slug: str) -> PortfolioRepo:
        for r in self.repos:
            if r.slug == slug:
                return r
        raise KeyError(f"repo not in portfolio: {slug}")


def load_portfolio(path: str | Path) -> Portfolio:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"portfolio file must be a mapping, got {type(raw).__name__}")
    version = str(raw.get("version", "v0"))
    repos_raw = raw.get("repos", [])
    if not isinstance(repos_raw, list):
        raise ValueError("portfolio.repos must be a list")
    repos = tuple(_parse_repo(r) for r in repos_raw)
    slugs = [r.slug for r in repos]
    if len(slugs) != len(set(slugs)):
        dupes = sorted({s for s in slugs if slugs.count(s) > 1})
        raise ValueError(f"duplicate slugs in portfolio: {dupes}")
    return Portfolio(version=version, repos=repos)


def _parse_repo(raw: object) -> PortfolioRepo:
    if not isinstance(raw, dict):
        raise ValueError(f"portfolio repo entry must be a mapping, got {raw!r}")
    slug = raw.get("slug")
    thesis = raw.get("thesis", "")
    if not isinstance(slug, str) or not slug:
        raise ValueError(f"portfolio repo missing slug: {raw!r}")
    if not isinstance(thesis, str):
        raise ValueError(f"portfolio repo thesis must be a string: {raw!r}")
    return PortfolioRepo(slug=slug, thesis=thesis)


def iter_slugs(repos: Iterable[PortfolioRepo]) -> Iterable[str]:
    for r in repos:
        yield r.slug
