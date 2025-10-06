"""
Corpus Reindex Script for Mosaic 2.0
Re-indexes existing corpora with text-embedding-3-small
"""

import json
import time
from typing import List, Dict, Any
from datetime import datetime
from .storage import get_conn
from .rag_engine import rag_engine, EmbeddingResult

def reindex_corpus() -> Dict[str, Any]:
    """Re-index existing corpus with new embeddings."""
    start_time = time.time()
    results = {
        "start_time": datetime.utcnow().isoformat(),
        "total_documents": 0,
        "successful_embeddings": 0,
        "failed_embeddings": 0,
        "errors": [],
        "processing_time": 0
    }
    
    try:
        # Get all existing embeddings
        with get_conn() as conn:
            rows = conn.execute(
                "SELECT text_hash, text, metadata FROM embeddings ORDER BY created_at DESC"
            ).fetchall()
        
        results["total_documents"] = len(rows)
        
        print(f"Starting corpus reindex: {len(rows)} documents")
        
        for i, (text_hash, text, metadata) in enumerate(rows):
            try:
                # Compute new embedding
                embedding_result = rag_engine.compute_embedding(text)
                
                if embedding_result:
                    # Update with new embedding
                    rag_engine.store_embedding(embedding_result, json.loads(metadata) if metadata else {})
                    results["successful_embeddings"] += 1
                    
                    if (i + 1) % 10 == 0:
                        print(f"Processed {i + 1}/{len(rows)} documents")
                else:
                    results["failed_embeddings"] += 1
                    results["errors"].append(f"Failed to embed document {i + 1}")
                
                # Rate limiting
                time.sleep(0.1)
                
            except Exception as e:
                results["failed_embeddings"] += 1
                results["errors"].append(f"Error processing document {i + 1}: {str(e)}")
        
        results["processing_time"] = time.time() - start_time
        results["end_time"] = datetime.utcnow().isoformat()
        
        print(f"Corpus reindex complete: {results['successful_embeddings']} successful, {results['failed_embeddings']} failed")
        
    except Exception as e:
        results["errors"].append(f"Fatal error during reindex: {str(e)}")
        results["processing_time"] = time.time() - start_time
    
    return results

def get_reindex_status() -> Dict[str, Any]:
    """Get current reindex status."""
    try:
        with get_conn() as conn:
            # Count total embeddings
            total_count = conn.execute("SELECT COUNT(*) FROM embeddings").fetchone()[0]
            
            # Count recent embeddings (last 24 hours)
            recent_count = conn.execute(
                "SELECT COUNT(*) FROM embeddings WHERE created_at > datetime('now', '-1 day')"
            ).fetchone()[0]
            
            return {
                "total_embeddings": total_count,
                "recent_embeddings": recent_count,
                "status": "operational"
            }
    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        }

if __name__ == "__main__":
    # Run reindex
    results = reindex_corpus()
    print(json.dumps(results, indent=2))
