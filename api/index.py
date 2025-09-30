import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import (
    BackgroundTasks,
    FastAPI,
    File,
    Header,
    HTTPException,
    UploadFile,
)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .settings import get_settings
from .startup_checks import startup_or_die
from .storage import (
    UPLOAD_ROOT,
    add_resume_version,
    ensure_session,
    fetch_job_matches,
    latest_metrics,
    list_resume_versions,
    record_wimd_output,
    session_exists,
    session_summary,
    store_file_upload,
    store_job_matches,
    update_job_match_status,
    wimd_history,
)

app = FastAPI()

MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_BYTES", str(8 * 1024 * 1024)))
DEFAULT_METRICS = {"clarity": 65, "action": 42, "momentum": 33}
JOB_LIBRARY = [
    {
        "job_id": "delta-strategist",
        "role": "Delta Strategist",
        "company": "Mosaic Delta Lab",
        "skills": ["analysis", "storytelling", "experimentation"],
        "values": ["Innovation", "Learning"],
        "location": "Remote",
    },
    {
        "job_id": "ops-navigator",
        "role": "Operations Navigator",
        "company": "What Is My Delta",
        "skills": ["systems", "automation", "collaboration"],
        "values": ["Clarity", "Momentum"],
        "location": "Hybrid — NYC",
    },
    {
        "job_id": "coach-in-residence",
        "role": "Coach In Residence",
        "company": "Opportunity Bridge",
        "skills": ["coaching", "facilitation", "writing"],
        "values": ["Empathy", "Action"],
        "location": "Remote",
    },
    {
        "job_id": "product-scout",
        "role": "Product Scout",
        "company": "Delta Ventures",
        "skills": ["research", "product sense", "communication"],
        "values": ["Discovery", "Autonomy"],
        "location": "Remote",
    },
]

# CORS configuration for Railway deployment


def _build_cors_origins() -> List[str]:
    candidates = [
        os.getenv("PUBLIC_SITE_ORIGIN", ""),
        "https://whatismydelta.com",
        "https://www.whatismydelta.com",
        "https://resonant-crostata-90b706.netlify.app",
    ]
    origins: List[str] = []
    for value in candidates:
        if not value:
            continue
        for item in value.split(","):
            origin = item.strip().rstrip("/")
            if origin:
                origins.append(origin)

    deduped: List[str] = []
    seen = set()
    for origin in origins:
        if origin not in seen:
            deduped.append(origin)
            seen.add(origin)
    return deduped


cors_origins = _build_cors_origins()

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_origin_regex=r"https://(www\.)?whatismydelta\.com",
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["content-type", "authorization", "x-session-id"],
    expose_headers=["*"],
)


class WimdRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class WimdResponse(BaseModel):
    session_id: str
    message: str
    metrics: Dict[str, Any]


class UploadResponse(BaseModel):
    session_id: str
    file: Dict[str, Any]


class OpportunitiesResponse(BaseModel):
    session_id: str
    opportunities: List[Dict[str, Any]]


class ApplyRequest(BaseModel):
    job_id: str = Field(..., min_length=1)
    notes: Optional[str] = None


class ResumeRewriteRequest(BaseModel):
    session_id: Optional[str] = None
    job_id: Optional[str] = None
    version_name: Optional[str] = None
    source_resume: Optional[str] = None


class ResumeCustomizeRequest(BaseModel):
    session_id: Optional[str] = None
    job_id: str = Field(..., min_length=1)
    resume: str = Field(..., min_length=1)
    highlight_skills: Optional[List[str]] = None


class ResumeFeedbackRequest(BaseModel):
    session_id: Optional[str] = None
    resume: str = Field(..., min_length=1)


class ResumeVersionResponse(BaseModel):
    session_id: str
    versions: List[Dict[str, Any]]


def _clamp(value: float) -> int:
    return max(0, min(100, round(value)))


def _update_metrics(prompt: str, current: Dict[str, Any]) -> Dict[str, int]:
    words = len(re.findall(r"\w+", prompt))
    sentiment_boost = 4 if "thank" in prompt.lower() else 0
    clarity = _clamp(current.get("clarity", DEFAULT_METRICS["clarity"]) + min(words // 12, 6) + sentiment_boost)
    action = _clamp(current.get("action", DEFAULT_METRICS["action"]) + min(words // 18, 5))
    momentum = _clamp(current.get("momentum", DEFAULT_METRICS["momentum"]) + min(words // 20, 4))
    return {"clarity": clarity, "action": action, "momentum": momentum}


def _coach_reply(prompt: str, metrics: Dict[str, int]) -> str:
    return (
        "Noted. Here's where you sit right now — "
        f"clarity {metrics['clarity']}%, action {metrics['action']}%, momentum {metrics['momentum']}%. "
        "Pick one lever to nudge next."
    )


def _score_job(metrics: Dict[str, int], job: Dict[str, Any]) -> Dict[str, Any]:
    base = (metrics.get("clarity", 0) * 0.4 + metrics.get("action", 0) * 0.35 + metrics.get("momentum", 0) * 0.25)
    skill_bias = 5 if "analysis" in job["skills"] and metrics.get("clarity", 0) > 70 else 0
    score = _clamp(base + skill_bias)
    return {
        "job_id": job["job_id"],
        "role": job["role"],
        "company": job["company"],
        "location": job["location"],
        "fit_score": score,
        "skills_match": job["skills"],
        "values_match": job["values"],
        "extras": {"source": "mosaic-generator"},
    }


def _generate_matches(metrics: Dict[str, int]) -> List[Dict[str, Any]]:
    matches = [_score_job(metrics, job) for job in JOB_LIBRARY]
    return sorted(matches, key=lambda item: item["fit_score"], reverse=True)


def _rewrite_resume_text(metrics: Dict[str, int], job_id: Optional[str], source: Optional[str]) -> str:
    summary = (
        f"Clarity {metrics.get('clarity', 0)} · Action {metrics.get('action', 0)} · "
        f"Momentum {metrics.get('momentum', 0)}"
    )
    header = "Resume Draft — Mosaic"
    target = f"Target Role: {job_id}" if job_id else "Exploratory Draft"
    body = source.strip() if source else "• Translate delta analysis into narrative impact\n• Highlight fast-track wins"
    return f"{header}\n{target}\nMetrics: {summary}\n\n{body}\n"


def _resolve_session(
    request_session: Optional[str],
    header_session: Optional[str],
    *,
    allow_create: bool,
) -> str:
    candidate = request_session or header_session
    if allow_create:
        return ensure_session(candidate)
    if not candidate or not session_exists(candidate):
        raise HTTPException(status_code=404, detail="session_not_found")
    ensure_session(candidate)
    return candidate


@app.on_event("startup")
async def _startup():
    await startup_or_die()


@app.get("/")
def root():
    s = get_settings()
    return {
        "message": "Mosaic Platform API - Complete Implementation",
        "interface_design": "Integrated with minimal app architecture",
        "deployment_timestamp": datetime.utcnow().isoformat() + "Z",
        "cache_bust": "nuclear_reset_complete",
        "endpoints": {
            "health": "/health",
            "config": "/config",
            "prompts": "/prompts/active",
            "wimd": "/wimd",
            "wimd_upload": "/wimd/upload",
            "wimd_metrics": "/wimd/metrics",
            "wimd_analysis": "/wimd/analysis",
            "ob_opportunities": "/ob/opportunities",
            "ob_matches": "/ob/matches",
            "ob_status": "/ob/status",
            "ob_apply": "/ob/apply",
            "resume_rewrite": "/resume/rewrite",
            "resume_customize": "/resume/customize",
            "resume_feedback": "/resume/feedback",
            "resume_versions": "/resume/versions",
        },
        "schemaVersion": s.APP_SCHEMA_VERSION,
    }


@app.get("/health")
def health():
    return {"ok": True, "timestamp": datetime.utcnow().isoformat() + "Z"}


@app.get("/config")
def config():
    s = get_settings()
    return {"apiBase": os.getenv("PUBLIC_API_BASE", ""), "schemaVersion": s.APP_SCHEMA_VERSION}


@app.get("/prompts/active")
def prompts_active():
    from .prompts_loader import read_registry

    reg = read_registry()
    return {"active": reg.get("active")}


@app.post("/wimd", response_model=WimdResponse)
async def wimd_chat(
    payload: WimdRequest,
    session_header: Optional[str] = Header(None, alias="X-Session-ID"),
):
    session_id = _resolve_session(payload.session_id, session_header, allow_create=True)
    current_metrics = latest_metrics(session_id) or DEFAULT_METRICS
    metrics = _update_metrics(payload.prompt, current_metrics)
    message = _coach_reply(payload.prompt, metrics)
    record_wimd_output(
        session_id,
        payload.prompt,
        message,
        analysis_data={"context": payload.context or {}},
        metrics=metrics,
    )
    return WimdResponse(session_id=session_id, message=message, metrics=metrics)


@app.get("/wimd/metrics")
def wimd_metrics(session_header: Optional[str] = Header(None, alias="X-Session-ID")):
    session_id = _resolve_session(None, session_header, allow_create=False)
    metrics = latest_metrics(session_id)
    if not metrics:
        raise HTTPException(status_code=404, detail="metrics_not_found")
    return {"session_id": session_id, "metrics": metrics}


@app.get("/wimd/analysis")
def wimd_analysis(session_header: Optional[str] = Header(None, alias="X-Session-ID")):
    session_id = _resolve_session(None, session_header, allow_create=False)
    history = wimd_history(session_id)
    return {"session_id": session_id, "history": history}


async def _save_upload(session_id: str, file: UploadFile) -> Dict[str, Any]:
    safe_name = re.sub(r"[^a-zA-Z0-9_.-]", "_", Path(file.filename or "upload").name)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    target = UPLOAD_ROOT / f"{session_id}_{timestamp}_{safe_name}"
    size = 0
    with target.open("wb") as buffer:
        while True:
            chunk = await file.read(1 << 20)
            if not chunk:
                break
            size += len(chunk)
            if size > MAX_UPLOAD_BYTES:
                buffer.close()
                try:
                    target.unlink()
                except FileNotFoundError:
                    pass
                raise HTTPException(status_code=413, detail="file_too_large")
            buffer.write(chunk)
    store_file_upload(session_id, file.filename or safe_name, file.content_type or "application/octet-stream", size, target)
    return {"filename": file.filename or safe_name, "size": size, "content_type": file.content_type}


@app.post("/wimd/upload", response_model=UploadResponse)
async def wimd_upload(
    background: BackgroundTasks,
    file: UploadFile = File(...),
    session_header: Optional[str] = Header(None, alias="X-Session-ID"),
):
    session_id = _resolve_session(None, session_header, allow_create=True)
    if not file.filename:
        raise HTTPException(status_code=400, detail="filename_required")
    meta = await _save_upload(session_id, file)
    background.add_task(file.close)
    metrics = latest_metrics(session_id) or DEFAULT_METRICS
    return UploadResponse(session_id=session_id, file={**meta, "metrics": metrics})


@app.get("/ob/opportunities", response_model=OpportunitiesResponse)
def ob_opportunities(session_header: Optional[str] = Header(None, alias="X-Session-ID")):
    session_id = _resolve_session(None, session_header, allow_create=False)
    metrics = latest_metrics(session_id)
    if not metrics:
        raise HTTPException(status_code=404, detail="metrics_not_ready")
    matches = _generate_matches(metrics)
    store_job_matches(session_id, matches)
    return OpportunitiesResponse(session_id=session_id, opportunities=matches)


@app.get("/ob/matches")
def ob_matches(session_header: Optional[str] = Header(None, alias="X-Session-ID")):
    session_id = _resolve_session(None, session_header, allow_create=False)
    return {"session_id": session_id, "matches": fetch_job_matches(session_id)}


@app.get("/ob/status")
def ob_status(session_header: Optional[str] = Header(None, alias="X-Session-ID")):
    session_id = _resolve_session(None, session_header, allow_create=False)
    matches = fetch_job_matches(session_id)
    applied = [match for match in matches if match.get("extras", {}).get("status") == "applied"]
    return {
        "session_id": session_id,
        "applied": applied,
        "available": matches,
    }


@app.post("/ob/apply")
def ob_apply(
    payload: ApplyRequest,
    session_header: Optional[str] = Header(None, alias="X-Session-ID"),
):
    session_id = _resolve_session(None, session_header, allow_create=False)
    matches = {match["job_id"]: match for match in fetch_job_matches(session_id)}
    if payload.job_id not in matches:
        raise HTTPException(status_code=404, detail="job_match_not_found")
    try:
        update_job_match_status(session_id, payload.job_id, status="applied", notes=payload.notes)
    except ValueError:
        raise HTTPException(status_code=404, detail="job_match_not_found")
    return {
        "session_id": session_id,
        "job": matches[payload.job_id],
        "status": "applied",
        "notes": payload.notes or "",
    }


@app.post("/resume/rewrite")
def resume_rewrite(
    payload: ResumeRewriteRequest,
    session_header: Optional[str] = Header(None, alias="X-Session-ID"),
):
    session_id = _resolve_session(payload.session_id, session_header, allow_create=True)
    metrics = latest_metrics(session_id) or DEFAULT_METRICS
    draft = _rewrite_resume_text(metrics, payload.job_id, payload.source_resume)
    version_name = payload.version_name or f"canonical-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    version_id = add_resume_version(session_id, version_name, draft, payload.job_id)
    return {
        "session_id": session_id,
        "version_id": version_id,
        "version_name": version_name,
        "resume": draft,
    }


@app.post("/resume/customize")
def resume_customize(
    payload: ResumeCustomizeRequest,
    session_header: Optional[str] = Header(None, alias="X-Session-ID"),
):
    session_id = _resolve_session(payload.session_id, session_header, allow_create=False)
    metrics = latest_metrics(session_id) or DEFAULT_METRICS
    highlights = payload.highlight_skills or []
    suffix = "\n\nHighlighted Skills:\n" + "\n".join(f"• {item}" for item in highlights) if highlights else ""
    draft = _rewrite_resume_text(metrics, payload.job_id, payload.resume) + suffix
    version_name = f"custom-{payload.job_id}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    version_id = add_resume_version(session_id, version_name, draft, payload.job_id)
    return {
        "session_id": session_id,
        "version_id": version_id,
        "version_name": version_name,
        "resume": draft,
    }


@app.post("/resume/feedback")
def resume_feedback(
    payload: ResumeFeedbackRequest,
    session_header: Optional[str] = Header(None, alias="X-Session-ID"),
):
    session_id = _resolve_session(payload.session_id, session_header, allow_create=False)
    line_count = payload.resume.count("\n") + 1
    word_count = len(re.findall(r"\w+", payload.resume))
    suggestions = []
    if line_count < 20:
        suggestions.append("Add more evidence-based bullets to demonstrate scope.")
    if "impact" not in payload.resume.lower():
        suggestions.append("Surface measurable impact (e.g., % lift, revenue, time saved).")
    if "summary" not in payload.resume.lower():
        suggestions.append("Consider opening with a 2-3 sentence summary that anchors your delta.")
    add_resume_version(session_id, f"feedback-{datetime.utcnow().strftime('%H%M%S')}", payload.resume, feedback={"suggestions": suggestions})
    return {
        "session_id": session_id,
        "analysis": {"word_count": word_count, "line_count": line_count},
        "suggestions": suggestions,
    }


@app.get("/resume/versions", response_model=ResumeVersionResponse)
def resume_versions(session_header: Optional[str] = Header(None, alias="X-Session-ID")):
    session_id = _resolve_session(None, session_header, allow_create=False)
    versions = list_resume_versions(session_id)
    return ResumeVersionResponse(session_id=session_id, versions=versions)


@app.get("/session/summary")
def session_summary_endpoint(session_header: Optional[str] = Header(None, alias="X-Session-ID")):
    session_id = _resolve_session(None, session_header, allow_create=False)
    return session_summary(session_id)
