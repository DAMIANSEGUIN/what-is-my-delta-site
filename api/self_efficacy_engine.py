"""
Self-Efficacy Metrics Engine for Mosaic 2.0
Computes experiment completion, learning velocity, confidence scores, and escalation signals.
"""

import json
import math
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass

from .storage import get_conn
from .settings import get_settings

@dataclass
class SelfEfficacyMetrics:
    """Computed self-efficacy metrics for a session"""
    session_id: str
    experiment_completion_rate: float  # 0-1
    learning_velocity: float  # learning events per day
    confidence_score: float  # 0-1
    escalation_risk: float  # 0-1 (higher = more risk)
    total_experiments: int
    completed_experiments: int
    learning_events: int
    days_active: int
    last_activity: Optional[str]
    metrics_timestamp: str

class SelfEfficacyEngine:
    """Handles self-efficacy metrics computation and escalation detection."""
    
    def __init__(self):
        self.settings = get_settings()
        self.metrics_enabled = self._check_feature_flag("SELF_EFFICACY_METRICS")
        self.escalation_enabled = self._check_feature_flag("COACH_ESCALATION")
    
    def _check_feature_flag(self, flag_name: str) -> bool:
        """Check if a feature flag is enabled."""
        try:
            with get_conn() as conn:
                row = conn.execute(
                    "SELECT enabled FROM feature_flags WHERE flag_name = ?",
                    (flag_name,)
                ).fetchone()
                return row and row[0] if row else False
        except Exception:
            return False
    
    def compute_session_metrics(self, session_id: str) -> SelfEfficacyMetrics:
        """Compute comprehensive self-efficacy metrics for a session."""
        if not self.metrics_enabled:
            return SelfEfficacyMetrics(
                session_id=session_id,
                experiment_completion_rate=0.0,
                learning_velocity=0.0,
                confidence_score=0.0,
                escalation_risk=0.0,
                total_experiments=0,
                completed_experiments=0,
                learning_events=0,
                days_active=0,
                last_activity=None,
                metrics_timestamp=datetime.utcnow().isoformat()
            )
        
        try:
            with get_conn() as conn:
                # Get experiment data
                experiment_rows = conn.execute(
                    """SELECT status, created_at, completed_at FROM experiments 
                       WHERE session_id = ? ORDER BY created_at""",
                    (session_id,)
                ).fetchall()
                
                # Get learning data
                learning_rows = conn.execute(
                    """SELECT created_at, confidence_score FROM learning_data 
                       WHERE session_id = ? ORDER BY created_at""",
                    (session_id,)
                ).fetchall()
                
                # Get self-efficacy metrics
                metrics_rows = conn.execute(
                    """SELECT metric_name, metric_value, created_at FROM self_efficacy_metrics 
                       WHERE session_id = ? ORDER BY created_at""",
                    (session_id,)
                ).fetchall()
                
                # Compute metrics
                total_experiments = len(experiment_rows)
                completed_experiments = sum(1 for row in experiment_rows if row[0] == 'completed')
                learning_events = len(learning_rows)
                
                # Experiment completion rate
                completion_rate = completed_experiments / total_experiments if total_experiments > 0 else 0.0
                
                # Learning velocity (events per day)
                if learning_rows:
                    first_learning = datetime.fromisoformat(learning_rows[0][0].replace('Z', '+00:00'))
                    last_learning = datetime.fromisoformat(learning_rows[-1][0].replace('Z', '+00:00'))
                    days_active = max(1, (last_learning - first_learning).days + 1)
                    learning_velocity = learning_events / days_active
                else:
                    days_active = 0
                    learning_velocity = 0.0
                
                # Confidence score
                confidence_scores = [row[1] for row in learning_rows if row[1] is not None]
                avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
                
                # Escalation risk calculation
                escalation_risk = self._calculate_escalation_risk(
                    completion_rate, learning_velocity, avg_confidence, days_active
                )
                
                # Last activity
                last_activity = None
                if experiment_rows:
                    last_activity = experiment_rows[-1][1]  # created_at of last experiment
                
                return SelfEfficacyMetrics(
                    session_id=session_id,
                    experiment_completion_rate=completion_rate,
                    learning_velocity=learning_velocity,
                    confidence_score=avg_confidence,
                    escalation_risk=escalation_risk,
                    total_experiments=total_experiments,
                    completed_experiments=completed_experiments,
                    learning_events=learning_events,
                    days_active=days_active,
                    last_activity=last_activity,
                    metrics_timestamp=datetime.utcnow().isoformat()
                )
                
        except Exception as e:
            print(f"Error computing metrics for session {session_id}: {e}")
            return SelfEfficacyMetrics(
                session_id=session_id,
                experiment_completion_rate=0.0,
                learning_velocity=0.0,
                confidence_score=0.0,
                escalation_risk=1.0,  # High risk if error
                total_experiments=0,
                completed_experiments=0,
                learning_events=0,
                days_active=0,
                last_activity=None,
                metrics_timestamp=datetime.utcnow().isoformat()
            )
    
    def _calculate_escalation_risk(self, completion_rate: float, learning_velocity: float, 
                                 confidence: float, days_active: int) -> float:
        """Calculate escalation risk based on multiple factors."""
        risk_factors = []
        
        # Low completion rate increases risk
        if completion_rate < 0.3:
            risk_factors.append(0.8)
        elif completion_rate < 0.6:
            risk_factors.append(0.4)
        else:
            risk_factors.append(0.1)
        
        # Low learning velocity increases risk
        if learning_velocity < 0.5:
            risk_factors.append(0.7)
        elif learning_velocity < 1.0:
            risk_factors.append(0.3)
        else:
            risk_factors.append(0.1)
        
        # Low confidence increases risk
        if confidence < 0.3:
            risk_factors.append(0.9)
        elif confidence < 0.6:
            risk_factors.append(0.5)
        else:
            risk_factors.append(0.1)
        
        # Long inactivity increases risk
        if days_active > 7 and learning_velocity < 0.2:
            risk_factors.append(0.8)
        
        # Calculate weighted average
        return sum(risk_factors) / len(risk_factors) if risk_factors else 0.0
    
    def should_escalate(self, session_id: str) -> Tuple[bool, str]:
        """Determine if session should be escalated to human coach."""
        if not self.escalation_enabled:
            return False, "Escalation feature disabled"
        
        metrics = self.compute_session_metrics(session_id)
        
        # Escalation triggers
        if metrics.escalation_risk > 0.7:
            return True, f"High escalation risk ({metrics.escalation_risk:.2f}) - low completion/confidence"
        
        if metrics.days_active > 14 and metrics.learning_velocity < 0.1:
            return True, "Long inactivity with minimal learning progress"
        
        if metrics.confidence_score < 0.2 and metrics.total_experiments > 3:
            return True, "Persistently low confidence across multiple experiments"
        
        return False, "No escalation needed"
    
    def get_escalation_prompt(self, session_id: str) -> Optional[str]:
        """Get escalation prompt for coach to contact Damian."""
        should_escalate, reason = self.should_escalate(session_id)
        
        if not should_escalate:
            return None
        
        metrics = self.compute_session_metrics(session_id)
        
        return f"""
🚨 COACH ESCALATION NEEDED

Session: {session_id}
Reason: {reason}

Metrics Summary:
- Experiment Completion: {metrics.completed_experiments}/{metrics.total_experiments} ({metrics.experiment_completion_rate:.1%})
- Learning Velocity: {metrics.learning_velocity:.2f} events/day
- Confidence Score: {metrics.confidence_score:.2f}
- Escalation Risk: {metrics.escalation_risk:.2f}
- Days Active: {metrics.days_active}

Recommended Action: Contact Damian for personalized coaching intervention.
"""
    
    def cleanup_stale_experiments(self, days_threshold: int = 30) -> Dict[str, Any]:
        """Clean up stale experiments and related data."""
        cutoff_date = datetime.utcnow() - timedelta(days=days_threshold)
        
        try:
            with get_conn() as conn:
                # Find stale experiments
                stale_experiments = conn.execute(
                    """SELECT id FROM experiments 
                       WHERE status = 'active' AND created_at < ?""",
                    (cutoff_date.isoformat(),)
                ).fetchall()
                
                if not stale_experiments:
                    return {
                        "cleaned": 0,
                        "message": "No stale experiments found"
                    }
                
                # Clean up related data
                experiment_ids = [row[0] for row in stale_experiments]
                placeholders = ",".join(["?"] * len(experiment_ids))
                
                # Delete related data
                conn.execute(f"DELETE FROM learning_data WHERE experiment_id IN ({placeholders})", experiment_ids)
                conn.execute(f"DELETE FROM experiments WHERE id IN ({placeholders})", experiment_ids)
                
                return {
                    "cleaned": len(experiment_ids),
                    "message": f"Cleaned {len(experiment_ids)} stale experiments"
                }
                
        except Exception as e:
            return {
                "cleaned": 0,
                "error": f"Cleanup failed: {str(e)}"
            }
    
    def record_analytics_entry(self, session_id: str, metrics: SelfEfficacyMetrics) -> None:
        """Record analytics entry for session metrics."""
        try:
            with get_conn() as conn:
                conn.execute(
                    """INSERT INTO self_efficacy_metrics 
                       (session_id, metric_name, metric_value, metric_type, context_data)
                       VALUES (?, ?, ?, ?, ?)""",
                    (session_id, "session_analytics", 1.0, "analytics",
                     json.dumps({
                         "experiment_completion_rate": metrics.experiment_completion_rate,
                         "learning_velocity": metrics.learning_velocity,
                         "confidence_score": metrics.confidence_score,
                         "escalation_risk": metrics.escalation_risk,
                         "total_experiments": metrics.total_experiments,
                         "completed_experiments": metrics.completed_experiments,
                         "learning_events": metrics.learning_events,
                         "days_active": metrics.days_active
                     })))
        except Exception as e:
            print(f"Error recording analytics for session {session_id}: {e}")
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get self-efficacy engine health status."""
        return {
            "metrics_enabled": self.metrics_enabled,
            "escalation_enabled": self.escalation_enabled,
            "feature_flags": {
                "SELF_EFFICACY_METRICS": self.metrics_enabled,
                "COACH_ESCALATION": self.escalation_enabled
            },
            "status": "operational" if self.metrics_enabled else "disabled"
        }

# Global self-efficacy engine instance
self_efficacy_engine = SelfEfficacyEngine()

def compute_session_metrics(session_id: str) -> SelfEfficacyMetrics:
    """Compute metrics using the global engine."""
    return self_efficacy_engine.compute_session_metrics(session_id)

def should_escalate(session_id: str) -> Tuple[bool, str]:
    """Check escalation using the global engine."""
    return self_efficacy_engine.should_escalate(session_id)

def get_escalation_prompt(session_id: str) -> Optional[str]:
    """Get escalation prompt using the global engine."""
    return self_efficacy_engine.get_escalation_prompt(session_id)

def cleanup_stale_experiments(days_threshold: int = 30) -> Dict[str, Any]:
    """Cleanup using the global engine."""
    return self_efficacy_engine.cleanup_stale_experiments(days_threshold)

def record_analytics_entry(session_id: str, metrics: SelfEfficacyMetrics) -> None:
    """Record analytics using the global engine."""
    self_efficacy_engine.record_analytics_entry(session_id, metrics)

def get_self_efficacy_health() -> Dict[str, Any]:
    """Get health status using the global engine."""
    return self_efficacy_engine.get_health_status()
