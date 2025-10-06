"""
Analytics Dashboard for Mosaic 2.0
Tracks match score distribution, rerank lift, and token usage
"""

import json
import csv
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from .storage import get_conn

class AnalyticsEngine:
    """Analytics engine for tracking semantic match improvements."""
    
    def __init__(self):
        self.metrics_cache = {}
        self.cache_ttl = 300  # 5 minutes
    
    def log_match_analytics(self, query: str, pre_scores: List[float], post_scores: List[float], 
                          improvement_pct: float, processing_time: float):
        """Log match analytics for tracking improvements."""
        try:
            with get_conn() as conn:
                # Create analytics table if it doesn't exist
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS match_analytics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        query_hash TEXT,
                        query_text TEXT,
                        pre_rerank_avg REAL,
                        post_rerank_avg REAL,
                        improvement_pct REAL,
                        processing_time REAL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Insert analytics record
                query_hash = self._get_query_hash(query)
                pre_avg = sum(pre_scores) / len(pre_scores) if pre_scores else 0.0
                post_avg = sum(post_scores) / len(post_scores) if post_scores else 0.0
                
                conn.execute("""
                    INSERT INTO match_analytics 
                    (query_hash, query_text, pre_rerank_avg, post_rerank_avg, improvement_pct, processing_time)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (query_hash, query, pre_avg, post_avg, improvement_pct, processing_time))
                
        except Exception as e:
            print(f"Error logging analytics: {e}")
    
    def log_token_usage(self, operation: str, tokens: int, cost: float, success: bool):
        """Log token usage for cost tracking."""
        try:
            with get_conn() as conn:
                # Create token usage table if it doesn't exist
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS token_usage (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        operation TEXT,
                        tokens INTEGER,
                        cost REAL,
                        success BOOLEAN,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Insert token usage record
                conn.execute("""
                    INSERT INTO token_usage (operation, tokens, cost, success)
                    VALUES (?, ?, ?, ?)
                """, (operation, tokens, cost, success))
                
        except Exception as e:
            print(f"Error logging token usage: {e}")
    
    def get_match_analytics(self, days: int = 7) -> Dict[str, Any]:
        """Get match analytics for the specified period."""
        try:
            with get_conn() as conn:
                # Get analytics data
                rows = conn.execute("""
                    SELECT 
                        AVG(pre_rerank_avg) as avg_pre_score,
                        AVG(post_rerank_avg) as avg_post_score,
                        AVG(improvement_pct) as avg_improvement,
                        AVG(processing_time) as avg_processing_time,
                        COUNT(*) as total_queries
                    FROM match_analytics 
                    WHERE timestamp > datetime('now', '-{} days')
                """.format(days)).fetchone()
                
                if rows:
                    return {
                        "period_days": days,
                        "total_queries": rows[4],
                        "avg_pre_score": round(rows[0], 3) if rows[0] else 0.0,
                        "avg_post_score": round(rows[1], 3) if rows[1] else 0.0,
                        "avg_improvement_pct": round(rows[2], 1) if rows[2] else 0.0,
                        "avg_processing_time": round(rows[3], 3) if rows[3] else 0.0,
                        "status": "operational"
                    }
                else:
                    return {
                        "period_days": days,
                        "total_queries": 0,
                        "avg_pre_score": 0.0,
                        "avg_post_score": 0.0,
                        "avg_improvement_pct": 0.0,
                        "avg_processing_time": 0.0,
                        "status": "no_data"
                    }
                    
        except Exception as e:
            return {
                "error": str(e),
                "status": "error"
            }
    
    def get_token_usage_analytics(self, days: int = 7) -> Dict[str, Any]:
        """Get token usage analytics for the specified period."""
        try:
            with get_conn() as conn:
                # Get token usage data
                rows = conn.execute("""
                    SELECT 
                        operation,
                        SUM(tokens) as total_tokens,
                        SUM(cost) as total_cost,
                        COUNT(*) as total_operations,
                        AVG(CASE WHEN success = 1 THEN tokens ELSE 0 END) as avg_successful_tokens
                    FROM token_usage 
                    WHERE timestamp > datetime('now', '-{} days')
                    GROUP BY operation
                """.format(days)).fetchall()
                
                operations = {}
                total_cost = 0.0
                total_tokens = 0
                
                for row in rows:
                    operation, tokens, cost, ops, avg_tokens = row
                    operations[operation] = {
                        "total_tokens": tokens,
                        "total_cost": round(cost, 4),
                        "total_operations": ops,
                        "avg_successful_tokens": round(avg_tokens, 1) if avg_tokens else 0
                    }
                    total_cost += cost
                    total_tokens += tokens
                
                return {
                    "period_days": days,
                    "total_cost": round(total_cost, 4),
                    "total_tokens": total_tokens,
                    "operations": operations,
                    "status": "operational"
                }
                
        except Exception as e:
            return {
                "error": str(e),
                "status": "error"
            }
    
    def export_analytics_csv(self, days: int = 7, filename: str = None) -> str:
        """Export analytics data to CSV."""
        try:
            if not filename:
                filename = f"mosaic_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with get_conn() as conn:
                # Get match analytics
                match_rows = conn.execute("""
                    SELECT query_text, pre_rerank_avg, post_rerank_avg, improvement_pct, processing_time, timestamp
                    FROM match_analytics 
                    WHERE timestamp > datetime('now', '-{} days')
                    ORDER BY timestamp DESC
                """.format(days)).fetchall()
                
                # Write to CSV
                with open(filename, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Query', 'Pre-Rerank Score', 'Post-Rerank Score', 'Improvement %', 'Processing Time', 'Timestamp'])
                    
                    for row in match_rows:
                        writer.writerow(row)
            
            return filename
            
        except Exception as e:
            print(f"Error exporting analytics: {e}")
            return None
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data."""
        return {
            "match_analytics": self.get_match_analytics(),
            "token_usage": self.get_token_usage_analytics(),
            "generated_at": datetime.utcnow().isoformat(),
            "status": "operational"
        }
    
    def _get_query_hash(self, query: str) -> str:
        """Generate hash for query."""
        import hashlib
        return hashlib.sha256(query.encode()).hexdigest()[:16]
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get analytics engine health status."""
        return {
            "analytics_enabled": True,
            "cache_size": len(self.metrics_cache),
            "cache_ttl": self.cache_ttl,
            "status": "operational"
        }

# Global analytics engine instance
analytics_engine = AnalyticsEngine()

def log_match_analytics(query: str, pre_scores: List[float], post_scores: List[float], 
                       improvement_pct: float, processing_time: float):
    """Log match analytics using the global engine."""
    analytics_engine.log_match_analytics(query, pre_scores, post_scores, improvement_pct, processing_time)

def log_token_usage(operation: str, tokens: int, cost: float, success: bool):
    """Log token usage using the global engine."""
    analytics_engine.log_token_usage(operation, tokens, cost, success)

def get_analytics_dashboard() -> Dict[str, Any]:
    """Get analytics dashboard data."""
    return analytics_engine.get_dashboard_data()

def export_analytics_csv(days: int = 7, filename: str = None) -> str:
    """Export analytics to CSV."""
    return analytics_engine.export_analytics_csv(days, filename)

def get_analytics_health() -> Dict[str, Any]:
    """Get analytics engine health status."""
    return analytics_engine.get_health_status()
