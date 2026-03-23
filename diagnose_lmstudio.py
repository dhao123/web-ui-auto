#!/usr/bin/env python3
"""
LM Studio 问题完整诊断工具
"""
import sys

def diagnose():
    print("=" * 70)
    print("🔍 LM Studio Action 为空问题 - 完整诊断")
    print("=" * 70)
    
    print("\n📋 现象分析:")
    print("  • Step 1: go_to_url 成功 ✅")
    print("  • Step 2+: action: {} 全为空 ❌")
    print("  • 日志显示: +tools (function_calling 模式)")
    
    print("\n🔍 问题根因:")
    print("  ┌─────────────────────────────────────────────────────────────┐")
    print("  │  本地模型（包括35B）无法正确使用 function_calling 模式        │")
    print("  │                                                             │")
    print("  │  当 tool_calling_method = 'function_calling' 时:            │")
    print("  │  1. browser-use 使用 OpenAI 函数调用 API                    │")
    print("  │  2. 本地模型未经过工具调用微调                              │")
    print("  │  3. 模型返回空或格式错误的工具调用                          │")
    print("  │  4. 结果: action: {}                                        │")
    print("  └─────────────────────────────────────────────────────────────┘")
    
    print("\n" + "=" * 70)
    print("✅ 彻底解决方案")
    print("=" * 70)
    
    print("\n🥇 方案 1: 强制使用 json_mode（代码已更新）")
    print("-" * 70)
    print("  已修改代码强制检测 LM Studio 并使用 json_mode:")
    print("  • 检测 base_url 包含 :1234 端口")
    print("  • 检测模型名称包含 qwen/llama 等本地模型标识")
    print("  • 无论 UI 如何设置，强制使用 json_mode")
    print("")
    print("  操作步骤:")
    print("  1. Ctrl+C 完全停止 WebUI")
    print("  2. python webui.py 重新启动")
    print("  3. 查看日志应显示: 🚨 LM Studio local model detected... json_mode")
    
    print("\n🥈 方案 2: 手动设置 Tool Calling Method")
    print("-" * 70)
    print("  如果不想重启，在 WebUI 中:")
    print("  1. 进入 '⚙️ Agent 配置' 页面")
    print("  2. Tool Calling Method: 选择 'json_mode'")
    print("  3. 重新运行任务")
    
    print("\n🥉 方案 3: 使用 ZKH AI Gateway（最稳定）")
    print("-" * 70)
    print("  LLM Provider: zkh")
    print("  LLM Model: ep_20251217_i18v (DeepSeek-V3)")
    print("  无需本地部署，工具调用能力强")
    
    print("\n" + "=" * 70)
    print("📊 各模式对比")
    print("=" * 70)
    print("  模式           日志标记    适用模型         本地模型可用?")
    print("  ─────────────────────────────────────────────────────────")
    print("  function_calling  +tools    GPT-4/DeepSeek-V3   ❌ 不可用")
    print("  json_mode         无标记    通用               ✅ 推荐")
    print("  raw              +rawtools  通用               ✅ 备选")
    print("")
    print("  您当前的日志显示 +tools = function_calling ❌")
    print("  目标：使用 json_mode（日志无 +tools 标记）✅")
    
    print("\n" + "=" * 70)
    print("🚀 立即执行")
    print("=" * 70)
    print("  请执行以下命令:")
    print("")
    print("  Ctrl+C          # 停止当前 WebUI")
    print("  python webui.py # 重新启动（加载更新后的代码）")
    print("")
    print("  然后查看启动日志中是否显示:")
    print("  🚨 LM Studio local model detected... Forcing 'json_mode'")
    print("=" * 70)

if __name__ == "__main__":
    diagnose()
