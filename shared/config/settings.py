"""
Shared Settings Configuration
Environment variables and configuration management for LinkOps microservices
"""

import os
from typing import Optional, List
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    """Global settings for LinkOps platform"""
    
    # Application settings
    APP_NAME: str = "LinkOps MLOps Platform"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # Database settings
    DATABASE_URL: str = Field(
        default="postgresql://linkops:linkops@postgres:5432/linkops",
        env="DATABASE_URL"
    )
    
    # Kafka settings
    KAFKA_BROKERS: str = Field(default="kafka:9092", env="KAFKA_BROKERS")
    KAFKA_TOPIC_PREFIX: str = Field(default="linkops", env="KAFKA_TOPIC_PREFIX")
    
    # OpenAI settings
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(default="gpt-4", env="OPENAI_MODEL")
    
    # Logging settings
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(default="json", env="LOG_FORMAT")
    
    # Security settings
    SECRET_KEY: str = Field(default="your-secret-key-here", env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Service URLs
    WHIS_SANITIZE_URL: str = Field(default="http://whis_sanitize:8000", env="WHIS_SANITIZE_URL")
    WHIS_SMITHING_URL: str = Field(default="http://whis_smithing:8000", env="WHIS_SMITHING_URL")
    WHIS_ENHANCE_URL: str = Field(default="http://whis_enhance:8000", env="WHIS_ENHANCE_URL")
    
    # Data lake settings
    DATA_LAKE_PATH: str = Field(default="/app/data_lake", env="DATA_LAKE_PATH")
    LOGS_PATH: str = Field(default="/app/logs", env="LOGS_PATH")
    
    # Agent settings
    AGENT_REGISTRY_PATH: str = Field(default="/app/registry", env="AGENT_REGISTRY_PATH")
    AGENT_DEPLOYMENT_TIMEOUT: int = Field(default=300, env="AGENT_DEPLOYMENT_TIMEOUT")
    
    # Kubernetes settings
    KUBECONFIG_PATH: str = Field(default="/root/.kube/config", env="KUBECONFIG_PATH")
    
    # AWS settings
    AWS_ACCESS_KEY_ID: Optional[str] = Field(default=None, env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(default=None, env="AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = Field(default="us-east-1", env="AWS_REGION")
    
    # Azure settings
    AZURE_CLIENT_ID: Optional[str] = Field(default=None, env="AZURE_CLIENT_ID")
    AZURE_CLIENT_SECRET: Optional[str] = Field(default=None, env="AZURE_CLIENT_SECRET")
    AZURE_TENANT_ID: Optional[str] = Field(default=None, env="AZURE_TENANT_ID")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()

def get_settings() -> Settings:
    """Get settings instance"""
    return settings

def validate_required_settings():
    """Validate that required settings are present"""
    required_settings = [
        "DATABASE_URL",
        "KAFKA_BROKERS",
        "SECRET_KEY"
    ]
    
    missing_settings = []
    for setting in required_settings:
        if not getattr(settings, setting, None):
            missing_settings.append(setting)
            
    if missing_settings:
        raise ValueError(f"Missing required settings: {', '.join(missing_settings)}")
        
    return True 