"""
技能执行API
提供技能执行和管理的接口
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.schemas.skill import (
    SkillExecutionRequest, 
    SkillExecutionResponse,
    SkillListResponse,
    SkillDetail,
    SkillHistoryResponse,
    SkillStatsResponse,
    UserPreferenceResponse
)
from app.services.skill_executor import skill_executor
from app.services.skill_history_service import SkillHistoryService
from app.api.deps import get_current_user, get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/execute", response_model=SkillExecutionResponse)
async def execute_skill(
    request: SkillExecutionRequest,
    current_user = Depends(get_current_user)
):
    """
    执行单个技能
    
    - **skill_id**: 技能ID
    - **input_text**: 输入文本
    - **parameters**: 执行参数
    - **temperature**: 温度参数 (0.0-1.0)
    - **max_tokens**: 最大token数
    """
    try:
        # 添加用户上下文
        if not request.parameters:
            request.parameters = {}
        
        # 可以在这里添加用户特定的参数
        request.parameters["user_id"] = str(current_user.id)
        request.parameters["username"] = current_user.username
        
        # 执行技能
        result = await skill_executor.execute_skill(request)
        
        if not result.success:
            raise HTTPException(
                status_code=400,
                detail=result.error
            )
        
        # 记录执行历史
        try:
            history_service = SkillHistoryService(db)
            skill = skill_executor.get_skill(request.skill_id)
            await history_service.record_execution(current_user, skill, request, result)
        except Exception as history_error:
            logger.warning(f"记录执行历史失败: {str(history_error)}")
            # 不抛出异常，避免影响主要功能
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"技能执行失败: {str(e)}"
        )

@router.post("/execute/batch", response_model=BatchSkillExecutionResponse)
async def execute_skills_batch(
    batch_request: BatchSkillExecutionRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    批量执行多个技能
    
    可以同时执行多个技能，返回所有结果
    """
    try:
        requests = batch_request.requests
        results = []
        total_time = 0.0
        total_tokens = 0
        total_cost = 0.0
        successful = 0
        failed = 0
        
        # 批量执行
        for i, request in enumerate(requests):
            try:
                # 添加用户上下文
                if not request.parameters:
                    request.parameters = {}
                request.parameters["user_id"] = str(current_user.id)
                request.parameters["username"] = current_user.username
                
                # 执行技能
                result = await skill_executor.execute_skill(request)
                
                # 记录历史
                try:
                    history_service = SkillHistoryService(db)
                    skill = skill_executor.get_skill(request.skill_id)
                    await history_service.record_execution(current_user, skill, request, result)
                except Exception as history_error:
                    logger.warning(f"记录批量执行历史失败: {str(history_error)}")
                
                # 更新统计
                if result.success:
                    successful += 1
                    total_time += (result.execution_time or 0.0)
                    total_tokens += (getattr(result, 'token_usage', 0) or 0)
                    total_cost += (getattr(result, 'cost', 0) or 0.0)
                else:
                    failed += 1
                
                results.append(result)
                
            except Exception as task_error:
                logger.error(f"批量执行中任务{i}失败: {str(task_error)}")
                results.append(SkillExecutionResponse(
                    success=False,
                    output="",
                    error=f"任务执行失败: {str(task_error)}"
                ))
                failed += 1
        
        return BatchSkillExecutionResponse(
            results=results,
            total_requests=len(requests),
            successful_requests=successful,
            failed_requests=failed,
            total_execution_time=total_time,
            total_token_usage=total_tokens,
            total_cost=total_cost
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"批量技能执行失败: {str(e)}"
        )

@router.get("/list", response_model=SkillListResponse)
async def list_skills(
    skill_type: str = None,
    current_user = Depends(get_current_user)
):
    """
    列出所有可用技能
    
    - **skill_type**: 可选，按类型筛选技能
    """
    try:
        all_skills = skill_executor.list_skills()
        
        # 按类型筛选
        if skill_type:
            filtered_skills = [
                skill for skill in all_skills 
                if skill.type.value == skill_type
            ]
        else:
            filtered_skills = all_skills
        
        # 转换为响应模型
        skill_details = []
        for skill in filtered_skills:
            skill_details.append(
                SkillDetail(
                    id=skill.id,
                    name=skill.name,
                    description=skill.description,
                    type=skill.type,
                    parameters=skill.parameters,
                    example_input=skill.example_input if hasattr(skill, 'example_input') else "",
                    example_output=skill.example_output if hasattr(skill, 'example_output') else ""
                )
            )
        
        return SkillListResponse(
            skills=skill_details,
            total=len(skill_details),
            skill_types=list(set(s.type.value for s in all_skills))
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取技能列表失败: {str(e)}"
        )

@router.get("/{skill_id}", response_model=SkillDetail)
async def get_skill_detail(
    skill_id: str,
    current_user = Depends(get_current_user)
):
    """
    获取技能详情
    
    - **skill_id**: 技能ID
    """
    try:
        skill = skill_executor.get_skill(skill_id)
        if not skill:
            raise HTTPException(
                status_code=404,
                detail=f"技能未找到: {skill_id}"
            )
        
        return SkillDetail(
            id=skill.id,
            name=skill.name,
            description=skill.description,
            type=skill.type,
            parameters=skill.parameters,
            example_input=skill.example_input if hasattr(skill, 'example_input') else "",
            example_output=skill.example_output if hasattr(skill, 'example_output') else ""
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取技能详情失败: {str(e)}"
        )

@router.post("/test")
async def test_skill_execution(
    request: SkillExecutionRequest,
    current_user = Depends(get_current_user)
):
    """
    测试技能执行（不保存历史）
    
    用于快速测试技能效果
    """
    try:
        # 执行技能但不保存历史
        result = await skill_executor.execute_skill(request)
        
        if not result.success:
            return {
                "success": False,
                "error": result.error,
                "test_output": result.output[:200] + "..." if len(result.output) > 200 else result.output
            }
        
        return {
            "success": True,
            "skill_used": result.skill_used,
            "test_output": result.output,
            "execution_time": result.execution_time
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"技能测试失败: {str(e)}"
        )

# ========== 历史记录API ==========

@router.get("/history", response_model=List[SkillHistoryResponse])
async def get_execution_history(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    skill_id: Optional[str] = Query(None, description="技能ID筛选"),
    limit: int = Query(50, ge=1, le=100, description="每页数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    start_date: Optional[datetime] = Query(None, description="开始日期"),
    end_date: Optional[datetime] = Query(None, description="结束日期"),
    success_only: bool = Query(False, description="仅显示成功记录")
):
    """
    获取技能执行历史记录
    
    - **skill_id**: 可选，按技能ID筛选
    - **limit**: 每页数量 (1-100)
    - **offset**: 偏移量
    - **start_date**: 开始日期
    - **end_date**: 结束日期
    - **success_only**: 仅显示成功记录
    """
    try:
        history_service = SkillHistoryService(db)
        history, total = await history_service.get_execution_history(
            user_id=current_user.id,
            limit=limit,
            offset=offset,
            skill_id=skill_id,
            start_date=start_date,
            end_date=end_date,
            success_only=success_only
        )
        
        return [
            SkillHistoryResponse(
                id=h.id,
                skill_id=h.skill_id,
                skill_name=h.skill_name,
                input_text=h.input_text[:100] + "..." if len(h.input_text) > 100 else h.input_text,
                output_text=h.output_text[:200] + "..." if len(h.output_text) > 200 else h.output_text,
                parameters=h.parameters,
                success=h.success,
                execution_time=h.execution_time,
                created_at=h.created_at
            )
            for h in history
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取历史记录失败: {str(e)}"
        )

@router.get("/history/{history_id}", response_model=SkillHistoryResponse)
async def get_history_detail(
    history_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    获取历史记录详情
    
    - **history_id**: 历史记录ID
    """
    try:
        history_service = SkillHistoryService(db)
        history = await history_service.get_history_by_id(history_id, current_user.id)
        
        if not history:
            raise HTTPException(
                status_code=404,
                detail="历史记录未找到"
            )
        
        return SkillHistoryResponse(
            id=history.id,
            skill_id=history.skill_id,
            skill_name=history.skill_name,
            input_text=history.input_text,
            output_text=history.output_text,
            parameters=history.parameters,
            success=history.success,
            execution_time=history.execution_time,
            created_at=history.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取历史记录详情失败: {str(e)}"
        )

@router.delete("/history/{history_id}")
async def delete_history(
    history_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    删除历史记录
    
    - **history_id**: 历史记录ID
    """
    try:
        history_service = SkillHistoryService(db)
        success = await history_service.delete_history(history_id, current_user.id)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail="历史记录未找到"
            )
        
        return {"message": "历史记录已删除"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"删除历史记录失败: {str(e)}"
        )

# ========== 统计分析API ==========

@router.get("/stats/user", response_model=SkillStatsResponse)
async def get_user_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    获取用户技能使用统计
    """
    try:
        history_service = SkillHistoryService(db)
        stats = await history_service.get_user_stats(current_user.id)
        
        return SkillStatsResponse(**stats)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取用户统计失败: {str(e)}"
        )

@router.get("/stats/skill/{skill_id}", response_model=SkillStatsResponse)
async def get_skill_stats(
    skill_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    获取技能使用统计
    
    - **skill_id**: 技能ID
    """
    try:
        history_service = SkillHistoryService(db)
        stats = await history_service.get_skill_stats(skill_id, current_user.id)
        
        return SkillStatsResponse(**stats)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取技能统计失败: {str(e)}"
        )

# ========== 用户偏好API ==========

@router.get("/preferences", response_model=List[UserPreferenceResponse])
async def get_user_preferences(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    获取用户技能偏好
    """
    try:
        history_service = SkillHistoryService(db)
        preferences = await history_service.get_user_preferences(current_user.id)
        
        return [
            UserPreferenceResponse(
                skill_id=pref.skill_id,
                favorite=pref.favorite,
                default_parameters=pref.default_parameters,
                usage_count=pref.usage_count,
                last_used=pref.last_used,
                rating=pref.rating
            )
            for pref in preferences
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取用户偏好失败: {str(e)}"
        )

@router.put("/preferences/{skill_id}", response_model=UserPreferenceResponse)
async def update_preference(
    skill_id: str,
    favorite: Optional[bool] = Query(None, description="是否收藏"),
    default_parameters: Optional[dict] = Query(None, description="默认参数"),
    rating: Optional[int] = Query(None, ge=1, le=5, description="评分 (1-5)"),
    feedback: Optional[str] = Query(None, description="反馈"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    更新用户技能偏好
    
    - **skill_id**: 技能ID
    - **favorite**: 是否收藏
    - **default_parameters**: 默认参数
    - **rating**: 评分 (1-5)
    - **feedback**: 反馈
    """
    try:
        history_service = SkillHistoryService(db)
        preference = await history_service.update_preference(
            user_id=current_user.id,
            skill_id=skill_id,
            favorite=favorite,
            default_parameters=default_parameters,
            rating=rating,
            feedback=feedback
        )
        
        return UserPreferenceResponse(
            skill_id=preference.skill_id,
            favorite=preference.favorite,
            default_parameters=preference.default_parameters,
            usage_count=preference.usage_count,
            last_used=preference.last_used,
            rating=preference.rating
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"更新用户偏好失败: {str(e)}"
        )