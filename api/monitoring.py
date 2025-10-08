"""
Monitoring and alerting system for WIMD prompt failures.
Provides automatic recovery and detailed logging.
"""

import time
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from .storage import get_conn
from .prompt_selector import get_prompt_response, get_prompt_health

class PromptMonitor:
    """Monitor prompt system health and trigger recovery actions."""

    def __init__(self):
        self.failure_threshold = 3  # Failed attempts before action
        self.recovery_actions = []

    def test_prompt_system(self) -> Dict[str, Any]:
        """Test the prompt system with a known good prompt."""
        test_prompt = "I feel stuck in my career"

        try:
            # Load CSV prompts like the main API does
            from .prompts_loader import read_registry
            import json
            import os

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
            except Exception as e:
                print(f"Failed to load CSV prompts: {e}")

            start_time = time.time()
            result = get_prompt_response(
                prompt=test_prompt,
                session_id="health_check",
                csv_prompts=csv_prompts,
                context=None
            )
            response_time = int((time.time() - start_time) * 1000)

            # Check if we got a real response (not error message)
            success = (
                result.get("response", "") != "No response available - CSV prompts not found and AI fallback disabled or failed"
                and result.get("source") != "none"
                and len(result.get("response", "")) > 10
            )

            return {
                "success": success,
                "response_time_ms": response_time,
                "source": result.get("source", "unknown"),
                "result": result,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    def log_failure(self, test_result: Dict[str, Any]):
        """Log prompt system failure for debugging."""
        try:
            with get_conn() as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS prompt_health_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        success BOOLEAN,
                        response_time_ms INTEGER,
                        source TEXT,
                        error TEXT,
                        full_result TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                conn.execute("""
                    INSERT INTO prompt_health_log
                    (success, response_time_ms, source, error, full_result)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    test_result.get("success", False),
                    test_result.get("response_time_ms"),
                    test_result.get("source"),
                    test_result.get("error"),
                    json.dumps(test_result)
                ))
        except Exception as e:
            print(f"Failed to log health check: {e}")

    def attempt_recovery(self) -> Dict[str, Any]:
        """Attempt to recover from prompt system failure."""
        recovery_actions = []

        try:
            # 1. Clear prompt cache
            with get_conn() as conn:
                result = conn.execute("DELETE FROM prompt_selector_cache").rowcount
                recovery_actions.append(f"Cleared {result} cache entries")

            # 2. Ensure AI fallback is enabled
            with get_conn() as conn:
                conn.execute("""
                    UPDATE feature_flags
                    SET enabled = 1
                    WHERE flag_name = 'AI_FALLBACK_ENABLED'
                """)
                recovery_actions.append("Enabled AI fallback")

            # 3. Test system again
            test_result = self.test_prompt_system()

            return {
                "recovery_attempted": True,
                "actions_taken": recovery_actions,
                "test_after_recovery": test_result,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return {
                "recovery_attempted": False,
                "error": str(e),
                "actions_taken": recovery_actions,
                "timestamp": datetime.utcnow().isoformat()
            }

    def get_recent_failures(self, hours: int = 24) -> list:
        """Get recent prompt system failures."""
        try:
            with get_conn() as conn:
                rows = conn.execute("""
                    SELECT success, response_time_ms, source, error, timestamp
                    FROM prompt_health_log
                    WHERE timestamp > datetime('now', '-{} hours')
                    ORDER BY timestamp DESC
                """.format(hours)).fetchall()

                return [
                    {
                        "success": bool(row[0]),
                        "response_time_ms": row[1],
                        "source": row[2],
                        "error": row[3],
                        "timestamp": row[4]
                    }
                    for row in rows
                ]
        except Exception:
            return []

    def get_health_summary(self) -> Dict[str, Any]:
        """Get comprehensive health summary."""
        test_result = self.test_prompt_system()
        recent_failures = self.get_recent_failures()
        prompt_health = get_prompt_health()

        # Calculate failure rate
        total_recent = len(recent_failures)
        failed_recent = len([f for f in recent_failures if not f["success"]])
        failure_rate = (failed_recent / total_recent * 100) if total_recent > 0 else 0

        return {
            "current_test": test_result,
            "prompt_system_health": prompt_health,
            "recent_failures": failed_recent,
            "total_recent_tests": total_recent,
            "failure_rate_percent": round(failure_rate, 2),
            "requires_attention": failure_rate > 50 or not test_result.get("success", False),
            "timestamp": datetime.utcnow().isoformat()
        }

# Global monitor instance
prompt_monitor = PromptMonitor()

def run_health_check() -> Dict[str, Any]:
    """Run comprehensive health check and return results."""
    return prompt_monitor.get_health_summary()

def attempt_system_recovery() -> Dict[str, Any]:
    """Attempt automatic system recovery."""
    return prompt_monitor.attempt_recovery()