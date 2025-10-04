"""
RAG-Powered Dynamic Source Discovery and Integration
Implements intelligent job source discovery and dynamic integration.
"""

import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass

from .rag_engine import get_rag_response, compute_embedding
from .storage import get_conn

@dataclass
class SourceDiscovery:
    """Result of source discovery process"""
    source_name: str
    source_type: str
    api_endpoint: str
    rate_limit: int
    confidence: float
    discovery_reason: str
    integration_status: str = "pending"

class RAGSourceDiscovery:
    """RAG-powered dynamic source discovery."""
    
    def __init__(self):
        self.source_knowledge_base = self._load_source_knowledge()
        self.discovered_sources = {}
        self.integration_cache = {}
    
    def _load_source_knowledge(self) -> Dict[str, Any]:
        """Load knowledge base of job sources and their characteristics."""
        return {
            "source_patterns": {
                "tech_jobs": ["greenhouse", "angelist", "hackernews"],
                "corporate_jobs": ["indeed", "linkedin", "glassdoor"],
                "startup_jobs": ["angelist", "reddit", "hackernews"],
                "remote_jobs": ["reddit", "hackernews", "angelist"],
                "freelance_jobs": ["reddit", "upwork", "freelancer"]
            },
            "source_characteristics": {
                "greenhouse": {"type": "tech", "rate_limit": 60, "api_required": True},
                "indeed": {"type": "corporate", "rate_limit": 100, "api_required": True},
                "linkedin": {"type": "corporate", "rate_limit": 100, "api_required": True},
                "reddit": {"type": "community", "rate_limit": 60, "api_required": False},
                "hackernews": {"type": "tech", "rate_limit": 60, "api_required": False},
                "angelist": {"type": "startup", "rate_limit": 60, "api_required": True}
            }
        }
    
    def discover_sources_for_query(self, query: str, location: str = None, job_type: str = None) -> List[SourceDiscovery]:
        """Use RAG to discover optimal sources for a job search query."""
        try:
            # Create context for RAG analysis
            context = {
                "query": query,
                "location": location,
                "job_type": job_type,
                "existing_sources": list(self.source_knowledge_base["source_characteristics"].keys()),
                "source_patterns": self.source_knowledge_base["source_patterns"]
            }
            
            # Use RAG to analyze query and suggest sources
            rag_response = get_rag_response(
                f"Analyze this job search query and suggest the best job sources: {query}. "
                f"Location: {location or 'Any'}. Job type: {job_type or 'Any'}. "
                f"Consider the source patterns and characteristics to recommend optimal sources.",
                context
            )
            
            # Parse RAG response to extract source recommendations
            recommended_sources = self._parse_rag_source_recommendations(rag_response["response"])
            
            # Create source discovery results
            discoveries = []
            for source_name, confidence in recommended_sources.items():
                if source_name in self.source_knowledge_base["source_characteristics"]:
                    source_info = self.source_knowledge_base["source_characteristics"][source_name]
                    discovery = SourceDiscovery(
                        source_name=source_name,
                        source_type=source_info["type"],
                        api_endpoint=f"https://api.{source_name}.com",
                        rate_limit=source_info["rate_limit"],
                        confidence=confidence,
                        discovery_reason=f"RAG analysis suggests {source_name} for {query}"
                    )
                    discoveries.append(discovery)
            
            return discoveries
            
        except Exception as e:
            print(f"Error in RAG source discovery: {e}")
            return []
    
    def _parse_rag_source_recommendations(self, rag_response: str) -> Dict[str, float]:
        """Parse RAG response to extract source recommendations with confidence scores."""
        # This is a simplified parser - in production, you'd use more sophisticated NLP
        recommendations = {}
        
        # Ensure rag_response is a string
        if isinstance(rag_response, dict):
            rag_response = str(rag_response)
        
        # Look for source mentions in the response
        for source_name in self.source_knowledge_base["source_characteristics"].keys():
            if source_name.lower() in rag_response.lower():
                # Simple confidence scoring based on mention frequency and context
                confidence = 0.7  # Base confidence
                if "recommended" in rag_response.lower() or "suggested" in rag_response.lower():
                    confidence += 0.2
                if "best" in rag_response.lower() or "optimal" in rag_response.lower():
                    confidence += 0.1
                
                recommendations[source_name] = min(confidence, 1.0)
        
        return recommendations
    
    def dynamically_integrate_source(self, discovery: SourceDiscovery) -> bool:
        """Dynamically integrate a discovered source into the system."""
        try:
            # Check if source is already integrated
            if discovery.source_name in self.discovered_sources:
                return True
            
            # Create dynamic source integration
            integration_config = {
                "source_name": discovery.source_name,
                "source_type": discovery.source_type,
                "api_endpoint": discovery.api_endpoint,
                "rate_limit": discovery.rate_limit,
                "confidence": discovery.confidence,
                "discovery_reason": discovery.discovery_reason,
                "integration_time": datetime.utcnow().isoformat(),
                "status": "integrated"
            }
            
            # Store integration config
            self.discovered_sources[discovery.source_name] = integration_config
            
            # Update database with new source
            self._store_dynamic_source(integration_config)
            
            return True
            
        except Exception as e:
            print(f"Error integrating dynamic source: {e}")
            return False
    
    def _store_dynamic_source(self, config: Dict[str, Any]):
        """Store dynamic source configuration in database."""
        try:
            with get_conn() as conn:
                conn.execute(
                    """INSERT OR REPLACE INTO dynamic_sources 
                       (source_name, source_type, api_endpoint, rate_limit, 
                        confidence, discovery_reason, integration_time, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        config["source_name"],
                        config["source_type"],
                        config["api_endpoint"],
                        config["rate_limit"],
                        config["confidence"],
                        config["discovery_reason"],
                        config["integration_time"],
                        config["status"]
                    )
                )
        except Exception as e:
            print(f"Error storing dynamic source: {e}")
    
    def get_optimal_sources_for_query(self, query: str, location: str = None, job_type: str = None) -> List[str]:
        """Get optimal sources for a query using RAG analysis."""
        try:
            # Discover sources using RAG
            discoveries = self.discover_sources_for_query(query, location, job_type)
            
            # Filter by confidence threshold
            optimal_sources = [
                discovery.source_name 
                for discovery in discoveries 
                if discovery.confidence >= 0.6
            ]
            
            # Integrate new sources dynamically
            for discovery in discoveries:
                if discovery.confidence >= 0.7:
                    self.dynamically_integrate_source(discovery)
            
            return optimal_sources
            
        except Exception as e:
            print(f"Error getting optimal sources: {e}")
            return []
    
    def get_discovery_analytics(self) -> Dict[str, Any]:
        """Get analytics on source discovery and integration."""
        try:
            with get_conn() as conn:
                # Get discovery statistics
                total_discoveries = conn.execute(
                    "SELECT COUNT(*) FROM dynamic_sources"
                ).fetchone()[0]
                
                active_sources = conn.execute(
                    "SELECT COUNT(*) FROM dynamic_sources WHERE status = 'integrated'"
                ).fetchone()[0]
                
                # Get source performance
                source_performance = conn.execute(
                    """SELECT source_name, AVG(confidence) as avg_confidence, 
                       COUNT(*) as usage_count
                       FROM dynamic_sources 
                       GROUP BY source_name"""
                ).fetchall()
                
                return {
                    "total_discoveries": total_discoveries,
                    "active_sources": active_sources,
                    "source_performance": [
                        {
                            "source_name": row[0],
                            "avg_confidence": row[1],
                            "usage_count": row[2]
                        }
                        for row in source_performance
                    ],
                    "discovery_status": "operational"
                }
                
        except Exception as e:
            print(f"Error getting discovery analytics: {e}")
            return {"discovery_status": "error", "error": str(e)}

# Global RAG source discovery instance
rag_source_discovery = RAGSourceDiscovery()

def discover_sources_for_query(query: str, location: str = None, job_type: str = None) -> List[SourceDiscovery]:
    """Discover optimal sources for a job search query using RAG."""
    return rag_source_discovery.discover_sources_for_query(query, location, job_type)

def get_optimal_sources_for_query(query: str, location: str = None, job_type: str = None) -> List[str]:
    """Get optimal sources for a query using RAG analysis."""
    return rag_source_discovery.get_optimal_sources_for_query(query, location, job_type)

def get_discovery_analytics() -> Dict[str, Any]:
    """Get analytics on source discovery and integration."""
    return rag_source_discovery.get_discovery_analytics()
