-- Migration 004: Add RAG tables for embeddings and job data
-- Created: 2025-10-03
-- Purpose: Support RAG baseline functionality

-- Embeddings table for storing text embeddings
CREATE TABLE IF NOT EXISTS embeddings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_hash TEXT UNIQUE NOT NULL,
    text TEXT NOT NULL,
    embedding TEXT NOT NULL, -- JSON array of floats
    model TEXT DEFAULT 'text-embedding-ada-002',
    metadata TEXT, -- JSON object
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Job postings table for storing job data
CREATE TABLE IF NOT EXISTS job_postings (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT NOT NULL,
    description TEXT NOT NULL,
    url TEXT NOT NULL,
    source TEXT NOT NULL,
    posted_date TIMESTAMP,
    salary_range TEXT,
    job_type TEXT,
    remote INTEGER DEFAULT 0,
    skills TEXT, -- JSON array
    experience_level TEXT,
    metadata TEXT, -- JSON object
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Job search cache for performance
CREATE TABLE IF NOT EXISTS job_search_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query_hash TEXT NOT NULL,
    query TEXT NOT NULL,
    location TEXT,
    results TEXT NOT NULL, -- JSON array of job IDs
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP DEFAULT (datetime('now', '+1 hour'))
);

-- RAG usage tracking
CREATE TABLE IF NOT EXISTS rag_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    operation TEXT NOT NULL, -- 'embed', 'retrieve', 'query'
    query_text TEXT,
    confidence REAL,
    fallback_used INTEGER DEFAULT 0,
    response_time REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_embeddings_text_hash ON embeddings (text_hash);
CREATE INDEX IF NOT EXISTS idx_embeddings_created_at ON embeddings (created_at);
CREATE INDEX IF NOT EXISTS idx_job_postings_source ON job_postings (source);
CREATE INDEX IF NOT EXISTS idx_job_postings_created_at ON job_postings (created_at);
CREATE INDEX IF NOT EXISTS idx_job_postings_remote ON job_postings (remote);
CREATE INDEX IF NOT EXISTS idx_job_search_cache_query_hash ON job_search_cache (query_hash);
CREATE INDEX IF NOT EXISTS idx_job_search_cache_expires_at ON job_search_cache (expires_at);
CREATE INDEX IF NOT EXISTS idx_rag_usage_session_id ON rag_usage (session_id);
CREATE INDEX IF NOT EXISTS idx_rag_usage_operation ON rag_usage (operation);
CREATE INDEX IF NOT EXISTS idx_rag_usage_created_at ON rag_usage (created_at);
