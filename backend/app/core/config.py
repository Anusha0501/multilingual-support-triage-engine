from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Multilingual Support Triage Engine"
    database_url: str = "sqlite+pysqlite:///:memory:"
    redis_url: str = "redis://localhost:6379/0"
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    langsmith_tracing: bool = False
    clerk_secret_key: str | None = None
    model_provider: str = "deterministic-fallback"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()
