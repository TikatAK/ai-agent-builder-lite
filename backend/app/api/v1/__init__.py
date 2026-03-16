from fastapi import APIRouter
from app.api.v1 import agents, auth, skills, conversations, health, skill_execution

api_router = APIRouter()

# 包含所有路由
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(skills.router, prefix="/skills", tags=["skills"])
api_router.include_router(skill_execution.router, prefix="/skill-execution", tags=["skill-execution"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["conversations"])
api_router.include_router(health.router, prefix="/health", tags=["health"])