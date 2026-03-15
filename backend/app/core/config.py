from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator
import secrets

class Settings(BaseSettings):
    """应用配置"""
    
    # 应用配置
    APP_NAME: str = "AI Agent Builder Lite"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"  # development, staging, production
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    LOG_REQUESTS: bool = True
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # 数据库配置
    DATABASE_URL: str = "postgresql+asyncpg://aiagent:aiagent123@localhost:5432/ai_agent_builder"
    POSTGRES_USER: str = "aiagent"
    POSTGRES_PASSWORD: str = "aiagent123"
    POSTGRES_DB: str = "ai_agent_builder"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    
    # RabbitMQ配置
    RABBITMQ_URL: str = "amqp://aiagent:aiagent123@localhost:5672"
    RABBITMQ_USER: str = "aiagent"
    RABBITMQ_PASSWORD: str = "aiagent123"
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    
    # Celery配置
    CELERY_BROKER_URL: str = "amqp://aiagent:aiagent123@localhost:5672"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # 安全配置
    SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # AI模型API密钥
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    DEEPSEEK_API_KEY: Optional[str] = None
    MOONSHOT_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    
    # 模型配置
    DEFAULT_MODEL: str = "gpt-4-turbo-preview"
    FALLBACK_MODEL: str = "gpt-3.5-turbo"
    MAX_TOKENS: int = 4096
    DEFAULT_TEMPERATURE: float = 0.7
    
    # 邮件配置
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: Optional[str] = None
    
    # 存储配置
    STORAGE_TYPE: str = "local"  # local, s3, azure, gcs
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    
    # 监控配置
    SENTRY_DSN: Optional[str] = None
    PROMETHEUS_METRICS_PORT: int = 8001
    
    # 功能开关
    FEATURE_AGENT_CREATION: bool = True
    FEATURE_SKILL_MARKET: bool = True
    FEATURE_TEAM_COLLABORATION: bool = False
    FEATURE_BILLING: bool = False
    FEATURE_ANALYTICS: bool = True
    
    # 限制配置
    MAX_AGENTS_PER_USER: int = 10
    MAX_SKILLS_PER_AGENT: int = 20
    MAX_API_CALLS_PER_DAY: int = 1000
    MAX_CONCURRENT_JOBS: int = 5
    
    # 部署配置
    DEPLOYMENT_MODE: str = "docker"  # docker, kubernetes, serverless
    DOMAIN_NAME: str = "localhost"
    SSL_ENABLED: bool = False
    
    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("DATABASE_URL", pre=True)
    def validate_database_url(cls, v, values):
        if not v:
            # 构建默认数据库URL
            user = values.get("POSTGRES_USER")
            password = values.get("POSTGRES_PASSWORD")
            host = values.get("POSTGRES_HOST")
            port = values.get("POSTGRES_PORT")
            db = values.get("POSTGRES_DB")
            return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# 创建全局配置实例
settings = Settings()

# 根据环境调整配置
if settings.ENVIRONMENT == "production":
    settings.DEBUG = False
    settings.LOG_LEVEL = "WARNING"
    settings.CORS_ORIGINS = ["https://your-domain.com"]
    settings.SSL_ENABLED = True
elif settings.ENVIRONMENT == "staging":
    settings.DEBUG = False
    settings.LOG_LEVEL = "INFO"
    settings.CORS_ORIGINS = ["https://staging.your-domain.com"]