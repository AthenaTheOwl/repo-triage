"""repo-triage — live demo (Streamlit Community Cloud).

Mirrors the no-arg `repo-triage show` verb as an interactive page. Reads the
latest committed monthly memo (repo_triage/*.md) and its hand-filled scoring
stubs (scoring/<month>/*.md) directly off disk — no network, no secrets — and
renders every portfolio repo ranked by composite thesis-alive score with its
forced ATTEND / RETIRE / FREEZE bucket and the binding reason.

Deploy: Streamlit Community Cloud -> New app -> repo AthenaTheOwl/repo-triage,
branch main, main file streamlit_app.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

REPO = Path(__file__).resolve().parent
# The package lives under src/; add it so importing repo_triage works whether or
# not the package was pip-installed. Reading the committed artifacts directly is
# the source of truth either way.
SRC = REPO / "src"
if SRC.exists() and str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from repo_triage.memo import load_memo  # noqa: E402
from repo_triage.rubric import FACTOR_KEYS  # noqa: E402
from repo_triage.scoring import parse_stub  # noqa: E402

ORDER = {"ATTEND": 0, "FREEZE": 1, "RETIRE": 2, "?": 3}


def latest_memo_path() -> Path | None:
    memos = sorted(REPO.glob("repo_triage/[0-9][0-9][0-9][0-9]-M[0-9][0-9].md"))
    return memos[-1] if memos else None


st.set_page_config(page_title="repo-triage — monthly attention memo", layout="wide")
st.title("repo-triage")
st.caption(
    "where does next month's shipping attention go, and why — every portfolio "
    "repo ranked by composite thesis-alive score, with a forced "
    "2 ATTEND / 3 RETIRE / rest FREEZE split."
)

memo_path = latest_memo_path()
if memo_path is None:
    st.warning("no committed memo found under repo_triage/*.md")
    st.stop()

memo = load_memo(memo_path)
month = memo_path.stem  # e.g. 2026-M07

bucket_of: dict[str, str] = {}
for slug in memo.attend:
    bucket_of[slug] = "ATTEND"
for slug in memo.retire:
    bucket_of[slug] = "RETIRE"
for slug in memo.freeze:
    bucket_of[slug] = "FREEZE"

scoring_dir = REPO / "scoring" / month
stub_paths = sorted(scoring_dir.glob("*.md"))
if not stub_paths:
    st.warning(f"no scoring stubs found under scoring/{month}/")
    st.stop()

stubs = {p.stem: parse_stub(p) for p in stub_paths}

st.subheader(f"{memo.month}  ·  rubric {memo.rubric_version}")

c1, c2, c3 = st.columns(3)
c1.metric("repos scored", len(stubs))
c2.metric("on ATTEND", len(memo.attend), help="next month's shipping attention")
c3.metric("on RETIRE", len(memo.retire), help="archived; needs a written revival rationale")

# --- ranked table (mirrors the show verb's ordering) ---------------------------
rows = []
for slug, stub in stubs.items():
    rows.append(
        {
            "composite": stub.composite,
            "repo": stub.repo,
            "bucket": bucket_of.get(stub.repo, "?"),
        }
    )
rows.sort(key=lambda r: (ORDER[r["bucket"]], -r["composite"], r["repo"]))
for i, r in enumerate(rows, start=1):
    r["rank"] = i

buckets_present = sorted({r["bucket"] for r in rows}, key=lambda b: ORDER[b])
chosen = st.multiselect(
    "show buckets",
    options=buckets_present,
    default=buckets_present,
    help="filter the ranked table by forced bucket",
)
shown = [r for r in rows if r["bucket"] in chosen] if chosen else rows

st.dataframe(
    [
        {
            "rank": r["rank"],
            "score /15": r["composite"],
            "bucket": r["bucket"],
            "repo": r["repo"],
        }
        for r in shown
    ],
    use_container_width=True,
    hide_index=True,
)

# --- headline finding ----------------------------------------------------------
top = rows[0]
st.success(
    f"**this month's shipping attention:** {', '.join(memo.attend)}. "
    f"top of the ranking is {top['repo']} at {top['composite']}/15. "
    f"archived (needs a written revival rationale): {', '.join(memo.retire)}. "
    f"{len(memo.freeze)} repos held without attention."
)

# --- per-repo evidence ---------------------------------------------------------
st.markdown("### per-repo evidence")
pick = st.selectbox(
    "inspect a repo's rubric scores",
    options=[r["repo"] for r in shown],
    help="the hand-scored 0-3 per factor with one line of evidence each",
)
stub = stubs[pick]
with st.expander(f"{pick} — composite {stub.composite}/15  ({bucket_of.get(pick, '?')})", expanded=True):
    for k in FACTOR_KEYS:
        ev = stub.evidence.get(k, "").strip()
        st.markdown(f"- **{k}** = {stub.scores.get(k, 0)}/3" + (f"  \n  {ev}" if ev else ""))

st.caption(
    "v0.1 ships one calibration month. the rubric + CLI live in `src/repo_triage/`; "
    "this page reads the committed memo and scoring stubs directly. "
    "repo: github.com/AthenaTheOwl/repo-triage"
)
