from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.base import User, Agent, AgentSkill, Skill
from app.schemas.agent import AgentCreate, AgentUpdate, AgentResponse

router = APIRouter(prefix="/agents", tags=["agents"])

class AgentListResponse(BaseModel):
    """Agent列表响应"""
    agents: List[AgentResponse]
    total: int
    page: int
    page_size: int

@router.get("/", response_model=AgentListResponse)
async def list_agents(
    page: int = 1,
    page_size: int = 20,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取Agent列表"""
    query = db.query(Agent).filter(Agent.owner_id == current_user.id)
    
    if search:
        query = query.filter(Agent.name.ilike(f"%{search}%"))
    
    total = query.count()
    agents = query.order_by(Agent.updated_at.desc())\
                 .offset((page - 1) * page_size)\
                 .limit(page_size)\
                 .all()
    
    return AgentListResponse(
        agents=agents,
        total=total,
        page=page,
        page_size=page_size
    )

@router.post("/", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_data: AgentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建新的Agent"""
    # 检查名称是否重复
    existing = db.query(Agent).filter(
        Agent.owner_id == current_user.id,
        Agent.name == agent_data.name
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Agent名称已存在"
        )
    
    # 创建Agent
    agent = Agent(
        name=agent_data.name,
        description=agent_data.description,
        system_prompt=agent_data.system_prompt,
        model=agent_data.model,
        temperature=int(agent_data.temperature * 100),  # 转换为0-100
        max_tokens=agent_data.max_tokens,
        is_public=agent_data.is_public,
        owner_id=current_user.id
    )
    
    db.add(agent)
    db.commit()
    db.refresh(agent)
    
    # 添加技能
    if agent_data.skill_ids:
        for skill_id in agent_data.skill_ids:
            skill = db.query(Skill).filter(Skill.id == skill_id).first()
            if skill:
                agent_skill = AgentSkill(
                    agent_id=agent.id,
                    skill_id=skill_id,
                    is_enabled=True
                )
                db.add(agent_skill)
        
        db.commit()
        db.refresh(agent)
    
    return agent

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取单个Agent详情"""
    agent = db.query(Agent).filter(
        Agent.id == agent_id,
        Agent.owner_id == current_user.id
    ).first()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent不存在或无权访问"
        )
    
    return agent

@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: str,
    agent_data: AgentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新Agent"""
    agent = db.query(Agent).filter(
        Agent.id == agent_id,
        Agent.owner_id == current_user.id
    ).first()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent不存在或无权访问"
        )
    
    # 更新字段
    update_data = agent_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == "temperature":
            value = int(value * 100)  # 转换为0-100
        setattr(agent, field, value)
    
    # 更新技能
    if agent_data.skill_ids is not None:
        # 删除现有技能关联
        db.query(AgentSkill).filter(AgentSkill.agent_id == agent_id).delete()
        
        # 添加新技能
        for skill_id in agent_data.skill_ids:
            skill = db.query(Skill).filter(Skill.id == skill_id).first()
            if skill:
                agent_skill = AgentSkill(
                    agent_id=agent.id,
                    skill_id=skill_id,
                    is_enabled=True
                )
                db.add(agent_skill)
    
    db.commit()
    db.refresh(agent)
    
    return agent

@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除Agent"""
    agent = db.query(Agent).filter(
        Agent.id == agent_id,
        Agent.owner_id == current_user.id
    ).first()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent不存在或无权访问"
        )
    
    db.delete(agent)
    db.commit()

@router.post("/{agent_id}/test")
async def test_agent(
    agent_id: str,
    message: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """测试Agent对话"""
    agent = db.query(Agent).filter(
        Agent.id == agent_id,
        Agent.owner_id == current_user.id
    ).first()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent不存在或无权访问"
        )
    
    # 这里会调用AI模型生成响应
    # 暂时返回模拟响应
    return {
        "agent_id": agent_id,
        "agent_name": agent.name,
        "message": message,
        "response": f"你好！我是{agent.name}，{agent.description or '一个AI助手'}。我收到了你的消息：'{message}'",
        "model": agent.model,
        "tokens_used": len(message) // 4 + 50
    }

@router.get("/{agent_id}/skills")
async def get_agent_skills(
    agent_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取Agent的技能列表"""
    agent = db.query(Agent).filter(
        Agent.id == agent_id,
        Agent.owner_id == current_user.id
    ).first()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent不存在或无权访问"
        )
    
    skills = db.query(Skill).join(AgentSkill).filter(
        AgentSkill.agent_id == agent_id,
        AgentSkill.is_enabled == True
    ).all()
    
    return {
        "agent_id": agent_id,
        "agent_name": agent.name,
        "skills": [
            {
                "id": skill.id,
                "name": skill.name,
                "description": skill.description,
                "category": skill.category,
                "icon": skill.icon
            }
            for skill in skills
        ]
    }