from pydantic import BaseSettings, AnyHttpUrl, validator

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    CLAUDE_API_KEY: str
    PUBLIC_SITE_ORIGIN: AnyHttpUrl = "https://whatismydelta.com"
    PUBLIC_API_BASE: str = ""
    APP_SCHEMA_VERSION: str = "v1"

    @validator("OPENAI_API_KEY","CLAUDE_API_KEY")
    def not_placeholder(cls, v):
        if not v or v.lower().startswith("sk-xxx"):
            raise ValueError("Missing real API key")
        return v

def get_settings() -> "Settings":
    return Settings(_env_file=None)
