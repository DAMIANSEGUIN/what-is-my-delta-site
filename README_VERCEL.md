# Mosaic API on Vercel (FastAPI)

This package exposes your Mosaic project (WIMD + JobSearchMaster) as HTTP endpoints using **FastAPI** on **Vercel**.

## Endpoints
- `GET /health` — quick check
- `POST /wimd` — `{ "prompt": "..." }`
- `POST /jobsearch` — `{ "query": "...", "location": "Toronto, ON", "max_results": 25 }`

## Quick Deploy (no choices)
1. Create a **private GitHub repo** (e.g., `mosaic-vercel-api`).
2. Add these files and push the repo.
3. Go to **Vercel** → **New Project** → import your repo.
4. Vercel auto-detects Python and deploys using `vercel.json`:
   - runtime: `python3.11`
   - functions: `/api/index.py`
5. Set **Environment Variables** in Vercel → Project → Settings:
   - e.g., `OPENAI_API_KEY`, any API keys your code needs.
6. Click **Deploy**. You will get a URL like `https://<project>.vercel.app`.

### Test
- `GET https://<project>.vercel.app/health`
- `POST https://<project>.vercel.app/wimd` with `{ "prompt": "hello" }`
- `POST https://<project>.vercel.app/jobsearch` with `{ "query": "python developer" }`

## Wire Your Real Logic
Edit `api/core/mosaic.py` and replace the stub functions with your real code calls.
Typical steps:
- Move your modules from `~/Downloads/Mosaic/` into `api/core/` (or create subfolders).
- Update imports in `api/core/mosaic.py` to call your actual engines.

Example:
```python
from .wimd.engine import generate_profile
from .jsm.pipeline import run_search

def run_wimd(prompt: str):
    return generate_profile(prompt)

def run_jobsearch(query: str, location: str, max_results: int):
    return run_search(query=query, location=location, limit=max_results)
```

Commit and push. Vercel redeploys automatically.

## Local Dev (optional)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# run locally with uvicorn
pip install uvicorn
uvicorn api.index:app --reload --port 8000
# open http://127.0.0.1:8000/docs
```

## Notes
- Keep secrets out of code. Use Vercel **Environment Variables**.
- If your job search needs scheduled runs, consider moving scheduled tasks to
  - Vercel cron jobs (Scheduled Functions), or
  - a small worker on **Render** calling your Vercel endpoints.
