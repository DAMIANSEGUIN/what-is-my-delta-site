import os
import re
import logging
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import (
    BackgroundTasks,
    Body,
    FastAPI,
    File,
    Header,
    HTTPException,
    Response,
    UploadFile,
)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import hashlib
import secrets
# import openai  # Temporarily disabled for testing
# import numpy as np  # Temporarily disabled for testing

from .settings import get_settings
from .startup_checks import startup_or_die
from .storage import (
    UPLOAD_ROOT,
    add_resume_version,
    authenticate_user,
    create_user,
    ensure_session,
    fetch_job_matches,
    get_conn,
    get_user_by_email,
    get_user_by_id,
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
from .prompt_selector import get_prompt_response, get_prompt_health
from .monitoring import run_health_check, attempt_system_recovery
from .experiment_engine import (
    ExperimentCreate, ExperimentUpdate, LearningData, CapabilityEvidence, SelfEfficacyMetric,
    create_experiment, update_experiment, complete_experiment, add_learning_data,
    capture_evidence, record_self_efficacy_metric, get_experiments, get_learning_data,
    get_self_efficacy_metrics, get_experiment_health
)
from .self_efficacy_engine import (
    compute_session_metrics, should_escalate, get_escalation_prompt, 
    cleanup_stale_experiments, record_analytics_entry, get_self_efficacy_health
)
from .rag_engine import (
    compute_embedding, batch_compute_embeddings, retrieve_similar, 
    get_rag_response, get_rag_health, discover_domain_adjacent_opportunities_rag
)
from .rag_source_discovery import (
    discover_sources_for_query, get_optimal_sources_for_query, get_discovery_analytics
)
from .cost_controls import check_cost_limits, check_resource_limits, record_usage, get_usage_analytics
from .competitive_intelligence import (
    analyze_company_strategic_needs, develop_competitive_positioning_strategy,
    create_strategic_resume_targeting, generate_job_search_ai_prompts,
    get_competitive_intelligence_health
)
from .osint_forensics import analyze_company_osint, get_osint_health
from .domain_adjacent_search import discover_domain_adjacent_opportunities, get_domain_adjacent_health
from .analytics import get_analytics_dashboard, export_analytics_csv, get_analytics_health
from .reranker import get_reranker_health
from .corpus_reindex import reindex_corpus, get_reindex_status
from .settings import get_feature_flag
from .job_sources import (
    GreenhouseSource, SerpApiSource, RedditSource, IndeedSource,
    LinkedInSource, GlassdoorSource, RemoteOKSource, WeWorkRemotelySource,
    DiceSource, MonsterSource, ZipRecruiterSource, CareerBuilderSource,
    HackerNewsSource
)

app = FastAPI()
logger = logging.getLogger(__name__)
HEALTH_DEBUG_ENABLED = os.getenv("HEALTH_DEBUG", "").lower() in {"1", "true", "yes", "on"}
SERVICE_READY = threading.Event()

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
    # Explicit list - don't rely on env var that might be misconfigured
    return [
        "https://whatismydelta.com",
        "https://www.whatismydelta.com",
        "https://resonant-crostata-90b706.netlify.app",
    ]


cors_origins = _build_cors_origins()

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["content-type", "authorization", "x-session-id"],
    expose_headers=["*"],
)


class WimdRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class UserRegister(BaseModel):
    email: str = Field(..., min_length=1)
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

class UserResponse(BaseModel):
    user_id: str
    email: str
    created_at: str
    last_login: Optional[str] = None


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


def _coach_reply(prompt: str, metrics: Dict[str, int], session_id: str = None) -> str:
    """Generate coach reply using CSV→AI fallback system"""
    from .prompts_loader import read_registry
    import json
    
    try:
        # Get CSV prompts data
        csv_prompts = None
        try:
            reg = read_registry()
            active_sha = reg.get("active")
            if active_sha:
                for version in reg.get("versions", []):
                    if version["sha256"] == active_sha:
                        try:
                            with open(version["file"], "r", encoding="utf-8") as f:
                                prompts_data = json.load(f)
                            csv_prompts = {"prompts": prompts_data}
                            break
                        except Exception:
                            continue
        except Exception:
            pass
        
        # Use prompt selector with CSV→AI fallback
        context = {"metrics": metrics}
        result = get_prompt_response(
            prompt=prompt,
            session_id=session_id or "default",
            csv_prompts=csv_prompts,
            context=context
        )
        
        if result.get("response"):
            return result["response"]
        else:
            return _fallback_reply(metrics)
            
    except Exception:
        return _fallback_reply(metrics)


def _fallback_reply(metrics: Dict[str, int]) -> str:
    """Fallback reply when prompts can't be loaded"""
    return (
        "Noted. Here's where you sit right now — "
        f"clarity {metrics['clarity']}%, action {metrics['action']}%, momentum {metrics['momentum']}%. "
        "Pick one lever to nudge next."
    )


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Calculate cosine similarity between two vectors"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def get_embeddings(text: str) -> List[float]:
    """Get OpenAI embeddings for text"""
    try:
        settings = get_settings()
        if not settings.OPENAI_API_KEY:
            raise ValueError("OpenAI API key not configured")
        
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error getting embeddings: {e}")
        return []


def semantic_search(user_prompt: str, prompts_data: List[Dict], session_history: List[str] = None) -> Optional[Dict]:
    """Find most semantically similar prompt using embeddings"""
    try:
        # Include session history for context
        context_text = user_prompt
        if session_history:
            context_text = f"{user_prompt} Context: {' '.join(session_history[-3:])}"
        
        # Get user prompt embedding
        user_embedding = get_embeddings(context_text)
        if not user_embedding:
            return None
        
        best_match = None
        best_score = 0.0
        
        for prompt in prompts_data:
            prompt_text = prompt.get("completion", "")
            if not prompt_text:
                continue
                
            # Get prompt embedding
            prompt_embedding = get_embeddings(prompt_text)
            if not prompt_embedding:
                continue
            
            # Calculate similarity
            similarity = cosine_similarity(user_embedding, prompt_embedding)
            
            if similarity > best_score:
                best_score = similarity
                best_match = prompt
        
        # Return best match if similarity is above threshold
        return best_match if best_score > 0.7 else None
        
    except Exception as e:
        print(f"Error in semantic search: {e}")
        return None


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
    SERVICE_READY.set()


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
    """Enhanced health check with prompt system monitoring for auto-restart"""
    try:
        if not SERVICE_READY.is_set():
            status = {
                "ok": True,
                "status": "initializing",
                "checks": {
                    "startup_complete": False,
                },
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
            if HEALTH_DEBUG_ENABLED:
                logger.info("Health check in startup grace period: %s", status)
            return status

        # Test critical prompt system functionality
        from .prompt_selector import get_prompt_health
        prompt_health = get_prompt_health()

        # Check if prompt system is working
        fallback_enabled = prompt_health.get("fallback_enabled", False)
        ai_available = prompt_health.get("ai_health", {}).get("any_available", False)

        if HEALTH_DEBUG_ENABLED:
            logger.info(
                "HEALTH CHECK DEBUG fallback_enabled=%s (type=%s) ai_available=%s prompt_health=%s",
                fallback_enabled,
                type(fallback_enabled),
                ai_available,
                prompt_health,
            )

        # System is healthy if either CSV works OR AI fallback is available
        prompt_system_ok = fallback_enabled or ai_available

        # Check database connectivity
        db_ok = True
        try:
            with get_conn() as conn:
                conn.execute("SELECT 1").fetchone()
        except Exception as e:
            logger.error("Database connectivity check failed: %s", e, exc_info=True)
            db_ok = False

        # Overall health
        overall_ok = prompt_system_ok and db_ok

        health_status = {
            "ok": overall_ok,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "checks": {
                "database": db_ok,
                "prompt_system": prompt_system_ok,
                "ai_fallback_enabled": fallback_enabled,
                "ai_available": ai_available
            }
        }

        if HEALTH_DEBUG_ENABLED:
            logger.info(
                "HEALTH CHECK STATUS overall_ok=%s prompt_system_ok=%s db_ok=%s",
                overall_ok,
                prompt_system_ok,
                db_ok,
            )

        # Return 503 if not healthy (triggers Railway restart)
        if not overall_ok:
            logger.warning("Health check failed; returning 503 with status payload %s", health_status)
            raise HTTPException(status_code=503, detail=health_status)

        if HEALTH_DEBUG_ENABLED:
            logger.info("Health check passed")
        return health_status

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Health check raised unexpected exception")
        # Critical failure - return 503 to trigger restart
        raise HTTPException(status_code=503, detail={
            "ok": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })

@app.get("/health/prompts")
def health_prompts():
    """Health check for prompt selector and AI fallback system"""
    try:
        prompt_health = get_prompt_health()
        return {
            "ok": True,
            "prompt_selector": prompt_health,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

@app.get("/health/comprehensive")
def health_comprehensive():
    """Comprehensive health check with automatic recovery"""
    try:
        health_summary = run_health_check()

        # If system needs attention, log it
        if health_summary.get("requires_attention", False):
            print(f"⚠️ Prompt system requires attention: {health_summary}")

        # Return 503 if critical failure to trigger Railway restart
        if not health_summary.get("current_test", {}).get("success", False):
            raise HTTPException(status_code=503, detail=health_summary)

        return health_summary
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail={
            "ok": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })

@app.post("/health/recover")
def health_recover():
    """Attempt automatic system recovery"""
    try:
        recovery_result = attempt_system_recovery()
        return recovery_result
    except Exception as e:
        return {
            "recovery_attempted": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

@app.get("/health/experiments")
def health_experiments():
    """Health check for experiment engine"""
    try:
        experiment_health = get_experiment_health()
        return {
            "ok": True,
            "experiment_engine": experiment_health,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }


@app.get("/config")
def config():
    s = get_settings()
    return {"apiBase": os.getenv("PUBLIC_API_BASE", ""), "schemaVersion": s.APP_SCHEMA_VERSION}


@app.get("/prompts/active")
def prompts_active():
    from .prompts_loader import read_registry

    reg = read_registry()
    return {"active": reg.get("active")}


@app.get("/prompts/{sha}")
def get_prompts(sha: str):
    """Get prompts content by SHA"""
    from .prompts_loader import read_registry
    import json
    
    reg = read_registry()
    if not reg.get("active"):
        raise HTTPException(status_code=404, detail="No active prompts")
    
    # Find the version with this SHA
    for version in reg.get("versions", []):
        if version["sha256"] == sha:
            try:
                with open(version["file"], "r", encoding="utf-8") as f:
                    prompts = json.load(f)
                return {"sha": sha, "prompts": prompts}
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error loading prompts: {str(e)}")
    
    raise HTTPException(status_code=404, detail="Prompts not found")


@app.get("/debug/cors")
def debug_cors():
    """Debug endpoint to show configured CORS origins"""
    return {
        "cors_origins": cors_origins,
        "public_site_origin_env": os.getenv("PUBLIC_SITE_ORIGIN", "NOT SET"),
        "middleware_config": {
            "allow_credentials": True,
            "allow_methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["content-type", "authorization", "x-session-id"],
        }
    }


@app.options("/wimd")
def wimd_options():
    """Explicit OPTIONS handler for Railway edge compatibility"""
    return Response(status_code=200)


@app.post("/wimd", response_model=WimdResponse)
async def wimd_chat(
    payload: WimdRequest,
    session_header: Optional[str] = Header(None, alias="X-Session-ID"),
):
    session_id = _resolve_session(payload.session_id, session_header, allow_create=True)
    current_metrics = latest_metrics(session_id) or DEFAULT_METRICS
    metrics = _update_metrics(payload.prompt, current_metrics)
    message = _coach_reply(payload.prompt, metrics, session_id)
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


@app.options("/wimd/upload")
def wimd_upload_options():
    """Explicit OPTIONS handler for Railway edge compatibility"""
    return Response(status_code=200)


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


@app.options("/ob/apply")
def ob_apply_options():
    """Explicit OPTIONS handler for Railway edge compatibility"""
    return Response(status_code=200)


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


@app.options("/resume/rewrite")
def resume_rewrite_options():
    """Explicit OPTIONS handler for Railway edge compatibility"""
    return Response(status_code=200)


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


@app.options("/resume/customize")
def resume_customize_options():
    """Explicit OPTIONS handler for Railway edge compatibility"""
    return Response(status_code=200)


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


@app.options("/resume/feedback")
def resume_feedback_options():
    """Explicit OPTIONS handler for Railway edge compatibility"""
    return Response(status_code=200)


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


# User Authentication Endpoints
@app.post("/auth/register", response_model=UserResponse)
async def register_user(payload: UserRegister):
    """Register a new user"""
    # Check if user already exists
    existing_user = get_user_by_email(payload.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Create new user
    user_id = create_user(payload.email, payload.password)
    user = get_user_by_id(user_id)
    
    return UserResponse(
        user_id=user["user_id"],
        email=user["email"],
        created_at=user["created_at"],
        last_login=user["last_login"]
    )


@app.post("/auth/login", response_model=UserResponse)
async def login_user(payload: UserLogin):
    """Login user and return user data"""
    user_id = authenticate_user(payload.email, payload.password)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = get_user_by_id(user_id)
    return UserResponse(
        user_id=user["user_id"],
        email=user["email"],
        created_at=user["created_at"],
        last_login=user["last_login"]
    )


@app.get("/auth/me", response_model=UserResponse)
async def get_current_user(user_id: str = Header(..., alias="X-User-ID")):
    """Get current user data"""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(
        user_id=user["user_id"],
        email=user["email"],
        created_at=user["created_at"],
        last_login=user["last_login"]
    )


@app.post("/auth/reset-password")
async def reset_password(email: str = Body(..., embed=True)):
    """Send password reset email (placeholder - needs email service)"""
    # Check if user exists
    conn = get_conn()
    cursor = conn.execute("SELECT user_id FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    if not user:
        # Don't reveal if user exists - security best practice
        return {"message": "If that email exists, a reset link has been sent"}

    # TODO: Implement actual email sending with reset token
    # For now, just return success message
    # In production, you would:
    # 1. Generate a secure reset token
    # 2. Store it in database with expiration
    # 3. Send email with reset link

    return {"message": "If that email exists, a reset link has been sent"}


@app.get("/resume/versions", response_model=ResumeVersionResponse)
def resume_versions(session_header: Optional[str] = Header(None, alias="X-Session-ID")):
    session_id = _resolve_session(None, session_header, allow_create=False)
    versions = list_resume_versions(session_id)
    return ResumeVersionResponse(session_id=session_id, versions=versions)


@app.get("/session/summary")
def session_summary_endpoint(session_header: Optional[str] = Header(None, alias="X-Session-ID")):
    session_id = _resolve_session(None, session_header, allow_create=False)
    return session_summary(session_id)

# Experiment Engine Endpoints
@app.post("/experiments/create")
def experiments_create(
    experiment_data: ExperimentCreate,
    session_header: Optional[str] = Header(None, alias="X-Session-ID")
):
    """Create a new experiment"""
    session_id = _resolve_session(None, session_header, allow_create=True)
    return create_experiment(session_id, experiment_data)

@app.post("/experiments/update")
def experiments_update(
    experiment_data: ExperimentUpdate,
    session_header: Optional[str] = Header(None, alias="X-Session-ID")
):
    """Update an existing experiment"""
    session_id = _resolve_session(None, session_header, allow_create=False)
    return update_experiment(session_id, experiment_data)

@app.post("/experiments/complete")
def experiments_complete(
    experiment_id: str,
    session_header: Optional[str] = Header(None, alias="X-Session-ID")
):
    """Mark an experiment as completed"""
    session_id = _resolve_session(None, session_header, allow_create=False)
    return complete_experiment(session_id, experiment_id)

@app.post("/learning/add")
def learning_add(
    learning_data: LearningData,
    session_header: Optional[str] = Header(None, alias="X-Session-ID")
):
    """Add learning data to an experiment"""
    session_id = _resolve_session(None, session_header, allow_create=False)
    return add_learning_data(session_id, learning_data)

@app.post("/evidence/capture")
def evidence_capture(
    evidence_data: CapabilityEvidence,
    session_header: Optional[str] = Header(None, alias="X-Session-ID")
):
    """Capture capability evidence"""
    session_id = _resolve_session(None, session_header, allow_create=True)
    return capture_evidence(session_id, evidence_data)

@app.post("/metrics/self-efficacy")
def metrics_self_efficacy(
    metric_data: SelfEfficacyMetric,
    session_header: Optional[str] = Header(None, alias="X-Session-ID")
):
    """Record a self-efficacy metric"""
    session_id = _resolve_session(None, session_header, allow_create=True)
    return record_self_efficacy_metric(session_id, metric_data)

@app.get("/experiments")
def experiments_list(session_header: Optional[str] = Header(None, alias="X-Session-ID")):
    """Get all experiments for a session"""
    session_id = _resolve_session(None, session_header, allow_create=False)
    experiments = get_experiments(session_id)
    return {"session_id": session_id, "experiments": experiments}

@app.get("/learning")
def learning_list(
    experiment_id: Optional[str] = None,
    session_header: Optional[str] = Header(None, alias="X-Session-ID")
):
    """Get learning data for a session or specific experiment"""
    session_id = _resolve_session(None, session_header, allow_create=False)
    learning_data = get_learning_data(session_id, experiment_id)
    return {"session_id": session_id, "learning_data": learning_data}

@app.get("/metrics")
def metrics_list(session_header: Optional[str] = Header(None, alias="X-Session-ID")):
    """Get self-efficacy metrics for a session"""
    session_id = _resolve_session(None, session_header, allow_create=False)
    metrics = get_self_efficacy_metrics(session_id)
    return {"session_id": session_id, "metrics": metrics}

# Self-Efficacy Engine Endpoints
@app.get("/self-efficacy/metrics")
def self_efficacy_metrics(session_header: Optional[str] = Header(None, alias="X-Session-ID")):
    """Get computed self-efficacy metrics for a session"""
    session_id = _resolve_session(None, session_header, allow_create=False)
    metrics = compute_session_metrics(session_id)
    
    # Record analytics entry
    record_analytics_entry(session_id, metrics)
    
    return {
        "session_id": session_id,
        "experiment_completion_rate": metrics.experiment_completion_rate,
        "learning_velocity": metrics.learning_velocity,
        "confidence_score": metrics.confidence_score,
        "escalation_risk": metrics.escalation_risk,
        "total_experiments": metrics.total_experiments,
        "completed_experiments": metrics.completed_experiments,
        "learning_events": metrics.learning_events,
        "days_active": metrics.days_active,
        "last_activity": metrics.last_activity,
        "metrics_timestamp": metrics.metrics_timestamp
    }

@app.get("/self-efficacy/escalation")
def self_efficacy_escalation(session_header: Optional[str] = Header(None, alias="X-Session-ID")):
    """Check if session should be escalated to human coach"""
    session_id = _resolve_session(None, session_header, allow_create=False)
    should_esc, reason = should_escalate(session_id)
    prompt = get_escalation_prompt(session_id) if should_esc else None
    
    return {
        "session_id": session_id,
        "should_escalate": should_esc,
        "reason": reason,
        "escalation_prompt": prompt
    }

@app.post("/self-efficacy/cleanup")
def self_efficacy_cleanup(days_threshold: int = 30):
    """Clean up stale experiments (admin endpoint)"""
    result = cleanup_stale_experiments(days_threshold)
    return result

@app.get("/health/self-efficacy")
def health_self_efficacy():
    """Health check for self-efficacy engine"""
    try:
        health = get_self_efficacy_health()
        return {
            "ok": True,
            "self_efficacy_engine": health,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

# RAG Engine Endpoints
@app.post("/rag/embed")
def rag_embed(text: str):
    """Compute embedding for text"""
    try:
        embedding_result = compute_embedding(text)
        if embedding_result:
            return {
                "text": embedding_result.text,
                "hash": embedding_result.hash,
                "model": embedding_result.model,
                "created_at": embedding_result.created_at
            }
        else:
            return {"error": "Failed to compute embedding"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/rag/batch-embed")
def rag_batch_embed(texts: List[str]):
    """Compute embeddings for multiple texts"""
    try:
        results = batch_compute_embeddings(texts)
        return {
            "results": [
                {
                    "text": result.text,
                    "hash": result.hash,
                    "model": result.model,
                    "created_at": result.created_at
                }
                for result in results
            ]
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/rag/embed")
def rag_embed(text: str):
    """Compute embedding for text"""
    try:
        result = compute_embedding(text)
        if result:
            return {
                "text": result.text,
                "embedding": result.embedding,
                "model": result.model,
                "cached": result.cached,
                "created_at": result.created_at
            }
        else:
            return {"error": "Failed to compute embedding"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/rag/batch-embed")
def rag_batch_embed(texts: str):  # Comma-separated texts
    """Batch compute embeddings for multiple texts"""
    try:
        text_list = [t.strip() for t in texts.split(',')]
        results = batch_compute_embeddings(text_list)
        return {
            "texts": text_list,
            "embeddings": [
                {
                    "text": result.text,
                    "embedding": result.embedding,
                    "model": result.model,
                    "cached": result.cached,
                    "created_at": result.created_at
                }
                for result in results
            ],
            "total_processed": len(results)
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/rag/retrieve")
def rag_retrieve(query: str, limit: int = 5, min_similarity: float = 0.7):
    """Retrieve similar content using RAG"""
    try:
        result = retrieve_similar(query, limit, min_similarity)
        return {
            "query": result.query,
            "matches": result.matches,
            "confidence": result.confidence,
            "fallback_used": result.fallback_used,
            "retrieval_time": result.retrieval_time
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/rag/query")
def rag_query(query: str, context: Dict[str, Any] = None):
    """Get RAG response with retrieval and fallback"""
    try:
        result = get_rag_response(query, context)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.post("/rag/domain-adjacent")
def rag_domain_adjacent(request: dict):
    """Discover domain adjacent opportunities using RAG semantic clustering."""
    try:
        user_skills = request.get("user_skills", [])
        user_domains = request.get("user_domains", [])
        
        # Use RAG-powered domain adjacent search
        results = discover_domain_adjacent_opportunities_rag(user_skills, user_domains)
        
        return results
    except Exception as e:
        return {"error": str(e)}

@app.get("/health/rag")
def health_rag():
    """Health check for RAG engine"""
    try:
        health = get_rag_health()
        return {
            "ok": True,
            "rag_engine": health,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

# Job Sources Endpoints
@app.get("/jobs/search")
def jobs_search(query: str, location: str = None, limit: int = 10):
    """Search jobs across all sources"""
    try:
        # Check cost limits first
        cost_check = check_cost_limits("job_search", 0.01)  # $0.01 per job search
        if not cost_check["allowed"]:
            return {
                "error": f"Cost limit exceeded: {cost_check['reason']}",
                "cost_limit": True
            }
        
        # Check resource limits
        resource_check = check_resource_limits("job_search")
        if not resource_check["allowed"]:
            return {
                "error": f"Resource limit exceeded: {resource_check['reason']}",
                "resource_limit": True
            }
        
        # Initialize job sources
        greenhouse = GreenhouseSource()
        serpapi = SerpApiSource()
        reddit = RedditSource()
        
        all_jobs = []
        success_count = 0
        
        # Search each source
        for source in [greenhouse, serpapi, reddit]:
            try:
                jobs = source.search_jobs(query, location, limit)
                all_jobs.extend(jobs)
                success_count += 1
            except Exception as e:
                print(f"Error searching {source.name}: {e}")
                continue
        
        # Remove duplicates and limit results
        unique_jobs = []
        seen_ids = set()
        for job in all_jobs:
            if job.id not in seen_ids:
                unique_jobs.append(job)
                seen_ids.add(job.id)
        
        # Record usage
        record_usage("job_search", 0.01, success_count > 0)
        
        return {
            "query": query,
            "location": location,
            "total_results": len(unique_jobs),
            "sources_used": success_count,
            "jobs": [
                {
                    "id": job.id,
                    "title": job.title,
                    "company": job.company,
                    "location": job.location,
                    "description": job.description[:200] + "..." if len(job.description) > 200 else job.description,
                    "url": job.url,
                    "source": job.source,
                    "remote": job.remote,
                    "skills": job.skills,
                    "experience_level": job.experience_level
                }
                for job in unique_jobs[:limit]
            ]
        }
    except Exception as e:
        record_usage("job_search", 0.01, False)
        return {"error": str(e)}

@app.get("/jobs/search/rag")
def jobs_search_rag(query: str, location: str = None, limit: int = 10):
    """RAG-powered job search with dynamic source discovery"""
    try:
        # Use RAG to discover optimal sources
        optimal_sources = get_optimal_sources_for_query(query, location)
        
        # Initialize all available sources (production-ready only by default)
        source_map = {
            # Production-ready sources (no API key required)
            "greenhouse": GreenhouseSource(),
            "serpapi": SerpApiSource(),
            "reddit": RedditSource(),
            "remoteok": RemoteOKSource(),
            "weworkremotely": WeWorkRemotelySource(),
            "hackernews": HackerNewsSource()
        }
        
        # Add stubbed sources only if feature flag is enabled
        if get_feature_flag("JOB_SOURCES_STUBBED_ENABLED"):
            source_map.update({
                "indeed": IndeedSource(),
                "linkedin": LinkedInSource(),
                "glassdoor": GlassdoorSource(),
                "dice": DiceSource(),
                "monster": MonsterSource(),
                "ziprecruiter": ZipRecruiterSource(),
                "careerbuilder": CareerBuilderSource()
            })
        
        all_jobs = []
        used_sources = []
        
        # Search optimal sources first
        for source_name in optimal_sources:
            if source_name in source_map:
                try:
                    source = source_map[source_name]
                    jobs = source.search_jobs(query, location, limit)
                    all_jobs.extend(jobs)
                    used_sources.append(source_name)
                except Exception as e:
                    print(f"Error searching {source_name}: {e}")
                    continue
        
        # Fallback to other sources if needed
        if len(all_jobs) < limit:
            for source_name, source in source_map.items():
                if source_name not in used_sources:
                    try:
                        jobs = source.search_jobs(query, location, limit)
                        all_jobs.extend(jobs)
                        used_sources.append(source_name)
                    except Exception as e:
                        print(f"Error searching {source_name}: {e}")
                        continue
        
        # Remove duplicates and limit results
        unique_jobs = []
        seen_ids = set()
        for job in all_jobs:
            if job.id not in seen_ids:
                unique_jobs.append(job)
                seen_ids.add(job.id)
        
        return {
            "query": query,
            "location": location,
            "rag_optimized": True,
            "optimal_sources": optimal_sources,
            "used_sources": used_sources,
            "total_results": len(unique_jobs),
            "jobs": [
                {
                    "id": job.id,
                    "title": job.title,
                    "company": job.company,
                    "location": job.location,
                    "description": job.description[:200] + "..." if len(job.description) > 200 else job.description,
                    "url": job.url,
                    "source": job.source,
                    "remote": job.remote,
                    "skills": job.skills,
                    "experience_level": job.experience_level
                }
                for job in unique_jobs[:limit]
            ]
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/jobs/{job_id}")
def get_job_details(job_id: str):
    """Get detailed job information"""
    try:
        # Try each source to find the job
        sources = [GreenhouseSource(), SerpApiSource(), RedditSource()]
        
        for source in sources:
            try:
                job = source.get_job_details(job_id)
                if job:
                    return {
                        "id": job.id,
                        "title": job.title,
                        "company": job.company,
                        "location": job.location,
                        "description": job.description,
                        "url": job.url,
                        "source": job.source,
                        "posted_date": job.posted_date.isoformat() if job.posted_date else None,
                        "salary_range": job.salary_range,
                        "job_type": job.job_type,
                        "remote": job.remote,
                        "skills": job.skills,
                        "experience_level": job.experience_level,
                        "metadata": job.metadata
                    }
            except Exception as e:
                print(f"Error getting job details from {source.name}: {e}")
                continue
        
        return {"error": "Job not found"}
    except Exception as e:
        return {"error": str(e)}

# RAG Source Discovery Endpoints
@app.get("/sources/discover")
def discover_sources(query: str, location: str = None, job_type: str = None):
    """Discover optimal sources for a job search query using RAG"""
    try:
        discoveries = discover_sources_for_query(query, location, job_type)
        return {
            "query": query,
            "location": location,
            "job_type": job_type,
            "discoveries": [
                {
                    "source_name": discovery.source_name,
                    "source_type": discovery.source_type,
                    "api_endpoint": discovery.api_endpoint,
                    "rate_limit": discovery.rate_limit,
                    "confidence": discovery.confidence,
                    "discovery_reason": discovery.discovery_reason,
                    "integration_status": discovery.integration_status
                }
                for discovery in discoveries
            ]
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/sources/analytics")
def get_source_analytics():
    """Get analytics on source discovery and integration"""
    try:
        analytics = get_discovery_analytics()
        return analytics
    except Exception as e:
        return {"error": str(e)}

# Cost Control Endpoints
@app.get("/cost/analytics")
def get_cost_analytics():
    """Get cost and usage analytics"""
    try:
        analytics = get_usage_analytics()
        return analytics
    except Exception as e:
        return {"error": str(e)}

@app.get("/cost/limits")
def get_cost_limits():
    """Get current cost limits and usage"""
    try:
        analytics = get_usage_analytics()
        return {
            "cost_limits": analytics.get("cost_limits", {}),
            "resource_limits": analytics.get("resource_limits", {}),
            "current_usage": analytics.get("current_usage", {}),
            "emergency_stop": analytics.get("emergency_stop", False),
            "status": analytics.get("status", "unknown")
        }
    except Exception as e:
        return {"error": str(e)}

# Competitive Intelligence Endpoints
@app.get("/intelligence/company/{company_name}")
def analyze_company(company_name: str, industry: str = None):
    """Analyze company strategic needs and pain points."""
    try:
        analysis = analyze_company_strategic_needs(company_name, industry)
        return {
            "company_name": analysis.company_name,
            "industry": analysis.industry,
            "size": analysis.size,
            "pain_points": analysis.pain_points,
            "key_priorities": analysis.key_priorities,
            "competitive_advantages": analysis.competitive_advantages,
            "hiring_patterns": analysis.hiring_patterns,
            "culture_indicators": analysis.culture_indicators,
            "strategic_challenges": analysis.strategic_challenges,
            "growth_indicators": analysis.growth_indicators,
            "analysis_date": analysis.analysis_date
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/intelligence/positioning")
def develop_positioning(request: dict):
    """Develop competitive positioning strategy."""
    try:
        target_role = request.get("target_role")
        company_name = request.get("company_name")
        industry = request.get("industry")
        
        # Analyze company first
        company_analysis = analyze_company_strategic_needs(company_name, industry)
        
        # Develop positioning
        positioning = develop_competitive_positioning_strategy(target_role, company_analysis)
        
        return {
            "target_role": positioning.target_role,
            "key_differentiators": positioning.key_differentiators,
            "unique_value_props": positioning.unique_value_props,
            "skill_gaps_to_address": positioning.skill_gaps_to_address,
            "experience_highlights": positioning.experience_highlights,
            "competitive_threats": positioning.competitive_threats,
            "positioning_strategy": positioning.positioning_strategy
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/intelligence/resume-targeting")
def create_resume_targeting(request: dict):
    """Create strategic resume targeting."""
    try:
        company_name = request.get("company_name")
        target_role = request.get("target_role")
        industry = request.get("industry")
        
        # Analyze company
        company_analysis = analyze_company_strategic_needs(company_name, industry)
        
        # Develop positioning
        positioning = develop_competitive_positioning_strategy(target_role, company_analysis)
        
        # Create targeting
        targeting = create_strategic_resume_targeting(company_analysis, positioning)
        
        return {
            "company_name": targeting.company_name,
            "target_role": targeting.target_role,
            "resume_focus_areas": targeting.resume_focus_areas,
            "keyword_optimization": targeting.keyword_optimization,
            "experience_prioritization": targeting.experience_prioritization,
            "skill_emphasis": targeting.skill_emphasis,
            "achievement_highlights": targeting.achievement_highlights,
            "pain_point_alignment": targeting.pain_point_alignment
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/intelligence/ai-prompts")
def generate_ai_prompts(request: dict):
    """Generate AI prompts for job search optimization."""
    try:
        company_name = request.get("company_name")
        target_role = request.get("target_role")
        industry = request.get("industry")
        
        # Analyze company
        company_analysis = analyze_company_strategic_needs(company_name, industry)
        
        # Develop positioning
        positioning = develop_competitive_positioning_strategy(target_role, company_analysis)
        
        # Generate prompts
        prompts = generate_job_search_ai_prompts(company_analysis, positioning)
        
        return prompts
    except Exception as e:
        return {"error": str(e)}

@app.get("/health/intelligence")
def get_intelligence_health():
    """Get competitive intelligence health status."""
    return get_competitive_intelligence_health()

# OSINT Forensics Endpoints
@app.post("/osint/analyze-company")
def analyze_company_osint_endpoint(request: dict):
    """Analyze company using OSINT forensics for values-driven job search."""
    try:
        company_name = request.get("company_name")
        job_postings = request.get("job_postings", [])
        user_values = request.get("user_values", [])
        user_passions = request.get("user_passions", [])
        
        # Generate OSINT report
        report = analyze_company_osint(company_name, job_postings, user_values, user_passions)
        
        return {
            "company_name": report.company_name,
            "analysis_date": report.analysis_date,
            "values_alignment": report.values_alignment,
            "passion_opportunities": report.passion_opportunities,
            "cultural_insights": report.cultural_insights,
            "growth_signals": report.growth_signals,
            "watch_outs": report.watch_outs,
            "receipts_table": report.receipts_table,
            "user_values_match": report.user_values_match,
            "passion_skills_alignment": report.passion_skills_alignment
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/osint/health")
def get_osint_health_endpoint():
    """Get OSINT forensics health status."""
    return get_osint_health()

# Domain Adjacent Search Endpoints
@app.post("/domain-adjacent/discover")
def discover_domain_adjacent_endpoint(request: dict):
    """Discover domain adjacent opportunities through semantic clustering."""
    try:
        user_skills = request.get("user_skills", [])
        user_domains = request.get("user_domains", [])
        
        # Generate domain adjacent search results
        results = discover_domain_adjacent_opportunities(user_skills, user_domains)
        
        return {
            "user_skills": results.user_skills,
            "user_domains": results.user_domains,
            "semantic_clusters": [
                {
                    "cluster_id": cluster.cluster_id,
                    "cluster_name": cluster.cluster_name,
                    "core_skills": cluster.core_skills,
                    "adjacent_skills": cluster.adjacent_skills,
                    "related_domains": cluster.related_domains,
                    "opportunity_areas": cluster.opportunity_areas,
                    "skill_gaps": cluster.skill_gaps,
                    "learning_paths": cluster.learning_paths,
                    "confidence_score": cluster.confidence_score,
                    "cluster_strength": cluster.cluster_strength
                }
                for cluster in results.semantic_clusters
            ],
            "skill_alignment": results.skill_alignment,
            "domain_expansion": results.domain_expansion,
            "opportunity_mapping": results.opportunity_mapping,
            "learning_recommendations": results.learning_recommendations,
            "career_paths": results.career_paths
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/domain-adjacent/health")
def get_domain_adjacent_health_endpoint():
    """Get domain adjacent search health status."""
    return get_domain_adjacent_health()

# Analytics Endpoints
@app.get("/analytics/dashboard")
def get_analytics_dashboard_endpoint():
    """Get comprehensive analytics dashboard data."""
    return get_analytics_dashboard()

@app.get("/analytics/export")
def export_analytics_endpoint(days: int = 7):
    """Export analytics data to CSV."""
    try:
        filename = export_analytics_csv(days)
        if filename:
            return {"filename": filename, "status": "success"}
        else:
            return {"error": "Failed to export analytics", "status": "error"}
    except Exception as e:
        return {"error": str(e), "status": "error"}

@app.get("/analytics/health")
def get_analytics_health_endpoint():
    """Get analytics engine health status."""
    return get_analytics_health()

# Reranker Endpoints
@app.get("/reranker/health")
def get_reranker_health_endpoint():
    """Get cross-encoder reranker health status."""
    return get_reranker_health()

# Corpus Reindex Endpoints
@app.post("/corpus/reindex")
def reindex_corpus_endpoint():
    """Re-index corpus with new embeddings."""
    try:
        results = reindex_corpus()
        return {
            "status": "success",
            "results": results
        }
    except Exception as e:
        return {"error": str(e), "status": "error"}

@app.get("/corpus/status")
def get_corpus_status_endpoint():
    """Get corpus reindex status."""
    return get_reindex_status()
