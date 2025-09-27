# Rolling Checklist (Gated)

| Step | What | Owner | Where | Status |
|---|---|---|---|---|
| 0.1 | Add `.gitignore` / `.env.example` | AI | repo | ✅ |
| 0.2 | Add GitHub Secret Scan action | AI | `.github/workflows/secret-scan.yml` | ✅ |
| 0.3 | Move secrets to Railway Variables | YOU | Railway UI | ✅ |
| 0.4 | Scan repo for secrets | AI | CI PR check | ☐ |
| 0.5 | Startup tripwire wired | AI | `api/settings.py`, `api/startup_checks.py` | ✅ |
| 0.6 | Strict CORS + `/config` | AI | `api/index.py` | ✅ |
| 0.7 | Frontend uses `/config.apiBase` | AI | frontend | ☐ |
| 0.8 | No client-side provider calls | AI | frontend/backend audit | ☐ |
| 4.1 | Custom domain setup | YOU | Netlify DNS → Railway | ✅ |
| 4.2 | Domain verification | AI | Railway dashboard | ✅ |
| 4.3 | SSL certificate | AI | Railway automatic | ✅ |
| 1.1 | Start cmd/health fixed | AI | `Procfile`, `railway.json` | ✅ |
| 1.2 | Set required envs | YOU | Railway Variables | ✅ |
| 1.3 | Deploy + smoke test | AI | logs + `verify_deploy.sh` | ✅ |
| 2.1 | Prompts registry implemented | AI | `api/prompts_loader.py` | ✅ |
| 2.2 | Ingest latest CSV | YOU | admin/upload | ✅ |
| 2.3 | Verify active SHA | AI | registry/endpoint | ✅ |
| 3.1 | Pre-deploy sanity | AI | `scripts/predeploy_sanity.sh` | ✅ |
| 3.2 | (Opt) DB + Alembic head | AI/YOU | DB/Alembic | ☐ |
| 3.3 | Final deploy + smoke | AI | `verify_deploy.sh` | ✅ |
