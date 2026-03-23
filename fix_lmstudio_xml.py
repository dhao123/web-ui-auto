#!/usr/bin/env python3
"""
修复 LM Studio XML 输出问题

问题: 模型输出 <tool_call> XML 格式，但系统期望 JSON
解决方案: 使用 json_mode 代替 raw 模式
"""

def main():
    print("=" * 70)
    print("🔧 LM Studio XML 输出问题修复")
    print("=" * 70)
    
    print("\n📋 问题分析:")
    print("  日志显示模型输出: <tool_call><function=AgentOutput>...</function></tool_call>")
    print("  但 browser-use 期望: JSON 格式")
    print("  原因: raw 模式下模型使用 XML 格式的工具调用")
    
    print("\n" + "=" * 70)
    print("✅ 解决方案")
    print("=" * 70)
    
    print("\n方案 1: 手动设置 Tool Calling Method（立即生效）")
    print("-" * 70)
    print("  1. 在 WebUI 的 '⚙️ Agent 配置' 页面")
    print("  2. 找到 'Tool Calling Method' (工具调用方法)")
    print("  3. 选择 'json_mode'")
    print("  4. 重新运行任务")
    
    print("\n方案 2: 重启 WebUI（代码已自动更新）")
    print("-" * 70)
    print("  1. 完全停止 WebUI: Ctrl+C")
    print("  2. 重新启动: python webui.py")
    print("  3. 代码已自动检测 LM Studio 并使用 'json_mode'")
    
    print("\n" + "=" * 70)
    print("📊 Tool Calling Method 说明:")
    print("  • auto          - 自动检测（已更新为 LM Studio 使用 json_mode）")
    print("  • json_mode     - JSON 格式输出（推荐用于 LM Studio）")
    print("  • raw           - 原始文本（可能输出 XML，不推荐）")
    print("  • function_calling - 标准函数调用（API 模型专用）")
    print("=" * 70)
    
    print("\n⚠️  如果 json_mode 仍有问题:")
    print("  • 尝试使用更大的模型（qwen2.5-14b 或 qwen3.5-14b）")
    print("  • 检查 LM Studio 的 Context Length 设置（建议 8192+）")
    print("  • 考虑使用 ZKH AI Gateway 在线模型")

if __name__ == "__main__":
    main()
