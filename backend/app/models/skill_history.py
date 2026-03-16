"""
技能执行历史记录模型
记录用户执行技能的历史，用于分析和回放
"""
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base

class SkillExecutionHistory(Base):
    """技能执行历史记录"""
    __tablename__ = "skill_execution_history"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 用户信息
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    username = Column(String(100), nullable=False)
    
    # 技能信息
    skill_id = Column(String(100), nullable=False, index=True)
    skill_name = Column(String(200), nullable=False)
    skill_type = Column(String(50), nullable=True)
    
    # 执行信息
    input_text = Column(Text, nullable=False)
    output_text = Column(Text, nullable=False)
    parameters = Column(JSON, nullable=True)  # 执行参数
    temperature = Column(Float, default=0.7)
    max_tokens = Column(Integer, default=1000)
    
    # 执行结果
    success = Column(Boolean, default=True, index=True)
    error_message = Column(Text, nullable=True)
    execution_time = Column(Float, default=0.0)  # 执行时间（秒）
    token_usage = Column(Integer, nullable=True)  # 使用的token数量
    cost = Column(Float, nullable=True)  # 执行成本
    
    # 元数据
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联关系
    user = relationship("User", back_populates="skill_history")
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "username": self.username,
            "skill_id": self.skill_id,
            "skill_name": self.skill_name,
            "skill_type": self.skill_type,
            "input_text": self.input_text,
            "output_text": self.output_text,
            "parameters": self.parameters,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "success": self.success,
            "error_message": self.error_message,
            "execution_time": self.execution_time,
            "token_usage": self.token_usage,
            "cost": self.cost,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    @classmethod
    def from_execution_result(cls, user, skill, request, result):
        """从执行结果创建历史记录"""
        return cls(
            user_id=user.id,
            username=user.username,
            skill_id=skill.id if skill else request.skill_id,
            skill_name=skill.name if skill else request.skill_id,
            skill_type=skill.type.value if skill and hasattr(skill.type, 'value') else None,
            input_text=request.input_text,
            output_text=result.output if result.success else result.error,
            parameters=request.parameters,
            temperature=request.temperature or 0.7,
            max_tokens=request.max_tokens or 1000,
            success=result.success,
            error_message=result.error if not result.success else None,
            execution_time=result.execution_time or 0.0,
            token_usage=getattr(result, 'token_usage', None),
            cost=getattr(result, 'cost', None),
        )


class SkillUsageStat(Base):
    """技能使用统计"""
    __tablename__ = "skill_usage_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 统计维度
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    skill_id = Column(String(100), nullable=False, index=True)
    skill_type = Column(String(50), nullable=True, index=True)
    date = Column(String(10), nullable=False, index=True)  # YYYY-MM-DD格式
    
    # 统计指标
    execution_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    total_execution_time = Column(Float, default=0.0)
    total_token_usage = Column(Integer, default=0)
    total_cost = Column(Float, default=0.0)
    
    # 更新时间
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联关系
    user = relationship("User", back_populates="skill_stats")
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "skill_id": self.skill_id,
            "skill_type": self.skill_type,
            "date": self.date,
            "execution_count": self.execution_count,
            "success_count": self.success_count,
            "success_rate": self.success_count / self.execution_count if self.execution_count > 0 else 0,
            "avg_execution_time": self.total_execution_time / self.execution_count if self.execution_count > 0 else 0,
            "avg_token_usage": self.total_token_usage / self.execution_count if self.execution_count > 0 else 0,
            "total_cost": self.total_cost,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class UserSkillPreference(Base):
    """用户技能偏好"""
    __tablename__ = "user_skill_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 用户和技能
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    skill_id = Column(String(100), nullable=False, index=True)
    
    # 偏好设置
    favorite = Column(Boolean, default=False, index=True)
    default_parameters = Column(JSON, nullable=True)  # 用户默认参数
    usage_count = Column(Integer, default=0)  # 使用次数
    last_used = Column(DateTime(timezone=True), nullable=True)
    
    # 评分和反馈
    rating = Column(Integer, nullable=True)  # 1-5星评分
    feedback = Column(Text, nullable=True)
    
    # 元数据
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 唯一约束
    __table_args__ = (('unique_user_skill', 'user_id', 'skill_id'),)
    
    # 关联关系
    user = relationship("User", back_populates="skill_preferences")
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "skill_id": self.skill_id,
            "favorite": self.favorite,
            "default_parameters": self.default_parameters,
            "usage_count": self.usage_count,
            "last_used": self.last_used.isoformat() if self.last_used else None,
            "rating": self.rating,
            "feedback": self.feedback,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }