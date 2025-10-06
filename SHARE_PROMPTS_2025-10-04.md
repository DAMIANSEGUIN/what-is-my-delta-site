# SHARE PROMPTS FOR MOSAIC TEAM - 2025-10-04

## 🎯 **FOR CURSOR (Claude in Cursor) - Semantic Match Upgrade**

```
Hi Cursor,

We’ve landed on a lean semantic matching upgrade that fits the current Mosaic use case and keeps spend tight. Please start with `docs/mosaic_semantic_match_upgrade_plan.md`; it captures the 0–30 day actions to get ~30% match improvement inside a $60 budget buffer and outlines expectations for the following two months.

Context you’ll need:
- CODEX distilled the roadmap and cost guardrails in `docs/mosaic_semantic_match_upgrade_plan.md`.
- Recent reasoning, user feedback, and cost projections are summarized in `CONVERSATION_NOTES.md`.
- Operating boundaries and handoff protocol live in `CODEX_INSTRUCTIONS_REVIEW.md`.

Near-term deliverables (implementation window: ~90 minutes, matching our previous deploy cadence):
1. Implement the embedding upgrade + corpus reindex and commit diffs.
2. Stand up the CPU-hosted cross-encoder reranker, capture latency, and document resource usage.
3. Add logging for pre/post rerank scores and token consumption; expose the metrics (dashboard or CSV).
4. Prep the one-week A/B test once instrumentation is ready, and push outcomes back into `CONVERSATION_NOTES.md`.

Note: the 30-day timeframe in the plan covers the beta test period before the Stage 2 marketing roll-out—don’t let it slow the build.

Please confirm once you’ve reviewed the README and collected any clarifying questions before coding.
```

## 🎯 **FOR CLAUDE CODE - Deployment & Monitoring Support**

```
Hi Claude Code,

Cursor will execute the semantic matching upgrade defined in `docs/mosaic_semantic_match_upgrade_plan.md`. Give the plan a read so you’re ready to assist post-implementation.

Key context:
- The immediate changes stay within a +$60 spending envelope and run on lightweight infra.
- Build execution target is ~90 minutes once Cursor starts; the 30-day horizon is for beta testing before the Stage 2 general-market push.
- We expect a new CPU microservice for the cross-encoder; ensure Railway/hosting capacity can absorb it without surprises.
- Cost telemetry and monitoring must track the extra embedding + rerank usage so we can escalate if the ceiling gets close.

References:
- Plan summary: docs/mosaic_semantic_match_upgrade_plan.md
- Prior deployment guidance: CLAUDE_CODE_HANDOFF_RAG_COST_CONTROLS_2025-10-03.md

For now, just acknowledge that you’re on standby and flag any infra risks you notice up front.
```

---
**Status**: Ready for team circulation once approved
**Primary context doc**: `docs/mosaic_semantic_match_upgrade_plan.md`
