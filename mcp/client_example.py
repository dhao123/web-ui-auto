"""
MCP Browser Client Example
MCP 浏览器控制客户端示例

演示如何使用 MCP 协议与浏览器服务器通信
"""

import asyncio
import json
from typing import Optional
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPBrowserClient:
    """MCP 浏览器客户端"""
    
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack: Optional[AsyncExitStack] = None
    
    async def connect(self):
        """连接到 MCP 服务器"""
        # 配置服务器参数
        server_params = StdioServerParameters(
            command="python",
            args=["mcp/server.py"],
            env=None
        )
        
        # 创建 exit stack 来管理多个上下文
        self.exit_stack = AsyncExitStack()
        
        # 建立连接 - 使用 exit_stack 来管理 stdio_client 的生命周期
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        read_stream, write_stream = stdio_transport
        
        # 创建会话 - 同样使用 exit_stack
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )
        
        # 初始化
        await self.session.initialize()
        
        print("✅ 已连接到 MCP 浏览器服务器")
    
    async def disconnect(self):
        """断开连接"""
        if self.exit_stack:
            await self.exit_stack.aclose()
            self.exit_stack = None
            self.session = None
        print("✅ 已断开连接")
    
    async def list_tools(self):
        """列出可用工具"""
        tools = await self.session.list_tools()
        print("\n📋 可用工具列表:")
        print("=" * 60)
        for tool in tools.tools:
            print(f"\n🔧 {tool.name}")
            print(f"   描述: {tool.description}")
            print(f"   参数: {json.dumps(tool.inputSchema, indent=2, ensure_ascii=False)}")
        print("=" * 60)
        return tools
    
    async def call_tool(self, name: str, arguments: dict):
        """调用工具"""
        print(f"\n▶️ 调用工具: {name}")
        print(f"   参数: {json.dumps(arguments, ensure_ascii=False)}")
        
        result = await self.session.call_tool(name, arguments)
        
        # 处理结果
        for content in result.content:
            if content.type == "text":
                print(f"   结果: {content.text}")
            elif content.type == "image":
                print(f"   结果: [图片数据, Base64 长度: {len(content.data)}]")
                # 保存截图
                import base64
                with open("screenshot.png", "wb") as f:
                    f.write(base64.b64decode(content.data))
                print(f"   💾 截图已保存到 screenshot.png")
        
        return result
    
    async def demo_scenario_1_basic_navigation(self):
        """演示场景1: 基本导航"""
        print("\n" + "=" * 60)
        print("🎬 演示场景 1: 基本导航")
        print("=" * 60)
        
        # 1. 启动浏览器
        await self.call_tool("browser_launch", {
            "headless": False,
            "window_width": 1280,
            "window_height": 720
        })
        
        # 2. 导航到示例网站
        await self.call_tool("browser_navigate", {
            "url": "https://example.com",
            "wait_until": "networkidle"
        })
        
        # 3. 获取页面内容
        await self.call_tool("browser_get_content", {
            "selector": "body"
        })
        
        # 4. 截图
        await self.call_tool("browser_screenshot", {
            "full_page": True
        })
    
    async def demo_scenario_2_form_interaction(self):
        """演示场景2: 表单交互"""
        print("\n" + "=" * 60)
        print("🎬 演示场景 2: 表单交互")
        print("=" * 60)
        
        # 导航到测试页面
        await self.call_tool("browser_navigate", {
            "url": "https://httpbin.org/forms/post",
            "wait_until": "networkidle"
        })
        
        # 获取页面元素
        await self.call_tool("browser_get_elements", {
            "selector": "input, textarea, button"
        })
        
        # 输入文本 (如果找到输入框)
        try:
            await self.call_tool("browser_input", {
                "selector": "input[name='custname']",
                "text": "张三",
                "clear_first": True
            })
        except Exception as e:
            print(f"   输入失败(可能页面结构不同): {e}")
        
        # 截图
        await self.call_tool("browser_screenshot", {
            "full_page": False
        })
    
    async def demo_scenario_3_javascript_execution(self):
        """演示场景3: JavaScript 执行"""
        print("\n" + "=" * 60)
        print("🎬 演示场景 3: JavaScript 执行")
        print("=" * 60)
        
        # 导航到网站
        await self.call_tool("browser_navigate", {
            "url": "https://example.com"
        })
        
        # 执行 JavaScript 获取页面信息
        await self.call_tool("browser_execute_js", {
            "script": """
                () => ({
                    title: document.title,
                    url: window.location.href,
                    userAgent: navigator.userAgent,
                    viewport: {
                        width: window.innerWidth,
                        height: window.innerHeight
                    },
                    links: Array.from(document.querySelectorAll('a')).map(a => ({
                        text: a.textContent.trim(),
                        href: a.href
                    })).slice(0, 5)
                })
            """
        })
        
        # 滚动页面
        await self.call_tool("browser_scroll", {
            "direction": "down",
            "amount": 500
        })
    
    async def demo_scenario_4_search_workflow(self):
        """演示场景4: 搜索工作流"""
        print("\n" + "=" * 60)
        print("🎬 演示场景 4: 搜索工作流")
        print("=" * 60)
        
        # 导航到搜索引擎
        await self.call_tool("browser_navigate", {
            "url": "https://www.bing.com",
            "wait_until": "networkidle"
        })
        
        # 获取搜索框
        await self.call_tool("browser_get_elements", {
            "selector": "input[type='search'], textarea, input[name='q']"
        })
        
        # 尝试在搜索框输入 (选择器可能需要根据实际情况调整)
        try:
            await self.call_tool("browser_input", {
                "selector": "textarea[name='q']",
                "text": "Model Context Protocol"
            })
            
            # 截图
            await self.call_tool("browser_screenshot", {
                "full_page": False
            })
            
        except Exception as e:
            print(f"   搜索输入失败: {e}")
            print("   💡 提示: 实际使用时需要根据页面结构调整选择器")
    
    async def run_all_demos(self):
        """运行所有演示"""
        try:
            await self.connect()
            
            # 列出可用工具
            await self.list_tools()
            
            # 运行演示场景
            await self.demo_scenario_1_basic_navigation()
            await self.demo_scenario_2_form_interaction()
            await self.demo_scenario_3_javascript_execution()
            await self.demo_scenario_4_search_workflow()
            
            # 关闭浏览器
            await self.call_tool("browser_close", {})
            
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await self.disconnect()


async def interactive_mode():
    """交互式模式"""
    client = MCPBrowserClient()
    
    try:
        await client.connect()
        await client.list_tools()
        
        print("\n" + "=" * 60)
        print("🎮 交互式模式")
        print("=" * 60)
        print("可用命令:")
        print("  launch [headless=true/false] - 启动浏览器")
        print("  navigate <url>               - 导航到 URL")
        print("  click <selector>             - 点击元素")
        print("  input <selector> <text>      - 输入文本")
        print("  screenshot [full]            - 截图")
        print("  content [selector]           - 获取内容")
        print("  scroll <up/down> [amount]    - 滚动页面")
        print("  js <code>                    - 执行 JS")
        print("  elements [selector]          - 获取元素列表")
        print("  close                        - 关闭浏览器")
        print("  quit                         - 退出")
        print("=" * 60)
        
        while True:
            try:
                command = input("\n> ").strip()
                if not command:
                    continue
                
                parts = command.split()
                cmd = parts[0].lower()
                
                if cmd == "quit":
                    break
                elif cmd == "launch":
                    headless = "true" in command or "false" not in command
                    await client.call_tool("browser_launch", {"headless": headless})
                elif cmd == "navigate":
                    if len(parts) < 2:
                        print("用法: navigate <url>")
                        continue
                    await client.call_tool("browser_navigate", {"url": parts[1]})
                elif cmd == "click":
                    if len(parts) < 2:
                        print("用法: click <selector>")
                        continue
                    await client.call_tool("browser_click", {"selector": parts[1]})
                elif cmd == "input":
                    if len(parts) < 3:
                        print("用法: input <selector> <text>")
                        continue
                    await client.call_tool("browser_input", {
                        "selector": parts[1],
                        "text": " ".join(parts[2:])
                    })
                elif cmd == "screenshot":
                    await client.call_tool("browser_screenshot", {
                        "full_page": "full" in command
                    })
                elif cmd == "content":
                    selector = parts[1] if len(parts) > 1 else "body"
                    await client.call_tool("browser_get_content", {"selector": selector})
                elif cmd == "scroll":
                    if len(parts) < 2:
                        print("用法: scroll <up/down> [amount]")
                        continue
                    await client.call_tool("browser_scroll", {
                        "direction": parts[1],
                        "amount": int(parts[2]) if len(parts) > 2 else 300
                    })
                elif cmd == "js":
                    if len(parts) < 2:
                        print("用法: js <code>")
                        continue
                    await client.call_tool("browser_execute_js", {
                        "script": " ".join(parts[1:])
                    })
                elif cmd == "elements":
                    selector = parts[1] if len(parts) > 1 else "button, a, input"
                    await client.call_tool("browser_get_elements", {"selector": selector})
                elif cmd == "close":
                    await client.call_tool("browser_close", {})
                else:
                    print(f"未知命令: {cmd}")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"错误: {e}")
    
    finally:
        await client.disconnect()


async def main():
    """主入口"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        await interactive_mode()
    else:
        print("🚀 MCP 浏览器客户端示例")
        print("运行方式:")
        print("  1. 自动演示模式: python mcp/client_example.py")
        print("  2. 交互式模式:   python mcp/client_example.py --interactive")
        print()
        
        # 运行自动演示
        client = MCPBrowserClient()
        await client.run_all_demos()


if __name__ == "__main__":
    asyncio.run(main())
