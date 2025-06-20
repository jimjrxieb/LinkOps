"""
Application settings configuration using Pydantic Settings
"""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application settings
    APP_NAME: str = Field(default="LinkOps Core", description="Application name")
    DEBUG: bool = Field(default=False, description="Debug mode")
    HOST: str = Field(default="0.0.0.0", description="Host to bind to")
    PORT: int = Field(default=8000, description="Port to bind to")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        description="Allowed CORS origins"
    )
    ALLOWED_HOSTS: List[str] = Field(
        default=["localhost", "127.0.0.1"],
        description="Allowed hosts"
    )
    
    # Database settings
    DATABASE_URL: str = Field(
        default="postgresql://user:password@localhost:5432/linkops",
        description="PostgreSQL database URL"
    )
    DATABASE_POOL_SIZE: int = Field(default=10, description="Database pool size")
    DATABASE_MAX_OVERFLOW: int = Field(default=20, description="Database max overflow")
    
    # Kafka settings
    KAFKA_BOOTSTRAP_SERVERS: str = Field(
        default="localhost:9092",
        description="Kafka bootstrap servers"
    )
    KAFKA_TOPIC_PREFIX: str = Field(
        default="linkops",
        description="Kafka topic prefix"
    )
    KAFKA_CONSUMER_GROUP: str = Field(
        default="linkops-core",
        description="Kafka consumer group"
    )
    
    # File storage settings
    SCREENSHOTS_DIR: str = Field(
        default="./screenshots",
        description="Directory for storing screenshots"
    )
    LOGS_DIR: str = Field(
        default="./logs",
        description="Directory for storing logs"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
_settings = None


def get_settings() -> Settings:
    """Get application settings singleton"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
