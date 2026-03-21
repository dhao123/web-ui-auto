"""
Token追踪LLM包装器
用于捕获LLM调用的真实token使用情况
"""
import logging
from typing import Any, Optional, List

from pydantic import Field, ConfigDict
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.outputs import ChatResult

logger = logging.getLogger(__name__)


class TokenTrackingLLM(BaseChatModel):
    """
    LLM包装器，用于追踪token使用情况
    
    这个包装器会拦截LLM调用，提取真实的token使用情况，
    并通过回调函数通知外部组件
    
    继承BaseChatModel以确保完全兼容LangChain
    """
    
    wrapped_llm: Any = Field(default=None, exclude=True)
    token_callback: Optional[Any] = Field(default=None, exclude=True)
    
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra='allow'
    )
    
    def __init__(self, llm: BaseChatModel, token_callback: Optional[callable] = None, **kwargs):
        """
        初始化Token追踪LLM
        
        Args:
            llm: 被包装的LLM实例
            token_callback: token使用回调函数，签名为 (prompt_tokens, completion_tokens) -> None
        """
        # 调用父类初始化
        super().__init__(wrapped_llm=llm, token_callback=token_callback, **kwargs)
    
    def _extract_token_usage(self, response: AIMessage) -> tuple[int, int]:
        """
        从LLM响应中提取token使用情况
        
        Args:
            response: LLM响应消息
            
        Returns:
            (prompt_tokens, completion_tokens) 元组
        """
        prompt_tokens = 0
        completion_tokens = 0
        
        # 方法1: 从response_metadata提取（OpenAI格式）
        if hasattr(response, 'response_metadata') and response.response_metadata:
            metadata = response.response_metadata
            
            # OpenAI格式: response_metadata.token_usage
            if 'token_usage' in metadata:
                token_usage = metadata['token_usage']
                prompt_tokens = token_usage.get('prompt_tokens', 0)
                completion_tokens = token_usage.get('completion_tokens', 0)
            
            # 其他格式: response_metadata.usage
            elif 'usage' in metadata:
                usage = metadata['usage']
                prompt_tokens = usage.get('prompt_tokens', 0)
                completion_tokens = usage.get('completion_tokens', 0)
        
        # 方法2: 从usage_metadata提取（LangChain新版本）
        if hasattr(response, 'usage_metadata') and response.usage_metadata:
            usage_metadata = response.usage_metadata
            if isinstance(usage_metadata, dict):
                prompt_tokens = usage_metadata.get('input_tokens', prompt_tokens)
                completion_tokens = usage_metadata.get('output_tokens', completion_tokens)
            else:
                # 可能是对象
                prompt_tokens = getattr(usage_metadata, 'input_tokens', prompt_tokens)
                completion_tokens = getattr(usage_metadata, 'output_tokens', completion_tokens)
        
        return prompt_tokens, completion_tokens
    
    def _notify_token_usage(self, prompt_tokens: int, completion_tokens: int):
        """通知token使用情况"""
        if self.token_callback and (prompt_tokens > 0 or completion_tokens > 0):
            try:
                self.token_callback(prompt_tokens, completion_tokens)
                logger.debug(f"Token usage notified: prompt={prompt_tokens}, completion={completion_tokens}")
            except Exception as e:
                logger.error(f"Error in token callback: {e}", exc_info=True)
    
    def _generate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None, 
                  run_manager: Optional[Any] = None, **kwargs: Any) -> ChatResult:
        """同步生成（拦截并追踪token）"""
        result = self.wrapped_llm._generate(messages, stop, run_manager, **kwargs)
        
        # 提取token使用情况
        if result.generations and result.generations[0]:
            message = result.generations[0].message
            if isinstance(message, AIMessage):
                prompt_tokens, completion_tokens = self._extract_token_usage(message)
                self._notify_token_usage(prompt_tokens, completion_tokens)
        
        return result
    
    async def _agenerate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None,
                        run_manager: Optional[Any] = None, **kwargs: Any) -> ChatResult:
        """异步生成（拦截并追踪token）"""
        result = await self.wrapped_llm._agenerate(messages, stop, run_manager, **kwargs)
        
        # 提取token使用情况
        if result.generations and result.generations[0]:
            message = result.generations[0].message
            if isinstance(message, AIMessage):
                prompt_tokens, completion_tokens = self._extract_token_usage(message)
                self._notify_token_usage(prompt_tokens, completion_tokens)
        
        return result
    
    @property
    def _llm_type(self) -> str:
        """返回LLM类型"""
        if self.wrapped_llm:
            return f"token_tracking_{self.wrapped_llm._llm_type}"
        return "token_tracking"
    
    @property
    def _identifying_params(self) -> dict:
        """返回识别参数"""
        if self.wrapped_llm:
            return self.wrapped_llm._identifying_params
        return {}
    
    def bind_tools(self, tools, **kwargs):
        """
        绑定工具到LLM
        
        策略：
        1. 调用wrapped_llm.bind_tools()获取RunnableBinding
        2. 修改RunnableBinding的bound属性，让它指向self而不是wrapped_llm
        3. 这样RunnableBinding在调用时会使用TokenTrackingLLM的方法
        """
        if self.wrapped_llm:
            # 调用wrapped_llm的bind_tools
            bound_llm = self.wrapped_llm.bind_tools(tools, **kwargs)
            
            # 修改bound属性，让它指向self
            # 这样RunnableBinding会调用我们的_agenerate方法
            if hasattr(bound_llm, 'bound'):
                # 创建一个新的RunnableBinding，bound指向self
                from langchain_core.runnables import RunnableBinding
                return RunnableBinding(
                    bound=self,
                    kwargs=bound_llm.kwargs if hasattr(bound_llm, 'kwargs') else {},
                    config=bound_llm.config if hasattr(bound_llm, 'config') else {},
                    config_factories=bound_llm.config_factories if hasattr(bound_llm, 'config_factories') else []
                )
            return bound_llm
        
        # 如果没有wrapped_llm，抛出错误
        raise NotImplementedError("TokenTrackingLLM requires a wrapped_llm")
    
    def __getattr__(self, name: str) -> Any:
        """代理其他属性到被包装的LLM"""
        # 首先检查是否是特殊属性
        if name in ('_llm_type', '_identifying_params'):
            # 这些是property，应该通过正常的属性访问
            return object.__getattribute__(self, name)
        
        # 避免在初始化过程中出错
        if name in ('wrapped_llm', 'token_callback'):
            try:
                return object.__getattribute__(self, name)
            except AttributeError:
                return None
        
        # 代理到被包装的LLM
        try:
            wrapped = object.__getattribute__(self, 'wrapped_llm')
            if wrapped is not None:
                return getattr(wrapped, name)
        except AttributeError:
            pass
        
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
