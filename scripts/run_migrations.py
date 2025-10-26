#!/usr/bin/env python3
"""
Manual migration runner for discount codes feature
Run this once to add discount code support to production database
"""

import os
import sys
from pathlib import Path

# Add parent directory to path to import api modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.storage import get_conn

def run_migrations():
    """Run all pending database migrations"""
    migrations_dir = Path(__file__).parent.parent / "data" / "migrations"

    print(f"📂 Migrations directory: {migrations_dir}")
    print(f"🔍 Checking for migrations...")

    with get_conn() as conn:
        cursor = conn.cursor()

        # Create tracking table
        print("📋 Creating schema_migrations tracking table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                id SERIAL PRIMARY KEY,
                migration_file VARCHAR(255) UNIQUE NOT NULL,
                applied_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
        conn.commit()

        # Get applied migrations
        cursor.execute("SELECT migration_file FROM schema_migrations")
        applied = {row[0] for row in cursor.fetchall()}
        print(f"✅ Already applied: {len(applied)} migrations")

        # Run each migration
        migration_files = sorted(migrations_dir.glob("*.sql"))
        print(f"📁 Found {len(migration_files)} migration files")

        for migration_file in migration_files:
            if migration_file.name in applied:
                print(f"⏭️  Skipping {migration_file.name} (already applied)")
                continue

            print(f"🚀 Running {migration_file.name}...")

            try:
                with open(migration_file, 'r') as f:
                    sql = f.read()

                cursor.execute(sql)

                cursor.execute(
                    "INSERT INTO schema_migrations (migration_file) VALUES (%s)",
                    (migration_file.name,)
                )

                conn.commit()
                print(f"✅ Successfully applied {migration_file.name}")

            except Exception as e:
                print(f"❌ Error applying {migration_file.name}: {e}")
                conn.rollback()
                raise

    print("🎉 All migrations complete!")

if __name__ == "__main__":
    print("🔧 Starting database migrations...")
    run_migrations()
