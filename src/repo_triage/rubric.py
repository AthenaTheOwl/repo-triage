"""Rubric loader.

Parses ``rules/v<N>.md`` into a small in-memory object. The rubric is
authored by hand; this loader only extracts the version stamp and the
five factor keys so other modules can pin and validate against them.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


FACTOR_KEYS: tuple[str, ...] = (
    "thesis_still_credible",
    "pull_from_outside",
    "shippable_next_step",
    "cost_of_freeze",
    "dependency_in_portfolio",
)


@dataclass(frozen=True)
class RubricFactor:
    key: str
    title: str


@dataclass(frozen=True)
class Rubric:
    version: str
    factors: tuple[RubricFactor, ...]

    @property
    def keys(self) -> tuple[str, ...]:
        return tuple(f.key for f in self.factors)


_VERSION_RE = re.compile(r"^---\s*\nversion:\s*(?P<v>[^\n]+)\n", re.MULTILINE)
_FACTOR_RE = re.compile(r"^###\s+(?P<key>[a-z_]+)\s*[—-]\s*(?P<title>.+)$", re.MULTILINE)


def load_rubric(path: str | Path) -> Rubric:
    text = Path(path).read_text(encoding="utf-8")
    m = _VERSION_RE.search(text)
    if not m:
        raise ValueError(f"rubric file missing version front-matter: {path}")
    version = m.group("v").strip()

    factors_found = [
        RubricFactor(key=fm.group("key").strip(), title=fm.group("title").strip())
        for fm in _FACTOR_RE.finditer(text)
    ]
    keys = tuple(f.key for f in factors_found)
    if keys != FACTOR_KEYS:
        raise ValueError(
            f"rubric factors must be exactly {FACTOR_KEYS} in order, got {keys}"
        )
    return Rubric(version=version, factors=tuple(factors_found))
