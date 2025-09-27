import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .settings import get_settings
from .startup_checks import startup_or_die

app = FastAPI()

origins = [os.getenv("PUBLIC_SITE_ORIGIN", "https://whatismydelta.com")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET","POST","OPTIONS"],
    allow_headers=["content-type","authorization"],
)

@app.on_event("startup")
async def _startup():
    startup_or_die()

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/config")
def config():
    s = get_settings()
    return {"apiBase": os.getenv("PUBLIC_API_BASE", ""), "schemaVersion": s.APP_SCHEMA_VERSION}
