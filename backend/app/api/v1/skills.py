from fastapi import APIRouter

router = APIRouter(tags=["skills"])

@router.get("/")
async def list_skills():
    """获取技能列表"""
    return {"message": "技能列表功能开发中"}

@router.get("/{skill_id}")
async def get_skill(skill_id: str):
    """获取单个技能"""
    return {"message": f"获取技能 {skill_id} 功能开发中"}

@router.post("/")
async def create_skill():
    """创建新技能"""
    return {"message": "创建技能功能开发中"}