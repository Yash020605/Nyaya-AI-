from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Settings class to load and validate configurations using Pydantic Settings.
    This ensures that missing environment variables or type mismatches are caught
    immediately when the application boots up.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )

    PROJECT_NAME: str = "NyayaAI"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "local"

    # CORS Origins (Allowing all for local development, can be tightened later)
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # MongoDB Configurations
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "nyaya_ai"

    # Qdrant Configurations
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_API_KEY: str = ""

    # LLM Configurations
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-flash"

    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

# Global settings instance
settings = Settings()
