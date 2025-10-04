"""
Cost Controls and Resource Management for Mosaic 2.0
Prevents runaway costs and resource exhaustion.
"""

import time
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

from .storage import get_conn

@dataclass
class CostLimit:
    """Cost limit configuration"""
    daily_limit: float = 10.0  # $10/day limit
    monthly_limit: float = 100.0  # $100/month limit
    per_request_limit: float = 0.01  # $0.01 per request limit
    emergency_stop: float = 50.0  # Emergency stop at $50

@dataclass
class ResourceLimit:
    """Resource limit configuration"""
    max_requests_per_minute: int = 60
    max_requests_per_hour: int = 1000
    max_requests_per_day: int = 10000
    max_embedding_requests: int = 100  # Per day
    max_job_search_requests: int = 500  # Per day
    max_concurrent_requests: int = 10

class CostController:
    """Manages costs and resource usage to prevent runaway expenses."""
    
    def __init__(self):
        self.cost_limits = CostLimit()
        self.resource_limits = ResourceLimit()
        self.usage_tracking = {}
        self.emergency_stop = False
    
    def check_cost_limits(self, operation: str, estimated_cost: float = 0.0) -> Dict[str, Any]:
        """Check if operation is within cost limits."""
        try:
            # Get current usage
            current_usage = self._get_current_usage()
            
            # Check daily limit
            if current_usage["daily_cost"] + estimated_cost > self.cost_limits.daily_limit:
                return {
                    "allowed": False,
                    "reason": "Daily cost limit exceeded",
                    "current_cost": current_usage["daily_cost"],
                    "limit": self.cost_limits.daily_limit
                }
            
            # Check monthly limit
            if current_usage["monthly_cost"] + estimated_cost > self.cost_limits.monthly_limit:
                return {
                    "allowed": False,
                    "reason": "Monthly cost limit exceeded",
                    "current_cost": current_usage["monthly_cost"],
                    "limit": self.cost_limits.monthly_limit
                }
            
            # Check emergency stop
            if current_usage["daily_cost"] > self.cost_limits.emergency_stop:
                self.emergency_stop = True
                return {
                    "allowed": False,
                    "reason": "Emergency stop triggered",
                    "current_cost": current_usage["daily_cost"],
                    "limit": self.cost_limits.emergency_stop
                }
            
            return {
                "allowed": True,
                "reason": "Within cost limits",
                "current_cost": current_usage["daily_cost"],
                "limit": self.cost_limits.daily_limit
            }
            
        except Exception as e:
            print(f"Error checking cost limits: {e}")
            return {
                "allowed": False,
                "reason": "Error checking limits",
                "error": str(e)
            }
    
    def check_resource_limits(self, operation: str) -> Dict[str, Any]:
        """Check if operation is within resource limits."""
        try:
            # Get current usage
            current_usage = self._get_current_usage()
            
            # Check per-minute limit
            if current_usage["requests_this_minute"] >= self.resource_limits.max_requests_per_minute:
                return {
                    "allowed": False,
                    "reason": "Rate limit exceeded (per minute)",
                    "current": current_usage["requests_this_minute"],
                    "limit": self.resource_limits.max_requests_per_minute
                }
            
            # Check per-hour limit
            if current_usage["requests_this_hour"] >= self.resource_limits.max_requests_per_hour:
                return {
                    "allowed": False,
                    "reason": "Rate limit exceeded (per hour)",
                    "current": current_usage["requests_this_hour"],
                    "limit": self.resource_limits.max_requests_per_hour
                }
            
            # Check per-day limit
            if current_usage["requests_today"] >= self.resource_limits.max_requests_per_day:
                return {
                    "allowed": False,
                    "reason": "Daily request limit exceeded",
                    "current": current_usage["requests_today"],
                    "limit": self.resource_limits.max_requests_per_day
                }
            
            # Check operation-specific limits
            if operation == "embedding" and current_usage["embedding_requests_today"] >= self.resource_limits.max_embedding_requests:
                return {
                    "allowed": False,
                    "reason": "Daily embedding limit exceeded",
                    "current": current_usage["embedding_requests_today"],
                    "limit": self.resource_limits.max_embedding_requests
                }
            
            if operation == "job_search" and current_usage["job_search_requests_today"] >= self.resource_limits.max_job_search_requests:
                return {
                    "allowed": False,
                    "reason": "Daily job search limit exceeded",
                    "current": current_usage["job_search_requests_today"],
                    "limit": self.resource_limits.max_job_search_requests
                }
            
            return {
                "allowed": True,
                "reason": "Within resource limits",
                "current": current_usage["requests_this_minute"],
                "limit": self.resource_limits.max_requests_per_minute
            }
            
        except Exception as e:
            print(f"Error checking resource limits: {e}")
            return {
                "allowed": False,
                "reason": "Error checking limits",
                "error": str(e)
            }
    
    def _get_current_usage(self) -> Dict[str, Any]:
        """Get current usage statistics."""
        try:
            with get_conn() as conn:
                # Get daily usage
                daily_usage = conn.execute(
                    """SELECT 
                        COUNT(*) as requests_today,
                        SUM(CASE WHEN operation = 'embedding' THEN 1 ELSE 0 END) as embedding_requests_today,
                        SUM(CASE WHEN operation = 'job_search' THEN 1 ELSE 0 END) as job_search_requests_today,
                        SUM(estimated_cost) as daily_cost
                       FROM usage_tracking 
                       WHERE DATE(created_at) = DATE('now')"""
                ).fetchone()
                
                # Get hourly usage
                hourly_usage = conn.execute(
                    """SELECT COUNT(*) as requests_this_hour
                       FROM usage_tracking 
                       WHERE created_at >= datetime('now', '-1 hour')"""
                ).fetchone()
                
                # Get minute usage
                minute_usage = conn.execute(
                    """SELECT COUNT(*) as requests_this_minute
                       FROM usage_tracking 
                       WHERE created_at >= datetime('now', '-1 minute')"""
                ).fetchone()
                
                # Get monthly usage
                monthly_usage = conn.execute(
                    """SELECT SUM(estimated_cost) as monthly_cost
                       FROM usage_tracking 
                       WHERE DATE(created_at) >= DATE('now', 'start of month')"""
                ).fetchone()
                
                return {
                    "requests_today": daily_usage[0] or 0,
                    "embedding_requests_today": daily_usage[1] or 0,
                    "job_search_requests_today": daily_usage[2] or 0,
                    "daily_cost": daily_usage[3] or 0.0,
                    "requests_this_hour": hourly_usage[0] or 0,
                    "requests_this_minute": minute_usage[0] or 0,
                    "monthly_cost": monthly_usage[0] or 0.0
                }
                
        except Exception as e:
            print(f"Error getting current usage: {e}")
            return {
                "requests_today": 0,
                "embedding_requests_today": 0,
                "job_search_requests_today": 0,
                "daily_cost": 0.0,
                "requests_this_hour": 0,
                "requests_this_minute": 0,
                "monthly_cost": 0.0
            }
    
    def record_usage(self, operation: str, estimated_cost: float = 0.0, success: bool = True):
        """Record usage for tracking and cost control."""
        try:
            with get_conn() as conn:
                conn.execute(
                    """INSERT INTO usage_tracking 
                       (operation, estimated_cost, success, created_at)
                       VALUES (?, ?, ?, ?)""",
                    (operation, estimated_cost, success, datetime.utcnow().isoformat())
                )
        except Exception as e:
            print(f"Error recording usage: {e}")
    
    def get_usage_analytics(self) -> Dict[str, Any]:
        """Get usage analytics for monitoring."""
        try:
            current_usage = self._get_current_usage()
            
            return {
                "cost_limits": {
                    "daily_limit": self.cost_limits.daily_limit,
                    "monthly_limit": self.cost_limits.monthly_limit,
                    "emergency_stop": self.cost_limits.emergency_stop
                },
                "resource_limits": {
                    "max_requests_per_minute": self.resource_limits.max_requests_per_minute,
                    "max_requests_per_hour": self.resource_limits.max_requests_per_hour,
                    "max_requests_per_day": self.resource_limits.max_requests_per_day
                },
                "current_usage": current_usage,
                "emergency_stop": self.emergency_stop,
                "status": "operational" if not self.emergency_stop else "emergency_stop"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

# Global cost controller instance
cost_controller = CostController()

def check_cost_limits(operation: str, estimated_cost: float = 0.0) -> Dict[str, Any]:
    """Check if operation is within cost limits."""
    return cost_controller.check_cost_limits(operation, estimated_cost)

def check_resource_limits(operation: str) -> Dict[str, Any]:
    """Check if operation is within resource limits."""
    return cost_controller.check_resource_limits(operation)

def record_usage(operation: str, estimated_cost: float = 0.0, success: bool = True):
    """Record usage for tracking and cost control."""
    cost_controller.record_usage(operation, estimated_cost, success)

def get_usage_analytics() -> Dict[str, Any]:
    """Get usage analytics for monitoring."""
    return cost_controller.get_usage_analytics()
