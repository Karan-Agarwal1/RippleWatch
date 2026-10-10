import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Locate potential .env files (check backend/.env then root .env)
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BASE_DIR.parent

env_paths = [BASE_DIR / ".env", ROOT_DIR / ".env"]
env_file = next((p for p in env_paths if p.exists()), BASE_DIR / ".env")

class Settings(BaseSettings):
    SERPAPI_KEY: str = ""
    GEMINI_API_KEY: str = ""
    DATABASE_URL: str = "sqlite:///./ripplewatch.db"
    CACHE_DIR: str = str(BASE_DIR / "cache")
    CACHE_TTL_HOURS: int = 24
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file=str(env_file),
        extra="ignore"
    )

settings = Settings()

# Ensure cache directory exists
os.makedirs(settings.CACHE_DIR, exist_ok=True)
