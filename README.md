# 🚦 WIMD Railway Deploy – Restart Protocol

Run this to begin every session:

```zsh
/Users/damianseguin/restart_wimd.sh
```

The script auto-loads APP_URL from wimd_config.sh (asks once, then saves), runs update_status.sh, logs to DEPLOY_STATUS_NOTE.md, and prints the last 10 lines.

---

# 📝 WIMD Railway Deploy – Context Note

> Action on Restart: run ~/restart_wimd.sh (auto-logs status; URL saved in wimd_config.sh)

## Required Env Vars (Railway → Variables)
OPENAI_API_KEY=sk-xxx
CLAUDE_API_KEY=sk-ant-xxx
PUBLIC_SITE_ORIGIN=https://whatismydelta.com
PUBLIC_API_BASE=
DATABASE_URL=
SENTRY_DSN=
APP_SCHEMA_VERSION=v1

## API Endpoints
- `GET /health` — basic health probe
- `GET /config` — returns `{ apiBase, schemaVersion }`
- `GET /prompts/active` — returns `{ active }` (may be null until a CSV is ingested)

## Verify Deploy
```zsh
./scripts/predeploy_sanity.sh
./scripts/verify_deploy.sh "$PUBLIC_API_BASE"
```

## One-Shot Fresh Deploy (New Railway Project)
- Run to create a brand-new Railway project, set variables, and deploy:
  
  ```zsh
  ./scripts/one_shot_new_deploy.sh
  ```

- Notes:
  - It does not delete your existing Railway project; it creates a new one with a timestamped name.
  - You’ll be prompted for variables based on `.env.example`.
  - After deploy, copy the service URL to `PUBLIC_API_BASE` as needed and re-run `./scripts/verify_deploy.sh`.
  - If you want to remove the old service/project, do so from the Railway dashboard to avoid accidental data loss.

## Railway Variables (Build vs Runtime)
- In the Railway service → Variables, ensure each variable is:
  - Scoped to the correct environment (e.g., Production)
  - Marked "Available during deploy" so Nixpacks can access it at build time
- Typical vars: `OPENAI_API_KEY`, `CLAUDE_API_KEY`, `PUBLIC_API_BASE`, `PUBLIC_SITE_ORIGIN`, `APP_SCHEMA_VERSION`

If build fails with "secret NAME: not found":
- The variable likely isn’t marked "Available during deploy" or isn’t defined for this service/environment.
- Toggle it on and redeploy.
