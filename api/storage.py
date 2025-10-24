import json
import os
import uuid
import hashlib
import secrets
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL")
DATA_ROOT = Path(os.getenv("DATA_ROOT", "data"))
UPLOAD_ROOT = Path(os.getenv("UPLOAD_ROOT", DATA_ROOT / "uploads"))
SESSION_TTL_DAYS = int(os.getenv("SESSION_TTL_DAYS", "30"))

UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)
DATA_ROOT.mkdir(parents=True, exist_ok=True)

connection_pool = None
if DATABASE_URL:
    try:
        print(f"[STORAGE] Attempting PostgreSQL connection...")
        connection_pool = pool.SimpleConnectionPool(1, 20, DATABASE_URL)
        print(f"[STORAGE] ✅ PostgreSQL connection pool created successfully")
    except Exception as e:
        print(f"[STORAGE] ❌ PostgreSQL connection failed: {e}")
        print(f"[STORAGE] Falling back to SQLite")
else:
    print(f"[STORAGE] DATABASE_URL not set, using SQLite")


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
    if connection_pool:
        conn = connection_pool.getconn()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            connection_pool.putconn(conn)
    else:
        import sqlite3
        DB_PATH = Path(os.getenv("DATABASE_PATH", DATA_ROOT / "mosaic.db"))
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
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                user_data TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS wimd_outputs (
                id SERIAL PRIMARY KEY,
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

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS job_matches (
                id SERIAL PRIMARY KEY,
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

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS resume_versions (
                id SERIAL PRIMARY KEY,
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

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS file_uploads (
                id SERIAL PRIMARY KEY,
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
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sessions (id, expires_at, user_data) VALUES (%s, %s, %s)",
            (session_id, _expiry_ts(), payload),
        )
    return session_id


def ensure_session(session_id: Optional[str], user_data: Optional[Dict[str, Any]] = None) -> str:
    if not session_id:
        return create_session(user_data)
    with get_conn() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT id FROM sessions WHERE id = %s", (session_id,))
        row = cursor.fetchone()
        if row is None:
            return create_session(user_data)
        cursor.execute(
            "UPDATE sessions SET expires_at = %s, user_data = COALESCE(%s, user_data) WHERE id = %s",
            (_expiry_ts(), _json_dump(user_data) if user_data is not None else None, session_id),
        )
    return session_id


def session_exists(session_id: str) -> bool:
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM sessions WHERE id = %s", (session_id,))
        row = cursor.fetchone()
    return row is not None


def get_session_data(session_id: str) -> Optional[Dict[str, Any]]:
    """Get user_data for a session"""
    with get_conn() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT user_data FROM sessions WHERE id = %s", (session_id,))
        row = cursor.fetchone()
        if row:
            return _json_load(row['user_data']) or {}
    return {}


def update_session_data(session_id: str, data: Dict[str, Any]) -> None:
    """Update user_data for a session"""
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE sessions SET user_data = %s, expires_at = %s WHERE id = %s",
            (_json_dump(data), _expiry_ts(), session_id),
        )


def record_wimd_output(
    session_id: str,
    prompt: str,
    response: str,
    analysis_data: Optional[Dict[str, Any]] = None,
    metrics: Optional[Dict[str, Any]] = None,
) -> None:
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO wimd_outputs (session_id, prompt, response, analysis_data, metrics)
            VALUES (%s, %s, %s, %s, %s)
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
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            "SELECT metrics FROM wimd_outputs WHERE session_id = %s ORDER BY created_at DESC LIMIT 1",
            (session_id,),
        )
        row = cursor.fetchone()
    if row and row["metrics"]:
        parsed = _json_load(row["metrics"])
        return parsed if isinstance(parsed, dict) else None
    return None


def wimd_history(session_id: str, limit: int = 25) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            """
            SELECT prompt, response, analysis_data, metrics, created_at
            FROM wimd_outputs
            WHERE session_id = %s
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (session_id, limit),
        )
        rows = cursor.fetchall()
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
        cursor = conn.cursor()
        cursor.execute("DELETE FROM job_matches WHERE session_id = %s", (session_id,))
        for match in matches:
            cursor.execute(
                """
                INSERT INTO job_matches (session_id, job_id, company, role, fit_score, skills_match, values_match, extras)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
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
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            "SELECT job_id, company, role, fit_score, skills_match, values_match, extras, created_at FROM job_matches WHERE session_id = %s ORDER BY fit_score DESC",
            (session_id,),
        )
        rows = cursor.fetchall()
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
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            "SELECT extras FROM job_matches WHERE session_id = %s AND job_id = %s",
            (session_id, job_id),
        )
        row = cursor.fetchone()
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
        cursor.execute(
            "UPDATE job_matches SET extras = %s WHERE session_id = %s AND job_id = %s",
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
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO resume_versions (session_id, job_id, version_name, content, feedback)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """,
            (session_id, job_id, version_name, content, _json_dump(feedback or {})),
        )
        result = cursor.fetchone()
        return result[0] if result else 0


def list_resume_versions(session_id: str) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            "SELECT id, job_id, version_name, content, feedback, created_at FROM resume_versions WHERE session_id = %s ORDER BY created_at DESC",
            (session_id,),
        )
        rows = cursor.fetchall()
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
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO file_uploads (session_id, filename, file_path, file_type, file_size)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (session_id, filename, str(file_path), file_type, file_size),
        )


def list_files(session_id: str) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            "SELECT id, filename, file_type, file_size, created_at FROM file_uploads WHERE session_id = %s ORDER BY created_at DESC",
            (session_id,),
        )
        rows = cursor.fetchall()
    return [dict(row) for row in rows]


def delete_session(session_id: str) -> None:
    """Delete a session and all related data (used for logout)"""
    with get_conn() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            "SELECT file_path FROM file_uploads WHERE session_id = %s",
            (session_id,)
        )
        file_rows = cursor.fetchall()

        cursor.execute("DELETE FROM file_uploads WHERE session_id = %s", (session_id,))
        cursor.execute("DELETE FROM resume_versions WHERE session_id = %s", (session_id,))
        cursor.execute("DELETE FROM job_matches WHERE session_id = %s", (session_id,))
        cursor.execute("DELETE FROM wimd_outputs WHERE session_id = %s", (session_id,))
        cursor.execute("DELETE FROM sessions WHERE id = %s", (session_id,))

        for row in file_rows:
            try:
                path = Path(row['file_path'])
                if path.exists() and path.is_file():
                    path.unlink()
            except OSError:
                pass


def cleanup_expired_sessions() -> None:
    cutoff = datetime.utcnow()
    with get_conn() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT id FROM sessions WHERE expires_at <= %s", (cutoff,))
        expired_ids = [row['id'] for row in cursor.fetchall()]
        if expired_ids:
            cursor.execute(
                "SELECT file_path FROM file_uploads WHERE session_id = ANY(%s)",
                (expired_ids,)
            )
            file_rows = cursor.fetchall()
            cursor.execute("DELETE FROM file_uploads WHERE session_id = ANY(%s)", (expired_ids,))
            cursor.execute("DELETE FROM resume_versions WHERE session_id = ANY(%s)", (expired_ids,))
            cursor.execute("DELETE FROM job_matches WHERE session_id = ANY(%s)", (expired_ids,))
            cursor.execute("DELETE FROM wimd_outputs WHERE session_id = ANY(%s)", (expired_ids,))
            cursor.execute("DELETE FROM sessions WHERE id = ANY(%s)", (expired_ids,))
            for row in file_rows:
                try:
                    path = Path(row['file_path'])
                    if path.exists() and path.is_file():
                        path.unlink()
                except OSError:
                    pass


def session_summary(session_id: str) -> Dict[str, Any]:
    data: Dict[str, Any] = {"session_id": session_id}
    with get_conn() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            "SELECT created_at, expires_at, user_data FROM sessions WHERE id = %s",
            (session_id,),
        )
        session_row = cursor.fetchone()
    if session_row:
        data["created_at"] = session_row["created_at"]
        data["expires_at"] = session_row["expires_at"]
        data["user_data"] = _json_load(session_row["user_data"]) or {}
    data["latest_metrics"] = latest_metrics(session_id) or {}
    data["files"] = list_files(session_id)
    data["resumes"] = list_resume_versions(session_id)
    data["job_matches"] = fetch_job_matches(session_id)
    return data

def hash_password(password: str) -> str:
    """Hash a password using SHA-256 with salt"""
    salt = secrets.token_hex(16)
    return hashlib.sha256((password + salt).encode()).hexdigest() + ":" + salt

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    try:
        hash_part, salt = hashed.split(":")
        return hashlib.sha256((password + salt).encode()).hexdigest() == hash_part
    except:
        return False

def create_user(email: str, password: str) -> str:
    """Create a new user and return user ID"""
    user_id = str(uuid.uuid4())
    password_hash = hash_password(password)
    now = datetime.utcnow().isoformat()

    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (id, email, password_hash, created_at, last_login) VALUES (%s, %s, %s, %s, %s)",
            (user_id, email, password_hash, now, now)
        )
    return user_id

def authenticate_user(email: str, password: str) -> Optional[str]:
    """Authenticate user and return user ID if successful"""
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, password_hash FROM users WHERE email = %s",
            (email,)
        )
        row = cursor.fetchone()

        if not row:
            return None

        user_id, password_hash = row
        if verify_password(password, password_hash):
            cursor.execute(
                "UPDATE users SET last_login = %s WHERE id = %s",
                (datetime.utcnow().isoformat(), user_id)
            )
            return user_id
        return None

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Get user by email"""
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, email, created_at, last_login FROM users WHERE email = %s",
            (email,)
        )
        row = cursor.fetchone()

        if not row:
            return None

        return {
            "user_id": row[0],
            "email": row[1],
            "created_at": row[2],
            "last_login": row[3]
        }

def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user by ID"""
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, email, created_at, last_login FROM users WHERE id = %s",
            (user_id,)
        )
        row = cursor.fetchone()

        if not row:
            return None

        return {
            "user_id": row[0],
            "email": row[1],
            "created_at": row[2],
            "last_login": row[3]
        }

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
    "create_user",
    "authenticate_user",
    "get_user_by_email",
    "get_user_by_id",
    "hash_password",
    "verify_password",
    "delete_session",
]
