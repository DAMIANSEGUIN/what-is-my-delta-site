# Self-Diagnostic Framework for Mosaic Platform
**Architecture-Specific Error Prevention & Auto-Triage System**

---

## System Architecture Overview

**Stack:**
- **Orchestration:** None (single FastAPI monolith)
- **Model Serving:** Direct API calls (OpenAI GPT-4, Anthropic Claude via Python clients)
- **Infrastructure:** Railway (backend), Netlify (frontend), PostgreSQL (database)
- **Observability:** Railway logs, health endpoints, no APM
- **Frontend:** Vanilla JavaScript ES6+
- **Backend:** FastAPI + Pydantic + uvicorn
- **Database:** PostgreSQL (migrated from SQLite)
- **LLM Providers:** OpenAI (embeddings, GPT-4), Anthropic (Claude)

---

## Error Taxonomy (Mosaic-Specific)

### 1. Infrastructure Errors
**Railway-Specific:**
- `RAILWAY_DEPLOY_FAILED` - Build or deploy crash
- `RAILWAY_DB_EPHEMERAL` - SQLite fallback active (PostgreSQL failed)
- `RAILWAY_ENV_VAR_MISSING` - DATABASE_URL, OPENAI_API_KEY, etc. not set
- `RAILWAY_TIMEOUT` - Health check timeout (>300s)
- `RAILWAY_RESTART_LOOP` - Container crash looping

**Database:**
- `PG_CONNECTION_FAILED` - PostgreSQL connection pool initialization failed
- `PG_SSL_REQUIRED` - Missing sslmode in DATABASE_URL
- `PG_AUTH_FAILED` - Invalid credentials in DATABASE_URL
- `PG_NETWORK_UNREACHABLE` - Internal network routing issue (railway.app vs railway.internal)
- `SQLITE_FALLBACK_ACTIVE` - Using ephemeral SQLite instead of PostgreSQL

**API Rate Limits:**
- `OPENAI_RATE_LIMIT` - 429 from OpenAI
- `ANTHROPIC_RATE_LIMIT` - 429 from Anthropic
- `OPENAI_QUOTA_EXCEEDED` - Monthly quota hit

### 2. Data Errors
**Session/State:**
- `SESSION_ORPHANED` - Session exists but user deleted
- `SESSION_EXPIRED` - TTL exceeded
- `PS101_STATE_CORRUPT` - prompt_index > len(prompts)
- `USER_DATA_NULL` - session.user_data is NULL when expected

**File Upload:**
- `UPLOAD_PATH_MISSING` - file_path in DB but file doesn't exist on disk
- `UPLOAD_SIZE_EXCEEDED` - File > limit (not currently enforced)

**Schema Drift:**
- `MISSING_COLUMN` - SQLite→PostgreSQL migration incomplete
- `TYPE_MISMATCH` - JSON field not parseable

### 3. Model/LLM Errors
**OpenAI:**
- `OPENAI_INVALID_KEY` - API key rejected
- `OPENAI_MODEL_NOT_FOUND` - Model name wrong/deprecated
- `OPENAI_CONTEXT_OVERFLOW` - Prompt > max_tokens
- `OPENAI_TIMEOUT` - Request timeout (>120s default)

**Anthropic:**
- `ANTHROPIC_INVALID_KEY` - API key rejected
- `ANTHROPIC_RATE_LIMIT` - Too many requests
- `ANTHROPIC_CONTENT_FILTERED` - Safety filter blocked response

**Quality:**
- `PROMPT_SELECTOR_FAIL` - No match found, fell back to generic
- `EMBEDDING_GENERATION_FAILED` - OpenAI embeddings error
- `RERANKER_UNAVAILABLE` - CrossEncoder model load failed (currently mocked)

### 4. Prompt/Tooling Errors
**JSON Parsing:**
- `PS101_STEP_MALFORMED` - JSON parse error in ps101_steps.json
- `PROMPT_CSV_CORRUPT` - CSV parse error in prompts.csv

**Tool Call Issues:**
- Not applicable (no function calling yet)

### 5. Integration Errors
**Third-Party APIs:**
- Job sources (12 external APIs/scrapers) - individual error codes per source
- `LINKEDIN_SCRAPE_BLOCKED` - Anti-bot detection
- `GREENHOUSE_API_DOWN` - HTTP 5xx

**Authentication:**
- `AUTH_INVALID_CREDENTIALS` - Password hash mismatch
- `AUTH_USER_NOT_FOUND` - Email not in users table
- `AUTH_SESSION_INVALID` - Session ID not found

---

## Auto-Labeling Rules

### Pattern Matching (Implemented in Code)

```python
# api/monitoring.py (to be created)

import re
from enum import Enum
from datetime import datetime, timedelta

class ErrorCategory(Enum):
    INFRA = "infrastructure"
    DATA = "data"
    MODEL = "model"
    PROMPT = "prompt"
    INTEGRATION = "integration"

def classify_error(exception: Exception, stage: str) -> tuple[ErrorCategory, str]:
    """Auto-classify errors by type and stage"""

    exc_str = str(exception)
    exc_type = type(exception).__name__

    # Infrastructure
    if "psycopg2" in exc_str or "connection" in exc_str.lower():
        if "password" in exc_str:
            return (ErrorCategory.INFRA, "PG_AUTH_FAILED")
        if "ssl" in exc_str.lower():
            return (ErrorCategory.INFRA, "PG_SSL_REQUIRED")
        if "could not connect" in exc_str:
            return (ErrorCategory.INFRA, "PG_NETWORK_UNREACHABLE")
        return (ErrorCategory.INFRA, "PG_CONNECTION_FAILED")

    if "sqlite" in exc_str.lower() and stage == "startup":
        return (ErrorCategory.INFRA, "SQLITE_FALLBACK_ACTIVE")

    # Model/LLM
    if "openai" in exc_str.lower():
        if "rate_limit" in exc_str or "429" in exc_str:
            return (ErrorCategory.MODEL, "OPENAI_RATE_LIMIT")
        if "quota" in exc_str.lower():
            return (ErrorCategory.MODEL, "OPENAI_QUOTA_EXCEEDED")
        if "context_length" in exc_str or "max_tokens" in exc_str:
            return (ErrorCategory.MODEL, "OPENAI_CONTEXT_OVERFLOW")
        if "invalid_api_key" in exc_str:
            return (ErrorCategory.MODEL, "OPENAI_INVALID_KEY")
        return (ErrorCategory.MODEL, "OPENAI_ERROR")

    if "anthropic" in exc_str.lower():
        if "rate_limit" in exc_str or "429" in exc_str:
            return (ErrorCategory.MODEL, "ANTHROPIC_RATE_LIMIT")
        if "invalid_api_key" in exc_str:
            return (ErrorCategory.MODEL, "ANTHROPIC_INVALID_KEY")
        return (ErrorCategory.MODEL, "ANTHROPIC_ERROR")

    # Data
    if exc_type == "KeyError" and stage in ["session_load", "ps101_flow"]:
        return (ErrorCategory.DATA, "SESSION_DATA_CORRUPT")

    if "FOREIGN KEY constraint" in exc_str:
        return (ErrorCategory.DATA, "SESSION_ORPHANED")

    # Prompt
    if exc_type == "JSONDecodeError" and "ps101" in stage:
        return (ErrorCategory.PROMPT, "PS101_STEP_MALFORMED")

    if exc_type == "csv.Error":
        return (ErrorCategory.PROMPT, "PROMPT_CSV_CORRUPT")

    # Integration
    if exc_type == "HTTPError" and stage.startswith("job_source_"):
        source = stage.replace("job_source_", "")
        return (ErrorCategory.INTEGRATION, f"{source.upper()}_API_ERROR")

    # Default
    return (ErrorCategory.INFRA, "UNKNOWN_ERROR")
```

### Anomaly Detection (Simple EWMA)

```python
# api/monitoring.py

from collections import defaultdict
from typing import Dict

class ErrorRateMonitor:
    """Track error rates with exponential weighted moving average"""

    def __init__(self, alpha=0.3):
        self.alpha = alpha  # smoothing factor
        self.ewma: Dict[str, float] = defaultdict(float)
        self.counts: Dict[str, int] = defaultdict(int)
        self.window_start = datetime.utcnow()

    def record_error(self, error_label: str):
        """Record an error occurrence"""
        self.counts[error_label] += 1

    def update_ewma(self, error_label: str, current_rate: float):
        """Update EWMA for error label"""
        if self.ewma[error_label] == 0:
            self.ewma[error_label] = current_rate
        else:
            self.ewma[error_label] = (
                self.alpha * current_rate +
                (1 - self.alpha) * self.ewma[error_label]
            )

    def is_anomalous(self, error_label: str, threshold_sigma=3) -> bool:
        """Detect if current rate is anomalous (>3σ from EWMA)"""
        current_rate = self.get_current_rate(error_label)
        baseline = self.ewma[error_label]

        if baseline == 0:
            return current_rate > 0  # Any error when baseline is 0

        deviation = abs(current_rate - baseline) / baseline
        return deviation > threshold_sigma

    def get_current_rate(self, error_label: str) -> float:
        """Get current error rate (errors per minute)"""
        elapsed = (datetime.utcnow() - self.window_start).total_seconds() / 60
        if elapsed == 0:
            return 0
        return self.counts[error_label] / elapsed
```

---

## Playbooks-as-Code (Mosaic-Specific)

### Playbook Structure

```yaml
# playbooks/pg_connection_failed.yml

- match:
    label: "PG_CONNECTION_FAILED"
    stage: "startup"
  severity: "CRITICAL"
  alert: "pager_high"

  gather:
    - railway_logs: 200  # Last 200 lines
    - env_vars: ["DATABASE_URL"]  # Redacted
    - postgres_service_status: true
    - network_config: true

  diagnose:
    - check: "DATABASE_URL starts with postgresql://"
      fail_label: "PG_URL_MALFORMED"
    - check: "DATABASE_URL contains railway.internal"
      fail_label: "PG_USING_PUBLIC_URL"
      recommendation: "Switch to private network URL"
    - check: "PostgreSQL service status == Active"
      fail_label: "PG_SERVICE_DOWN"

  remediate:
    - action: "fallback_sqlite"
      when: "auto"  # Always fallback to keep app running
      log: "WARNING: Using SQLite fallback - data will not persist"

    - action: "alert_ops"
      when: "rate_5m > 1"  # More than 1 error in 5 min
      message: "PostgreSQL connection failing - check DATABASE_URL config"

    - action: "circuit_breaker"
      when: "rate_5m > 5"
      params:
        disable_feature: "user_registration"
        message: "Registration temporarily disabled - database issues"
```

### Implementation (Python)

```python
# api/playbooks.py

import yaml
from pathlib import Path
from typing import Dict, List, Any

class PlaybookExecutor:
    """Execute playbooks based on error classification"""

    def __init__(self, playbooks_dir: Path = Path("playbooks")):
        self.playbooks = self._load_playbooks(playbooks_dir)

    def _load_playbooks(self, dir: Path) -> Dict[str, Any]:
        """Load all YAML playbooks"""
        playbooks = {}
        for file in dir.glob("*.yml"):
            with open(file) as f:
                data = yaml.safe_load(f)
                playbooks[data[0]['match']['label']] = data[0]
        return playbooks

    def execute(self, error_label: str, exception: Exception, stage: str):
        """Execute playbook for error label"""
        playbook = self.playbooks.get(error_label)
        if not playbook:
            return None

        # Gather context
        context = self._gather_context(playbook['gather'])

        # Run diagnostics
        diagnosis = self._diagnose(playbook.get('diagnose', []), context)

        # Execute remediations
        for action in playbook.get('remediate', []):
            if self._should_run(action, context):
                self._run_action(action, context)

        return {
            "playbook": error_label,
            "context": context,
            "diagnosis": diagnosis,
            "actions_taken": [a['action'] for a in playbook.get('remediate', [])]
        }

    def _gather_context(self, gather_spec: List[Dict]) -> Dict:
        """Gather diagnostic context"""
        context = {}
        # Implementation would fetch Railway logs, env vars, etc.
        return context

    def _diagnose(self, checks: List[Dict], context: Dict) -> List[str]:
        """Run diagnostic checks"""
        failures = []
        for check in checks:
            # Evaluate check against context
            # If check fails, add to failures with recommendation
            pass
        return failures

    def _should_run(self, action: Dict, context: Dict) -> bool:
        """Determine if action should run based on 'when' condition"""
        when = action.get('when', 'always')
        if when == 'auto' or when == 'always':
            return True
        # Evaluate condition (e.g., "rate_5m > 1")
        return False

    def _run_action(self, action: Dict, context: Dict):
        """Execute remediation action"""
        action_type = action['action']

        if action_type == "fallback_sqlite":
            print(f"[PLAYBOOK] {action.get('log', 'Executing fallback')}")
            # Already happens automatically in code

        elif action_type == "alert_ops":
            # Send alert (email, Slack, PagerDuty, etc.)
            print(f"[PLAYBOOK] ALERT: {action['message']}")

        elif action_type == "circuit_breaker":
            # Disable feature
            # Set feature flag or update config
            print(f"[PLAYBOOK] Circuit breaker: {action['params']}")
```

---

## Automated Context Gathering

### On Error, Auto-Attach:

```python
# api/error_context.py

def gather_error_context(
    exception: Exception,
    stage: str,
    error_label: str
) -> Dict[str, Any]:
    """Gather full context for error triage"""

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "error_label": error_label,
        "stage": stage,
        "exception": {
            "type": type(exception).__name__,
            "message": str(exception),
            "traceback": traceback.format_exc()
        },

        # Last 100 traces (if tracing implemented)
        "recent_requests": get_recent_requests(limit=100),

        # Top failing inputs (from error logs)
        "failing_inputs": get_failing_inputs(error_label, limit=20),

        # Schema/config state
        "database_schema": get_schema_version(),
        "feature_flags": get_feature_flags(),

        # Model/prompt versions
        "openai_models_used": ["gpt-4", "text-embedding-ada-002"],
        "anthropic_models_used": ["claude-3-sonnet"],
        "prompt_version": get_prompt_version(),

        # Recent deploys
        "recent_deploys": get_recent_deploys(limit=5),

        # Environment state
        "env_vars_set": {
            "DATABASE_URL": "***REDACTED***" if os.getenv("DATABASE_URL") else None,
            "OPENAI_API_KEY": "***SET***" if os.getenv("OPENAI_API_KEY") else None,
            "ANTHROPIC_API_KEY": "***SET***" if os.getenv("CLAUDE_API_KEY") else None,
        },

        # System health
        "health_check": call_health_endpoint(),
        "postgres_status": check_postgres_connection(),
    }
```

---

## Automated Fixes (Priority-Ordered)

### 1. Retry with Jitter (429/5xx)

```python
# api/retry_utils.py

import time
import random
from functools import wraps

def retry_with_exponential_backoff(
    max_retries=3,
    base_delay=1,
    max_delay=60,
    jitter=True
):
    """Retry decorator with exponential backoff and jitter"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries:
                        raise

                    if "429" in str(e) or "5" in str(getattr(e, 'status_code', '')):
                        # Calculate backoff
                        delay = min(base_delay * (2 ** attempt), max_delay)
                        if jitter:
                            delay *= (0.5 + random.random())  # 50-150% of delay

                        print(f"[RETRY] Attempt {attempt + 1} failed, retrying in {delay:.2f}s")
                        time.sleep(delay)
                    else:
                        raise  # Don't retry non-retriable errors
        return wrapper
    return decorator

# Usage
@retry_with_exponential_backoff(max_retries=3)
def call_openai_api(prompt: str):
    # OpenAI API call
    pass
```

### 2. Failover (Secondary Provider)

```python
# api/ai_clients.py (enhanced)

class MultiProviderLLM:
    """Failover between OpenAI and Anthropic"""

    def __init__(self):
        self.primary = "openai"
        self.secondary = "anthropic"
        self.circuit_breaker_threshold = 0.10  # 10% error rate
        self.error_window = []  # Last 100 requests

    def generate(self, prompt: str, **kwargs):
        """Generate with automatic failover"""

        # Check circuit breaker
        if self._should_use_secondary():
            provider = self.secondary
        else:
            provider = self.primary

        try:
            if provider == "openai":
                result = self._call_openai(prompt, **kwargs)
            else:
                result = self._call_anthropic(prompt, **kwargs)

            self._record_success()
            return result

        except Exception as e:
            self._record_failure()

            # Try failover
            if provider == self.primary:
                print(f"[FAILOVER] {self.primary} failed, trying {self.secondary}")
                return self._call_anthropic(prompt, **kwargs)
            else:
                raise  # Both failed

    def _should_use_secondary(self) -> bool:
        """Check if circuit breaker is open"""
        if len(self.error_window) < 20:
            return False

        recent_errors = sum(self.error_window[-100:])
        error_rate = recent_errors / min(len(self.error_window), 100)

        return error_rate > self.circuit_breaker_threshold
```

### 3. Schema Drift Auto-Detection

```python
# api/schema_guard.py

from typing import Any, Dict
from pydantic import BaseModel, ValidationError

def validate_and_route(
    record: Dict[str, Any],
    schema: BaseModel,
    table_name: str
):
    """Validate schema and route to DLQ if invalid"""

    try:
        validated = schema(**record)
        return ("ok", validated)

    except ValidationError as e:
        # Send to dead letter queue
        send_to_dlq({
            "table": table_name,
            "record": record,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        })

        # Increment DLQ metric
        increment_metric("dlq.count", tags={"table": table_name})

        # Check if this is a known drift pattern
        if is_known_drift(record, e):
            propose_schema_update(record, e, table_name)

        return ("quarantine", None)

def propose_schema_update(record: Dict, error: ValidationError, table: str):
    """Auto-generate schema migration proposal"""
    # Analyze error and infer schema changes needed
    # Create GitHub issue or PR with proposed migration
    print(f"[SCHEMA_GUARD] Proposed schema update for {table}")
    print(f"  Error: {error}")
    print(f"  Sample record: {record}")
```

### 4. Circuit Breakers

```python
# api/circuit_breaker.py

from datetime import datetime, timedelta
from collections import defaultdict

class CircuitBreaker:
    """Automatic circuit breaker for high error rates"""

    def __init__(self, threshold=0.05, window_minutes=5):
        self.threshold = threshold  # 5% error rate
        self.window = timedelta(minutes=window_minutes)
        self.errors = defaultdict(list)  # route -> [timestamps]
        self.successes = defaultdict(list)
        self.open_circuits = set()

    def record_call(self, route: str, success: bool):
        """Record API call result"""
        now = datetime.utcnow()

        if success:
            self.successes[route].append(now)
        else:
            self.errors[route].append(now)

        # Clean old data
        self._clean_old_data(route, now)

        # Check if circuit should open
        if self._should_open_circuit(route):
            self.open_circuits.add(route)
            print(f"[CIRCUIT_BREAKER] Opened circuit for {route}")

    def is_open(self, route: str) -> bool:
        """Check if circuit is open for route"""
        return route in self.open_circuits

    def _should_open_circuit(self, route: str) -> bool:
        """Determine if error rate exceeds threshold"""
        total_errors = len(self.errors[route])
        total_successes = len(self.successes[route])
        total_calls = total_errors + total_successes

        if total_calls < 20:  # Need minimum sample
            return False

        error_rate = total_errors / total_calls
        return error_rate > self.threshold

    def _clean_old_data(self, route: str, now: datetime):
        """Remove data outside window"""
        cutoff = now - self.window
        self.errors[route] = [t for t in self.errors[route] if t > cutoff]
        self.successes[route] = [t for t in self.successes[route] if t > cutoff]
```

---

## Baked-In Reproducibility

### Immutable Artifacts Tracking

```python
# api/deployment_manifest.py

import subprocess
import hashlib

def generate_deployment_manifest() -> Dict[str, Any]:
    """Generate immutable deployment manifest"""

    return {
        "timestamp": datetime.utcnow().isoformat(),

        # Code version
        "git_commit": subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip(),
        "git_branch": subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip(),

        # Dependencies
        "requirements_hash": hash_file("requirements.txt"),
        "python_version": subprocess.check_output(['python', '--version']).decode().strip(),

        # Data/Prompts
        "prompts_csv_hash": hash_file("prompts/prompts.csv"),
        "ps101_steps_hash": hash_file("prompts/ps101_steps.json"),

        # Model versions
        "openai_models": {
            "gpt-4": "gpt-4-0613",  # Pin versions
            "embeddings": "text-embedding-ada-002"
        },
        "anthropic_models": {
            "claude": "claude-3-sonnet-20240229"
        },

        # Database schema
        "schema_version": get_schema_version(),

        # Feature flags
        "feature_flags": get_feature_flags(),
    }

def hash_file(filepath: str) -> str:
    """Generate SHA-256 hash of file"""
    with open(filepath, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

# Store manifest on startup
DEPLOYMENT_MANIFEST = generate_deployment_manifest()
```

### One-Click Rollback

```python
# scripts/rollback.py

def rollback_to_commit(commit_hash: str):
    """Rollback to specific commit"""
    subprocess.run(['git', 'checkout', commit_hash])
    subprocess.run(['git', 'push', 'railway-origin', 'HEAD:main', '--force'])
    print(f"[ROLLBACK] Deployed commit {commit_hash}")

def automatic_rollback_on_error_budget():
    """Auto-rollback if error budget exceeded"""
    error_budget = 0.01  # 1% error rate allowed
    window_minutes = 15

    current_error_rate = get_error_rate(window_minutes)

    if current_error_rate > error_budget:
        print(f"[AUTO_ROLLBACK] Error rate {current_error_rate:.2%} exceeds budget {error_budget:.2%}")

        # Get previous deployment manifest
        previous_deploy = get_previous_deployment()
        rollback_to_commit(previous_deploy['git_commit'])
```

---

## Continuous Quality Gates

### Golden Dataset Tests

```python
# tests/golden_dataset.py

import pytest
from api.index import app
from fastapi.testclient import client

GOLDEN_DATASET = [
    {
        "input": "I feel stuck in my career...",
        "expected_contains": ["PS101", "step", "question"],
        "expected_json_valid": True,
    },
    {
        "input": "Help me find a job",
        "expected_contains": ["job", "search"],
        "expected_no_contains": ["error", "failed"],
    },
]

@pytest.mark.golden
def test_golden_dataset():
    """Run golden dataset on every deploy"""
    client = TestClient(app)

    for case in GOLDEN_DATASET:
        response = client.post("/wimd/ask", json={"prompt": case["input"]})

        assert response.status_code == 200
        data = response.json()

        if case.get("expected_json_valid"):
            assert isinstance(data, dict)

        for expected in case.get("expected_contains", []):
            assert expected.lower() in str(data).lower()

        for not_expected in case.get("expected_no_contains", []):
            assert not_expected.lower() not in str(data).lower()
```

### Regression Tests (Prompt/Model)

```python
# tests/test_prompts.py

def test_ps101_json_validity():
    """Ensure PS101 steps are valid JSON"""
    with open("prompts/ps101_steps.json") as f:
        data = json.load(f)

    assert isinstance(data, list)
    assert len(data) == 10  # 10 steps

    for step in data:
        assert "step" in step
        assert "title" in step
        assert "prompts" in step
        assert isinstance(step["prompts"], list)

def test_prompt_csv_validity():
    """Ensure prompts CSV is valid"""
    import csv
    with open("prompts/prompts.csv") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) > 0
    for row in rows:
        assert "prompt" in row or "question" in row
        assert "response" in row or "completion" in row
```

---

## Minimal Metrics (Instrumented)

### Health Endpoint Enhancement

```python
# api/index.py (enhanced /health)

@app.get("/health")
async def health_check():
    """Enhanced health check with metrics"""

    return {
        "ok": True,
        "timestamp": datetime.utcnow().isoformat(),

        # Database
        "database": {
            "connected": check_postgres_connection(),
            "type": "postgresql" if connection_pool else "sqlite",
            "fallback_active": connection_pool is None
        },

        # AI Clients
        "ai": {
            "openai_available": check_openai_connection(),
            "anthropic_available": check_anthropic_connection(),
        },

        # Metrics (last 5 minutes)
        "metrics": {
            "requests_total": get_request_count(minutes=5),
            "error_rate": get_error_rate(minutes=5),
            "p95_latency_ms": get_p95_latency(minutes=5),
            "invalid_json_rate": get_invalid_json_rate(minutes=5),
        },

        # Deployment
        "deployment": {
            "git_commit": DEPLOYMENT_MANIFEST['git_commit'][:8],
            "deployed_at": DEPLOYMENT_MANIFEST['timestamp'],
        }
    }
```

### Logging Instrumentation

```python
# api/instrumentation.py

import logging
import time
from functools import wraps

logger = logging.getLogger(__name__)

def instrument_latency(func):
    """Measure and log function latency"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            duration_ms = (time.perf_counter() - start) * 1000
            logger.info(f"[LATENCY] {func.__name__}: {duration_ms:.2f}ms")
            return result
        except Exception as e:
            duration_ms = (time.perf_counter() - start) * 1000
            logger.error(f"[LATENCY] {func.__name__} FAILED after {duration_ms:.2f}ms: {e}")
            raise
    return wrapper

# Usage
@instrument_latency
def call_openai(prompt: str):
    # ...
    pass
```

---

## Production Patterns Checklist

### Pre-Deployment Checklist

**Before pushing to Railway:**

```bash
# Run this script before every deploy
./pre_deploy_check.sh

#!/bin/bash
# Pre-deployment validation

echo "Running pre-deployment checks..."

# 1. Golden dataset tests
pytest tests/test_golden_dataset.py -v || exit 1

# 2. Regression tests
pytest tests/test_prompts.py -v || exit 1

# 3. Schema validation
python -c "import api.storage; api.storage.init_db()" || exit 1

# 4. Environment variables check
python -c "
import os
required = ['DATABASE_URL', 'OPENAI_API_KEY', 'CLAUDE_API_KEY']
missing = [k for k in required if not os.getenv(k)]
if missing:
    print(f'Missing env vars: {missing}')
    exit(1)
" || exit 1

# 5. Database connection test
python -c "
from api.storage import get_conn
with get_conn() as conn:
    print('Database connection: OK')
" || exit 1

echo "✅ All pre-deployment checks passed"
```

### Context Manager Pattern Enforcement

**Rule:** ALL database operations MUST use context manager pattern:

```python
# ✅ CORRECT
with get_conn() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()

# ❌ WRONG (causes AttributeError in PostgreSQL)
conn = get_conn()
cursor = conn.execute("SELECT * FROM users WHERE email = ?", (email,))
```

**Validation:** Add pre-commit hook to check for this pattern:

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check for incorrect get_conn() usage
if grep -rn "conn = get_conn()" api/*.py; then
    echo "ERROR: Found incorrect get_conn() usage"
    echo "Must use: with get_conn() as conn:"
    exit 1
fi
```

### Idempotent Operations

```python
# Ensure all write operations are idempotent

# User creation - use ON CONFLICT
def create_user(email: str, password: str) -> str:
    user_id = str(uuid.uuid4())
    password_hash = hash_password(password)

    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (id, email, password_hash, created_at)
            VALUES (%s, %s, %s, NOW())
            ON CONFLICT (email) DO NOTHING
            RETURNING id
        """, (user_id, email, password_hash))
        result = cursor.fetchone()
        return result[0] if result else get_user_by_email(email)['user_id']
```

---

## LLM-Specific Gotchas & Mitigations

### 1. Context Overflow

```python
def truncate_by_salience(text: str, max_tokens: int = 4000) -> str:
    """Truncate text intelligently by salience"""
    # Simple heuristic: keep first 40% and last 40%, drop middle 20%
    tokens = text.split()
    if len(tokens) <= max_tokens:
        return text

    keep_start = int(max_tokens * 0.4)
    keep_end = int(max_tokens * 0.4)

    return (
        ' '.join(tokens[:keep_start]) +
        ' [...truncated...] ' +
        ' '.join(tokens[-keep_end:])
    )
```

### 2. Provider Multi-Homing

Already implemented in `MultiProviderLLM` class above.

### 3. Safety Filtering

```python
# api/safety.py

import re

DENYLIST = [
    r'\b(password|api[_-]?key|secret|token)\s*[:=]\s*\S+',
    # Add more patterns
]

def sanitize_output(text: str) -> str:
    """Remove sensitive data from LLM output"""
    for pattern in DENYLIST:
        text = re.sub(pattern, '[REDACTED]', text, flags=re.IGNORECASE)
    return text

def is_safe_output(text: str) -> bool:
    """Check if output is safe to show user"""
    # Check for PII, credentials, unsafe content
    for pattern in DENYLIST:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    return True
```

---

## Self-Diagnostic Protocol

**Before making ANY code change, check:**

1. **Will this break the context manager pattern?**
   - All `get_conn()` uses must be `with get_conn() as conn:`
   - Never `conn = get_conn()` directly

2. **Does this introduce SQL syntax differences?**
   - PostgreSQL uses `%s` not `?`
   - PostgreSQL uses `SERIAL` not `AUTOINCREMENT`
   - PostgreSQL needs `cursor = conn.cursor()` before executing

3. **Could this fail silently?**
   - Add explicit error logging
   - Don't swallow exceptions without logging
   - Add health check validation

4. **Is this idempotent?**
   - Can it be run multiple times safely?
   - Use `ON CONFLICT` clauses
   - Check for existence before creating

5. **Does this have a rollback path?**
   - Can I undo this change easily?
   - Is there a feature flag to disable it?
   - Do I have a backup of the old code?

6. **Have I tested the error path?**
   - What happens if PostgreSQL is down?
   - What happens if API key is invalid?
   - What happens if input is malformed?

7. **Is the error observable?**
   - Will this error show up in logs?
   - Will it trigger an alert?
   - Can I diagnose it from the logs alone?

---

## Summary: Error Prevention Workflow

**On every code change:**

```
1. Read SELF_DIAGNOSTIC_FRAMEWORK.md
2. Check: Context manager pattern correct?
3. Check: SQL syntax PostgreSQL-compatible?
4. Check: Errors logged explicitly?
5. Check: Idempotent operations?
6. Check: Rollback path exists?
7. Run: ./pre_deploy_check.sh
8. Deploy: git push railway-origin main
9. Verify: Check /health endpoint
10. Monitor: Watch Railway logs for 5 minutes
```

**If deployment fails:**

```
1. Get Railway logs (Deploy Logs tab)
2. Find error message in logs
3. Classify error using ErrorCategory
4. Execute playbook for error label
5. If no playbook, add context to URGENT_FOR_NARS
6. If bug introduced, rollback immediately
7. Fix locally, test with golden dataset
8. Redeploy with fix
```

---

**END OF SELF-DIAGNOSTIC FRAMEWORK**
