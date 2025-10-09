import asyncio
import os

import httpx

from .storage import cleanup_expired_sessions, init_db
from .settings import get_settings
from .migrations import run_migration

async def ping_openai(client):
    k=os.getenv("OPENAI_API_KEY")
    if not k: 
        print("OPENAI_API_KEY not set, skipping ping")
        return
    try:
        r=await client.get("https://api.openai.com/v1/models",
                           headers={"Authorization": f"Bearer {k}"}, timeout=10.0)
        r.raise_for_status()
        print("OpenAI API ping successful")
    except Exception as e:
        print(f"OpenAI API ping failed: {e}")

async def ping_anthropic(client):
    k=os.getenv("CLAUDE_API_KEY")
    if not k: 
        print("CLAUDE_API_KEY not set, skipping ping")
        return
    try:
        r=await client.get("https://api.anthropic.com/v1/models",
                           headers={"x-api-key": k, "anthropic-version": "2023-06-01"}, timeout=10.0)
        r.raise_for_status()
        print("Anthropic API ping successful")
    except Exception as e:
        print(f"Anthropic API ping failed: {e}")

async def run():
    _ = get_settings()
    init_db()

    # Run migration to sync feature flags from JSON to database
    try:
        print("Running feature flag sync migration...")
        result = run_migration("004_sync_feature_flags_from_json", dry_run=False)
        if result.get("success"):
            print("✅ Feature flags synced to database")
        else:
            print("⚠️ Feature flag sync failed, but continuing startup")
    except Exception as e:
        print(f"⚠️ Migration error: {e}, continuing startup")

    cleanup_expired_sessions()
    print("Settings loaded successfully")
    async with httpx.AsyncClient() as client:
        await asyncio.gather(ping_openai(client), ping_anthropic(client))

async def startup_or_die():
    print("Starting up...")
    await run()
    print("Startup complete")
