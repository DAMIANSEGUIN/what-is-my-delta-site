"""
Prompt selector for Mosaic 2.0 with CSV→AI fallback system.
Handles prompt selection, caching, and AI fallback when CSV prompts fail.
"""

import json
import hashlib
import time
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from .storage import get_conn
from .ai_clients import get_ai_fallback_response, get_ai_health_status
from .settings import get_settings

class PromptSelector:
    """Handles prompt selection with CSV→AI fallback logic."""
    
    def __init__(self):
        self.settings = get_settings()
        self.cache_ttl_hours = 24
        # Don't cache feature flag - check dynamically to allow runtime updates
    
    def _check_feature_flag(self, flag_name: str) -> bool:
        """Check if a feature flag is enabled."""
        try:
            with get_conn() as conn:
                row = conn.execute(
                    "SELECT enabled FROM feature_flags WHERE flag_name = ?",
                    (flag_name,)
                ).fetchone()
                # FORCE BOOLEAN CONVERSION - SQLite returns 0/1, not True/False
                # This is critical because Python evaluates `0 or False` as False
                return bool(row[0]) if row else False
        except Exception:
            # If feature flags table doesn't exist, default to False
            return False
    
    def _hash_prompt(self, prompt: str) -> str:
        """Create a hash for prompt caching."""
        return hashlib.sha256(prompt.encode()).hexdigest()
    
    def _get_cached_response(self, prompt_hash: str) -> Optional[Dict[str, Any]]:
        """Get cached response for a prompt hash."""
        try:
            with get_conn() as conn:
                row = conn.execute(
                    "SELECT csv_available, ai_fallback_used, last_updated FROM prompt_selector_cache WHERE prompt_hash = ?",
                    (prompt_hash,)
                ).fetchone()
                
                if row:
                    # Check if cache is still valid
                    last_updated = datetime.fromisoformat(row[2])
                    if (datetime.now() - last_updated).total_seconds() < (self.cache_ttl_hours * 3600):
                        return {
                            "csv_available": bool(row[0]),
                            "ai_fallback_used": bool(row[1]),
                            "cached": True
                        }
        except Exception as e:
            print(f"⚠️ Cache lookup failed: {e}")
        
        return None
    
    def _update_cache(self, prompt_hash: str, csv_available: bool, ai_fallback_used: bool):
        """Update cache with prompt selection results."""
        try:
            with get_conn() as conn:
                conn.execute(
                    """INSERT OR REPLACE INTO prompt_selector_cache 
                       (prompt_hash, csv_available, ai_fallback_used, last_updated)
                       VALUES (?, ?, ?, ?)""",
                    (prompt_hash, csv_available, ai_fallback_used, datetime.now().isoformat())
                )
        except Exception as e:
            print(f"⚠️ Cache update failed: {e}")
    
    def _log_fallback_usage(self, session_id: str, prompt_hash: str, csv_response: str, 
                           ai_response: str, fallback_reason: str, response_time_ms: int):
        """Log AI fallback usage for analytics."""
        try:
            with get_conn() as conn:
                conn.execute(
                    """INSERT INTO ai_fallback_logs 
                       (session_id, prompt_hash, csv_response, ai_response, fallback_reason, response_time_ms)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (session_id, prompt_hash, csv_response, ai_response, fallback_reason, response_time_ms)
                )
        except Exception as e:
            print(f"⚠️ Fallback logging failed: {e}")
    
    def select_prompt_response(self, prompt: str, session_id: str, 
                              csv_prompts: Optional[Dict[str, Any]] = None,
                              context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Select the best prompt response using CSV→AI fallback logic."""
        start_time = time.time()
        prompt_hash = self._hash_prompt(prompt)

        # Check if PS101 is active - disable cache for PS101 sessions
        from .storage import get_session_data
        session_data = get_session_data(session_id) if session_id else {}
        ps101_active = session_data.get("ps101_active", False)

        # CACHE DISABLED: The cache stores only metadata (csv_available, ai_fallback_used)
        # but returns placeholder string "Cached response" instead of actual response.
        # This breaks PS101 tangent handling and other flows.
        # TODO: Either store actual responses in cache OR remove caching entirely
        # For now: cache lookup disabled
        # cached = self._get_cached_response(prompt_hash)
        # if cached and cached["cached"]: ...

        # Try CSV prompts first using semantic search
        csv_response = None
        csv_available = False

        if csv_prompts:
            try:
                # Use semantic search to find best matching prompt
                from .index import semantic_search

                prompts_data = csv_prompts.get("prompts", [])
                best_match = semantic_search(prompt, prompts_data, session_history=None)

                if best_match:
                    # CSV rows use "completion"; JSON overrides may use "response"
                    csv_response = best_match.get("response") or best_match.get("completion", "")
                    csv_available = True
                    print(f"✓ Semantic match found for '{prompt[:50]}...' -> '{best_match.get('prompt', '')[:50]}...'")
                else:
                    print(f"⚠️ No semantic match found for '{prompt[:50]}...'")
            except Exception as e:
                print(f"⚠️ CSV prompt lookup failed: {e}")
        
        # If CSV response found, use it
        if csv_response:
            self._update_cache(prompt_hash, True, False)
            return {
                "response": csv_response,
                "source": "csv",
                "csv_available": True,
                "ai_fallback_used": False,
                "response_time_ms": int((time.time() - start_time) * 1000)
            }
        
        # CSV failed, try AI fallback if enabled
        fallback_enabled = self._check_feature_flag("AI_FALLBACK_ENABLED")
        if fallback_enabled:
            ai_health = get_ai_health_status()
            if ai_health.get("any_available", False):
                try:
                    ai_result = get_ai_fallback_response(prompt, context)
                    
                    if ai_result.get("fallback_used", False):
                        # Log the fallback usage
                        self._log_fallback_usage(
                            session_id, prompt_hash, csv_response or "",
                            ai_result.get("response", ""), "csv_unavailable",
                            ai_result.get("response_time_ms", 0)
                        )
                        
                        self._update_cache(prompt_hash, False, True)
                        return {
                            "response": ai_result.get("response", ""),
                            "source": "ai_fallback",
                            "provider": ai_result.get("provider", "unknown"),
                            "csv_available": False,
                            "ai_fallback_used": True,
                            "response_time_ms": ai_result.get("response_time_ms", 0)
                        }
                except Exception as e:
                    print(f"⚠️ AI fallback failed: {e}")
        
        # All methods failed
        self._update_cache(prompt_hash, False, False)
        return {
            "response": "No response available - CSV prompts not found and AI fallback disabled or failed",
            "source": "none",
            "csv_available": False,
            "ai_fallback_used": False,
            "error": "All response methods failed",
            "response_time_ms": int((time.time() - start_time) * 1000)
        }
    
    def get_fallback_stats(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Get AI fallback usage statistics."""
        try:
            with get_conn() as conn:
                if session_id:
                    # Get stats for specific session
                    row = conn.execute(
                        """SELECT COUNT(*) as total_fallbacks, 
                                  AVG(response_time_ms) as avg_response_time,
                                  COUNT(DISTINCT prompt_hash) as unique_prompts
                           FROM ai_fallback_logs WHERE session_id = ?""",
                        (session_id,)
                    ).fetchone()
                else:
                    # Get global stats
                    row = conn.execute(
                        """SELECT COUNT(*) as total_fallbacks,
                                  AVG(response_time_ms) as avg_response_time,
                                  COUNT(DISTINCT prompt_hash) as unique_prompts
                           FROM ai_fallback_logs"""
                    ).fetchone()
                
                if row:
                    return {
                        "total_fallbacks": row[0] or 0,
                        "avg_response_time_ms": int(row[1] or 0),
                        "unique_prompts": row[2] or 0,
                        "fallback_enabled": self._check_feature_flag("AI_FALLBACK_ENABLED")
                    }
        except Exception as e:
            print(f"⚠️ Stats query failed: {e}")
        
        return {
            "total_fallbacks": 0,
            "avg_response_time_ms": 0,
            "unique_prompts": 0,
            "fallback_enabled": self._check_feature_flag("AI_FALLBACK_ENABLED")
        }
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get prompt selector health status."""
        return {
            "fallback_enabled": self._check_feature_flag("AI_FALLBACK_ENABLED"),
            "ai_health": get_ai_health_status(),
            "cache_ttl_hours": self.cache_ttl_hours
        }

# Global prompt selector instance
prompt_selector = PromptSelector()

def get_prompt_response(prompt: str, session_id: str, 
                      csv_prompts: Optional[Dict[str, Any]] = None,
                      context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Get prompt response using the global prompt selector."""
    return prompt_selector.select_prompt_response(prompt, session_id, csv_prompts, context)

def get_prompt_stats(session_id: Optional[str] = None) -> Dict[str, Any]:
    """Get prompt selector statistics."""
    return prompt_selector.get_fallback_stats(session_id)

def get_prompt_health() -> Dict[str, Any]:
    """Get prompt selector health status."""
    return prompt_selector.get_health_status()
