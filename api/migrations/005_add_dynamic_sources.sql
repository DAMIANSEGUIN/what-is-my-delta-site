-- Migration 005: Add dynamic sources table for RAG-powered source discovery
-- Created: 2025-10-03
-- Purpose: Support RAG-powered dynamic source discovery and integration

-- Dynamic sources table for RAG-discovered sources
CREATE TABLE IF NOT EXISTS dynamic_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name TEXT UNIQUE NOT NULL,
    source_type TEXT NOT NULL,
    api_endpoint TEXT NOT NULL,
    rate_limit INTEGER DEFAULT 60,
    confidence REAL DEFAULT 0.0,
    discovery_reason TEXT,
    integration_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending',
    last_used TIMESTAMP,
    usage_count INTEGER DEFAULT 0,
    success_rate REAL DEFAULT 0.0,
    metadata TEXT, -- JSON object for additional source configuration
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Source discovery analytics table
CREATE TABLE IF NOT EXISTS source_discovery_analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query_hash TEXT NOT NULL,
    query_text TEXT NOT NULL,
    location TEXT,
    job_type TEXT,
    discovered_sources TEXT NOT NULL, -- JSON array of discovered sources
    selected_sources TEXT NOT NULL, -- JSON array of selected sources
    confidence_scores TEXT, -- JSON object of confidence scores
    discovery_time REAL, -- Time taken for discovery in seconds
    integration_success INTEGER DEFAULT 0, -- 1 if integration successful
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Source performance tracking
CREATE TABLE IF NOT EXISTS source_performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name TEXT NOT NULL,
    query_hash TEXT NOT NULL,
    response_time REAL,
    success INTEGER DEFAULT 0, -- 1 if successful
    error_message TEXT,
    results_count INTEGER DEFAULT 0,
    confidence_score REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_name) REFERENCES dynamic_sources(source_name)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_dynamic_sources_name ON dynamic_sources (source_name);
CREATE INDEX IF NOT EXISTS idx_dynamic_sources_type ON dynamic_sources (source_type);
CREATE INDEX IF NOT EXISTS idx_dynamic_sources_status ON dynamic_sources (status);
CREATE INDEX IF NOT EXISTS idx_dynamic_sources_confidence ON dynamic_sources (confidence);
CREATE INDEX IF NOT EXISTS idx_dynamic_sources_last_used ON dynamic_sources (last_used);
CREATE INDEX IF NOT EXISTS idx_source_discovery_analytics_query_hash ON source_discovery_analytics (query_hash);
CREATE INDEX IF NOT EXISTS idx_source_discovery_analytics_created_at ON source_discovery_analytics (created_at);
CREATE INDEX IF NOT EXISTS idx_source_performance_source_name ON source_performance (source_name);
CREATE INDEX IF NOT EXISTS idx_source_performance_created_at ON source_performance (created_at);
CREATE INDEX IF NOT EXISTS idx_source_performance_success ON source_performance (success);
