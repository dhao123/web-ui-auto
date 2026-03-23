from openai import OpenAI
import os
import logging
from typing import Any, Optional, Sequence, Union, Mapping

from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.language_models.base import LanguageModelInput
from langchain_core.messages import AIMessage, SystemMessage, BaseMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool
from langchain_core.utils.function_calling import convert_to_openai_tool

from src.utils import config

logger = logging.getLogger(__name__)


class ZKHChatOpenAI(ChatOpenAI):
    """
    ZKH AI Gateway 专用的 ChatOpenAI 子类
    
    ZKH API 不支持以下参数，需要过滤：
    - tool_choice 的对象格式 {"type": "function", "function": {"name": "..."}}
    - parallel_tool_calls
    - response_format
    - strict (在 tools 中)
    """
    
    def _filter_unsupported_params(self, kwargs: dict) -> dict:
        """过滤 ZKH 不支持的参数"""
        filtered = kwargs.copy()
        
        # 移除不支持的顶级参数
        unsupported_params = ['parallel_tool_calls', 'response_format', 'stream_options']
        for param in unsupported_params:
            if param in filtered:
                logger.debug(f"ZKH: Removing unsupported parameter '{param}'")
                del filtered[param]
        
        # 处理 tool_choice: 只支持字符串格式 ("auto", "required", "none")
        if 'tool_choice' in filtered:
            tool_choice = filtered['tool_choice']
            if isinstance(tool_choice, dict):
                # 将对象格式转换为 "required"
                logger.debug(f"ZKH: Converting tool_choice from {tool_choice} to 'required'")
                filtered['tool_choice'] = 'required'
        
        # 处理 tools: 移除 strict 参数
        if 'tools' in filtered and filtered['tools']:
            cleaned_tools = []
            for tool in filtered['tools']:
                if isinstance(tool, dict):
                    tool_copy = tool.copy()
                    if 'function' in tool_copy and isinstance(tool_copy['function'], dict):
                        func = tool_copy['function'].copy()
                        if 'strict' in func:
                            del func['strict']
                        tool_copy['function'] = func
                    cleaned_tools.append(tool_copy)
                else:
                    cleaned_tools.append(tool)
            filtered['tools'] = cleaned_tools
        
        return filtered
    
    def _generate(
        self,
        messages: list[BaseMessage],
        stop: Optional[list[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> Any:
        """重写 _generate 方法，在调用前过滤参数"""
        filtered_kwargs = self._filter_unsupported_params(kwargs)
        return super()._generate(messages, stop, run_manager, **filtered_kwargs)
    
    async def _agenerate(
        self,
        messages: list[BaseMessage],
        stop: Optional[list[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> Any:
        """重写 _agenerate 方法，在调用前过滤参数"""
        filtered_kwargs = self._filter_unsupported_params(kwargs)
        return await super()._agenerate(messages, stop, run_manager, **filtered_kwargs)


class DeepSeekR1ChatOpenAI(ChatOpenAI):
    """支持 DeepSeek R1 推理模式的 ChatOpenAI 子类"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.client = OpenAI(
            base_url=kwargs.get("base_url"),
            api_key=kwargs.get("api_key")
        )

    async def ainvoke(
            self,
            input: LanguageModelInput,
            config: Optional[RunnableConfig] = None,
            *,
            stop: Optional[list[str]] = None,
            **kwargs: Any,
    ) -> AIMessage:
        message_history = []
        for input_ in input:
            if isinstance(input_, SystemMessage):
                message_history.append({"role": "system", "content": input_.content})
            elif isinstance(input_, AIMessage):
                message_history.append({"role": "assistant", "content": input_.content})
            else:
                message_history.append({"role": "user", "content": input_.content})

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=message_history
        )

        reasoning_content = getattr(response.choices[0].message, 'reasoning_content', None)
        content = response.choices[0].message.content
        return AIMessage(content=content, reasoning_content=reasoning_content)

    def invoke(
            self,
            input: LanguageModelInput,
            config: Optional[RunnableConfig] = None,
            *,
            stop: Optional[list[str]] = None,
            **kwargs: Any,
    ) -> AIMessage:
        message_history = []
        for input_ in input:
            if isinstance(input_, SystemMessage):
                message_history.append({"role": "system", "content": input_.content})
            elif isinstance(input_, AIMessage):
                message_history.append({"role": "assistant", "content": input_.content})
            else:
                message_history.append({"role": "user", "content": input_.content})

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=message_history
        )

        reasoning_content = getattr(response.choices[0].message, 'reasoning_content', None)
        content = response.choices[0].message.content
        return AIMessage(content=content, reasoning_content=reasoning_content)


class DeepSeekR1ChatOllama(ChatOllama):
    """支持本地 DeepSeek R1 推理模式的 ChatOllama 子类"""

    async def ainvoke(
            self,
            input: LanguageModelInput,
            config: Optional[RunnableConfig] = None,
            *,
            stop: Optional[list[str]] = None,
            **kwargs: Any,
    ) -> AIMessage:
        org_ai_message = await super().ainvoke(input=input)
        org_content = org_ai_message.content
        if "</think>" in org_content:
            reasoning_content = org_content.split("</think>")[0].replace("<think>", "")
            content = org_content.split("</think>")[1]
            if "**JSON Response:**" in content:
                content = content.split("**JSON Response:**")[-1]
        else:
            reasoning_content = None
            content = org_content
        return AIMessage(content=content, reasoning_content=reasoning_content)

    def invoke(
            self,
            input: LanguageModelInput,
            config: Optional[RunnableConfig] = None,
            *,
            stop: Optional[list[str]] = None,
            **kwargs: Any,
    ) -> AIMessage:
        org_ai_message = super().invoke(input=input)
        org_content = org_ai_message.content
        if "</think>" in org_content:
            reasoning_content = org_content.split("</think>")[0].replace("<think>", "")
            content = org_content.split("</think>")[1]
            if "**JSON Response:**" in content:
                content = content.split("**JSON Response:**")[-1]
        else:
            reasoning_content = None
            content = org_content
        return AIMessage(content=content, reasoning_content=reasoning_content)


def get_llm_model(provider: str, **kwargs):
    """
    获取 LLM 模型实例
    
    支持的 provider:
    - zkh: ZKH AI Gateway (默认)
    - openai: OpenAI
    - deepseek: DeepSeek
    - ollama: Ollama 本地模型
    - lmstudio: LM Studio 本地模型 (OpenAI 兼容 API)
    
    :param provider: LLM 供应商名称
    :param kwargs: 模型配置参数
    :return: LLM 模型实例
    """
    # Ollama 和 LM Studio 不需要 API Key (LM Studio 支持空 API key)
    if provider not in ("ollama", "lmstudio"):
        env_var = f"{provider.upper()}_API_KEY"
        api_key = kwargs.get("api_key", "") or os.getenv(env_var, "")
        if not api_key:
            provider_display = config.PROVIDER_DISPLAY_NAMES.get(provider, provider.upper())
            error_msg = f"💥 {provider_display} API key not found! 🔑 Please set the `{env_var}` environment variable or provide it in the UI."
            raise ValueError(error_msg)
        kwargs["api_key"] = api_key
    
    # ==================== ZKH AI Gateway (默认供应商) ====================
    if provider == "zkh":
        # ZKH API 兼容 OpenAI 格式，但有部分参数限制
        base_url = kwargs.get("base_url") or os.getenv("ZKH_ENDPOINT", "https://ai-dev-gateway.zkh360.com/llm/v1")
        
        return ZKHChatOpenAI(
            model=kwargs.get("model_name", "ep_20250815_yc11"),
            temperature=kwargs.get("temperature", 0.0),
            base_url=base_url,
            api_key=api_key,
        )
    
    # ==================== OpenAI ====================
    elif provider == "openai":
        base_url = kwargs.get("base_url") or os.getenv("OPENAI_ENDPOINT", "https://api.openai.com/v1")
        
        return ChatOpenAI(
            model=kwargs.get("model_name", "gpt-4o"),
            temperature=kwargs.get("temperature", 0.0),
            base_url=base_url,
            api_key=api_key,
        )
    
    # ==================== DeepSeek ====================
    elif provider == "deepseek":
        base_url = kwargs.get("base_url") or os.getenv("DEEPSEEK_ENDPOINT", "https://api.deepseek.com")
        
        # DeepSeek Reasoner 模型支持推理内容
        if kwargs.get("model_name", "deepseek-chat") == "deepseek-reasoner":
            return DeepSeekR1ChatOpenAI(
                model=kwargs.get("model_name", "deepseek-reasoner"),
                temperature=kwargs.get("temperature", 0.0),
                base_url=base_url,
                api_key=api_key,
            )
        else:
            return ChatOpenAI(
                model=kwargs.get("model_name", "deepseek-chat"),
                temperature=kwargs.get("temperature", 0.0),
                base_url=base_url,
                api_key=api_key,
            )
    
    # ==================== Ollama (本地模型) ====================
    elif provider == "ollama":
        base_url = kwargs.get("base_url") or os.getenv("OLLAMA_ENDPOINT", "http://localhost:11434")
        
        # 本地 DeepSeek R1 模型支持推理内容
        if "deepseek-r1" in kwargs.get("model_name", "qwen2.5:7b"):
            return DeepSeekR1ChatOllama(
                model=kwargs.get("model_name", "deepseek-r1:14b"),
                temperature=kwargs.get("temperature", 0.0),
                num_ctx=kwargs.get("num_ctx", 32000),
                base_url=base_url,
            )
        else:
            return ChatOllama(
                model=kwargs.get("model_name", "qwen2.5:7b"),
                temperature=kwargs.get("temperature", 0.0),
                num_ctx=kwargs.get("num_ctx", 32000),
                num_predict=kwargs.get("num_predict", 1024),
                base_url=base_url,
            )
    
    # ==================== LM Studio (本地模型 - OpenAI 兼容 API) ====================
    elif provider == "lmstudio":
        # LM Studio 默认端口是 1234，用户可配置 base_url
        base_url = kwargs.get("base_url") or os.getenv("LMSTUDIO_ENDPOINT", "http://localhost:1234/v1")
        # LM Studio 支持空 API key，如果未提供则使用空字符串
        api_key = kwargs.get("api_key", "") or os.getenv("LMSTUDIO_API_KEY", "")
        
        return ChatOpenAI(
            model=kwargs.get("model_name", "qwen3.5-9b"),
            temperature=kwargs.get("temperature", 0.0),
            base_url=base_url,
            api_key=api_key if api_key else "not-needed",  # LM Studio 接受任意 API key 或 "not-needed"
        )
    
    else:
        raise ValueError(f"Unsupported provider: {provider}. Supported providers: zkh, openai, deepseek, ollama, lmstudio")
