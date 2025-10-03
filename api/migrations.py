"""
Migration framework for Mosaic 2.0 database schema updates.
Provides backup/restore functionality and dry-run capabilities.
"""

import os
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import json

from .storage import get_conn, DB_PATH

class MigrationManager:
    """Manages database migrations with backup/restore capabilities."""
    
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.backup_dir = Path("data/migration_backups")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def create_backup(self, description: str = "") -> str:
        """Create a timestamped backup of the database."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}_{description}.db" if description else f"backup_{timestamp}.db"
        backup_path = self.backup_dir / backup_name
        
        shutil.copy2(self.db_path, backup_path)
        print(f"✅ Backup created: {backup_path}")
        return str(backup_path)
    
    def restore_backup(self, backup_path: str) -> bool:
        """Restore database from backup."""
        try:
            shutil.copy2(backup_path, self.db_path)
            print(f"✅ Database restored from: {backup_path}")
            return True
        except Exception as e:
            print(f"❌ Restore failed: {e}")
            return False
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """List available backups."""
        backups = []
        for backup_file in self.backup_dir.glob("backup_*.db"):
            stat = backup_file.stat()
            backups.append({
                "path": str(backup_file),
                "name": backup_file.name,
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat()
            })
        return sorted(backups, key=lambda x: x["created"], reverse=True)
    
    def dry_run_migration(self, migration_sql: str) -> Dict[str, Any]:
        """Perform a dry run of migration SQL without executing."""
        try:
            # Create a temporary copy for dry run
            temp_db = self.db_path.parent / f"temp_dry_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            shutil.copy2(self.db_path, temp_db)
            
            # Test the migration on the copy
            with sqlite3.connect(temp_db) as conn:
                conn.execute("PRAGMA foreign_keys = ON")
                # Parse and validate SQL statements
                statements = [stmt.strip() for stmt in migration_sql.split(';') if stmt.strip()]
                
                results = {
                    "statements": len(statements),
                    "valid": True,
                    "errors": [],
                    "warnings": []
                }
                
                for i, statement in enumerate(statements):
                    try:
                        # Validate syntax without executing
                        conn.execute(f"EXPLAIN QUERY PLAN {statement}")
                        results[f"statement_{i+1}"] = "valid"
                    except sqlite3.Error as e:
                        results["valid"] = False
                        results["errors"].append(f"Statement {i+1}: {str(e)}")
                
            # Clean up temp file
            temp_db.unlink()
            
            return results
            
        except Exception as e:
            return {
                "valid": False,
                "errors": [f"Dry run failed: {str(e)}"],
                "statements": 0
            }
    
    def execute_migration(self, migration_sql: str, description: str = "") -> bool:
        """Execute migration with automatic backup."""
        try:
            # Create backup before migration
            backup_path = self.create_backup(description)
            
            # Execute migration
            with get_conn() as conn:
                statements = [stmt.strip() for stmt in migration_sql.split(';') if stmt.strip()]
                for statement in statements:
                    conn.execute(statement)
            
            print(f"✅ Migration executed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            print(f"💡 Restore backup with: restore_backup('{backup_path}')")
            return False

# Migration definitions for Mosaic 2.0
MIGRATIONS = {
    "001_add_feature_flags": """
        CREATE TABLE IF NOT EXISTS feature_flags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flag_name TEXT UNIQUE NOT NULL,
            enabled BOOLEAN DEFAULT FALSE,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        INSERT OR IGNORE INTO feature_flags (flag_name, enabled, description) VALUES
        ('AI_FALLBACK_ENABLED', FALSE, 'Enable AI fallback when CSV prompts fail'),
        ('EXPERIMENTS_ENABLED', FALSE, 'Enable experiment engine functionality'),
        ('SELF_EFFICACY_METRICS', FALSE, 'Enable self-efficacy metrics collection'),
        ('RAG_BASELINE', FALSE, 'Enable RAG baseline functionality'),
        ('COACH_ESCALATION', FALSE, 'Enable coach escalation signals');
    """,
    
    "002_add_experiments_schema": """
        CREATE TABLE IF NOT EXISTS experiments (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            session_id TEXT,
            experiment_name TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (session_id) REFERENCES sessions (id)
        );
        
        CREATE TABLE IF NOT EXISTS learning_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            experiment_id TEXT,
            session_id TEXT,
            learning_type TEXT NOT NULL,
            content TEXT,
            confidence_score REAL,
            evidence_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (experiment_id) REFERENCES experiments (id),
            FOREIGN KEY (session_id) REFERENCES sessions (id)
        );
        
        CREATE TABLE IF NOT EXISTS capability_evidence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            capability_name TEXT NOT NULL,
            evidence_type TEXT,
            evidence_data TEXT,
            confidence_level REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions (id)
        );
        
        CREATE TABLE IF NOT EXISTS self_efficacy_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            metric_name TEXT NOT NULL,
            metric_value REAL,
            metric_type TEXT,
            context_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions (id)
        );
        
        CREATE INDEX IF NOT EXISTS idx_experiments_user_id ON experiments (user_id);
        CREATE INDEX IF NOT EXISTS idx_experiments_session_id ON experiments (session_id);
        CREATE INDEX IF NOT EXISTS idx_learning_data_experiment_id ON learning_data (experiment_id);
        CREATE INDEX IF NOT EXISTS idx_capability_evidence_session_id ON capability_evidence (session_id);
        CREATE INDEX IF NOT EXISTS idx_self_efficacy_session_id ON self_efficacy_metrics (session_id);
    """,
    
    "003_add_ai_fallback_tables": """
        CREATE TABLE IF NOT EXISTS ai_fallback_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            prompt_hash TEXT,
            csv_response TEXT,
            ai_response TEXT,
            fallback_reason TEXT,
            response_time_ms INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions (id)
        );
        
        CREATE TABLE IF NOT EXISTS prompt_selector_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt_hash TEXT UNIQUE,
            csv_available BOOLEAN,
            ai_fallback_used BOOLEAN,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_ai_fallback_session_id ON ai_fallback_logs (session_id);
        CREATE INDEX IF NOT EXISTS idx_ai_fallback_prompt_hash ON ai_fallback_logs (prompt_hash);
        CREATE INDEX IF NOT EXISTS idx_prompt_selector_hash ON prompt_selector_cache (prompt_hash);
    """
}

def run_migration(migration_name: str, dry_run: bool = True) -> Dict[str, Any]:
    """Run a specific migration with optional dry run."""
    if migration_name not in MIGRATIONS:
        return {"error": f"Migration '{migration_name}' not found"}
    
    manager = MigrationManager()
    migration_sql = MIGRATIONS[migration_name]
    
    if dry_run:
        print(f"🔍 Dry run for migration: {migration_name}")
        return manager.dry_run_migration(migration_sql)
    else:
        print(f"🚀 Executing migration: {migration_name}")
        success = manager.execute_migration(migration_sql, migration_name)
        return {"success": success}

def list_available_migrations() -> List[str]:
    """List all available migrations."""
    return list(MIGRATIONS.keys())

def get_migration_status() -> Dict[str, Any]:
    """Get current migration status."""
    manager = MigrationManager()
    return {
        "available_migrations": list_available_migrations(),
        "backups": manager.list_backups(),
        "database_path": str(DB_PATH),
        "database_exists": DB_PATH.exists()
    }

if __name__ == "__main__":
    # Example usage
    print("🔍 Available migrations:")
    for migration in list_available_migrations():
        print(f"  - {migration}")
    
    print("\n🔍 Migration status:")
    status = get_migration_status()
    print(json.dumps(status, indent=2))
