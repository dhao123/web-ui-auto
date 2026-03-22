"""
MCP 与 WebUI 集成示例
展示如何在现有的 WebUI 项目中集成 MCP 功能

注意：这是一个独立示例，不影响现有代码
"""

import asyncio
import gradio as gr
from typing import Optional, List, Dict, Any
from contextlib import AsyncExitStack
import base64
from io import BytesIO

# 导入 MCP
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPWebUIIntegration:
    """
    MCP WebUI 集成类
    
    这是一个示例，展示如何将 MCP 浏览器控制集成到 Gradio 界面中
    可以作为未来扩展功能的参考
    """
    
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack: Optional[AsyncExitStack] = None
        self.is_connected = False
        self.history: List[Dict[str, Any]] = []
    
    async def initialize(self):
        """初始化 MCP 客户端"""
        try:
            # 配置服务器参数
            server_params = StdioServerParameters(
                command="python",
                args=["mcp/server.py"],
                env=None
            )
            
            # 创建 exit stack
            self.exit_stack = AsyncExitStack()
            
            # 建立连接
            stdio_transport = await self.exit_stack.enter_async_context(
                stdio_client(server_params)
            )
            read_stream, write_stream = stdio_transport
            
            # 创建会话
            self.session = await self.exit_stack.enter_async_context(
                ClientSession(read_stream, write_stream)
            )
            
            # 初始化
            await self.session.initialize()
            self.is_connected = True
            
            return "✅ MCP 客户端已连接"
        except Exception as e:
            return f"❌ 连接失败: {str(e)}"
    
    async def cleanup(self):
        """清理资源"""
        if self.exit_stack:
            await self.exit_stack.aclose()
            self.exit_stack = None
            self.session = None
        self.is_connected = False
        return "✅ MCP 客户端已断开"
    
    async def _call_tool(self, name: str, arguments: dict):
        """内部调用工具的方法"""
        if not self.is_connected or not self.session:
            raise Exception("MCP 客户端未连接")
        return await self.session.call_tool(name, arguments)
    
    async def launch_browser(self, headless: bool = False, width: int = 1280, height: int = 720):
        """启动浏览器"""
        if not self.is_connected:
            return "❌ 请先初始化 MCP 客户端"
        
        try:
            result = await self._call_tool("browser_launch", {
                "headless": headless,
                "window_width": width,
                "window_height": height
            })
            self._add_to_history("launch", {"headless": headless, "width": width, "height": height})
            return self._format_result(result)
        except Exception as e:
            return f"❌ 错误: {str(e)}"
    
    async def navigate(self, url: str):
        """导航到 URL"""
        if not self.is_connected:
            return "❌ 请先初始化 MCP 客户端"
        
        try:
            result = await self._call_tool("browser_navigate", {"url": url})
            self._add_to_history("navigate", {"url": url})
            return self._format_result(result)
        except Exception as e:
            return f"❌ 错误: {str(e)}"
    
    async def click(self, selector: str):
        """点击元素"""
        try:
            result = await self._call_tool("browser_click", {"selector": selector})
            self._add_to_history("click", {"selector": selector})
            return self._format_result(result)
        except Exception as e:
            return f"❌ 错误: {str(e)}"
    
    async def input_text(self, selector: str, text: str):
        """输入文本"""
        try:
            result = await self._call_tool("browser_input", {
                "selector": selector,
                "text": text,
                "clear_first": True
            })
            self._add_to_history("input", {"selector": selector, "text": text})
            return self._format_result(result)
        except Exception as e:
            return f"❌ 错误: {str(e)}"
    
    async def take_screenshot(self, full_page: bool = False) -> tuple:
        """
        截图
        返回: (文本结果, 图片数据)
        """
        if not self.is_connected:
            return "❌ 请先初始化 MCP 客户端", None
        
        try:
            result = await self._call_tool("browser_screenshot", {"full_page": full_page})
            
            text_output = ""
            image_data = None
            
            for content in result.content:
                if content.type == "text":
                    text_output += content.text + "\n"
                elif content.type == "image":
                    # 将 base64 转换为图片
                    image_bytes = base64.b64decode(content.data)
                    image_data = BytesIO(image_bytes)
            
            self._add_to_history("screenshot", {"full_page": full_page})
            return text_output, image_data
        except Exception as e:
            return f"❌ 错误: {str(e)}", None
    
    async def get_page_content(self, selector: str = "body"):
        """获取页面内容"""
        try:
            result = await self._call_tool("browser_get_content", {"selector": selector})
            return self._format_result(result)
        except Exception as e:
            return f"❌ 错误: {str(e)}"
    
    async def execute_js(self, script: str):
        """执行 JavaScript"""
        try:
            result = await self._call_tool("browser_execute_js", {"script": script})
            return self._format_result(result)
        except Exception as e:
            return f"❌ 错误: {str(e)}"
    
    async def get_elements(self, selector: str = "button, a, input"):
        """获取元素列表"""
        try:
            result = await self._call_tool("browser_get_elements", {"selector": selector})
            return self._format_result(result)
        except Exception as e:
            return f"❌ 错误: {str(e)}"
    
    async def scroll(self, direction: str, amount: int = 300):
        """滚动页面"""
        try:
            result = await self._call_tool("browser_scroll", {
                "direction": direction,
                "amount": amount
            })
            self._add_to_history("scroll", {"direction": direction, "amount": amount})
            return self._format_result(result)
        except Exception as e:
            return f"❌ 错误: {str(e)}"
    
    async def close_browser(self):
        """关闭浏览器"""
        try:
            result = await self._call_tool("browser_close", {})
            self._add_to_history("close", {})
            return self._format_result(result)
        except Exception as e:
            return f"❌ 错误: {str(e)}"
    
    def _format_result(self, result) -> str:
        """格式化结果"""
        output = []
        for content in result.content:
            if content.type == "text":
                output.append(content.text)
        return "\n".join(output)
    
    def _add_to_history(self, action: str, params: dict):
        """添加到历史记录"""
        import time
        self.history.append({
            "action": action,
            "params": params,
            "timestamp": time.time()
        })
    
    def get_history(self) -> str:
        """获取操作历史"""
        if not self.history:
            return "暂无操作记录"
        
        lines = ["📜 操作历史:", "=" * 60]
        for i, record in enumerate(self.history, 1):
            params_str = ", ".join([f"{k}={v}" for k, v in record["params"].items()])
            lines.append(f"{i}. {record['action']}({params_str})")
        return "\n".join(lines)


def create_mcp_demo_ui():
    """
    创建 MCP 演示界面
    
    这是一个独立的 Gradio 界面，演示 MCP 功能
    """
    integration = MCPWebUIIntegration()
    
    with gr.Blocks(title="MCP Browser Control Demo") as demo:
        gr.Markdown("""
        # 🌐 MCP Browser Control Demo
        
        基于 **Model Context Protocol** 的浏览器自动化控制演示
        
        **注意**: 这是一个独立示例，不影响主项目的 webui.py
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                # 连接控制
                gr.Markdown("### 🔌 连接控制")
                connect_btn = gr.Button("连接 MCP 服务器", variant="primary")
                disconnect_btn = gr.Button("断开连接", variant="secondary")
                connection_status = gr.Textbox(label="连接状态", value="未连接", interactive=False)
                
                # 浏览器控制
                gr.Markdown("### 🚀 浏览器控制")
                headless_check = gr.Checkbox(label="无头模式", value=False)
                width_slider = gr.Slider(label="窗口宽度", minimum=800, maximum=1920, value=1280, step=10)
                height_slider = gr.Slider(label="窗口高度", minimum=600, maximum=1080, value=720, step=10)
                launch_btn = gr.Button("启动浏览器", variant="primary")
                close_btn = gr.Button("关闭浏览器")
                
                # 导航控制
                gr.Markdown("### 🧭 导航控制")
                url_input = gr.Textbox(label="URL", placeholder="https://example.com", value="https://example.com")
                navigate_btn = gr.Button("导航", variant="primary")
                
                # 元素交互
                gr.Markdown("### 🖱️ 元素交互")
                selector_input = gr.Textbox(label="CSS 选择器", placeholder="button, input, #id, .class")
                text_input = gr.Textbox(label="输入文本", placeholder="要输入的文本")
                
                with gr.Row():
                    click_btn = gr.Button("点击")
                    input_btn = gr.Button("输入文本")
                
                # 页面操作
                gr.Markdown("### 📄 页面操作")
                with gr.Row():
                    screenshot_btn = gr.Button("📸 截图")
                    content_btn = gr.Button("📝 获取内容")
                    elements_btn = gr.Button("🔍 获取元素")
                
                full_page_check = gr.Checkbox(label="全页面截图", value=False)
                
                # 滚动
                gr.Markdown("### ⬆️⬇️ 滚动")
                with gr.Row():
                    scroll_up_btn = gr.Button("⬆️ 向上滚动")
                    scroll_down_btn = gr.Button("⬇️ 向下滚动")
                scroll_amount = gr.Slider(label="滚动距离", minimum=100, maximum=1000, value=300, step=50)
                
                # JavaScript
                gr.Markdown("### ⚡ JavaScript 执行")
                js_code = gr.Textbox(
                    label="JavaScript 代码",
                    placeholder="() => document.title",
                    lines=3
                )
                execute_js_btn = gr.Button("执行", variant="primary")
            
            with gr.Column(scale=2):
                # 输出区域
                gr.Markdown("### 📤 操作输出")
                output_text = gr.Textbox(label="输出", lines=15, max_lines=20)
                screenshot_output = gr.Image(label="截图预览", type="pil")
                
                # 历史记录
                gr.Markdown("### 📜 历史记录")
                history_text = gr.Textbox(label="操作历史", lines=5, interactive=False)
                refresh_history_btn = gr.Button("🔄 刷新历史")
        
        # 事件处理
        async def on_connect():
            result = await integration.initialize()
            return result
        
        async def on_disconnect():
            result = await integration.cleanup()
            return "未连接"
        
        async def on_launch(headless, width, height):
            return await integration.launch_browser(headless, width, height)
        
        async def on_navigate(url):
            return await integration.navigate(url)
        
        async def on_click(selector):
            return await integration.click(selector)
        
        async def on_input(selector, text):
            return await integration.input_text(selector, text)
        
        async def on_screenshot(full_page):
            text, image = await integration.take_screenshot(full_page)
            return text, image
        
        async def on_get_content():
            return await integration.get_page_content()
        
        async def on_get_elements():
            return await integration.get_elements()
        
        async def on_scroll(direction, amount):
            return await integration.scroll(direction, amount)
        
        async def on_execute_js(code):
            return await integration.execute_js(code)
        
        async def on_close():
            return await integration.close_browser()
        
        def on_refresh_history():
            return integration.get_history()
        
        # 绑定事件
        connect_btn.click(on_connect, outputs=connection_status)
        disconnect_btn.click(on_disconnect, outputs=connection_status)
        launch_btn.click(on_launch, inputs=[headless_check, width_slider, height_slider], outputs=output_text)
        navigate_btn.click(on_navigate, inputs=url_input, outputs=output_text)
        click_btn.click(on_click, inputs=selector_input, outputs=output_text)
        input_btn.click(on_input, inputs=[selector_input, text_input], outputs=output_text)
        screenshot_btn.click(on_screenshot, inputs=full_page_check, outputs=[output_text, screenshot_output])
        content_btn.click(on_get_content, outputs=output_text)
        elements_btn.click(on_get_elements, outputs=output_text)
        scroll_up_btn.click(lambda amt: on_scroll("up", amt), inputs=scroll_amount, outputs=output_text)
        scroll_down_btn.click(lambda amt: on_scroll("down", amt), inputs=scroll_amount, outputs=output_text)
        execute_js_btn.click(on_execute_js, inputs=js_code, outputs=output_text)
        close_btn.click(on_close, outputs=output_text)
        refresh_history_btn.click(on_refresh_history, outputs=history_text)
    
    return demo


if __name__ == "__main__":
    print("🚀 MCP WebUI 集成示例")
    print("=" * 60)
    print("这是一个演示如何在 Gradio 中集成 MCP 的示例")
    print("启动后将打开一个新的 Web 界面")
    print("=" * 60)
    
    demo = create_mcp_demo_ui()
    demo.launch(server_name="127.0.0.1", server_port=8888, share=False)
