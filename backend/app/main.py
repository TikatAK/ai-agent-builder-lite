from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.core.database import engine, Base, init_db
from app.api.v1 import api_router

# 设置日志
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    logger.info("Starting AI Agent Builder Lite API...")
    
    # 初始化数据库
    await init_db()
    logger.info("Database initialized successfully")
    
    yield
    
    # 关闭时
    logger.info("Shutting down AI Agent Builder Lite API...")

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
    
    # 包含API路由
    app.include_router(api_router, prefix="/api/v1")
    
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