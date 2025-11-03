# Mosaic Semantic Match Upgrade Plan (Q4 2025)

## Purpose
- Document a cost-aware path to improve Mosaic's job-to-resume semantic matching by ~30% without exceeding an extra $60 in the next 30 days.
- Provide Cursor (implementation) and Claude Code (deployment) a clear runbook that aligns with CODEX_INSTRUCTIONS and Mosaic's team protocols.

## Guiding Principles
- Prioritise measurable match-quality lift over feature expansion.
- Keep infra changes lightweight; revisit heavier orchestration only if Mosaic's content profile grows beyond curated résumés + job specs.
- Maintain handoff discipline: CODEX plans, Cursor builds/tests locally, Claude Code assists only for deployment/infrastructure issues.
- Capture observability from day one so future scaling decisions are data-backed.

## Immediate Enhancements (0–30 Days)
**Budget Guardrail:** <= $60 incremental spend

1. **Embedding Upgrade & Reindex** (Owner: Cursor)
   - Swap current embeddings to `text-embedding-3-small` or Cohere Embed Lite (whichever is already available) and re-embed existing résumé/job corpora.
   - Expected lift: +20–25% recall gain on internal evaluation set.
   - Cost: ≈ $25 for re-embed + fresh traffic.

2. **Lightweight Cross-Encoder Rerank** (Owner: Cursor)
   - Deploy `cross-encoder/ms-marco-MiniLM-L-6-v2` on a CPU container; rerank top 10 retrieval hits per query.
   - Target latency overhead <150 ms; infra cost ≈ $20 for the month using a small autoscaling instance.

3. **Scoring & Telemetry Improvements** (Owner: CODEX → Cursor)
   - Add normalized cosine scoring, simple keyword boosts, and log pre/post-rerank scores in analytics.
   - Ship an internal dashboard (or CSV export) that tracks match score distribution, rerank lift, and token usage.
   - Cost: engineering time only.

4. **A/B Validation Sprint** (Owner: CODEX for design, Cursor for execution)
   - Run 1-week experiment with existing beta users; success criteria = ≥30% increase in high-quality matches (manual spot-check) and no latency >1.2 s at P95.
   - Document findings in `CONVERSATION_NOTES.md` for future reference.

## Month-by-Month Roadmap (90 Days)
- **Month 1 (Now):** Deliver immediate enhancements above; finalize evaluation rubric and instrumentation. Compile before/after metrics in a short addendum to this README.
- **Month 2:** Introduce selective sparse boost (BM25/TF-IDF) only for low-confidence matches, refine rerank thresholds, and expand labeled evaluation set using user feedback. Budget impact: +$80 max (already covered in existing infra).
- **Month 3:** Add caching for frequent queries, automate weekly re-embeds, and prepare optional GPU-based reranker path if demand rises. Reassess vendor commitments with actual usage data before scaling spend.

## Metrics & Checkpoints
- Primary KPI: Match score (or acceptance rate) uplift vs baseline; target ≥30% by end of Month 1.
- Secondary KPIs: P95 latency (<1.2 s), monthly token spend (<$400), rerank hit rate, manual QA approval rate.
- Review cadence: Weekly stand-up notes (Cursor), bi-weekly planning check-in (CODEX → Human), monthly budget review.

## Alignment with Team Roles & Protocols
- **CODEX (Planning):** Owns ongoing documentation updates, evaluation design, and handoff specs per `CODEX_INSTRUCTIONS`.
- **Cursor (Claude in Cursor):** Executes embedding swap, reranker deployment, and telemetry wiring in the local environment; reports diffs/tests.
- **Claude Code:** On-call only if deployment infra or Railway configuration work emerges.
- **Human Gatekeeper:** Approves any spend increases, manages secrets/API keys, and greenlights production deploys.

## Risks & Mitigations
- **Latency creep:** Mitigate with small rerank candidate set (≤10) and monitor P95 metrics.
- **Cost overruns:** Enable token usage logging; freeze additional features if spend nears $60 cap this month.
- **Data drift:** Schedule weekly corpus health checks and document re-embed cadence.

## Next Actions (Sequence)
1. CODEX: Share this plan with Cursor and annotate required config updates.
2. Cursor: Implement embedding swap + rerank, run smoke tests, capture baseline metrics.
3. CODEX & Cursor: Launch A/B week, review results, update `CONVERSATION_NOTES.md` and this README snapshot if targets met.
