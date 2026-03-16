"""
用户模型
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from passlib.context import CryptContext
from app.models.base import Base

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    """用户模型"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 基本信息
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(200), nullable=True)
    
    # 认证信息
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # 个人设置
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    preferences = Column(JSON, nullable=True)  # 用户偏好设置
    
    # 使用统计
    total_executions = Column(Integer, default=0)
    total_tokens_used = Column(Integer, default=0)
    total_cost = Column(Float, default=0.0)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # 关联关系
    skill_history = relationship(
        "SkillExecutionHistory", 
        back_populates="user",
        cascade="all, delete-orphan"
    )
    skill_stats = relationship(
        "SkillUsageStat",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    skill_preferences = relationship(
        "UserSkillPreference",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    def verify_password(self, password: str) -> bool:
        """验证密码"""
        return pwd_context.verify(password, self.hashed_password)
    
    def set_password(self, password: str):
        """设置密码"""
        self.hashed_password = pwd_context.hash(password)
    
    def to_dict(self, include_sensitive: bool = False):
        """转换为字典格式"""
        data = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "avatar_url": self.avatar_url,
            "bio": self.bio,
            "preferences": self.preferences,
            "total_executions": self.total_executions,
            "total_tokens_used": self.total_tokens_used,
            "total_cost": self.total_cost,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }
        
        if include_sensitive:
            data["hashed_password"] = self.hashed_password
            
        return data
    
    @classmethod
    def create_default_user(cls):
        """创建默认用户（用于测试）"""
        user = cls(
            username="testuser",
            email="test@example.com",
            full_name="Test User",
            is_active=True,
            is_superuser=False,
            preferences={
                "theme": "light",
                "language": "zh-CN",
                "notifications": True
            }
        )
        user.set_password("testpassword")
        return user


class UserSession(Base):
    """用户会话模型"""
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 会话信息
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    session_token = Column(String(500), unique=True, index=True, nullable=False)
    user_agent = Column(Text, nullable=True)
    ip_address = Column(String(50), nullable=True)
    
    # 会话状态
    is_active = Column(Boolean, default=True, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_activity = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联关系
    user = relationship("User")
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "session_token": self.session_token,
            "user_agent": self.user_agent,
            "ip_address": self.ip_address,
            "is_active": self.is_active,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
        }