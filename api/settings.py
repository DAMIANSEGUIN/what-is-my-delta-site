from functools import lru_cache
from pathlib import Path
from typing import Optional
import json

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: Optional[str] = None
    CLAUDE_API_KEY: Optional[str] = None
    PUBLIC_SITE_ORIGIN: AnyHttpUrl = "https://whatismydelta.com"
    PUBLIC_API_BASE: str = ""
    APP_SCHEMA_VERSION: str = "v1"

_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"


@lru_cache()
def get_settings() -> "Settings":
    env_file = _ENV_PATH if _ENV_PATH.exists() else None
    return Settings(_env_file=env_file)

@lru_cache()
def get_feature_flag(flag_name: str) -> bool:
    """Get feature flag status from feature_flags.json"""
    try:
        flags_path = Path(__file__).resolve().parent.parent / "feature_flags.json"
        if flags_path.exists():
            with open(flags_path, 'r') as f:
                flags_data = json.load(f)
                return flags_data.get("flags", {}).get(flag_name, {}).get("enabled", False)
        return False
    except Exception:
        return False
