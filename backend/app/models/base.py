from datetime import datetime
from typing import Optional
from sqlalchemy import Column, DateTime, Integer, String, Boolean, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class TimestampMixin:
    """时间戳混入类"""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class User(Base, TimestampMixin):
    """用户模型"""
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # 关系
    agents = relationship("Agent", back_populates="owner", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"

class Agent(Base, TimestampMixin):
    """AI Agent模型"""
    __tablename__ = "agents"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    system_prompt = Column(Text, nullable=False)
    model = Column(String(50), nullable=False)  # gpt-4-turbo, claude-3-opus等
    temperature = Column(Integer, default=70)  # 0-100 scale
    max_tokens = Column(Integer, default=2048)
    is_public = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # 外键
    owner_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    
    # 关系
    owner = relationship("User", back_populates="agents")
    skills = relationship("AgentSkill", back_populates="agent", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="agent", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Agent(id={self.id}, name={self.name}, model={self.model})>"

class Skill(Base, TimestampMixin):
    """技能模型"""
    __tablename__ = "skills"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False, index=True)  # tool, productivity, development等
    icon = Column(String(50), nullable=True)
    code = Column(Text, nullable=False)  # 技能实现代码
    config_schema = Column(JSON, nullable=True)  # 配置JSON Schema
    is_public = Column(Boolean, default=True)
    popularity = Column(Integer, default=0)
    
    # 关系
    agent_skills = relationship("AgentSkill", back_populates="skill", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Skill(id={self.id}, name={self.name}, category={self.category})>"

class AgentSkill(Base, TimestampMixin):
    """Agent与技能关联模型"""
    __tablename__ = "agent_skills"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    agent_id = Column(String(36), ForeignKey("agents.id"), nullable=False, index=True)
    skill_id = Column(String(36), ForeignKey("skills.id"), nullable=False, index=True)
    config = Column(JSON, nullable=True)  # 技能特定配置
    order = Column(Integer, default=0)  # 执行顺序
    is_enabled = Column(Boolean, default=True)
    
    # 唯一约束
    __table_args__ = (('unique_agent_skill', 'agent_id', 'skill_id'),)
    
    # 关系
    agent = relationship("Agent", back_populates="skills")
    skill = relationship("Skill", back_populates="agent_skills")
    
    def __repr__(self):
        return f"<AgentSkill(agent_id={self.agent_id}, skill_id={self.skill_id})>"

class Conversation(Base, TimestampMixin):
    """对话模型"""
    __tablename__ = "conversations"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(200), nullable=True)
    
    # 外键
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    agent_id = Column(String(36), ForeignKey("agents.id"), nullable=False, index=True)
    
    # 关系
    user = relationship("User", back_populates="conversations")
    agent = relationship("Agent", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, title={self.title})>"

class Message(Base, TimestampMixin):
    """消息模型"""
    __tablename__ = "messages"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    role = Column(String(20), nullable=False)  # system, user, assistant, tool
    content = Column(Text, nullable=False)
    tokens = Column(Integer, default=0)
    metadata = Column(JSON, nullable=True)
    
    # 外键
    conversation_id = Column(String(36), ForeignKey("conversations.id"), nullable=False, index=True)
    
    # 关系
    conversation = relationship("Conversation", back_populates="messages")
    
    def __repr__(self):
        return f"<Message(id={self.id}, role={self.role}, tokens={self.tokens})>"

class APICall(Base, TimestampMixin):
    """API调用记录"""
    __tablename__ = "api_calls"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    agent_id = Column(String(36), ForeignKey("agents.id"), nullable=True, index=True)
    endpoint = Column(String(100), nullable=False)
    model = Column(String(50), nullable=True)
    input_tokens = Column(Integer, default=0)
    output_tokens = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    cost = Column(Integer, default=0)  # 成本（分）
    duration = Column(Integer, default=0)  # 耗时（毫秒）
    status = Column(String(20), default="success")  # success, error, rate_limit
    
    def __repr__(self):
        return f"<APICall(id={self.id}, endpoint={self.endpoint}, tokens={self.total_tokens})>"