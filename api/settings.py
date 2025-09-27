from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl

class Settings(BaseSettings):
    OPENAI_API_KEY: Optional[str] = None
    CLAUDE_API_KEY: Optional[str] = None
    PUBLIC_SITE_ORIGIN: AnyHttpUrl = "https://whatismydelta.com"
    PUBLIC_API_BASE: str = ""
    APP_SCHEMA_VERSION: str = "v1"

def get_settings() -> "Settings":
    return Settings(_env_file=None)
