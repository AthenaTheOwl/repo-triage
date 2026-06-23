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

from repo_triage.memo import _bucket  # noqa: E402
from repo_triage.memo import load_memo  # noqa: E402
from repo_triage.rubric import FACTOR_KEYS  # noqa: E402
from repo_triage.scoring import ScoringStub, parse_stub  # noqa: E402

FACTOR_TITLES = {
    "thesis_still_credible": "thesis still credible",
    "pull_from_outside": "pull from outside",
    "shippable_next_step": "shippable next step",
    "cost_of_freeze": "cost of freeze",
    "dependency_in_portfolio": "dependency in the portfolio",
}

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

# --- interactive: re-score and re-rank with the real engine --------------------
st.markdown("---")
st.markdown("## re-score a repo yourself — drive the real ranking engine")
st.caption(
    "the table above reads the committed memo. below you edit the 0-3 factor "
    "scores for any repo and the page re-runs the actual engine: "
    "`ScoringStub.composite` for the per-repo totals and `repo_triage.memo._bucket` "
    "for the forced 2 ATTEND / 3 RETIRE / rest FREEZE split. nothing here is "
    "hardcoded — change a slider and watch the buckets re-rank live."
)

edit_repo = st.selectbox(
    "repo to re-score",
    options=[r["repo"] for r in rows],
    help="pre-filled with this repo's committed scores; edit them below",
)

base_stub = stubs[edit_repo]
st.markdown(f"**editing `{edit_repo}`** — committed composite {base_stub.composite}/15")

new_scores: dict[str, int] = {}
cols = st.columns(len(FACTOR_KEYS))
for col, k in zip(cols, FACTOR_KEYS):
    new_scores[k] = col.slider(
        FACTOR_TITLES.get(k, k),
        min_value=0,
        max_value=3,
        value=int(base_stub.scores.get(k, 0)),
        key=f"slider_{k}",
        help="0-3 per the v0 rubric",
    )

# Build a fresh stub for the edited repo and run the REAL composite property.
edited_stub = ScoringStub(
    repo=base_stub.repo,
    month=base_stub.month,
    rubric_version=base_stub.rubric_version,
    scores=new_scores,
    evidence=base_stub.evidence,
    author=base_stub.author,
)

delta = edited_stub.composite - base_stub.composite
st.metric(
    f"{edit_repo} composite /15",
    edited_stub.composite,
    delta=delta if delta else None,
    help="recomputed live by ScoringStub.composite (sum of the five factors)",
)

# Swap the edited stub into the full set and re-run the REAL bucketing engine.
live_stubs = [edited_stub if s.repo == edit_repo else s for s in stubs.values()]
attend, retire, freeze = _bucket(live_stubs)
live_bucket: dict[str, str] = {}
for slug in attend:
    live_bucket[slug] = "ATTEND"
for slug in retire:
    live_bucket[slug] = "RETIRE"
for slug in freeze:
    live_bucket[slug] = "FREEZE"

composite_of = {s.repo: s.composite for s in live_stubs}
live_rows = sorted(
    ({"repo": s.repo, "composite": s.composite, "bucket": live_bucket.get(s.repo, "?")} for s in live_stubs),
    key=lambda r: (ORDER[r["bucket"]], -r["composite"], r["repo"]),
)

new_bucket = live_bucket.get(edit_repo, "?")
old_bucket = bucket_of.get(edit_repo, "?")
if new_bucket != old_bucket:
    st.warning(
        f"with your scores, **{edit_repo}** moves from **{old_bucket}** to "
        f"**{new_bucket}**."
    )
else:
    st.info(f"with your scores, **{edit_repo}** stays in **{new_bucket}**.")

st.markdown("**live ranking (your edit applied, real engine):**")
st.dataframe(
    [
        {
            "rank": i,
            "score /15": r["composite"],
            "bucket": r["bucket"],
            "repo": r["repo"] + ("  ← edited" if r["repo"] == edit_repo else ""),
        }
        for i, r in enumerate(live_rows, start=1)
    ],
    use_container_width=True,
    hide_index=True,
)
st.caption(
    f"ATTEND: {', '.join(attend)}  ·  RETIRE: {', '.join(retire)}  ·  "
    f"FREEZE: {len(freeze)} held. "
    "this split is produced by the same `_bucket` function the CLI uses to write "
    "the monthly memo."
)
