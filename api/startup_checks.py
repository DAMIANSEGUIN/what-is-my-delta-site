import asyncio, httpx, os
from .settings import get_settings

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
    print("Settings loaded successfully")
    async with httpx.AsyncClient() as client:
        await asyncio.gather(ping_openai(client), ping_anthropic(client))

async def startup_or_die():
    print("Starting up...")
    await run()
    print("Startup complete")
