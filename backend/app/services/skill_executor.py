"""
技能执行引擎
负责执行AI助手的各种技能，如文本处理、代码生成、数据分析等
"""
from typing import Dict, List, Any, Optional
import logging
from app.core.llm.base import LLMService, MessageRole
from app.core.llm.providers import get_llm_provider
from app.models.skill import Skill, SkillType
from app.schemas.skill import SkillExecutionRequest, SkillExecutionResponse

logger = logging.getLogger(__name__)

class SkillExecutor:
    """技能执行引擎"""
    
    def __init__(self, llm_service: Optional[LLMService] = None):
        self.llm_service = llm_service or get_llm_provider()
        self.skill_registry: Dict[str, Skill] = {}
        self._register_builtin_skills()
    
    def _register_builtin_skills(self):
        """注册内置技能"""
        builtin_skills = [
            Skill(
                id="text_summarize",
                name="文本总结",
                description="将长文本总结为简洁的要点",
                type=SkillType.TEXT_PROCESSING,
                prompt_template="请将以下文本总结为3-5个要点：\n\n{input}",
                parameters={
                    "max_length": {"type": "int", "default": 500, "description": "最大输出长度"}
                }
            ),
            Skill(
                id="code_explain",
                name="代码解释",
                description="解释代码的功能和逻辑",
                type=SkillType.CODE_ASSISTANT,
                prompt_template="请解释以下代码的功能和逻辑：\n\n```{language}\n{code}\n```",
                parameters={
                    "language": {"type": "string", "required": True, "description": "编程语言"},
                    "detail_level": {"type": "string", "default": "medium", "description": "详细程度"}
                }
            ),
            Skill(
                id="translate",
                name="翻译",
                description="文本翻译",
                type=SkillType.TEXT_PROCESSING,
                prompt_template="请将以下文本从{source_lang}翻译到{target_lang}：\n\n{text}",
                parameters={
                    "source_lang": {"type": "string", "default": "auto", "description": "源语言"},
                    "target_lang": {"type": "string", "required": True, "description": "目标语言"}
                }
            ),
            Skill(
                id="learning_plan",
                name="学习计划制定",
                description="根据主题制定学习计划",
                type=SkillType.LEARNING_ASSISTANT,
                prompt_template="请为以下主题制定一个{timeframe}的学习计划：\n\n主题：{topic}\n\n要求：{requirements}",
                parameters={
                    "topic": {"type": "string", "required": True, "description": "学习主题"},
                    "timeframe": {"type": "string", "default": "一周", "description": "时间框架"},
                    "requirements": {"type": "string", "default": "", "description": "特殊要求"}
                }
            )
        ]
        
        for skill in builtin_skills:
            self.register_skill(skill)
    
    def register_skill(self, skill: Skill):
        """注册新技能"""
        self.skill_registry[skill.id] = skill
        logger.info(f"注册技能: {skill.name} ({skill.id})")
    
    async def execute_skill(self, request: SkillExecutionRequest) -> SkillExecutionResponse:
        """执行技能"""
        try:
            # 获取技能
            skill = self.skill_registry.get(request.skill_id)
            if not skill:
                return SkillExecutionResponse(
                    success=False,
                    error=f"技能未找到: {request.skill_id}",
                    output=""
                )
            
            # 构建提示词
            prompt = self._build_prompt(skill, request.parameters, request.input_text)
            
            # 调用LLM执行
            messages = [
                {"role": MessageRole.SYSTEM.value, "content": skill.prompt_template},
                {"role": MessageRole.USER.value, "content": prompt}
            ]
            
            output = await self.llm_service.generate_completion(
                messages=messages,
                temperature=request.temperature or 0.7,
                max_tokens=request.max_tokens or 1000
            )
            
            return SkillExecutionResponse(
                success=True,
                output=output,
                skill_used=skill.name,
                execution_time=0  # TODO: 添加实际执行时间计算
            )
            
        except Exception as e:
            logger.error(f"技能执行失败: {str(e)}", exc_info=True)
            return SkillExecutionResponse(
                success=False,
                error=str(e),
                output=""
            )
    
    def _build_prompt(self, skill: Skill, parameters: Dict[str, Any], input_text: str) -> str:
        """构建提示词"""
        # 如果有参数模板，使用模板
        if skill.prompt_template:
            try:
                # 合并参数和输入文本
                context = parameters.copy()
                context["input"] = input_text
                
                # 格式化模板
                prompt = skill.prompt_template.format(**context)
                return prompt
            except KeyError as e:
                raise ValueError(f"缺少必要参数: {e}")
        
        # 如果没有模板，直接使用输入文本
        return input_text
    
    def list_skills(self) -> List[Skill]:
        """列出所有可用技能"""
        return list(self.skill_registry.values())
    
    def get_skill(self, skill_id: str) -> Optional[Skill]:
        """获取特定技能"""
        return self.skill_registry.get(skill_id)
    
    async def execute_multiple_skills(
        self, 
        requests: List[SkillExecutionRequest]
    ) -> List[SkillExecutionResponse]:
        """批量执行多个技能"""
        results = []
        for request in requests:
            result = await self.execute_skill(request)
            results.append(result)
        return results

# 全局技能执行器实例
skill_executor = SkillExecutor()