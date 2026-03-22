"""
MCP Browser Control Server
基于 MCP 协议的浏览器控制服务器

提供以下功能：
- 浏览器导航 (navigate)
- 元素点击 (click)
- 文本输入 (input)
- 页面截图 (screenshot)
- 获取页面信息 (get_page_info)
- 执行 JavaScript (execute_js)
"""

import asyncio
import json
import base64
from typing import Optional, Dict, Any, List
from contextlib import asynccontextmanager
from dataclasses import dataclass

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
from playwright.async_api import async_playwright, Page, Browser, BrowserContext


@dataclass
class BrowserState:
    """浏览器状态管理"""
    browser: Optional[Browser] = None
    context: Optional[BrowserContext] = None
    page: Optional[Page] = None
    is_initialized: bool = False


class MCPBrowserServer:
    """MCP 浏览器控制服务器"""
    
    def __init__(self):
        self.state = BrowserState()
        self.server = Server("browser-control-server")
        self._setup_handlers()
    
    def _setup_handlers(self):
        """设置 MCP 处理器"""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """列出所有可用工具"""
            return [
                Tool(
                    name="browser_launch",
                    description="启动浏览器实例",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "headless": {
                                "type": "boolean",
                                "description": "是否使用无头模式",
                                "default": False
                            },
                            "window_width": {
                                "type": "integer",
                                "description": "窗口宽度",
                                "default": 1280
                            },
                            "window_height": {
                                "type": "integer",
                                "description": "窗口高度",
                                "default": 720
                            }
                        }
                    }
                ),
                Tool(
                    name="browser_navigate",
                    description="导航到指定 URL",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "目标 URL"
                            },
                            "wait_until": {
                                "type": "string",
                                "description": "等待条件: load/domcontentloaded/networkidle",
                                "default": "networkidle"
                            }
                        },
                        "required": ["url"]
                    }
                ),
                Tool(
                    name="browser_click",
                    description="点击页面元素",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "selector": {
                                "type": "string",
                                "description": "CSS 选择器"
                            },
                            "timeout": {
                                "type": "integer",
                                "description": "超时时间(毫秒)",
                                "default": 5000
                            }
                        },
                        "required": ["selector"]
                    }
                ),
                Tool(
                    name="browser_input",
                    description="在输入框中输入文本",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "selector": {
                                "type": "string",
                                "description": "CSS 选择器"
                            },
                            "text": {
                                "type": "string",
                                "description": "要输入的文本"
                            },
                            "clear_first": {
                                "type": "boolean",
                                "description": "是否先清空输入框",
                                "default": True
                            }
                        },
                        "required": ["selector", "text"]
                    }
                ),
                Tool(
                    name="browser_screenshot",
                    description="截取页面截图",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "full_page": {
                                "type": "boolean",
                                "description": "是否截取全页面",
                                "default": False
                            },
                            "selector": {
                                "type": "string",
                                "description": "仅截取特定元素(可选)"
                            }
                        }
                    }
                ),
                Tool(
                    name="browser_get_content",
                    description="获取页面内容",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "selector": {
                                "type": "string",
                                "description": "CSS 选择器(可选,不传则返回整个页面文本)",
                                "default": "body"
                            }
                        }
                    }
                ),
                Tool(
                    name="browser_scroll",
                    description="滚动页面",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "direction": {
                                "type": "string",
                                "description": "滚动方向: up/down/left/right",
                                "enum": ["up", "down", "left", "right"]
                            },
                            "amount": {
                                "type": "integer",
                                "description": "滚动距离(像素)",
                                "default": 300
                            }
                        },
                        "required": ["direction"]
                    }
                ),
                Tool(
                    name="browser_execute_js",
                    description="执行 JavaScript 代码",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "script": {
                                "type": "string",
                                "description": "JavaScript 代码"
                            }
                        },
                        "required": ["script"]
                    }
                ),
                Tool(
                    name="browser_get_elements",
                    description="获取页面元素列表",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "selector": {
                                "type": "string",
                                "description": "CSS 选择器",
                                "default": "button, a, input"
                            }
                        }
                    }
                ),
                Tool(
                    name="browser_close",
                    description="关闭浏览器",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[Any]:
            """调用工具"""
            try:
                if name == "browser_launch":
                    return await self._handle_launch(arguments)
                elif name == "browser_navigate":
                    return await self._handle_navigate(arguments)
                elif name == "browser_click":
                    return await self._handle_click(arguments)
                elif name == "browser_input":
                    return await self._handle_input(arguments)
                elif name == "browser_screenshot":
                    return await self._handle_screenshot(arguments)
                elif name == "browser_get_content":
                    return await self._handle_get_content(arguments)
                elif name == "browser_scroll":
                    return await self._handle_scroll(arguments)
                elif name == "browser_execute_js":
                    return await self._handle_execute_js(arguments)
                elif name == "browser_get_elements":
                    return await self._handle_get_elements(arguments)
                elif name == "browser_close":
                    return await self._handle_close(arguments)
                else:
                    return [TextContent(type="text", text=f"未知工具: {name}")]
            except Exception as e:
                return [TextContent(type="text", text=f"错误: {str(e)}")]
    
    async def _ensure_initialized(self):
        """确保浏览器已初始化"""
        if not self.state.is_initialized:
            raise Exception("浏览器未启动,请先调用 browser_launch")
    
    async def _handle_launch(self, arguments: Dict[str, Any]) -> List[Any]:
        """处理浏览器启动"""
        headless = arguments.get("headless", False)
        width = arguments.get("window_width", 1280)
        height = arguments.get("window_height", 720)
        
        if self.state.browser:
            await self.state.browser.close()
        
        playwright = await async_playwright().start()
        self.state.browser = await playwright.chromium.launch(
            headless=headless,
            args=[f'--window-size={width},{height}']
        )
        self.state.context = await self.state.browser.new_context(
            viewport={"width": width, "height": height}
        )
        self.state.page = await self.state.context.new_page()
        self.state.is_initialized = True
        
        return [TextContent(
            type="text",
            text=f"✅ 浏览器已启动\n模式: {'无头' if headless else '有界面'}\n分辨率: {width}x{height}"
        )]
    
    async def _handle_navigate(self, arguments: Dict[str, Any]) -> List[Any]:
        """处理页面导航"""
        await self._ensure_initialized()
        
        url = arguments["url"]
        wait_until = arguments.get("wait_until", "networkidle")
        
        await self.state.page.goto(url, wait_until=wait_until)
        
        return [TextContent(
            type="text",
            text=f"✅ 已导航到: {url}\n标题: {await self.state.page.title()}\nURL: {self.state.page.url}"
        )]
    
    async def _handle_click(self, arguments: Dict[str, Any]) -> List[Any]:
        """处理元素点击"""
        await self._ensure_initialized()
        
        selector = arguments["selector"]
        timeout = arguments.get("timeout", 5000)
        
        await self.state.page.click(selector, timeout=timeout)
        
        return [TextContent(
            type="text",
            text=f"✅ 已点击元素: {selector}"
        )]
    
    async def _handle_input(self, arguments: Dict[str, Any]) -> List[Any]:
        """处理文本输入"""
        await self._ensure_initialized()
        
        selector = arguments["selector"]
        text = arguments["text"]
        clear_first = arguments.get("clear_first", True)
        
        if clear_first:
            await self.state.page.fill(selector, "")
        
        await self.state.page.fill(selector, text)
        
        return [TextContent(
            type="text",
            text=f"✅ 已在 {selector} 输入: {text[:50]}{'...' if len(text) > 50 else ''}"
        )]
    
    async def _handle_screenshot(self, arguments: Dict[str, Any]) -> List[Any]:
        """处理截图"""
        await self._ensure_initialized()
        
        full_page = arguments.get("full_page", False)
        selector = arguments.get("selector")
        
        screenshot_options = {
            "full_page": full_page,
            "type": "png"
        }
        
        if selector:
            element = await self.state.page.query_selector(selector)
            if not element:
                return [TextContent(type="text", text=f"❌ 未找到元素: {selector}")]
            screenshot = await element.screenshot()
        else:
            screenshot = await self.state.page.screenshot(**screenshot_options)
        
        # 返回 Base64 编码的图片
        base64_image = base64.b64encode(screenshot).decode('utf-8')
        
        return [
            TextContent(type="text", text=f"✅ 截图成功 ({'全页面' if full_page else '视口'}{f' 元素: {selector}' if selector else ''})"),
            ImageContent(type="image", data=base64_image, mimeType="image/png")
        ]
    
    async def _handle_get_content(self, arguments: Dict[str, Any]) -> List[Any]:
        """处理获取页面内容"""
        await self._ensure_initialized()
        
        selector = arguments.get("selector", "body")
        
        element = await self.state.page.query_selector(selector)
        if not element:
            return [TextContent(type="text", text=f"❌ 未找到元素: {selector}")]
        
        text = await element.inner_text()
        
        # 截断过长的内容
        max_length = 5000
        if len(text) > max_length:
            text = text[:max_length] + f"\n\n... (已截断,共 {len(text)} 字符)"
        
        return [TextContent(
            type="text",
            text=f"✅ 获取内容 ({selector}):\n\n{text}"
        )]
    
    async def _handle_scroll(self, arguments: Dict[str, Any]) -> List[Any]:
        """处理页面滚动"""
        await self._ensure_initialized()
        
        direction = arguments["direction"]
        amount = arguments.get("amount", 300)
        
        direction_map = {
            "up": (0, -amount),
            "down": (0, amount),
            "left": (-amount, 0),
            "right": (amount, 0)
        }
        
        dx, dy = direction_map.get(direction, (0, amount))
        
        await self.state.page.evaluate(f"window.scrollBy({dx}, {dy})")
        
        # 获取当前滚动位置
        scroll_info = await self.state.page.evaluate("""
            () => ({
                x: window.pageXOffset,
                y: window.pageYOffset,
                height: document.documentElement.scrollHeight
            })
        """)
        
        return [TextContent(
            type="text",
            text=f"✅ 已向 {direction} 滚动 {amount}px\n当前位置: ({scroll_info['x']}, {scroll_info['y']}) / 总高度: {scroll_info['height']}"
        )]
    
    async def _handle_execute_js(self, arguments: Dict[str, Any]) -> List[Any]:
        """处理执行 JavaScript"""
        await self._ensure_initialized()
        
        script = arguments["script"]
        
        result = await self.state.page.evaluate(script)
        
        result_str = json.dumps(result, ensure_ascii=False, indent=2) if result is not None else "undefined"
        
        return [TextContent(
            type="text",
            text=f"✅ JavaScript 执行结果:\n```json\n{result_str}\n```"
        )]
    
    async def _handle_get_elements(self, arguments: Dict[str, Any]) -> List[Any]:
        """处理获取元素列表"""
        await self._ensure_initialized()
        
        selector = arguments.get("selector", "button, a, input")
        
        elements = await self.state.page.query_selector_all(selector)
        
        element_list = []
        for i, element in enumerate(elements[:20]):  # 最多返回20个
            try:
                tag = await element.evaluate("el => el.tagName")
                text = await element.inner_text()
                element_type = await element.get_attribute("type") or ""
                placeholder = await element.get_attribute("placeholder") or ""
                href = await element.get_attribute("href") or ""
                
                info = f"[{i+1}] <{tag.lower()}>"
                if text.strip():
                    info += f" 文本: '{text.strip()[:30]}'"
                if element_type:
                    info += f" 类型: {element_type}"
                if placeholder:
                    info += f" 提示: {placeholder}"
                if href:
                    info += f" 链接: {href[:50]}"
                
                element_list.append(info)
            except:
                continue
        
        return [TextContent(
            type="text",
            text=f"✅ 找到 {len(elements)} 个元素 (显示前 {len(element_list)} 个):\n\n" + "\n".join(element_list)
        )]
    
    async def _handle_close(self, arguments: Dict[str, Any]) -> List[Any]:
        """处理关闭浏览器"""
        if self.state.browser:
            await self.state.browser.close()
            self.state = BrowserState()
        
        return [TextContent(
            type="text",
            text="✅ 浏览器已关闭"
        )]
    
    async def run(self):
        """运行 MCP 服务器"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """主入口"""
    server = MCPBrowserServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
