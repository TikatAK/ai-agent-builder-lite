from typing import List, Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime

class AgentBase(BaseModel):
    """Agent基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="Agent名称")
    description: Optional[str] = Field(None, max_length=500, description="Agent描述")
    system_prompt: str = Field(..., min_length=10, max_length=5000, description="系统提示词")
    model: str = Field(..., description="AI模型")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="温度参数")
    max_tokens: int = Field(2048, ge=1, le=128000, description="最大token数")
    is_public: bool = Field(False, description="是否公开")

class AgentCreate(AgentBase):
    """创建Agent请求模型"""
    skill_ids: Optional[List[str]] = Field(default_factory=list, description="技能ID列表")

class AgentUpdate(BaseModel):
    """更新Agent请求模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    system_prompt: Optional[str] = Field(None, min_length=10, max_length=5000)
    model: Optional[str] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(None, ge=1, le=128000)
    is_public: Optional[bool] = None
    skill_ids: Optional[List[str]] = None

class AgentResponse(AgentBase):
    """Agent响应模型"""
    id: str
    owner_id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class SkillBase(BaseModel):
    """技能基础模型"""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=10, max_length=500)
    category: str = Field(..., description="技能分类")
    icon: Optional[str] = None
    code: str = Field(..., description="技能代码")
    config_schema: Optional[dict] = None
    is_public: bool = True

class SkillCreate(SkillBase):
    """创建技能请求模型"""
    pass

class SkillResponse(SkillBase):
    """技能响应模型"""
    id: str
    popularity: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ConversationBase(BaseModel):
    """对话基础模型"""
    title: Optional[str] = Field(None, max_length=200)

class ConversationResponse(ConversationBase):
    """对话响应模型"""
    id: str
    user_id: str
    agent_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    """消息基础模型"""
    role: str = Field(..., description="消息角色")
    content: str = Field(..., description="消息内容")
    metadata: Optional[dict] = None

class MessageCreate(MessageBase):
    """创建消息请求模型"""
    conversation_id: str

class MessageResponse(MessageBase):
    """消息响应模型"""
    id: str
    conversation_id: str
    tokens: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: str = Field(..., min_length=1, max_length=5000)
    conversation_id: Optional[str] = None
    stream: bool = Field(False, description="是否使用流式响应")

class ChatResponse(BaseModel):
    """聊天响应模型"""
    response: str
    conversation_id: str
    message_id: str
    tokens_used: int
    model: str

class TestAgentRequest(BaseModel):
    """测试Agent请求模型"""
    message: str = Field(..., min_length=1, max_length=1000)

class TestAgentResponse(BaseModel):
    """测试Agent响应模型"""
    agent_id: str
    agent_name: str
    message: str
    response: str
    model: str
    tokens_used: int