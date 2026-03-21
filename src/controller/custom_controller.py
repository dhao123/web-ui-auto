import pdb

import pyperclip
from typing import Optional, Type, Callable, Dict, Any, Union, Awaitable, TypeVar
from pydantic import BaseModel
from browser_use.agent.views import ActionResult
from browser_use.browser.context import BrowserContext
from browser_use.controller.service import Controller, DoneAction
from browser_use.controller.registry.service import Registry, RegisteredAction
from main_content_extractor import MainContentExtractor
from browser_use.controller.views import (
    ClickElementAction,
    DoneAction,
    ExtractPageContentAction,
    GoToUrlAction,
    InputTextAction,
    OpenTabAction,
    ScrollAction,
    SearchGoogleAction,
    SendKeysAction,
    SwitchTabAction,
)
import logging
import inspect
import asyncio
import os
from langchain_core.language_models.chat_models import BaseChatModel
from browser_use.agent.views import ActionModel, ActionResult

from src.utils.mcp_client import create_tool_param_model, setup_mcp_client_and_tools
from src.mcp_servers import ZKHEcommerceServer

from browser_use.utils import time_execution_sync

logger = logging.getLogger(__name__)

Context = TypeVar('Context')


class CustomController(Controller):
    def __init__(self, exclude_actions: list[str] = [],
                 output_model: Optional[Type[BaseModel]] = None,
                 ask_assistant_callback: Optional[Union[Callable[[str, BrowserContext], Dict[str, Any]], Callable[
                     [str, BrowserContext], Awaitable[Dict[str, Any]]]]] = None,
                 ):
        super().__init__(exclude_actions=exclude_actions, output_model=output_model)
        self._register_custom_actions()
        self.ask_assistant_callback = ask_assistant_callback
        self.mcp_client = None
        self.mcp_server_config = None
        # 初始化内置MCP服务器
        self.zkh_ecommerce_server = ZKHEcommerceServer()
        self._register_builtin_mcp_tools()

    def _register_custom_actions(self):
        """Register all custom browser actions"""

        @self.registry.action(
            "When executing tasks, prioritize autonomous completion. However, if you encounter a definitive blocker "
            "that prevents you from proceeding independently – such as needing credentials you don't possess, "
            "requiring subjective human judgment, needing a physical action performed, encountering complex CAPTCHAs, "
            "or facing limitations in your capabilities – you must request human assistance."
        )
        async def ask_for_assistant(query: str, browser: BrowserContext):
            if self.ask_assistant_callback:
                if inspect.iscoroutinefunction(self.ask_assistant_callback):
                    user_response = await self.ask_assistant_callback(query, browser)
                else:
                    user_response = self.ask_assistant_callback(query, browser)
                msg = f"AI ask: {query}. User response: {user_response['response']}"
                logger.info(msg)
                return ActionResult(extracted_content=msg, include_in_memory=True)
            else:
                return ActionResult(extracted_content="Human cannot help you. Please try another way.",
                                    include_in_memory=True)

        @self.registry.action(
            'Upload file to interactive element with file path ',
        )
        async def upload_file(index: int, path: str, browser: BrowserContext, available_file_paths: list[str]):
            if path not in available_file_paths:
                return ActionResult(error=f'File path {path} is not available')

            if not os.path.exists(path):
                return ActionResult(error=f'File {path} does not exist')

            dom_el = await browser.get_dom_element_by_index(index)

            file_upload_dom_el = dom_el.get_file_upload_element()

            if file_upload_dom_el is None:
                msg = f'No file upload element found at index {index}'
                logger.info(msg)
                return ActionResult(error=msg)

            file_upload_el = await browser.get_locate_element(file_upload_dom_el)

            if file_upload_el is None:
                msg = f'No file upload element found at index {index}'
                logger.info(msg)
                return ActionResult(error=msg)

            try:
                await file_upload_el.set_input_files(path)
                msg = f'Successfully uploaded file to index {index}'
                logger.info(msg)
                return ActionResult(extracted_content=msg, include_in_memory=True)
            except Exception as e:
                msg = f'Failed to upload file to index {index}: {str(e)}'
                logger.info(msg)
                return ActionResult(error=msg)
    
    def _register_builtin_mcp_tools(self):
        """注册内置MCP工具（震坤行电商工具集）"""
        from pydantic import Field, create_model
        from browser_use.controller.registry.views import ActionModel
        
        # 注册 extract_price 工具
        @self.registry.action(
            "从页面中提取价格（支持未税价和含税价）。优先用于震坤行电商价格提取场景。"
        )
        async def zkh_extract_price(
            price_type: str = "untaxed",
            selector: Optional[str] = None,
            browser: BrowserContext = None
        ):
            """提取价格工具"""
            if not browser:
                return ActionResult(error="Browser context is required")
            
            page = browser.context.pages[0] if browser.context.pages else None
            if not page:
                return ActionResult(error="No active page found")
            
            result = await self.zkh_ecommerce_server.extract_price(
                page=page,
                price_type=price_type,
                selector=selector
            )
            
            if result["success"]:
                msg = f"成功提取价格: {result['price']} {result['currency']} (原始文本: {result['price_text']})"
                logger.info(msg)
                return ActionResult(extracted_content=msg, include_in_memory=True)
            else:
                return ActionResult(error=result["error"], include_in_memory=True)
        
        # 注册 verify_cart_status 工具
        @self.registry.action(
            "验证购物车状态和商品数量。用于确认加购操作是否成功。"
        )
        async def zkh_verify_cart_status(
            expected_count: Optional[int] = None,
            browser: BrowserContext = None
        ):
            """验证购物车状态工具"""
            if not browser:
                return ActionResult(error="Browser context is required")
            
            page = browser.context.pages[0] if browser.context.pages else None
            if not page:
                return ActionResult(error="No active page found")
            
            result = await self.zkh_ecommerce_server.verify_cart_status(
                page=page,
                expected_count=expected_count
            )
            
            msg = result["message"]
            logger.info(msg)
            
            if result["success"]:
                return ActionResult(extracted_content=msg, include_in_memory=True)
            else:
                return ActionResult(error=msg, include_in_memory=True)
        
        # 注册 wait_for_element 工具
        @self.registry.action(
            "智能等待页面元素出现。用于处理动态加载的元素。"
        )
        async def zkh_wait_for_element(
            selector: str,
            timeout: int = 10000,
            state: str = "visible",
            browser: BrowserContext = None
        ):
            """智能等待元素工具"""
            if not browser:
                return ActionResult(error="Browser context is required")
            
            page = browser.context.pages[0] if browser.context.pages else None
            if not page:
                return ActionResult(error="No active page found")
            
            result = await self.zkh_ecommerce_server.wait_for_element(
                page=page,
                selector=selector,
                timeout=timeout,
                state=state
            )
            
            if result["success"]:
                msg = f"元素已出现: {result['selector']}, 等待时间: {result['wait_time']}s"
                logger.info(msg)
                return ActionResult(extracted_content=msg, include_in_memory=True)
            else:
                return ActionResult(error=result["error"], include_in_memory=True)
        
        # 注册 capture_network 工具
        @self.registry.action(
            "捕获网络请求（用于调试和问题定位）。当遇到加购失败等问题时使用。"
        )
        async def zkh_capture_network(
            url_pattern: Optional[str] = None,
            duration: int = 5000,
            browser: BrowserContext = None
        ):
            """捕获网络请求工具"""
            if not browser:
                return ActionResult(error="Browser context is required")
            
            page = browser.context.pages[0] if browser.context.pages else None
            if not page:
                return ActionResult(error="No active page found")
            
            result = await self.zkh_ecommerce_server.capture_network(
                page=page,
                url_pattern=url_pattern,
                duration=duration
            )
            
            if result["success"]:
                msg = f"捕获到 {result['count']} 个网络请求"
                logger.info(msg)
                # 只返回摘要，避免日志过长
                return ActionResult(
                    extracted_content=f"{msg}. 前5个请求: {result['requests'][:5]}",
                    include_in_memory=True
                )
            else:
                return ActionResult(error=result["error"], include_in_memory=True)
        
        logger.info("内置MCP工具已注册: zkh_extract_price, zkh_verify_cart_status, zkh_wait_for_element, zkh_capture_network")

    @time_execution_sync('--act')
    async def act(
            self,
            action: ActionModel,
            browser_context: Optional[BrowserContext] = None,
            #
            page_extraction_llm: Optional[BaseChatModel] = None,
            sensitive_data: Optional[Dict[str, str]] = None,
            available_file_paths: Optional[list[str]] = None,
            #
            context: Context | None = None,
    ) -> ActionResult:
        """Execute an action"""

        try:
            for action_name, params in action.model_dump(exclude_unset=True).items():
                if params is not None:
                    if action_name.startswith("mcp"):
                        # this is a mcp tool
                        logger.debug(f"Invoke MCP tool: {action_name}")
                        mcp_tool = self.registry.registry.actions.get(action_name).function
                        result = await mcp_tool.ainvoke(params)
                    else:
                        result = await self.registry.execute_action(
                            action_name,
                            params,
                            browser=browser_context,
                            page_extraction_llm=page_extraction_llm,
                            sensitive_data=sensitive_data,
                            available_file_paths=available_file_paths,
                            context=context,
                        )

                    if isinstance(result, str):
                        return ActionResult(extracted_content=result)
                    elif isinstance(result, ActionResult):
                        return result
                    elif result is None:
                        return ActionResult()
                    else:
                        raise ValueError(f'Invalid action result type: {type(result)} of {result}')
            return ActionResult()
        except Exception as e:
            raise e

    async def setup_mcp_client(self, mcp_server_config: Optional[Dict[str, Any]] = None):
        self.mcp_server_config = mcp_server_config
        if self.mcp_server_config:
            self.mcp_client = await setup_mcp_client_and_tools(self.mcp_server_config)
            self.register_mcp_tools()

    def register_mcp_tools(self):
        """
        Register the MCP tools used by this controller.
        """
        if self.mcp_client:
            for server_name in self.mcp_client.server_name_to_tools:
                for tool in self.mcp_client.server_name_to_tools[server_name]:
                    tool_name = f"mcp.{server_name}.{tool.name}"
                    self.registry.registry.actions[tool_name] = RegisteredAction(
                        name=tool_name,
                        description=tool.description,
                        function=tool,
                        param_model=create_tool_param_model(tool),
                    )
                    logger.info(f"Add mcp tool: {tool_name}")
                logger.debug(
                    f"Registered {len(self.mcp_client.server_name_to_tools[server_name])} mcp tools for {server_name}")
        else:
            logger.warning(f"MCP client not started.")

    async def close_mcp_client(self):
        if self.mcp_client:
            await self.mcp_client.__aexit__(None, None, None)
