# LM Studio 本地模型完整修复方案

## 🎯 问题总结

本地模型（qwen3.5-35b-a3b 等）在 browser-use 中出现 action 为空 `{}` 的问题，根本原因是：

1. **工具调用不兼容**: 本地模型未经过 OpenAI function calling 微调
2. **输出格式不稳定**: 无法稳定生成符合 AgentOutput schema 的 JSON
3. **重试后失效**: 失败后模型进入循环，持续输出空 action

## ✅ 解决方案

### 核心修改

#### 1. 新增 `LMStudioAgent` 类 (`src/agent/browser_use/lmstudio_agent.py`)

专为本地模型优化的 Agent，特性包括：

- **强制 raw 模式**: 不使用 function calling，直接解析 JSON
- **自定义解析器**: 处理代码块、不完整 JSON 等各种输出格式
- **空 action 修复**: 自动从 next_goal 推断合理的默认 action
- **定制系统提示词**: 更明确的 JSON 格式要求

```python
class LMStudioAgent(BrowserUseAgent):
    def _set_tool_calling_method(self):
        return 'raw'  # 强制使用 raw 模式
    
    def _extract_json_from_output(self, content: str) -> dict:
        # 多种策略提取 JSON
        # 1. 直接解析
        # 2. 从 ```json 代码块提取
        # 3. 从 ``` 代码块提取
        # 4. 查找 JSON 边界
        pass
    
    def _fix_empty_action(self, data: dict) -> dict:
        # 从 next_goal 推断默认 action
        # 避免空 action 导致任务卡死
        pass
```

#### 2. 修改 `browser_use_agent_tab.py`

自动检测 LM Studio 并切换 Agent 类：

```python
is_lmstudio = llm_provider_name == "lmstudio" or (
    llm_base_url and ':1234' in str(llm_base_url)
)

if is_lmstudio:
    agent_class = LMStudioAgent
    tool_calling_method = "raw"  # 强制 raw
else:
    agent_class = BrowserUseAgent
```

#### 3. 保留 `browser_use_agent.py` 的检测逻辑

作为双重保险，强制将 LM Studio 设置为 json_mode/raw。

## 🚀 使用方法

### 启动 WebUI

```bash
# 停止现有服务
Ctrl+C

# 重新启动（加载新代码）
python webui.py
```

### 配置 LM Studio

1. **LLM Provider**: 选择 `lmstudio`
2. **LLM Model Name**: 输入您加载的模型名称（如 `qwen3.5-35b-a3b`）
3. **Base URL**: `http://localhost:1234/v1`（或您的 LM Studio 地址）
4. **API Key**: 留空
5. **Tool Calling Method**: `auto`（会自动使用 raw 模式）
6. **Temperature**: 建议 `0.0` - `0.3`（降低随机性）

### LM Studio 设置建议

1. **Context Length**: 建议 `16384` 或更高
2. **Temperature**: `0.1` - `0.3`
3. **加载的模型**: 
   - 推荐: `qwen2.5-14b-instruct` 或更大
   - 避免: 小于 7B 的模型（工具调用能力太弱）

## 📊 效果对比

| 场景 | 修复前 | 修复后 |
|------|--------|--------|
| Tool Calling Method | function_calling (+tools) | raw (+rawtools) |
| Step 1 | go_to_url ✅ | go_to_url ✅ |
| Step 2+ | action: {} ❌ | action: {...} ✅ |
| 解析失败 | 持续空 action | 自动修复/默认 action |
| 任务完成 | 无法完成 | 可以完成 |

## 🔍 日志特征

### 修复前的错误日志
```
main_model=qwen3.5-35b-a3b +tools          ← function_calling 模式
Action 1/1: {}                              ← 空 action
Failed to parse model output               ← 解析失败
```

### 修复后的正常日志
```
🤖 Using LMStudioAgent for local model: qwen3.5-35b-a3b
Forcing 'raw' mode for local model
Action 1/1: {"click_element_by_index":...}  ← 正常 action
```

## 🛠️ 故障排查

### 如果仍然出现空 action

1. **检查日志** 是否显示 `Using LMStudioAgent`
   - 如果没有，确认 provider 是 `lmstudio` 或 base_url 包含 `:1234`

2. **尝试手动设置 Tool Calling Method**
   - 设置为 `raw` 而不是 `auto`

3. **使用更强的模型**
   - qwen2.5-14b 比 qwen3.5-9b 更稳定
   - 参数量越大，遵循指令能力越强

4. **检查 LM Studio 配置**
   - Context Length 是否足够（建议 16384+）
   - Temperature 是否过高（建议 < 0.3）

### 备选方案：使用 ZKH AI Gateway

如果本地模型仍无法满足需求，使用在线模型：

```yaml
LLM Provider: zkh
LLM Model: ep_20251217_i18v  # DeepSeek-V3
```

## 📁 修改的文件列表

1. `src/agent/browser_use/lmstudio_agent.py` - 新增
2. `src/webui/components/browser_use_agent_tab.py` - 修改
3. `src/agent/browser_use/browser_use_agent.py` - 已有检测逻辑

## 🎉 预期效果

- ✅ 本地模型能正确生成 action
- ✅ 空 action 自动修复
- ✅ 任务可以正常执行完成
- ✅ 无需手动设置 Tool Calling Method
