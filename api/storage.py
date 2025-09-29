import json
import os
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

DATA_ROOT = Path(os.getenv("DATA_ROOT", "data"))
DB_PATH = Path(os.getenv("DATABASE_PATH", DATA_ROOT / "mosaic.db"))
UPLOAD_ROOT = Path(os.getenv("UPLOAD_ROOT", DATA_ROOT / "uploads"))
SESSION_TTL_DAYS = int(os.getenv("SESSION_TTL_DAYS", "30"))

UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)
DATA_ROOT.mkdir(parents=True, exist_ok=True)


def _json_dump(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False)


def _json_load(raw: Optional[str]) -> Any:
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


@contextmanager
def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                user_data TEXT
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS wimd_outputs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                prompt TEXT,
                response TEXT,
                analysis_data TEXT,
                metrics TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS job_matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                job_id TEXT,
                company TEXT,
                role TEXT,
                fit_score REAL,
                skills_match TEXT,
                values_match TEXT,
                extras TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS resume_versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                job_id TEXT,
                version_name TEXT,
                content TEXT,
                feedback TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS file_uploads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                filename TEXT,
                file_path TEXT,
                file_type TEXT,
                file_size INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
            )
            """
        )


def _expiry_ts() -> datetime:
    return datetime.utcnow() + timedelta(days=SESSION_TTL_DAYS)


def create_session(user_data: Optional[Dict[str, Any]] = None) -> str:
    session_id = uuid.uuid4().hex
    payload = _json_dump(user_data or {})
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO sessions (id, expires_at, user_data) VALUES (?, ?, ?)",
            (session_id, _expiry_ts(), payload),
        )
    return session_id


def ensure_session(session_id: Optional[str], user_data: Optional[Dict[str, Any]] = None) -> str:
    if not session_id:
        return create_session(user_data)
    with get_conn() as conn:
        row = conn.execute("SELECT id FROM sessions WHERE id = ?", (session_id,)).fetchone()
        if row is None:
            return create_session(user_data)
        conn.execute(
            "UPDATE sessions SET expires_at = ?, user_data = COALESCE(?, user_data) WHERE id = ?",
            (_expiry_ts(), _json_dump(user_data) if user_data is not None else None, session_id),
        )
    return session_id


def session_exists(session_id: str) -> bool:
    with get_conn() as conn:
        row = conn.execute("SELECT 1 FROM sessions WHERE id = ?", (session_id,)).fetchone()
    return row is not None


def record_wimd_output(
    session_id: str,
    prompt: str,
    response: str,
    analysis_data: Optional[Dict[str, Any]] = None,
    metrics: Optional[Dict[str, Any]] = None,
) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO wimd_outputs (session_id, prompt, response, analysis_data, metrics)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                session_id,
                prompt,
                response,
                _json_dump(analysis_data or {}),
                _json_dump(metrics or {}),
            ),
        )


def latest_metrics(session_id: str) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT metrics FROM wimd_outputs WHERE session_id = ? ORDER BY created_at DESC LIMIT 1",
            (session_id,),
        ).fetchone()
    if row and row["metrics"]:
        parsed = _json_load(row["metrics"])
        return parsed if isinstance(parsed, dict) else None
    return None


def wimd_history(session_id: str, limit: int = 25) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT prompt, response, analysis_data, metrics, created_at
            FROM wimd_outputs
            WHERE session_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (session_id, limit),
        ).fetchall()
    history: List[Dict[str, Any]] = []
    for row in rows:
        history.append(
            {
                "prompt": row["prompt"],
                "response": row["response"],
                "analysis": _json_load(row["analysis_data"]) or {},
                "metrics": _json_load(row["metrics"]) or {},
                "created_at": row["created_at"],
            }
        )
    return history


def store_job_matches(session_id: str, matches: List[Dict[str, Any]]) -> None:
    with get_conn() as conn:
        conn.execute("DELETE FROM job_matches WHERE session_id = ?", (session_id,))
        for match in matches:
            conn.execute(
                """
                INSERT INTO job_matches (session_id, job_id, company, role, fit_score, skills_match, values_match, extras)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    match.get("job_id"),
                    match.get("company"),
                    match.get("role"),
                    float(match.get("fit_score", 0.0)),
                    _json_dump(match.get("skills_match", [])),
                    _json_dump(match.get("values_match", [])),
                    _json_dump(match.get("extras", {})),
                ),
            )


def fetch_job_matches(session_id: str) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT job_id, company, role, fit_score, skills_match, values_match, extras, created_at FROM job_matches WHERE session_id = ? ORDER BY fit_score DESC",
            (session_id,),
        ).fetchall()
    matches = []
    for row in rows:
        matches.append(
            {
                "job_id": row["job_id"],
                "company": row["company"],
                "role": row["role"],
                "fit_score": row["fit_score"],
                "skills_match": _json_load(row["skills_match"]) or [],
                "values_match": _json_load(row["values_match"]) or [],
                "extras": _json_load(row["extras"]) or {},
                "created_at": row["created_at"],
            }
        )
    return matches


def update_job_match_status(
    session_id: str,
    job_id: str,
    status: str,
    notes: Optional[str] = None,
) -> None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT extras FROM job_matches WHERE session_id = ? AND job_id = ?",
            (session_id, job_id),
        ).fetchone()
        if row is None:
            raise ValueError("job_match_not_found")
        extras = _json_load(row["extras"]) or {}
        extras.update(
            {
                "status": status,
                "status_notes": notes or "",
                "status_at": datetime.utcnow().isoformat() + "Z",
            }
        )
        conn.execute(
            "UPDATE job_matches SET extras = ? WHERE session_id = ? AND job_id = ?",
            (_json_dump(extras), session_id, job_id),
        )


def add_resume_version(
    session_id: str,
    version_name: str,
    content: str,
    job_id: Optional[str] = None,
    feedback: Optional[Dict[str, Any]] = None,
) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO resume_versions (session_id, job_id, version_name, content, feedback)
            VALUES (?, ?, ?, ?, ?)
            """,
            (session_id, job_id, version_name, content, _json_dump(feedback or {})),
        )
        return cur.lastrowid


def list_resume_versions(session_id: str) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, job_id, version_name, content, feedback, created_at FROM resume_versions WHERE session_id = ? ORDER BY created_at DESC",
            (session_id,),
        ).fetchall()
    versions: List[Dict[str, Any]] = []
    for row in rows:
        versions.append(
            {
                "id": row["id"],
                "job_id": row["job_id"],
                "version_name": row["version_name"],
                "content": row["content"],
                "feedback": _json_load(row["feedback"]) or {},
                "created_at": row["created_at"],
            }
        )
    return versions


def store_file_upload(
    session_id: str,
    filename: str,
    file_type: str,
    file_size: int,
    file_path: Path,
) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO file_uploads (session_id, filename, file_path, file_type, file_size)
            VALUES (?, ?, ?, ?, ?)
            """,
            (session_id, filename, str(file_path), file_type, file_size),
        )


def list_files(session_id: str) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, filename, file_type, file_size, created_at FROM file_uploads WHERE session_id = ? ORDER BY created_at DESC",
            (session_id,),
        ).fetchall()
    return [dict(row) for row in rows]


def cleanup_expired_sessions() -> None:
    cutoff = datetime.utcnow()
    with get_conn() as conn:
        expired_ids = [row[0] for row in conn.execute("SELECT id FROM sessions WHERE expires_at <= ?", (cutoff,)).fetchall()]
        if expired_ids:
            placeholders = ",".join(["?"] * len(expired_ids))
            file_rows = conn.execute(
                f"SELECT file_path FROM file_uploads WHERE session_id IN ({placeholders})",
                expired_ids,
            ).fetchall()
            conn.execute(f"DELETE FROM file_uploads WHERE session_id IN ({placeholders})", expired_ids)
            conn.execute(f"DELETE FROM resume_versions WHERE session_id IN ({placeholders})", expired_ids)
            conn.execute(f"DELETE FROM job_matches WHERE session_id IN ({placeholders})", expired_ids)
            conn.execute(f"DELETE FROM wimd_outputs WHERE session_id IN ({placeholders})", expired_ids)
            conn.execute(f"DELETE FROM sessions WHERE id IN ({placeholders})", expired_ids)
            for row in file_rows:
                try:
                    path = Path(row[0])
                    if path.exists() and path.is_file():
                        path.unlink()
                except OSError:
                    pass


def session_summary(session_id: str) -> Dict[str, Any]:
    data: Dict[str, Any] = {"session_id": session_id}
    with get_conn() as conn:
        session_row = conn.execute(
            "SELECT created_at, expires_at, user_data FROM sessions WHERE id = ?",
            (session_id,),
        ).fetchone()
    if session_row:
        data["created_at"] = session_row["created_at"]
        data["expires_at"] = session_row["expires_at"]
        data["user_data"] = _json_load(session_row["user_data"]) or {}
    data["latest_metrics"] = latest_metrics(session_id) or {}
    data["files"] = list_files(session_id)
    data["resumes"] = list_resume_versions(session_id)
    data["job_matches"] = fetch_job_matches(session_id)
    return data

__all__ = [
    "UPLOAD_ROOT",
    "create_session",
    "ensure_session",
    "session_exists",
    "record_wimd_output",
    "latest_metrics",
    "wimd_history",
    "store_job_matches",
    "fetch_job_matches",
    "update_job_match_status",
    "add_resume_version",
    "list_resume_versions",
    "store_file_upload",
    "list_files",
    "cleanup_expired_sessions",
    "init_db",
    "session_summary",
]
