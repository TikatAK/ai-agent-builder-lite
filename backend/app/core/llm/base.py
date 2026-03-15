from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field
import logging
from enum import Enum

logger = logging.getLogger(__name__)

class LLMProvider(str, Enum):
    """支持的LLM提供商"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    DEEPSEEK = "deepseek"
    MOONSHOT = "moonshot"
    GOOGLE = "google"
    OLLAMA = "ollama"
    CUSTOM = "custom"

class MessageRole(str, Enum):
    """消息角色"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"
    TOOL = "tool"

class Message(BaseModel):
    """聊天消息"""
    role: MessageRole
    content: str
    name: Optional[str] = None
    tool_calls: Optional[List[Dict]] = None
    tool_call_id: Optional[str] = None

class LLMConfig(BaseModel):
    """LLM配置"""
    provider: LLMProvider
    model: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=4096, ge=1, le=128000)
    top_p: float = Field(default=1.0, ge=0.0, le=1.0)
    frequency_penalty: float = Field(default=0.0, ge=-2.0, le=2.0)
    presence_penalty: float = Field(default=0.0, ge=-2.0, le=2.0)
    stop: Optional[List[str]] = None
    timeout: int = Field(default=30, ge=1, le=300)
    max_retries: int = Field(default=3, ge=0, le=10)

class LLMResponse(BaseModel):
    """LLM响应"""
    content: str
    model: str
    provider: LLMProvider
    usage: Dict[str, int] = Field(default_factory=dict)
    finish_reason: Optional[str] = None
    tool_calls: Optional[List[Dict]] = None

class BaseLLM(ABC):
    """LLM基类"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.client = None
        self._initialize_client()
    
    @abstractmethod
    def _initialize_client(self):
        """初始化客户端"""
        pass
    
    @abstractmethod
    async def chat_completion(
        self,
        messages: List[Message],
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[Union[str, Dict]] = None,
        **kwargs
    ) -> LLMResponse:
        """
        聊天补全
        
        Args:
            messages: 消息列表
            tools: 可用工具列表
            tool_choice: 工具选择策略
            **kwargs: 其他参数
            
        Returns:
            LLMResponse: LLM响应
        """
        pass
    
    @abstractmethod
    async def stream_chat_completion(
        self,
        messages: List[Message],
        tools: Optional[List[Dict]] = None,
        **kwargs
    ):
        """
        流式聊天补全
        
        Args:
            messages: 消息列表
            tools: 可用工具列表
            **kwargs: 其他参数
            
        Yields:
            str: 流式响应块
        """
        pass
    
    @abstractmethod
    async def embeddings(self, text: str) -> List[float]:
        """
        获取文本嵌入
        
        Args:
            text: 输入文本
            
        Returns:
            List[float]: 嵌入向量
        """
        pass
    
    def validate_messages(self, messages: List[Message]) -> bool:
        """验证消息列表"""
        if not messages:
            return False
        
        # 检查消息角色顺序
        for i, msg in enumerate(messages):
            if i == 0 and msg.role != MessageRole.SYSTEM:
                logger.warning("First message should be system message")
                return False
            
            if msg.role == MessageRole.SYSTEM and i != 0:
                logger.warning("System message should be first")
                return False
        
        return True
    
    def format_messages(self, messages: List[Message]) -> List[Dict]:
        """格式化消息为API所需格式"""
        formatted = []
        for msg in messages:
            formatted_msg = {
                "role": msg.role.value,
                "content": msg.content
            }
            if msg.name:
                formatted_msg["name"] = msg.name
            if msg.tool_calls:
                formatted_msg["tool_calls"] = msg.tool_calls
            if msg.tool_call_id:
                formatted_msg["tool_call_id"] = msg.tool_call_id
            formatted.append(formatted_msg)
        return formatted
    
    async def health_check(self) -> bool:
        """健康检查"""
        try:
            # 发送一个简单的测试消息
            test_messages = [
                Message(role=MessageRole.SYSTEM, content="You are a helpful assistant."),
                Message(role=MessageRole.USER, content="Hello, are you working?")
            ]
            response = await self.chat_completion(test_messages, max_tokens=10)
            return bool(response.content)
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    def get_cost_estimate(self, messages: List[Message], response_tokens: int) -> float:
        """估算成本（美元）"""
        # 这里实现成本估算逻辑
        # 实际实现需要根据不同的模型定价
        input_tokens = sum(len(msg.content) // 4 for msg in messages)
        total_tokens = input_tokens + response_tokens
        
        # 示例：GPT-4 Turbo定价
        if "gpt-4" in self.config.model:
            input_cost_per_1k = 0.01  # $0.01 per 1K tokens
            output_cost_per_1k = 0.03  # $0.03 per 1K tokens
        elif "gpt-3.5" in self.config.model:
            input_cost_per_1k = 0.001  # $0.001 per 1K tokens
            output_cost_per_1k = 0.002  # $0.002 per 1K tokens
        else:
            # 默认估算
            input_cost_per_1k = 0.001
            output_cost_per_1k = 0.002
        
        cost = (input_tokens / 1000 * input_cost_per_1k) + (response_tokens / 1000 * output_cost_per_1k)
        return round(cost, 6)