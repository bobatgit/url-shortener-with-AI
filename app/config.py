from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Base configuration
    app_name: str = "URL Shortener"
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = environment == "development"
    
    # Database
    database_url: str = os.getenv(
        "DATABASE_URL",
        f"sqlite:///./data/urls_{environment}.db"
    )
    
    # Security
    rate_limit_requests: int = int(os.getenv("RATE_LIMIT_REQUESTS", "60"))
    rate_limit_window: int = int(os.getenv("RATE_LIMIT_WINDOW", "60"))
    
    # Cache
    cache_ttl: int = int(os.getenv("CACHE_TTL", "3600"))
    cache_max_size: int = int(os.getenv("CACHE_MAX_SIZE", "1000"))
    
    # URL settings
    min_custom_length: int = 3
    max_custom_length: int = 32
    default_code_length: int = 6
    max_url_length: int = 2048
    
    class Config:
        env_file = ".env"

settings = Settings()