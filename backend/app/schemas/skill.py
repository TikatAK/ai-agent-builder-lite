"""
技能相关Pydantic模型
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum

# ========== 技能类型枚举 ==========

class SkillType(str, Enum):
    """技能类型枚举"""
    TEXT_PROCESSING = "文本处理"
    CODE_ASSISTANT = "代码助手"
    LEARNING_ASSISTANT = "学习助手"
    OFFICE_ASSISTANT = "办公助手"
    DATA_ANALYSIS = "数据分析"
    TRANSLATION = "翻译"
    CUSTOM = "自定义"

# ========== 技能执行相关模型 ==========

class SkillParameter(BaseModel):
    """技能参数定义"""
    type: str = Field(..., description="参数类型")
    default: Optional[Any] = Field(None, description="默认值")
    required: bool = Field(False, description="是否必填")
    description: str = Field(..., description="参数描述")
    options: Optional[List[str]] = Field(None, description="可选值列表")
    min: Optional[float] = Field(None, description="最小值")
    max: Optional[float] = Field(None, description="最大值")
    step: Optional[float] = Field(None, description="步长")

class SkillExecutionRequest(BaseModel):
    """技能执行请求"""
    skill_id: str = Field(..., description="技能ID")
    input_text: str = Field(..., min_length=1, description="输入文本")
    parameters: Optional[Dict[str, Any]] = Field(None, description="执行参数")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0, description="温度参数")
    max_tokens: Optional[int] = Field(1000, ge=1, le=128000, description="最大token数")
    
    @validator('temperature')
    def validate_temperature(cls, v):
        if v is not None and (v < 0.0 or v > 2.0):
            raise ValueError('温度参数必须在0.0到2.0之间')
        return v

class SkillExecutionResponse(BaseModel):
    """技能执行响应"""
    success: bool = Field(..., description="是否成功")
    output: str = Field(..., description="输出内容")
    skill_used: Optional[str] = Field(None, description="使用的技能名称")
    execution_time: Optional[float] = Field(None, ge=0.0, description="执行时间（秒）")
    error: Optional[str] = Field(None, description="错误信息")
    token_usage: Optional[int] = Field(None, ge=0, description="使用的token数量")
    cost: Optional[float] = Field(None, ge=0.0, description="执行成本")

# ========== 技能管理相关模型 ==========

class SkillDetail(BaseModel):
    """技能详情"""
    id: str = Field(..., description="技能ID")
    name: str = Field(..., description="技能名称")
    description: str = Field(..., description="技能描述")
    type: SkillType = Field(..., description="技能类型")
    parameters: Dict[str, SkillParameter] = Field(..., description="技能参数")
    example_input: Optional[str] = Field(None, description="示例输入")
    example_output: Optional[str] = Field(None, description="示例输出")

class SkillListResponse(BaseModel):
    """技能列表响应"""
    skills: List[SkillDetail] = Field(..., description="技能列表")
    total: int = Field(..., ge=0, description="总技能数")
    skill_types: List[str] = Field(..., description="技能类型列表")

# ========== 历史记录相关模型 ==========

class SkillHistoryResponse(BaseModel):
    """技能历史记录响应"""
    id: int = Field(..., description="历史记录ID")
    skill_id: str = Field(..., description="技能ID")
    skill_name: str = Field(..., description="技能名称")
    input_text: str = Field(..., description="输入文本")
    output_text: str = Field(..., description="输出文本")
    parameters: Optional[Dict[str, Any]] = Field(None, description="执行参数")
    success: bool = Field(..., description="是否成功")
    execution_time: float = Field(..., ge=0.0, description="执行时间（秒）")
    created_at: datetime = Field(..., description="创建时间")
    
    class Config:
        from_attributes = True

class SkillHistoryListResponse(BaseModel):
    """技能历史记录列表响应"""
    history: List[SkillHistoryResponse] = Field(..., description="历史记录列表")
    total: int = Field(..., ge=0, description="总记录数")
    page: int = Field(..., ge=1, description="当前页码")
    page_size: int = Field(..., ge=1, le=100, description="每页数量")

# ========== 统计分析相关模型 ==========

class DailyStat(BaseModel):
    """每日统计"""
    date: str = Field(..., description="日期")
    count: int = Field(..., ge=0, description="执行次数")

class UserDistribution(BaseModel):
    """用户分布"""
    user_id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    count: int = Field(..., ge=0, description="使用次数")

class PopularSkill(BaseModel):
    """热门技能"""
    skill_id: str = Field(..., description="技能ID")
    skill_name: str = Field(..., description="技能名称")
    count: int = Field(..., ge=0, description="使用次数")

class SkillStatsResponse(BaseModel):
    """技能统计响应"""
    # 基础统计
    total_executions: int = Field(0, ge=0, description="总执行次数")
    success_count: int = Field(0, ge=0, description="成功次数")
    success_rate: float = Field(0.0, ge=0.0, le=1.0, description="成功率")
    total_execution_time: float = Field(0.0, ge=0.0, description="总执行时间")
    avg_execution_time: float = Field(0.0, ge=0.0, description="平均执行时间")
    total_tokens_used: int = Field(0, ge=0, description="总token使用量")
    avg_tokens_per_execution: float = Field(0.0, ge=0.0, description="平均每次token使用量")
    total_cost: float = Field(0.0, ge=0.0, description="总成本")
    avg_cost_per_execution: float = Field(0.0, ge=0.0, description="平均每次成本")
    
    # 分布统计
    popular_skills: List[PopularSkill] = Field(default_factory=list, description="热门技能")
    daily_stats: List[DailyStat] = Field(default_factory=list, description="每日统计")
    user_distribution: List[UserDistribution] = Field(default_factory=list, description="用户分布")
    
    # 技能特定字段
    skill_id: Optional[str] = Field(None, description="技能ID")
    
    class Config:
        from_attributes = True

# ========== 用户偏好相关模型 ==========

class UserPreferenceResponse(BaseModel):
    """用户偏好响应"""
    skill_id: str = Field(..., description="技能ID")
    favorite: bool = Field(False, description="是否收藏")
    default_parameters: Optional[Dict[str, Any]] = Field(None, description="默认参数")
    usage_count: int = Field(0, ge=0, description="使用次数")
    last_used: Optional[datetime] = Field(None, description="最后使用时间")
    rating: Optional[int] = Field(None, ge=1, le=5, description="评分")
    feedback: Optional[str] = Field(None, description="反馈")
    
    class Config:
        from_attributes = True

# ========== 批量执行相关模型 ==========

class BatchSkillExecutionRequest(BaseModel):
    """批量技能执行请求"""
    requests: List[SkillExecutionRequest] = Field(..., min_items=1, max_items=10, description="执行请求列表")

class BatchSkillExecutionResponse(BaseModel):
    """批量技能执行响应"""
    results: List[SkillExecutionResponse] = Field(..., description="执行结果列表")
    total_requests: int = Field(..., ge=0, description="总请求数")
    successful_requests: int = Field(..., ge=0, description="成功请求数")
    failed_requests: int = Field(..., ge=0, description="失败请求数")
    total_execution_time: float = Field(..., ge=0.0, description="总执行时间")
    total_token_usage: int = Field(..., ge=0, description="总token使用量")
    total_cost: float = Field(..., ge=0.0, description="总成本")

# ========== 技能搜索相关模型 ==========

class SkillSearchRequest(BaseModel):
    """技能搜索请求"""
    query: str = Field(..., min_length=1, max_length=100, description="搜索关键词")
    skill_type: Optional[SkillType] = Field(None, description="技能类型筛选")
    limit: int = Field(10, ge=1, le=50, description="返回数量限制")

class SkillSearchResponse(BaseModel):
    """技能搜索响应"""
    skills: List[SkillDetail] = Field(..., description="搜索结果")
    total: int = Field(..., ge=0, description="总结果数")
    query: str = Field(..., description="搜索关键词")

# ========== 自定义技能相关模型 ==========

class CustomSkillCreate(BaseModel):
    """自定义技能创建请求"""
    name: str = Field(..., min_length=1, max_length=100, description="技能名称")
    description: str = Field(..., min_length=10, max_length=500, description="技能描述")
    type: SkillType = Field(..., description="技能类型")
    prompt_template: str = Field(..., min_length=10, description="提示词模板")
    parameters: Dict[str, SkillParameter] = Field(default_factory=dict, description="技能参数")
    example_input: Optional[str] = Field(None, description="示例输入")
    example_output: Optional[str] = Field(None, description="示例输出")
    is_public: bool = Field(False, description="是否公开")

class CustomSkillUpdate(BaseModel):
    """自定义技能更新请求"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=10, max_length=500)
    type: Optional[SkillType] = None
    prompt_template: Optional[str] = Field(None, min_length=10)
    parameters: Optional[Dict[str, SkillParameter]] = None
    example_input: Optional[str] = None
    example_output: Optional[str] = None
    is_public: Optional[bool] = None