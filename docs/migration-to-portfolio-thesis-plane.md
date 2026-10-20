# Carry the monthly decision into portfolio-thesis-plane

This repository remains archived. The maintained successor is
`portfolio-thesis-plane`; use it for new portfolio attention decisions. Preserve
old memos and scorecards as dated observations rather than regenerating them from
the current repository state.

Before migrating, retain the portfolio membership file, rubric version, month,
per-repo scores, written rationale and final ATTEND/FREEZE/RETIRE allocation.
Hash that bundle and keep the source paths in a migration manifest. A repo that
has since been renamed or archived should retain its historical identity in the
old month and get an explicit successor mapping for future work.

The count discipline survives the move: the successor still forces two ATTEND
and three RETIRE repos. Its scoring differs. portfolio-thesis-plane scores every
repo each ISO week, 0-20, as the sum of five different factors (its DEC-PTP-001)
read from hand-curated signal files; nobody enters the rubric v0 scores there.
Keep the archived hand scores as recorded. An assistant may retrieve evidence,
summarize changes and draft rationale. It should not silently replace the
person's five-factor scores with inferred scores from commit counts, stars, or
its own enthusiasm for a new feature. If an archived score was never filled in,
leave it blank; do not backfill it. In portfolio-thesis-plane, a repo with no
curated signals scores 0 and can be forced into RETIRE, so give each migrated
repo signals before reading its first weekly result as a decision.

For the first migrated week, compare the successor's allocation with the last
archived month for the repos both registries list. Only dream-replay-cli
appears in both today, so the comparison covers that one repo; the other
nineteen archived repos keep their last monthly verdict as a dated record. The
successor's committed weeks (2026-W25 and 2026-W26) predate this archive, so
that first week still has to be curated and generated there. Explain any change
in classification. Because the successor uses a different rubric and cadence, treat
the switch as an explicit new decision and preserve the old scores without
converting them into apparently comparable numbers.

This is a manual migration recipe, not a newly shipped converter, and it leaves
this archived project's monthly records intact.
