"""
技能执行API
提供技能执行和管理的接口
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.skill import (
    SkillExecutionRequest, 
    SkillExecutionResponse,
    SkillListResponse,
    SkillDetail
)
from app.services.skill_executor import skill_executor
from app.api.deps import get_current_user

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
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"技能执行失败: {str(e)}"
        )

@router.post("/execute/batch", response_model=List[SkillExecutionResponse])
async def execute_skills_batch(
    requests: List[SkillExecutionRequest],
    current_user = Depends(get_current_user)
):
    """
    批量执行多个技能
    
    可以同时执行多个技能，返回所有结果
    """
    try:
        # 为每个请求添加用户上下文
        for request in requests:
            if not request.parameters:
                request.parameters = {}
            request.parameters["user_id"] = str(current_user.id)
            request.parameters["username"] = current_user.username
        
        # 批量执行
        results = await skill_executor.execute_multiple_skills(requests)
        
        # 检查是否有失败的任务
        failed_tasks = [i for i, r in enumerate(results) if not r.success]
        if failed_tasks:
            logger.warning(f"批量执行中有失败的任务: {failed_tasks}")
        
        return results
        
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