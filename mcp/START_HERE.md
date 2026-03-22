# 🚀 MCP Browser Control - 从这里开始

## 什么是 MCP？一句话解释

**MCP (Model Context Protocol)** 是让 AI 能统一、标准化地控制外部工具（如浏览器）的协议。就像 USB 让各种设备能统一连接到电脑一样。

---

## 📂 文件说明

| 文件 | 用途 | 阅读顺序 |
|-----|------|---------|
| `README.md` | 完整概念介绍 | ⭐ 第1个读 |
| `ARCHITECTURE.md` | 架构详解和流程图 | 第2个读 |
| `server.py` | MCP 服务器实现 | 查看代码 |
| `client_example.py` | 客户端使用示例 | 查看代码 |
| `webui_integration_example.py` | Gradio 集成示例 | 查看代码 |
| `quickstart.py` | 一键测试脚本 | 直接运行 |
| `config.json` | MCP 配置文件 | 参考 |
| `requirements.txt` | Python 依赖 | 安装用 |

---

## 🎯 5 分钟快速上手

### 1. 安装依赖 (1分钟)

```bash
cd /Users/zhangdonghao/Documents/mycode/zkhAI/web-ui-auto
source .venv/bin/activate
pip install mcp playwright
playwright install chromium
```

### 2. 运行快速测试 (2分钟)

```bash
python mcp/quickstart.py
```

你会看到: ✅ 所有测试通过!

### 3. 运行交互式客户端 (2分钟)

```bash
python mcp/client_example.py --interactive
```

输入命令体验:
```
> launch
> navigate https://example.com
> screenshot
> close
> quit
```

### 4. 启动 WebUI 演示 (可选)

```bash
python mcp/webui_integration_example.py
```

打开浏览器访问: http://127.0.0.1:8888

---

## 🧠 核心概念速记

```
┌─────────────────────────────────────────┐
│              MCP 核心                    │
├─────────────────────────────────────────┤
│                                          │
│  Client (客户端)   ◄──────►   Server (服务端)
│      │                           │      │
│      │ 1. 请求: "导航到xxx"       │      │
│      │ ────────────────────────► │      │
│      │                           │      │
│      │ 2. 执行: 调用 Playwright  │      │
│      │                           │      │
│      │ 3. 响应: "已完成"          │      │
│      │ ◄──────────────────────── │      │
│      │                           │      │
│      └───────────────────────────┘      │
│                                          │
│  通信协议: JSON-RPC over stdio          │
│                                          │
└─────────────────────────────────────────┘
```

---

## 🔧 可用工具列表

| 工具名 | 功能 | 示例 |
|-------|------|------|
| `browser_launch` | 启动浏览器 | `launch headless=false` |
| `browser_navigate` | 导航到 URL | `navigate https://google.com` |
| `browser_click` | 点击元素 | `click button#submit` |
| `browser_input` | 输入文本 | `input input#search "hello"` |
| `browser_screenshot` | 截图 | `screenshot full_page=true` |
| `browser_get_content` | 获取页面内容 | `content selector=body` |
| `browser_scroll` | 滚动页面 | `scroll down amount=500` |
| `browser_execute_js` | 执行 JS | `js "() => document.title"` |
| `browser_get_elements` | 获取元素列表 | `elements button, a` |
| `browser_close` | 关闭浏览器 | `close` |

---

## 📝 代码示例

### 基础使用

```python
import asyncio
from mcp.client_example import MCPBrowserClient

async def main():
    client = MCPBrowserClient()
    
    # 连接
    await client.connect()
    
    # 启动浏览器
    await client.call_tool("browser_launch", {"headless": False})
    
    # 导航
    await client.call_tool("browser_navigate", {"url": "https://example.com"})
    
    # 截图
    await client.call_tool("browser_screenshot", {"full_page": True})
    
    # 关闭
    await client.call_tool("browser_close", {})
    await client.disconnect()

asyncio.run(main())
```

### 集成到现有项目

```python
# 在你的 WebUI 代码中
from mcp.webui_integration_example import MCPWebUIIntegration

integration = MCPWebUIIntegration()
await integration.initialize()

# 使用 MCP 控制浏览器
result = await integration.navigate("https://example.com")
```

---

## 🔗 与主项目的关系

```
web-ui-auto/                    # 主项目
├── webui.py                    # 主入口 (不受影响)
├── src/                        # 源代码 (不受影响)
│   ├── agent/
│   ├── browser/
│   └── controller/
├── mcp/                        # ✅ MCP 项目 (新增,独立)
│   ├── server.py
│   ├── client_example.py
│   └── ...
└── ...
```

**重要**: mcp/ 目录完全独立，不影响现有代码运行！

---

## 📚 学习路径

1. **理解概念** → 阅读 `README.md`
2. **了解架构** → 阅读 `ARCHITECTURE.md`
3. **动手实践** → 运行 `quickstart.py`
4. **深入代码** → 查看 `server.py` 和 `client_example.py`
5. **集成应用** → 参考 `webui_integration_example.py`

---

## ❓ 常见问题

**Q: 这个和主项目的 browser_use 有什么区别？**

A: 
- 主项目: 完整的 AI Agent 系统，包含任务规划、LLM 交互等
- MCP 项目: 标准化的浏览器控制协议，可以被任何 MCP Client 使用

**Q: 为什么要用 MCP？**

A: 
- 标准化: 不同 AI 模型/工具可以用统一方式控制浏览器
- 可扩展: 容易添加新的工具
- 可复用: 浏览器控制逻辑可以被多个项目共用

**Q: 如何在 Claude/Cursor 中使用？**

A: 配置 `config.json`:
```json
{
  "mcpServers": {
    "browser": {
      "command": "python",
      "args": ["/Users/zhangdonghao/Documents/mycode/zkhAI/web-ui-auto/mcp/server.py"]
    }
  }
}
```

然后在 Claude Desktop 或 Cursor 的 MCP 设置中加载此配置。

---

## 🎉 下一步

1. 运行 `python mcp/quickstart.py` 体验效果
2. 阅读 `mcp/README.md` 深入理解原理
3. 尝试修改 `server.py` 添加自定义工具
4. 在自己的项目中集成 MCP Client

有问题？查看代码注释或搜索 MCP 官方文档！
