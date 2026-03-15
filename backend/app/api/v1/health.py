from fastapi import APIRouter
from app.core.database import check_db_health

router = APIRouter(tags=["health"])

@router.get("/")
async def health_check():
    """健康检查"""
    db_healthy = await check_db_health()
    
    return {
        "status": "healthy" if db_healthy else "degraded",
        "service": "ai-agent-builder-lite",
        "version": "0.1.0",
        "database": "connected" if db_healthy else "disconnected",
        "timestamp": "2026-03-16T02:15:00Z"
    }

@router.get("/ready")
async def readiness_check():
    """就绪检查"""
    db_healthy = await check_db_health()
    
    if not db_healthy:
        return {
            "status": "not_ready",
            "reason": "database_not_connected",
            "timestamp": "2026-03-16T02:15:00Z"
        }, 503
    
    return {
        "status": "ready",
        "services": ["api", "database"],
        "timestamp": "2026-03-16T02:15:00Z"
    }

@router.get("/live")
async def liveness_check():
    """存活检查"""
    return {
        "status": "alive",
        "timestamp": "2026-03-16T02:15:00Z"
    }