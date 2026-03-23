#!/usr/bin/env python3
"""
诊断和修复 LM Studio action 为空的问题
"""
import sys

def diagnose():
    print("=" * 70)
    print("🔧 LM Studio Action 为空问题诊断工具")
    print("=" * 70)
    
    print("\n📋 问题分析:")
    print("  日志显示 action: {} 空对象，这是工具调用(Tool Calling)兼容性问题")
    print("  LM Studio 本地模型不支持标准 OpenAI 函数调用格式")
    
    print("\n✅ 解决方案（选择其一）:")
    
    print("\n" + "-" * 70)
    print("方案 1: 修改 Agent 配置（推荐，立即生效）")
    print("-" * 70)
    print("  1. 在 WebUI 的 '⚙️ Agent 配置' 页面")
    print("  2. 找到 'Tool Calling Method' (工具调用方法)")
    print("  3. 从 'auto' 改为 'raw'")
    print("  4. 重新运行任务")
    
    print("\n" + "-" * 70)
    print("方案 2: 重启 WebUI（代码已自动检测 LM Studio）")
    print("-" * 70)
    print("  1. 完全停止 WebUI: Ctrl+C")
    print("  2. 重新启动: python webui_enterprise.py 或 python webui.py")
    print("  3. 代码已自动检测 LM Studio 并使用 'raw' 模式")
    
    print("\n" + "-" * 70)
    print("方案 3: 使用更强大的模型")
    print("-" * 70)
    print("  如果 'raw' 模式仍有问题，建议:")
    print("  • 使用 qwen2.5-14b 或更大参数量的模型")
    print("  • 或使用 ZKH AI Gateway 的在线模型")
    
    print("\n" + "=" * 70)
    print("📊 各模式说明:")
    print("  • auto      - 自动检测（已更新支持 LM Studio）")
    print("  • raw       - 直接文本输出（推荐用于本地模型）")
    print("  • function_calling - 标准函数调用（仅支持 API 模型）")
    print("  • json_mode - JSON 格式输出")
    print("=" * 70)

if __name__ == "__main__":
    diagnose()
