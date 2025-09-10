from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import os

# Import your project logic from api/core/mosaic.py
from .core.mosaic import run_wimd, run_jobsearch

app = FastAPI(title="Mosaic API (WIMD + JSM)", version="1.0.0")

class WIMDRequest(BaseModel):
    prompt: str = Field(..., description="User prompt or profile text")

class JobSearchRequest(BaseModel):
    query: str = Field(..., description="Search keywords")
    location: Optional[str] = Field(default="Toronto, ON", description="City/region filter")
    max_results: int = Field(default=25, ge=1, le=200)

@app.get("/")
def root():
    return {
        "message": "Mosaic API Server",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "wimd": "POST /wimd",
            "jobsearch": "POST /jobsearch",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/wimd")
def wimd(req: WIMDRequest):
    try:
        result = run_wimd(req.prompt)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/jobsearch")
def jobsearch(req: JobSearchRequest):
    try:
        result = run_jobsearch(query=req.query, location=req.location, max_results=req.max_results)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
