-- Migration 006: Add usage tracking for cost and resource management
-- Created: 2025-10-03
-- Purpose: Track usage to prevent runaway costs and resource exhaustion

-- Usage tracking table
CREATE TABLE IF NOT EXISTS usage_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operation TEXT NOT NULL, -- 'embedding', 'job_search', 'rag_query', etc.
    estimated_cost REAL DEFAULT 0.0,
    actual_cost REAL DEFAULT 0.0,
    success INTEGER DEFAULT 1, -- 1 if successful, 0 if failed
    response_time REAL, -- Response time in seconds
    error_message TEXT,
    metadata TEXT, -- JSON object for additional tracking data
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cost alerts table
CREATE TABLE IF NOT EXISTS cost_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alert_type TEXT NOT NULL, -- 'daily_limit', 'monthly_limit', 'emergency_stop'
    threshold_value REAL NOT NULL,
    current_value REAL NOT NULL,
    alert_message TEXT,
    acknowledged INTEGER DEFAULT 0, -- 1 if acknowledged
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Resource usage summary table (for performance)
CREATE TABLE IF NOT EXISTS usage_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL, -- YYYY-MM-DD format
    operation TEXT NOT NULL,
    request_count INTEGER DEFAULT 0,
    total_cost REAL DEFAULT 0.0,
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    avg_response_time REAL DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date, operation)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_usage_tracking_operation ON usage_tracking (operation);
CREATE INDEX IF NOT EXISTS idx_usage_tracking_created_at ON usage_tracking (created_at);
CREATE INDEX IF NOT EXISTS idx_usage_tracking_success ON usage_tracking (success);
CREATE INDEX IF NOT EXISTS idx_cost_alerts_type ON cost_alerts (alert_type);
CREATE INDEX IF NOT EXISTS idx_cost_alerts_created_at ON cost_alerts (created_at);
CREATE INDEX IF NOT EXISTS idx_usage_summary_date ON usage_summary (date);
CREATE INDEX IF NOT EXISTS idx_usage_summary_operation ON usage_summary (operation);

-- Create daily summary trigger
CREATE TRIGGER IF NOT EXISTS update_usage_summary
AFTER INSERT ON usage_tracking
BEGIN
    INSERT OR REPLACE INTO usage_summary (
        date, operation, request_count, total_cost, 
        success_count, failure_count, avg_response_time, updated_at
    )
    SELECT 
        DATE(NEW.created_at) as date,
        NEW.operation,
        COUNT(*) as request_count,
        SUM(estimated_cost) as total_cost,
        SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as success_count,
        SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as failure_count,
        AVG(response_time) as avg_response_time,
        CURRENT_TIMESTAMP as updated_at
    FROM usage_tracking 
    WHERE DATE(created_at) = DATE(NEW.created_at) 
    AND operation = NEW.operation
    GROUP BY DATE(created_at), operation;
END;
