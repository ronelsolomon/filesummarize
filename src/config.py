"""Configuration settings for the Python Code Explainer application."""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import HttpUrl, field_validator


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    APP_NAME: str = "Python Code Explainer"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # File handling
    UPLOAD_FOLDER: Path = Path("uploads")
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS: set[str] = {"py"}
    
    # LLM Settings
    OLLAMA_HOST: HttpUrl = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama2")
    
    # Document generation
    OUTPUT_FOLDER: Path = Path("docs")
    
    @validator("UPLOAD_FOLDER", "OUTPUT_FOLDER", pre=True)
    def create_folders(cls, v: Path) -> Path:
        """Ensure upload and output folders exist."""
        v = Path(v)
        v.mkdir(parents=True, exist_ok=True)
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()
