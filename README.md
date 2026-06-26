# repo-triage

Twenty active repos. Every month the rubric forces exactly two onto the ATTEND
list, three into RETIRE, and leaves the other fifteen frozen. The counts are
non-negotiable, which is the whole point — you can't attend to everything, so the
memo makes you say out loud what you're dropping.

## What it does

Attention drifts to whichever repo emitted the most recent salient signal: a green
CI, a kind reply, an idea at breakfast. The loudest repo wins the month, not the one
that most needs the month. repo-triage replaces the feeling with a written rule.

Each active repo is hand-scored 0-15 against a five-factor thesis-alive rubric. The
top two by composite score get ATTEND — next month's shipping time goes there. The
bottom three get RETIRE: archived, revived only on a new written rationale. Everyone
else gets FREEZE: still alive, no attention this month. The rubric is a checklist a
person fills in once per repo per month, not LLM vibes. A model can draft the
rationale; it does not assign the score. One file per month is the artifact; the
forced 2/3/rest counts are the discipline.

## Try it

No arguments. It reads the committed memo (`repo_triage/2026-M07.md`) and its scoring
stubs, then prints every portfolio repo ranked by composite score with its forced
bucket:

```bash
python -m uv run repo-triage show
```

```
repo triage - 2026-07  (rubric v0)
ranked by composite thesis-alive score (0-15); attention is forced:
  2 ATTEND  /  3 RETIRE  /  rest FREEZE

  rank  score  bucket   repo
     1  15/15  ATTEND   grid-silicon
     2  14/15  ATTEND   dream-replay-cli
     3  12/15  FREEZE   cdcp-control-plane
    ...
    20   0/15  RETIRE   quux-prototype

this month's shipping attention: grid-silicon, dream-replay-cli
```

The ranked list is the point. grid-silicon at 15/15 buys the month; quux-prototype
at 0/15 gets archived. The rubric decides, not the most recent green checkmark.

## Live demo

`streamlit_app.py` (repo root) is the `show` verb as an interactive page: the same
ranked attention table, 2-3 summary metrics, a bucket filter, and per-repo rubric
evidence. It reads the committed memo and scoring stubs directly — no network, no
secrets.

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Deploy on Streamlit Community Cloud: new app → repo `AthenaTheOwl/repo-triage`,
branch `main`, main file `streamlit_app.py`.

<!-- live url: https://<your-app>.streamlit.app (fill in after first deploy) -->

## How to run

```bash
python -m uv sync

# day 1 of the month — emit one hand-fill stub per portfolio repo
python -m uv run repo-triage score-template \
    --portfolio config/portfolio.yaml \
    --rubric rules/v0.md \
    --month 2026-07 \
    --out scoring/2026-M07/

# days 2-4 — the operator fills in each stub by hand

# day 5 — render the memo and run the four gates
python -m uv run repo-triage render-memo \
    --scoring scoring/2026-M07/ \
    --portfolio config/portfolio.yaml \
    --rubric rules/v0.md \
    --month 2026-07 \
    --out repo_triage/2026-M07.md

python -m uv run repo-triage enforce-counts repo_triage/2026-M07.md --portfolio config/portfolio.yaml
python -m uv run repo-triage validate-schemas repo_triage/2026-M07.md --memo-schema schemas/memo.schema.json --scoring-schema schemas/scoring.schema.json --scoring-dir scoring/2026-M07/
python -m uv run repo-triage rubric-pinned repo_triage/2026-M07.md --rubric rules/v0.md
python -m uv run repo-triage voice-lint repo_triage/2026-M07.md
```

The four gates are the teeth: `enforce-counts` refuses a memo that doesn't hit
2/3/rest, `validate-schemas` checks the typed shape, `rubric-pinned` confirms the
score came from the committed rubric and not a later edit, `voice-lint` keeps the
prose honest. CI runs all four on every PR. See `docs/methodology.md` for why the
discipline looks this way, and `docs/system-map.md` for the file-level orientation.

## How it connects

[cdcp-control-plane](https://github.com/AthenaTheOwl/cdcp-control-plane) is the
downstream consumer — it takes the typed monthly memo as an input artifact, so the
attention decision made here flows into the control plane rather than living in
someone's head. In this month's run cdcp-control-plane itself scores 12/15 and lands
in FREEZE, which is the system declining to make an exception for the thing
consuming it.

## Layout

```
repo-triage/
  src/repo_triage/        portfolio, rubric, scoring, memo, cli
  rules/v0.md             the 5-factor rubric
  config/portfolio.yaml   the 20 active portfolio repos
  schemas/                scoring.schema.json, memo.schema.json
  scoring/2026-M07/       one hand-filled stub per repo
  repo_triage/2026-M07.md the first monthly memo
  scripts/                thin shims over the CLI
  streamlit_app.py        the show verb as a page
  tests/  docs/  specs/  .github/workflows/ci.yml
```

## License

MIT. See `LICENSE`.
</content>
</invoke>
