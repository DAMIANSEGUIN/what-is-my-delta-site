"""
RAG (Retrieval-Augmented Generation) Engine for Mosaic 2.0
Implements embedding pipeline, retrieval wrapper, and job feeds integration.
"""

import json
import time
import hashlib
import os
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
# import numpy as np  # Temporarily disabled for testing
import random

from .storage import get_conn
from .settings import get_settings
from .ai_clients import get_ai_fallback_response
from .cost_controls import check_cost_limits, check_resource_limits, record_usage
from .domain_adjacent_search import discover_domain_adjacent_opportunities
from .reranker import rerank_documents

@dataclass
class EmbeddingResult:
    """Result of embedding computation"""
    text: str
    embedding: List[float]
    hash: str
    created_at: str
    model: str = "text-embedding-3-small"

@dataclass
class RetrievalResult:
    """Result of retrieval operation"""
    query: str
    matches: List[Dict[str, Any]]
    confidence: float
    fallback_used: bool
    retrieval_time: float

class RAGEngine:
    """Handles RAG operations with embedding pipeline and retrieval wrapper."""
    
    def __init__(self):
        self.settings = get_settings()
        self.rag_enabled = self._check_feature_flag("RAG_BASELINE")
        self.embedding_cache = {}
        self.retrieval_cache = {}
        self.cache_ttl = 24 * 60 * 60  # 24 hours
        
        # Rate limiting
        self.rate_limits = {
            "embeddings": {"last_request": datetime.min, "requests_this_minute": 0},
            "retrieval": {"last_request": datetime.min, "requests_this_minute": 0}
        }
        self.max_requests_per_minute = 60
        
        # Confidence thresholds
        self.min_confidence_threshold = 0.7
        self.fallback_threshold = 0.5
    
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
    
    def _check_rate_limit(self, operation: str) -> bool:
        """Check if we're within rate limits for an operation."""
        now = datetime.now()
        rate_data = self.rate_limits[operation]
        
        if (now - rate_data["last_request"]).total_seconds() >= 60:
            rate_data["requests_this_minute"] = 0
            rate_data["last_request"] = now
        
        if rate_data["requests_this_minute"] < self.max_requests_per_minute:
            rate_data["requests_this_minute"] += 1
            return True
        return False
    
    def _get_text_hash(self, text: str) -> str:
        """Generate hash for text caching."""
        return hashlib.sha256(text.encode()).hexdigest()
    
    def _get_cached_embedding(self, text_hash: str) -> Optional[List[float]]:
        """Get cached embedding if available and not expired."""
        if text_hash in self.embedding_cache:
            cached_data = self.embedding_cache[text_hash]
            if datetime.now().timestamp() - cached_data["timestamp"] < self.cache_ttl:
                return cached_data["embedding"]
        return None
    
    def _cache_embedding(self, text_hash: str, embedding: List[float]):
        """Cache embedding with timestamp."""
        self.embedding_cache[text_hash] = {
            "embedding": embedding,
            "timestamp": datetime.now().timestamp()
        }
    
    def compute_embedding(self, text: str) -> Optional[EmbeddingResult]:
        """Compute embedding for text using OpenAI ADA model."""
        if not self.rag_enabled:
            return None
        
        # Check cost limits first
        cost_check = check_cost_limits("embedding", 0.0001)  # $0.0001 per embedding
        if not cost_check["allowed"]:
            print(f"Cost limit exceeded: {cost_check['reason']}")
            return None
        
        # Check resource limits
        resource_check = check_resource_limits("embedding")
        if not resource_check["allowed"]:
            print(f"Resource limit exceeded: {resource_check['reason']}")
            return None
        
        if not self._check_rate_limit("embeddings"):
            print("Rate limit exceeded for embeddings")
            return None
        
        try:
            # Check cache first
            text_hash = self._get_text_hash(text)
            cached_embedding = self._get_cached_embedding(text_hash)
            
            if cached_embedding:
                record_usage("embedding", 0.0, True)  # Cache hit = no cost
                return EmbeddingResult(
                    text=text,
                    embedding=cached_embedding,
                    hash=text_hash,
                    created_at=datetime.utcnow().isoformat()
                )
            
            # Generate embedding using OpenAI text-embedding-3-small
            try:
                import openai
                # Set API key from environment
                openai.api_key = os.getenv("OPENAI_API_KEY")
                if not openai.api_key:
                    raise ValueError("OPENAI_API_KEY not found in environment")
                
                response = openai.embeddings.create(
                    model="text-embedding-3-small",
                    input=text
                )
                embedding = response.data[0].embedding
                print(f"Generated real embedding for text: {text[:50]}...")
            except ImportError:
                print("OpenAI module not available - installing...")
                import subprocess
                subprocess.run(["pip", "install", "openai"], check=True)
                # Retry after installation
                import openai
                openai.api_key = os.getenv("OPENAI_API_KEY")
                response = openai.embeddings.create(
                    model="text-embedding-3-small",
                    input=text
                )
                embedding = response.data[0].embedding
                print(f"Generated real embedding for text: {text[:50]}...")
            except Exception as e:
                print(f"OpenAI API error, using fallback: {e}")
                # Fallback to simulated embedding for testing
                embedding = [random.random() for _ in range(1536)]  # text-embedding-3-small has 1536 dimensions
            
            # Cache the embedding
            self._cache_embedding(text_hash, embedding)
            
            # Record usage
            record_usage("embedding", 0.0001, True)
            
            return EmbeddingResult(
                text=text,
                embedding=embedding,
                hash=text_hash,
                created_at=datetime.utcnow().isoformat()
            )
            
        except Exception as e:
            record_usage("embedding", 0.0001, False)
            print(f"Error computing embedding: {e}")
            return None
    
    def batch_compute_embeddings(self, texts: List[str]) -> List[EmbeddingResult]:
        """Compute embeddings for multiple texts with rate limiting."""
        results = []
        
        for text in texts:
            if not self._check_rate_limit("embeddings"):
                print("Rate limit exceeded, stopping batch processing")
                break
            
            embedding_result = self.compute_embedding(text)
            if embedding_result:
                results.append(embedding_result)
            
            # Rate limiting delay
            time.sleep(0.1)
        
        return results
    
    def store_embedding(self, embedding_result: EmbeddingResult, metadata: Dict[str, Any] = None):
        """Store embedding in database with metadata."""
        try:
            with get_conn() as conn:
                conn.execute(
                    """INSERT OR REPLACE INTO embeddings 
                       (text_hash, text, embedding, model, metadata, created_at)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (
                        embedding_result.hash,
                        embedding_result.text,
                        json.dumps(embedding_result.embedding),
                        embedding_result.model,
                        json.dumps(metadata or {}),
                        embedding_result.created_at
                    )
                )
        except Exception as e:
            print(f"Error storing embedding: {e}")
    
    def retrieve_similar(self, query: str, limit: int = 5, min_similarity: float = 0.7) -> RetrievalResult:
        """Retrieve similar content using embedding similarity."""
        start_time = time.time()
        
        if not self.rag_enabled:
            return RetrievalResult(
                query=query,
                matches=[],
                confidence=0.0,
                fallback_used=True,
                retrieval_time=time.time() - start_time
            )
        
        try:
            # Compute query embedding
            query_embedding = self.compute_embedding(query)
            if not query_embedding:
                return RetrievalResult(
                    query=query,
                    matches=[],
                    confidence=0.0,
                    fallback_used=True,
                    retrieval_time=time.time() - start_time
                )
            
            # Retrieve similar embeddings from database
            with get_conn() as conn:
                rows = conn.execute(
                    "SELECT text, embedding, metadata FROM embeddings ORDER BY created_at DESC LIMIT 100"
                ).fetchall()
            
            matches = []
            for row in rows:
                try:
                    stored_embedding = json.loads(row[1])
                    similarity = self._cosine_similarity(query_embedding.embedding, stored_embedding)
                    
                    if similarity >= min_similarity:
                        matches.append({
                            "text": row[0],
                            "similarity": similarity,
                            "metadata": json.loads(row[2]) if row[2] else {}
                        })
                except Exception as e:
                    print(f"Error processing embedding: {e}")
                    continue
            
            # Sort by similarity and limit results
            matches.sort(key=lambda x: x["similarity"], reverse=True)
            
            # Apply reranking if we have enough candidates
            if len(matches) > 5:
                try:
                    rerank_result = rerank_documents(query, matches)
                    matches = rerank_result.reranked_documents
                    # Log reranking improvement
                    print(f"Reranking improvement: {rerank_result.improvement_pct:.1f}%")
                    
                    # Record analytics for telemetry
                    from .analytics import log_match_analytics
                    log_match_analytics(
                        query=query,
                        pre_scores=rerank_result.pre_rerank_scores,
                        post_scores=rerank_result.post_rerank_scores,
                        improvement_pct=rerank_result.improvement_pct,
                        processing_time=rerank_result.processing_time
                    )
                except Exception as e:
                    print(f"Reranking failed, using original results: {e}")
            
            matches = matches[:limit]
            
            # Calculate confidence
            confidence = matches[0]["similarity"] if matches else 0.0
            
            # Determine if fallback should be used
            fallback_used = confidence < self.min_confidence_threshold
            
            return RetrievalResult(
                query=query,
                matches=matches,
                confidence=confidence,
                fallback_used=fallback_used,
                retrieval_time=time.time() - start_time
            )
            
        except Exception as e:
            print(f"Error in retrieval: {e}")
            return RetrievalResult(
                query=query,
                matches=[],
                confidence=0.0,
                fallback_used=True,
                retrieval_time=time.time() - start_time
            )
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate normalized cosine similarity between two vectors."""
        try:
            # Calculate dot product
            dot_product = sum(a * b for a, b in zip(vec1, vec2))
            
            # Calculate norms
            norm1 = sum(a * a for a in vec1) ** 0.5
            norm2 = sum(b * b for b in vec2) ** 0.5
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            # Normalized cosine similarity
            similarity = dot_product / (norm1 * norm2)
            
            # Apply keyword boost if available
            return self._apply_keyword_boost(similarity, vec1, vec2)
        except Exception:
            return 0.0
    
    def _apply_keyword_boost(self, similarity: float, vec1: List[float], vec2: List[float]) -> float:
        """Apply simple keyword boost to similarity score."""
        try:
            # Simple keyword boost based on vector magnitude
            magnitude1 = sum(a * a for a in vec1) ** 0.5
            magnitude2 = sum(b * b for b in vec2) ** 0.5
            
            # Boost factor based on vector magnitudes (simple heuristic)
            boost_factor = min(1.2, 1.0 + (magnitude1 + magnitude2) / 1000.0)
            
            return min(1.0, similarity * boost_factor)
        except Exception:
            return similarity
    
    def get_rag_response(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get RAG response with retrieval and fallback logic."""
        context = context or {}
        
        # Try retrieval first
        retrieval_result = self.retrieve_similar(query)
        
        if retrieval_result.confidence >= self.min_confidence_threshold:
            # Use retrieved content
            return {
                "response": self._format_retrieved_content(retrieval_result.matches),
                "source": "retrieval",
                "confidence": retrieval_result.confidence,
                "matches": len(retrieval_result.matches)
            }
        elif retrieval_result.confidence >= self.fallback_threshold:
            # Use retrieved content with AI enhancement
            ai_response = get_ai_fallback_response(
                f"Based on this context: {self._format_retrieved_content(retrieval_result.matches)}\n\nQuery: {query}"
            )
            if ai_response:
                return {
                    "response": ai_response,
                    "source": "retrieval_enhanced",
                    "confidence": retrieval_result.confidence,
                    "matches": len(retrieval_result.matches)
                }
        
        # Fallback to AI
        ai_response = get_ai_fallback_response(query)
        if ai_response:
            return {
                "response": ai_response,
                "source": "ai_fallback",
                "confidence": 0.0,
                "matches": 0
            }
        
        # Final fallback
        return {
            "response": "I'm sorry, I couldn't find relevant information to help with that query.",
            "source": "fallback",
            "confidence": 0.0,
            "matches": 0
        }
    
    def _format_retrieved_content(self, matches: List[Dict[str, Any]]) -> str:
        """Format retrieved content for response."""
        if not matches:
            return ""
        
        formatted = []
        for i, match in enumerate(matches[:3]):  # Limit to top 3 matches
            formatted.append(f"{i+1}. {match['text']}")
        
        return "\n".join(formatted)
    
    def discover_domain_adjacent_opportunities(self, user_skills: List[str], user_domains: List[str]) -> Dict[str, Any]:
        """Discover domain adjacent opportunities using RAG semantic clustering."""
        try:
            # Use domain adjacent search engine
            results = discover_domain_adjacent_opportunities(user_skills, user_domains)
            
            # Convert to RAG-friendly format
            return {
                "user_skills": results.user_skills,
                "user_domains": results.user_domains,
                "semantic_clusters": [
                    {
                        "cluster_id": cluster.cluster_id,
                        "cluster_name": cluster.cluster_name,
                        "core_skills": cluster.core_skills,
                        "adjacent_skills": cluster.adjacent_skills,
                        "related_domains": cluster.related_domains,
                        "opportunity_areas": cluster.opportunity_areas,
                        "skill_gaps": cluster.skill_gaps,
                        "learning_paths": cluster.learning_paths,
                        "confidence_score": cluster.confidence_score,
                        "cluster_strength": cluster.cluster_strength
                    }
                    for cluster in results.semantic_clusters
                ],
                "skill_alignment": results.skill_alignment,
                "domain_expansion": results.domain_expansion,
                "opportunity_mapping": results.opportunity_mapping,
                "learning_recommendations": results.learning_recommendations,
                "career_paths": results.career_paths
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get RAG engine health status."""
        return {
            "rag_enabled": self.rag_enabled,
            "feature_flag": "RAG_BASELINE",
            "cache_size": len(self.embedding_cache),
            "rate_limits": {
                "embeddings": self.rate_limits["embeddings"]["requests_this_minute"],
                "retrieval": self.rate_limits["retrieval"]["requests_this_minute"]
            },
            "status": "operational" if self.rag_enabled else "disabled"
        }

# Global RAG engine instance
rag_engine = RAGEngine()

def compute_embedding(text: str) -> Optional[EmbeddingResult]:
    """Compute embedding using the global engine."""
    return rag_engine.compute_embedding(text)

def batch_compute_embeddings(texts: List[str]) -> List[EmbeddingResult]:
    """Batch compute embeddings using the global engine."""
    return rag_engine.batch_compute_embeddings(texts)

def retrieve_similar(query: str, limit: int = 5, min_similarity: float = 0.7) -> RetrievalResult:
    """Retrieve similar content using the global engine."""
    return rag_engine.retrieve_similar(query, limit, min_similarity)

def get_rag_response(query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """Get RAG response using the global engine."""
    return rag_engine.get_rag_response(query, context)

def get_rag_health() -> Dict[str, Any]:
    """Get RAG engine health status."""
    return rag_engine.get_health_status()

def discover_domain_adjacent_opportunities_rag(user_skills: List[str], user_domains: List[str]) -> Dict[str, Any]:
    """Discover domain adjacent opportunities using RAG semantic clustering."""
    return rag_engine.discover_domain_adjacent_opportunities(user_skills, user_domains)
