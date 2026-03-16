"""
技能历史记录服务
管理技能执行历史的记录、查询和分析
"""
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, and_, or_
import logging

from app.models.skill_history import SkillExecutionHistory, SkillUsageStat, UserSkillPreference
from app.models.user import User
from app.schemas.skill import SkillExecutionRequest, SkillExecutionResponse
from app.services.skill_executor import Skill

logger = logging.getLogger(__name__)

class SkillHistoryService:
    """技能历史记录服务"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # ========== 历史记录管理 ==========
    
    async def record_execution(
        self,
        user: User,
        skill: Optional[Skill],
        request: SkillExecutionRequest,
        result: SkillExecutionResponse
    ) -> SkillExecutionHistory:
        """记录技能执行历史"""
        try:
            # 创建历史记录
            history = SkillExecutionHistory.from_execution_result(
                user=user,
                skill=skill,
                request=request,
                result=result
            )
            
            # 保存到数据库
            self.db.add(history)
            
            # 更新用户统计
            user.total_executions += 1
            if result.success:
                user.total_tokens_used += (getattr(result, 'token_usage', 0) or 0)
                user.total_cost += (getattr(result, 'cost', 0) or 0)
            
            # 更新技能使用统计
            await self._update_skill_stats(user, skill, request, result)
            
            # 更新用户技能偏好
            await self._update_user_preference(user, skill, request)
            
            self.db.commit()
            self.db.refresh(history)
            
            logger.info(f"记录技能执行历史: user={user.username}, skill={request.skill_id}, success={result.success}")
            return history
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"记录技能执行历史失败: {str(e)}", exc_info=True)
            raise
    
    async def get_execution_history(
        self,
        user_id: int,
        limit: int = 50,
        offset: int = 0,
        skill_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        success_only: bool = False
    ) -> Tuple[List[SkillExecutionHistory], int]:
        """获取用户技能执行历史"""
        try:
            # 构建查询条件
            query = self.db.query(SkillExecutionHistory).filter(
                SkillExecutionHistory.user_id == user_id
            )
            
            if skill_id:
                query = query.filter(SkillExecutionHistory.skill_id == skill_id)
            
            if start_date:
                query = query.filter(SkillExecutionHistory.created_at >= start_date)
            
            if end_date:
                query = query.filter(SkillExecutionHistory.created_at <= end_date)
            
            if success_only:
                query = query.filter(SkillExecutionHistory.success == True)
            
            # 获取总数
            total = query.count()
            
            # 获取分页数据
            history = query.order_by(
                desc(SkillExecutionHistory.created_at)
            ).offset(offset).limit(limit).all()
            
            return history, total
            
        except Exception as e:
            logger.error(f"获取技能执行历史失败: {str(e)}", exc_info=True)
            raise
    
    async def get_history_by_id(self, history_id: int, user_id: int) -> Optional[SkillExecutionHistory]:
        """根据ID获取历史记录"""
        try:
            history = self.db.query(SkillExecutionHistory).filter(
                SkillExecutionHistory.id == history_id,
                SkillExecutionHistory.user_id == user_id
            ).first()
            
            return history
            
        except Exception as e:
            logger.error(f"获取历史记录失败: {str(e)}", exc_info=True)
            raise
    
    async def delete_history(self, history_id: int, user_id: int) -> bool:
        """删除历史记录"""
        try:
            history = await self.get_history_by_id(history_id, user_id)
            if not history:
                return False
            
            self.db.delete(history)
            self.db.commit()
            
            logger.info(f"删除历史记录: id={history_id}, user={user_id}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"删除历史记录失败: {str(e)}", exc_info=True)
            raise
    
    # ========== 统计分析 ==========
    
    async def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """获取用户技能使用统计"""
        try:
            # 基础统计
            total_executions = self.db.query(func.count(SkillExecutionHistory.id)).filter(
                SkillExecutionHistory.user_id == user_id
            ).scalar() or 0
            
            success_count = self.db.query(func.count(SkillExecutionHistory.id)).filter(
                SkillExecutionHistory.user_id == user_id,
                SkillExecutionHistory.success == True
            ).scalar() or 0
            
            total_time = self.db.query(func.sum(SkillExecutionHistory.execution_time)).filter(
                SkillExecutionHistory.user_id == user_id
            ).scalar() or 0.0
            
            total_tokens = self.db.query(func.sum(SkillExecutionHistory.token_usage)).filter(
                SkillExecutionHistory.user_id == user_id
            ).scalar() or 0
            
            total_cost = self.db.query(func.sum(SkillExecutionHistory.cost)).filter(
                SkillExecutionHistory.user_id == user_id
            ).scalar() or 0.0
            
            # 最常用技能
            popular_skills = self.db.query(
                SkillExecutionHistory.skill_id,
                SkillExecutionHistory.skill_name,
                func.count(SkillExecutionHistory.id).label('count')
            ).filter(
                SkillExecutionHistory.user_id == user_id
            ).group_by(
                SkillExecutionHistory.skill_id,
                SkillExecutionHistory.skill_name
            ).order_by(
                desc('count')
            ).limit(5).all()
            
            # 最近活动
            recent_activity = self.db.query(SkillExecutionHistory).filter(
                SkillExecutionHistory.user_id == user_id
            ).order_by(
                desc(SkillExecutionHistory.created_at)
            ).limit(10).all()
            
            return {
                "total_executions": total_executions,
                "success_count": success_count,
                "success_rate": success_count / total_executions if total_executions > 0 else 0,
                "total_execution_time": total_time,
                "avg_execution_time": total_time / total_executions if total_executions > 0 else 0,
                "total_tokens_used": total_tokens,
                "avg_tokens_per_execution": total_tokens / total_executions if total_executions > 0 else 0,
                "total_cost": total_cost,
                "avg_cost_per_execution": total_cost / total_executions if total_executions > 0 else 0,
                "popular_skills": [
                    {
                        "skill_id": skill.skill_id,
                        "skill_name": skill.skill_name,
                        "count": skill.count
                    }
                    for skill in popular_skills
                ],
                "recent_activity": [h.to_dict() for h in recent_activity]
            }
            
        except Exception as e:
            logger.error(f"获取用户统计失败: {str(e)}", exc_info=True)
            raise
    
    async def get_skill_stats(self, skill_id: str, user_id: Optional[int] = None) -> Dict[str, Any]:
        """获取技能使用统计"""
        try:
            # 构建查询条件
            filters = [SkillExecutionHistory.skill_id == skill_id]
            if user_id:
                filters.append(SkillExecutionHistory.user_id == user_id)
            
            query = self.db.query(SkillExecutionHistory).filter(and_(*filters))
            
            # 基础统计
            total_executions = query.count()
            success_count = query.filter(SkillExecutionHistory.success == True).count()
            
            # 时间分布（最近30天）
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            daily_stats = self.db.query(
                func.date(SkillExecutionHistory.created_at).label('date'),
                func.count(SkillExecutionHistory.id).label('count')
            ).filter(
                and_(*filters),
                SkillExecutionHistory.created_at >= thirty_days_ago
            ).group_by(
                func.date(SkillExecutionHistory.created_at)
            ).order_by(
                desc('date')
            ).all()
            
            # 用户分布
            user_distribution = self.db.query(
                SkillExecutionHistory.user_id,
                SkillExecutionHistory.username,
                func.count(SkillExecutionHistory.id).label('count')
            ).filter(
                SkillExecutionHistory.skill_id == skill_id
            ).group_by(
                SkillExecutionHistory.user_id,
                SkillExecutionHistory.username
            ).order_by(
                desc('count')
            ).limit(10).all()
            
            return {
                "skill_id": skill_id,
                "total_executions": total_executions,
                "success_count": success_count,
                "success_rate": success_count / total_executions if total_executions > 0 else 0,
                "daily_stats": [
                    {
                        "date": stat.date.isoformat() if hasattr(stat.date, 'isoformat') else str(stat.date),
                        "count": stat.count
                    }
                    for stat in daily_stats
                ],
                "user_distribution": [
                    {
                        "user_id": dist.user_id,
                        "username": dist.username,
                        "count": dist.count
                    }
                    for dist in user_distribution
                ]
            }
            
        except Exception as e:
            logger.error(f"获取技能统计失败: {str(e)}", exc_info=True)
            raise
    
    # ========== 用户偏好管理 ==========
    
    async def get_user_preferences(self, user_id: int) -> List[UserSkillPreference]:
        """获取用户技能偏好"""
        try:
            preferences = self.db.query(UserSkillPreference).filter(
                UserSkillPreference.user_id == user_id
            ).order_by(
                desc(UserSkillPreference.usage_count)
            ).all()
            
            return preferences
            
        except Exception as e:
            logger.error(f"获取用户偏好失败: {str(e)}", exc_info=True)
            raise
    
    async def update_preference(
        self,
        user_id: int,
        skill_id: str,
        favorite: Optional[bool] = None,
        default_parameters: Optional[Dict[str, Any]] = None,
        rating: Optional[int] = None,
        feedback: Optional[str] = None
    ) -> UserSkillPreference:
        """更新用户技能偏好"""
        try:
            # 查找或创建偏好记录
            preference = self.db.query(UserSkillPreference).filter(
                UserSkillPreference.user_id == user_id,
                UserSkillPreference.skill_id == skill_id
            ).first()
            
            if not preference:
                preference = UserSkillPreference(
                    user_id=user_id,
                    skill_id=skill_id,
                    favorite=False,
                    default_parameters={},
                    usage_count=0
                )
                self.db.add(preference)
            
            # 更新字段
            if favorite is not None:
                preference.favorite = favorite
            
            if default_parameters is not None:
                preference.default_parameters = default_parameters
            
            if rating is not None:
                preference.rating = rating
            
            if feedback is not None:
                preference.feedback = feedback
            
            preference.last_used = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(preference)
            
            return preference
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"更新用户偏好失败: {str(e)}", exc_info=True)
            raise
    
    # ========== 私有方法 ==========
    
    async def _update_skill_stats(
        self,
        user: User,
        skill: Optional[Skill],
        request: SkillExecutionRequest,
        result: SkillExecutionResponse
    ):
        """更新技能使用统计"""
        try:
            today = datetime.utcnow().strftime("%Y-%m-%d")
            
            # 查找或创建统计记录
            stat = self.db.query(SkillUsageStat).filter(
                SkillUsageStat.user_id == user.id,
                SkillUsageStat.skill_id == request.skill_id,
                SkillUsageStat.date == today
            ).first()
            
            if not stat:
                stat = SkillUsageStat(
                    user_id=user.id,
                    skill_id=request.skill_id,
                    skill_type=skill.type.value if skill and hasattr(skill.type, 'value') else None,
                    date=today,
                    execution_count=0,
                    success_count=0,
                    total_execution_time=0.0,
                    total_token_usage=0,
                    total_cost=0.0
                )
                self.db.add(stat)
            
            # 更新统计
            stat.execution_count += 1
            if result.success:
                stat.success_count += 1
            
            stat.total_execution_time += (result.execution_time or 0.0)
            stat.total_token_usage += (getattr(result, 'token_usage', 0) or 0)
            stat.total_cost += (getattr(result, 'cost', 0) or 0.0)
            
        except Exception as e:
            logger.error(f"更新技能统计失败: {str(e)}", exc_info=True)
            # 不抛出异常，避免影响主要功能
    
    async def _update_user_preference(
        self,
        user: User,
        skill: Optional[Skill],
        request: SkillExecutionRequest
    ):
        """更新用户技能偏好"""
        try:
            # 查找或创建偏好记录
            preference = self.db.query(UserSkillPreference).filter(
                UserSkillPreference.user_id == user.id,
                UserSkillPreference.skill_id == request.skill_id
            ).first()
            
            if not preference:
                preference = UserSkillPreference(
                    user_id=user.id,
                    skill_id=request.skill_id,
                    favorite=False,
                    default_parameters=request.parameters or {},
                    usage_count=0
                )
                self.db.add(preference)
            
            # 更新使用次数
            preference.usage_count += 1
            preference.last_used = datetime.utcnow()
            
            # 如果这是第一次成功使用，可以自动设置为收藏
            if preference.usage_count == 1 and skill:
                preference.favorite = True
            
        except Exception as e:
            logger.error(f"更新用户偏好失败: {str(e)}", exc_info=True)
            # 不抛出异常，避免影响主要功能