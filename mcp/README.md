# MCP (Model Context Protocol) 完全指南

## 什么是 MCP？

**MCP (Model Context Protocol)** 是由 Anthropic 推出的开放协议，用于标准化 AI 模型与外部工具、数据源之间的交互方式。

### 简单理解

```
传统方式 (混乱的集成):
┌─────────┐     ┌─────────────┐     ┌─────────┐
│   LLM   │◄───►│  Tool A API │◄───►│ 数据/服务 │
│         │     ├─────────────┤     └─────────┘
│         │     │  Tool B SDK │◄───►┌─────────┐
│         │◄───►├─────────────┤◄───►│ 数据/服务 │
│         │     │  Tool C HTTP│     └─────────┘
└─────────┘     └─────────────┘
         ↑ 每个工具都要单独适配

MCP 方式 (标准化):
┌─────────┐     ┌─────────────┐     ┌─────────┐
│   LLM   │◄───►│  MCP Client │◄───►│ MCP Server│◄───► 任意工具/数据
│         │     │  (统一协议)  │     │(标准化接口)│
└─────────┘     └─────────────┘     └─────────┘
         ↑ 一次接入，无限扩展
```

---

## MCP 核心架构

### 1. 架构组件

```
┌─────────────────────────────────────────────────────────────┐
│                     MCP 架构全景                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌───────────────┐         JSON-RPC          ┌───────────┐ │
│  │  MCP Client   │◄─────────────────────────►│MCP Server │ │
│  │  (Host)       │    (标准通信协议)          │  (工具)   │ │
│  │               │                           │           │ │
│  │ • Claude      │                           │ • 文件系统│ │
│  │ • Cursor      │                           │ • 数据库  │ │
│  │ • 本项目 Agent│                           │ • API 服务│ │
│  │               │                           │ • 浏览器  │ │
│  └───────┬───────┘                           └─────┬─────┘ │
│          │                                        │       │
│          │         ┌─────────────────┐            │       │
│          │         │  Capability     │            │       │
│          └────────►│  Negotiation    │◄───────────┘       │
│                    │  (能力协商)      │                    │
│                    └─────────────────┘                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. 通信协议

MCP 使用 **JSON-RPC 2.0** 作为底层通信协议：

```json
// 请求示例
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "browser_navigate",
    "arguments": {
      "url": "https://example.com"
    }
  }
}

// 响应示例
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Successfully navigated to https://example.com"
      }
    ],
    "isError": false
  }
}
```

---

## MCP 核心概念

### 1. Resources (资源)

资源是 MCP 暴露的数据源，可以被 LLM 读取：

```python
# 示例：暴露文件系统资源
@mcp.resource("file://{path}")
def read_file(path: str) -> str:
    """读取文件内容"""
    with open(path, 'r') as f:
        return f.read()

# LLM 可以通过 URI 访问
# resource://file:///Users/name/documents/report.txt
```

### 2. Tools (工具)

工具是 MCP 暴露的可执行功能：

```python
# 示例：浏览器导航工具
@mcp.tool()
def browser_navigate(url: str) -> str:
    """
    Navigate browser to specified URL.
    
    Args:
        url: The target URL to navigate to
    """
    # 执行导航逻辑
    return f"Navigated to {url}"
```

### 3. Prompts (提示模板)

预定义的提示模板，帮助 LLM 更好地使用工具：

```python
@mcp.prompt()
def browser_automation_guide() -> str:
    """
    You are a browser automation assistant. Follow these rules:
    1. Always check current URL before navigation
    2. Wait for page load after navigation
    3. Use specific selectors for element interaction
    """
```

---

## MCP vs 传统 Function Calling

| 特性 | Function Calling | MCP |
|------|------------------|-----|
| **协议** | 各厂商不同 (OpenAI/Anthropic/Google) | 标准化协议 |
| **发现机制** | 静态定义 | 动态发现 (Discovery) |
| **传输层** | HTTP/直接调用 | stdio / SSE / HTTP |
| **上下文** | 单次调用 | 可维护会话状态 |
| **生态** | 碎片化 | 统一生态 |

---

## MCP 传输方式

### 1. stdio (标准输入输出)

```
┌─────────┐    stdin/stdout    ┌─────────┐
│  Client │◄──────────────────►│ Server  │
│ (Parent)│   (本地进程通信)   │ (Child) │
└─────────┘                    └─────────┘

适用场景：
• 本地工具集成
• 命令行工具
• 开发调试
```

### 2. SSE (Server-Sent Events)

```
┌─────────┐    HTTP POST     ┌─────────┐
│  Client │◄────────────────►│ Server  │
│         │   (初始化连接)    │ (HTTP)  │
│         │◄─────────────────│         │
│         │   SSE 事件流      │         │
└─────────┘                  └─────────┘

适用场景：
• 远程服务
• Web 应用
• 云服务集成
```

---

## MCP 在浏览器自动化中的应用

### 为什么浏览器需要 MCP？

```
传统浏览器自动化的问题：
┌─────────────────────────────────────────┐
│ 1. 状态管理复杂                         │
│    - Cookie、LocalStorage、Session      │
│    - 多标签页状态                       │
│    - 页面生命周期                       │
│                                         │
│ 2. 元素定位脆弱                         │
│    - DOM 结构变化                       │
│    - 动态加载内容                       │
│    - Shadow DOM                         │
│                                         │
│ 3. 与 AI 集成困难                       │
│    - 截图 → 理解 → 决策 → 执行         │
│    - 循环反馈复杂                       │
└─────────────────────────────────────────┘

MCP 解决方案：
┌─────────────────────────────────────────┐
│ 1. 标准化接口                            │
│    - 统一的操作原语                     │
│    - 清晰的状态描述                     │
│                                         │
│ 2. 结构化数据                            │
│    - DOM 快照标准化                     │
│    - 操作结果结构化                     │
│                                         │
│ 3. 双向通信                              │
│    - LLM 可随时查询状态                 │
│    - 工具可主动推送事件                 │
└─────────────────────────────────────────┘
```

---

## 实践项目：MCP 浏览器控制器

见本项目 `mcp/` 目录下的完整实现：

```
mcp/
├── README.md           # 本文件
├── server.py           # MCP 服务器实现
├── client_example.py   # 客户端使用示例
└── config.json         # MCP 配置文件
```

### 快速开始

```bash
# 1. 安装依赖
pip install mcp playwright

# 2. 启动 MCP 服务器
python mcp/server.py

# 3. 运行客户端示例
python mcp/client_example.py
```

---

## 更多资源

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Anthropic MCP 公告](https://www.anthropic.com/news/model-context-protocol)
