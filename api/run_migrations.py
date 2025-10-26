"""
Database migration runner - runs on application startup
"""

import os
import logging
from pathlib import Path
from api.storage import get_conn

logger = logging.getLogger(__name__)


def run_migrations():
    """Run all pending database migrations"""
    migrations_dir = Path(__file__).parent.parent / "data" / "migrations"

    if not migrations_dir.exists():
        logger.warning(f"Migrations directory not found: {migrations_dir}")
        return

    # Get all .sql migration files in order
    migration_files = sorted(migrations_dir.glob("*.sql"))

    if not migration_files:
        logger.info("No migration files found")
        return

    # Create migrations tracking table if it doesn't exist
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                id SERIAL PRIMARY KEY,
                migration_file VARCHAR(255) UNIQUE NOT NULL,
                applied_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
        conn.commit()

        logger.info("Schema migrations table ready")

        # Run each migration if not already applied
        for migration_file in migration_files:
            migration_name = migration_file.name

            # Check if already applied
            cursor.execute("""
                SELECT COUNT(*) FROM schema_migrations
                WHERE migration_file = %s
            """, (migration_name,))

            if cursor.fetchone()[0] > 0:
                logger.info(f"Migration already applied: {migration_name}")
                continue

            # Read and execute migration
            try:
                logger.info(f"Running migration: {migration_name}")

                with open(migration_file, 'r') as f:
                    migration_sql = f.read()

                # Execute migration
                cursor.execute(migration_sql)

                # Record migration as applied
                cursor.execute("""
                    INSERT INTO schema_migrations (migration_file)
                    VALUES (%s)
                """, (migration_name,))

                conn.commit()
                logger.info(f"✅ Migration applied: {migration_name}")

            except Exception as e:
                conn.rollback()
                logger.error(f"❌ Migration failed: {migration_name} - {e}")
                raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_migrations()
