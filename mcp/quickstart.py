#!/usr/bin/env python3
"""
MCP Browser Control - Quick Start
快速开始脚本

一键测试 MCP 浏览器控制功能
"""

import asyncio
import sys


async def quick_test():
    """快速测试"""
    print("🚀 MCP Browser Control 快速测试")
    print("=" * 60)
    
    try:
        # 尝试相对导入（从 mcp 目录内运行）
        from client_example import MCPBrowserClient
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保已安装依赖: pip install -r mcp/requirements.txt")
        return
    
    client = MCPBrowserClient()
    
    try:
        # 1. 连接
        print("\n1️⃣ 连接到 MCP 服务器...")
        await client.connect()
        
        # 2. 启动浏览器
        print("\n2️⃣ 启动浏览器...")
        await client.call_tool("browser_launch", {
            "headless": True,  # 无头模式，适合测试
            "window_width": 1280,
            "window_height": 720
        })
        
        # 3. 导航
        print("\n3️⃣ 导航到 example.com...")
        await client.call_tool("browser_navigate", {
            "url": "https://example.com"
        })
        
        # 4. 获取内容
        print("\n4️⃣ 获取页面内容...")
        await client.call_tool("browser_get_content", {
            "selector": "body"
        })
        
        # 5. 截图
        print("\n5️⃣ 截图...")
        await client.call_tool("browser_screenshot", {
            "full_page": False
        })
        
        # 6. 执行 JavaScript
        print("\n6️⃣ 执行 JavaScript...")
        await client.call_tool("browser_execute_js", {
            "script": "() => ({ title: document.title, url: window.location.href })"
        })
        
        # 7. 关闭浏览器
        print("\n7️⃣ 关闭浏览器...")
        await client.call_tool("browser_close", {})
        
        print("\n" + "=" * 60)
        print("✅ 所有测试通过！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await client.disconnect()


def print_usage():
    """打印使用说明"""
    print("""
🌐 MCP Browser Control - 使用说明
====================================

📁 项目结构:
    mcp/
    ├── README.md              # 完整文档
    ├── server.py              # MCP 服务器
    ├── client_example.py      # 客户端示例
    ├── webui_integration_example.py  # WebUI 集成
    ├── quickstart.py          # 本文件
    ├── config.json            # 配置文件
    └── requirements.txt       # 依赖列表

🚀 快速开始:

    1. 安装依赖:
       pip install -r mcp/requirements.txt
       playwright install chromium

    2. 运行快速测试:
       python mcp/quickstart.py

    3. 运行客户端示例 (自动演示):
       python mcp/client_example.py

    4. 交互式模式:
       python mcp/client_example.py --interactive

    5. 启动 WebUI 演示:
       python mcp/webui_integration_example.py

🔧 可用工具:

    • browser_launch          - 启动浏览器
    • browser_navigate        - 页面导航
    • browser_click           - 点击元素
    • browser_input           - 输入文本
    • browser_screenshot      - 截图
    • browser_get_content     - 获取页面内容
    • browser_scroll          - 滚动页面
    • browser_execute_js      - 执行 JavaScript
    • browser_get_elements    - 获取元素列表
    • browser_close           - 关闭浏览器

📚 了解更多:
    请查看 mcp/README.md 获取完整文档
""")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help", "help"]:
        print_usage()
    else:
        asyncio.run(quick_test())
