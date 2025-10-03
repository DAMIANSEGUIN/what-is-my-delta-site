"""
Experiment Engine for Mosaic 2.0
Handles experiment creation, learning data capture, and self-efficacy metrics.
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from .storage import get_conn
from .settings import get_settings

class ExperimentCreate(BaseModel):
    """Request model for creating an experiment"""
    experiment_name: str = Field(..., description="Name of the experiment")
    description: Optional[str] = Field(None, description="Description of the experiment")
    user_id: Optional[str] = Field(None, description="User ID (optional)")

class ExperimentUpdate(BaseModel):
    """Request model for updating an experiment"""
    experiment_id: str = Field(..., description="Experiment ID")
    status: Optional[str] = Field(None, description="New status")
    description: Optional[str] = Field(None, description="Updated description")

class LearningData(BaseModel):
    """Request model for adding learning data"""
    experiment_id: str = Field(..., description="Experiment ID")
    learning_type: str = Field(..., description="Type of learning (skill, knowledge, behavior)")
    content: str = Field(..., description="Learning content")
    confidence_score: Optional[float] = Field(None, description="Confidence score (0-1)")
    evidence_data: Optional[Dict[str, Any]] = Field(None, description="Additional evidence data")

class CapabilityEvidence(BaseModel):
    """Request model for capturing capability evidence"""
    capability_name: str = Field(..., description="Name of the capability")
    evidence_type: str = Field(..., description="Type of evidence")
    evidence_data: Dict[str, Any] = Field(..., description="Evidence data")
    confidence_level: Optional[float] = Field(None, description="Confidence level (0-1)")

class SelfEfficacyMetric(BaseModel):
    """Request model for self-efficacy metrics"""
    metric_name: str = Field(..., description="Name of the metric")
    metric_value: float = Field(..., description="Metric value")
    metric_type: Optional[str] = Field(None, description="Type of metric")
    context_data: Optional[Dict[str, Any]] = Field(None, description="Context data")

class ExperimentEngine:
    """Handles experiment engine operations with feature flag support."""
    
    def __init__(self):
        self.settings = get_settings()
        self.experiments_enabled = self._check_feature_flag("EXPERIMENTS_ENABLED")
    
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
    
    def create_experiment(self, session_id: str, experiment_data: ExperimentCreate, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a new experiment."""
        if not self.experiments_enabled:
            return {"error": "Experiments feature not enabled"}
        
        experiment_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        try:
            with get_conn() as conn:
                conn.execute(
                    """INSERT INTO experiments (id, user_id, session_id, experiment_name, description, status, created_at, updated_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (experiment_id, user_id, session_id, experiment_data.experiment_name, 
                     experiment_data.description, "active", now, now)
                )
            
            return {
                "experiment_id": experiment_id,
                "status": "created",
                "message": "Experiment created successfully"
            }
        except Exception as e:
            return {"error": f"Failed to create experiment: {str(e)}"}
    
    def update_experiment(self, session_id: str, experiment_data: ExperimentUpdate) -> Dict[str, Any]:
        """Update an existing experiment."""
        if not self.experiments_enabled:
            return {"error": "Experiments feature not enabled"}
        
        try:
            with get_conn() as conn:
                # Check if experiment exists and belongs to session
                row = conn.execute(
                    "SELECT id FROM experiments WHERE id = ? AND session_id = ?",
                    (experiment_data.experiment_id, session_id)
                ).fetchone()
                
                if not row:
                    return {"error": "Experiment not found or access denied"}
                
                # Update experiment
                update_fields = []
                update_values = []
                
                if experiment_data.status:
                    update_fields.append("status = ?")
                    update_values.append(experiment_data.status)
                
                if experiment_data.description:
                    update_fields.append("description = ?")
                    update_values.append(experiment_data.description)
                
                if update_fields:
                    update_fields.append("updated_at = ?")
                    update_values.append(datetime.utcnow().isoformat())
                    update_values.append(experiment_data.experiment_id)
                    
                    conn.execute(
                        f"UPDATE experiments SET {', '.join(update_fields)} WHERE id = ?",
                        update_values
                    )
                
                return {
                    "experiment_id": experiment_data.experiment_id,
                    "status": "updated",
                    "message": "Experiment updated successfully"
                }
        except Exception as e:
            return {"error": f"Failed to update experiment: {str(e)}"}
    
    def complete_experiment(self, session_id: str, experiment_id: str) -> Dict[str, Any]:
        """Mark an experiment as completed."""
        if not self.experiments_enabled:
            return {"error": "Experiments feature not enabled"}
        
        try:
            with get_conn() as conn:
                # Check if experiment exists and belongs to session
                row = conn.execute(
                    "SELECT id FROM experiments WHERE id = ? AND session_id = ?",
                    (experiment_id, session_id)
                ).fetchone()
                
                if not row:
                    return {"error": "Experiment not found or access denied"}
                
                # Mark as completed
                conn.execute(
                    "UPDATE experiments SET status = ?, completed_at = ?, updated_at = ? WHERE id = ?",
                    ("completed", datetime.utcnow().isoformat(), datetime.utcnow().isoformat(), experiment_id)
                )
                
                return {
                    "experiment_id": experiment_id,
                    "status": "completed",
                    "message": "Experiment completed successfully"
                }
        except Exception as e:
            return {"error": f"Failed to complete experiment: {str(e)}"}
    
    def add_learning_data(self, session_id: str, learning_data: LearningData) -> Dict[str, Any]:
        """Add learning data to an experiment."""
        if not self.experiments_enabled:
            return {"error": "Experiments feature not enabled"}
        
        try:
            with get_conn() as conn:
                # Verify experiment exists and belongs to session
                row = conn.execute(
                    "SELECT id FROM experiments WHERE id = ? AND session_id = ?",
                    (learning_data.experiment_id, session_id)
                ).fetchone()
                
                if not row:
                    return {"error": "Experiment not found or access denied"}
                
                # Add learning data
                conn.execute(
                    """INSERT INTO learning_data (experiment_id, session_id, learning_type, content, confidence_score, evidence_data)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (learning_data.experiment_id, session_id, learning_data.learning_type,
                     learning_data.content, learning_data.confidence_score,
                     json.dumps(learning_data.evidence_data or {}))
                )
                
                return {
                    "experiment_id": learning_data.experiment_id,
                    "status": "learning_added",
                    "message": "Learning data added successfully"
                }
        except Exception as e:
            return {"error": f"Failed to add learning data: {str(e)}"}
    
    def capture_evidence(self, session_id: str, evidence_data: CapabilityEvidence) -> Dict[str, Any]:
        """Capture capability evidence."""
        if not self.experiments_enabled:
            return {"error": "Experiments feature not enabled"}
        
        try:
            with get_conn() as conn:
                conn.execute(
                    """INSERT INTO capability_evidence (session_id, capability_name, evidence_type, evidence_data, confidence_level)
                       VALUES (?, ?, ?, ?, ?)""",
                    (session_id, evidence_data.capability_name, evidence_data.evidence_type,
                     json.dumps(evidence_data.evidence_data), evidence_data.confidence_level)
                )
                
                return {
                    "session_id": session_id,
                    "status": "evidence_captured",
                    "message": "Capability evidence captured successfully"
                }
        except Exception as e:
            return {"error": f"Failed to capture evidence: {str(e)}"}
    
    def record_self_efficacy_metric(self, session_id: str, metric_data: SelfEfficacyMetric) -> Dict[str, Any]:
        """Record a self-efficacy metric."""
        if not self.experiments_enabled:
            return {"error": "Experiments feature not enabled"}
        
        try:
            with get_conn() as conn:
                conn.execute(
                    """INSERT INTO self_efficacy_metrics (session_id, metric_name, metric_value, metric_type, context_data)
                       VALUES (?, ?, ?, ?, ?)""",
                    (session_id, metric_data.metric_name, metric_data.metric_value,
                     metric_data.metric_type, json.dumps(metric_data.context_data or {}))
                )
                
                return {
                    "session_id": session_id,
                    "status": "metric_recorded",
                    "message": "Self-efficacy metric recorded successfully"
                }
        except Exception as e:
            return {"error": f"Failed to record metric: {str(e)}"}
    
    def get_experiments(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all experiments for a session."""
        if not self.experiments_enabled:
            return []
        
        try:
            with get_conn() as conn:
                rows = conn.execute(
                    """SELECT id, experiment_name, description, status, created_at, updated_at, completed_at
                       FROM experiments WHERE session_id = ? ORDER BY created_at DESC""",
                    (session_id,)
                ).fetchall()
                
                experiments = []
                for row in rows:
                    experiments.append({
                        "experiment_id": row[0],
                        "experiment_name": row[1],
                        "description": row[2],
                        "status": row[3],
                        "created_at": row[4],
                        "updated_at": row[5],
                        "completed_at": row[6]
                    })
                
                return experiments
        except Exception as e:
            return []
    
    def get_learning_data(self, session_id: str, experiment_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get learning data for a session or specific experiment."""
        if not self.experiments_enabled:
            return []
        
        try:
            with get_conn() as conn:
                if experiment_id:
                    rows = conn.execute(
                        """SELECT learning_type, content, confidence_score, evidence_data, created_at
                           FROM learning_data WHERE session_id = ? AND experiment_id = ? ORDER BY created_at DESC""",
                        (session_id, experiment_id)
                    ).fetchall()
                else:
                    rows = conn.execute(
                        """SELECT learning_type, content, confidence_score, evidence_data, created_at
                           FROM learning_data WHERE session_id = ? ORDER BY created_at DESC""",
                        (session_id,)
                    ).fetchall()
                
                learning_data = []
                for row in rows:
                    learning_data.append({
                        "learning_type": row[0],
                        "content": row[1],
                        "confidence_score": row[2],
                        "evidence_data": json.loads(row[3]) if row[3] else {},
                        "created_at": row[4]
                    })
                
                return learning_data
        except Exception as e:
            return []
    
    def get_self_efficacy_metrics(self, session_id: str) -> List[Dict[str, Any]]:
        """Get self-efficacy metrics for a session."""
        if not self.experiments_enabled:
            return []
        
        try:
            with get_conn() as conn:
                rows = conn.execute(
                    """SELECT metric_name, metric_value, metric_type, context_data, created_at
                       FROM self_efficacy_metrics WHERE session_id = ? ORDER BY created_at DESC""",
                    (session_id,)
                ).fetchall()
                
                metrics = []
                for row in rows:
                    metrics.append({
                        "metric_name": row[0],
                        "metric_value": row[1],
                        "metric_type": row[2],
                        "context_data": json.loads(row[3]) if row[3] else {},
                        "created_at": row[4]
                    })
                
                return metrics
        except Exception as e:
            return []
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get experiment engine health status."""
        return {
            "experiments_enabled": self.experiments_enabled,
            "feature_flag": "EXPERIMENTS_ENABLED",
            "status": "operational" if self.experiments_enabled else "disabled"
        }

# Global experiment engine instance
experiment_engine = ExperimentEngine()

def create_experiment(session_id: str, experiment_data: ExperimentCreate, user_id: Optional[str] = None) -> Dict[str, Any]:
    """Create a new experiment using the global engine."""
    return experiment_engine.create_experiment(session_id, experiment_data, user_id)

def update_experiment(session_id: str, experiment_data: ExperimentUpdate) -> Dict[str, Any]:
    """Update an experiment using the global engine."""
    return experiment_engine.update_experiment(session_id, experiment_data)

def complete_experiment(session_id: str, experiment_id: str) -> Dict[str, Any]:
    """Complete an experiment using the global engine."""
    return experiment_engine.complete_experiment(session_id, experiment_id)

def add_learning_data(session_id: str, learning_data: LearningData) -> Dict[str, Any]:
    """Add learning data using the global engine."""
    return experiment_engine.add_learning_data(session_id, learning_data)

def capture_evidence(session_id: str, evidence_data: CapabilityEvidence) -> Dict[str, Any]:
    """Capture evidence using the global engine."""
    return experiment_engine.capture_evidence(session_id, evidence_data)

def record_self_efficacy_metric(session_id: str, metric_data: SelfEfficacyMetric) -> Dict[str, Any]:
    """Record self-efficacy metric using the global engine."""
    return experiment_engine.record_self_efficacy_metric(session_id, metric_data)

def get_experiments(session_id: str) -> List[Dict[str, Any]]:
    """Get experiments using the global engine."""
    return experiment_engine.get_experiments(session_id)

def get_learning_data(session_id: str, experiment_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get learning data using the global engine."""
    return experiment_engine.get_learning_data(session_id, experiment_id)

def get_self_efficacy_metrics(session_id: str) -> List[Dict[str, Any]]:
    """Get self-efficacy metrics using the global engine."""
    return experiment_engine.get_self_efficacy_metrics(session_id)

def get_experiment_health() -> Dict[str, Any]:
    """Get experiment engine health status."""
    return experiment_engine.get_health_status()
