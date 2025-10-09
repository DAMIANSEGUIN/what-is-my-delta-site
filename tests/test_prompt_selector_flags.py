import sqlite3

import pytest

from api import storage
from api.prompt_selector import PromptSelector


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """Point storage.get_conn at an isolated SQLite database for this test."""
    db_path = tmp_path / "test_flags.db"
    monkeypatch.setattr(storage, "DB_PATH", db_path)

    with storage.get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE feature_flags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                flag_name TEXT UNIQUE NOT NULL,
                enabled BOOLEAN DEFAULT 0
            )
            """
        )
    return db_path


def test_check_feature_flag_returns_bool(temp_db):
    with storage.get_conn() as conn:
        conn.execute(
            "INSERT INTO feature_flags (flag_name, enabled) VALUES (?, ?)",
            ("AI_FALLBACK_ENABLED", 1),
        )

    selector = PromptSelector()
    value = selector._check_feature_flag("AI_FALLBACK_ENABLED")

    assert value is True
    assert isinstance(value, bool)


def test_check_feature_flag_handles_zero(temp_db):
    with storage.get_conn() as conn:
        conn.execute(
            "INSERT INTO feature_flags (flag_name, enabled) VALUES (?, ?)",
            ("AI_FALLBACK_ENABLED", 0),
        )

    selector = PromptSelector()
    value = selector._check_feature_flag("AI_FALLBACK_ENABLED")

    assert value is False
    assert isinstance(value, bool)
