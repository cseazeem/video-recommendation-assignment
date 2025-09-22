from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"
    API_BASE_URL: str = "https://api.socialverseapp.com"
    FLIC_TOKEN: str = "replace_me"
    EMBEDDING_MODE: str = "local"
    CACHE_BACKEND: str = "memory"
    REDIS_URL: str = "redis://localhost:6379/0"
    APP_LOG_LEVEL: str = "INFO"

settings = Settings()
