# AI Routing Plan (CSV → AI → Metrics Fallback)

This document is the authoritative specification for coach responses. All agents must keep it synchronized with implementation.

## Flow Overview

1. **Primary Source – CSV Library**
   - Load prompts from `data/prompts_{sha}.json` via `api/prompts_loader.py`.
   - Score relevance between the user prompt and each entry (see Matching Rules).
   - If best score ≥ `CSV_MATCH_THRESHOLD` (default 0.55), return that prompt’s completion.

2. **Secondary Source – AI APIs**
   - If the CSV score is below threshold or the library is unavailable, call the configured AI provider (OpenAI or Anthropic) using session metrics/context.
   - Provider selection controlled by `AI_PRIMARY_PROVIDER`; fallback provider optional (`AI_SECONDARY_PROVIDER`).
   - Respect `AI_TIMEOUT_SECS`, emit structured logs on failure, and surface the AI-generated reply when successful.

3. **Safety Net – Metrics-Based Message**
   - When CSV lookup fails *and* every AI attempt errors or times out, respond with `_fallback_reply(metrics)` to keep the chat responsive and transparent.

## Matching Rules (Stage 1)

- Compute relevance via keyword/phrase similarity (initial implementation may use stdlib `difflib`; later upgrades can replace with embeddings without changing the contract).
- Threshold configurable through `CSV_MATCH_THRESHOLD` environment variable.
- Always record the match score and chosen path (CSV / AI / fallback) for observability.

## AI Invocation (Stage 2)

- Encapsulate provider logic in `api/ai_clients.py` with a common interface: `generate_reply(prompt, metrics, context) -> str`.
- Inputs must include:
  - User prompt text
  - Current metrics snapshot (`clarity`, `action`, `momentum`)
  - Optional session context (recent prompts, job targets)
- Providers pull credentials from `Settings` (`OPENAI_API_KEY`, `CLAUDE_API_KEY`).
- Errors should raise custom exceptions so `_coach_reply` can distinguish between retry-worthy and terminal failures.

## Configuration

| Variable | Default | Description |
| --- | --- | --- |
| `CSV_MATCH_THRESHOLD` | `0.55` | Minimum relevance to accept CSV answer |
| `AI_FALLBACK_ENABLED` | `true` | Feature flag for Stage 2 |
| `AI_PRIMARY_PROVIDER` | `openai` | `openai` or `anthropic` |
| `AI_SECONDARY_PROVIDER` | _(optional)_ | Optional backup provider |
| `AI_TIMEOUT_SECS` | `8` | Timeout per provider request |

Document any change to these defaults in this file and `OPERATIONS_MANUAL.md`.

## Implementation Checklist

1. Refactor `_coach_reply` to consume a selector module that returns `(completion, score, metadata)`.
2. Add AI client abstraction with structured error handling.
3. Update `requirements.txt` with provider SDKs (`openai`, `anthropic`).
4. Extend `api/settings.py` for new env vars.
5. Write unit tests covering CSV hit/miss, AI success, AI failure → fallback.
6. Update `scripts/verify_deploy.sh` (or new script) to smoke-test all three stages.

## Logging & Telemetry

- Emit structured log events (e.g., `chat_path="csv"`, `chat_path="ai"`, `chat_path="fallback"`).
- Capture AI errors with enough detail for debugging but without leaking sensitive payloads.
- Surface summary stats in ops dashboards when available.

## Maintenance Notes

- Keep `prompts.csv` canonical; regenerate derived JSON via `ingest_prompts` before deploys.
- Revisit threshold and matching strategy after collecting real usage metrics.
- If providers change, update this plan, `PROJECT_STRUCTURE.md`, and `CONVERSATION_NOTES.md` before coding.

