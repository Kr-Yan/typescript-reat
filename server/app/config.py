# app/config.py (Fixed)
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    app_name: str = "GMGN Trading API"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 3001
    
    # CORS settings
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Database settings (NEW - these were missing!)
    database_url: str = "postgresql://localhost:5432/fallback_db"
    secret_key: str = "dev-fallback-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = False  # Allow both DATABASE_URL and database_url

settings = Settings()