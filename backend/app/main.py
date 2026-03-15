from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import logging
from typing import Optional

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1 import api_router
from app.core.middleware import RequestLoggingMiddleware
from app.core.logging import setup_logging

# 设置日志
setup_logging()
logger = logging.getLogger(__name__)

security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    logger.info("Starting AI Agent Builder Lite API...")
    
    # 创建数据库表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Database tables created successfully")
    
    yield
    
    # 关闭时
    logger.info("Shutting down AI Agent Builder Lite API...")
    await engine.dispose()

def create_application() -> FastAPI:
    """创建FastAPI应用实例"""
    app = FastAPI(
        title="AI Agent Builder Lite API",
        description="让每个人都能轻松创建专属AI助手的低代码平台",
        version="0.1.0",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
        lifespan=lifespan,
    )
    
    # 配置CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 添加请求日志中间件
    if settings.LOG_REQUESTS:
        app.add_middleware(RequestLoggingMiddleware)
    
    # 包含API路由
    app.include_router(api_router, prefix="/api/v1")
    
    # 健康检查端点
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "service": "ai-agent-builder-lite",
            "version": "0.1.0",
            "environment": settings.ENVIRONMENT,
        }
    
    # 根端点
    @app.get("/")
    async def root():
        return {
            "message": "Welcome to AI Agent Builder Lite API",
            "docs": "/docs" if settings.DEBUG else None,
            "version": "0.1.0",
        }
    
    return app

app = create_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )