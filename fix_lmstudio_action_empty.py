#!/usr/bin/env python3
"""
修复 LM Studio action 为空 {} 的问题

问题: 模型理解任务但输出空 action {}
根因: qwen3.5-9b 工具调用能力弱，无法稳定生成 JSON action
"""

def analyze():
    print("=" * 70)
    print("🔍 LM Studio Action 为空问题分析")
    print("=" * 70)
    
    print("\n📋 日志现象:")
    print("  ✅ Eval: 模型正确理解当前状态")
    print("  ✅ Memory: 模型记住任务目标")  
    print("  ✅ Next goal: 模型规划下一步")
    print("  ❌ Action: {}  <- 空对象，无法生成有效操作")
    
    print("\n🔍 问题根因:")
    print("  1. qwen3.5-9b 是较小参数模型（9B）")
    print("  2. 本地部署模型缺少工具调用微调")
    print("  3. browser-use 的提示词对本地模型不够友好")
    
    print("\n" + "=" * 70)
    print("✅ 推荐解决方案（按优先级）")
    print("=" * 70)
    
    print("\n🥇 方案 1: 更换更强大的模型（推荐）")
    print("-" * 70)
    print("  在 LM Studio 中加载更强模型:")
    print("  • qwen2.5-14b-instruct  <- 推荐，工具调用能力较好")
    print("  • qwen2.5-32b-instruct  <- 效果更好，需要更多显存")
    print("  • deepseek-coder-v2      <- 代码/结构化输出能力强")
    print("  操作: LM Studio -> 下载模型 -> 加载上述模型")
    
    print("\n🥈 方案 2: 调整 Temperature 为 0.0")
    print("-" * 70)
    print("  在 WebUI Agent 配置中:")
    print("  • LLM Temperature: 0.0  <- 降低随机性")
    print("  • 重试任务")
    
    print("\n🥉 方案 3: 使用 ZKH AI Gateway（最稳定）")
    print("-" * 70)
    print("  切换回在线模型:")
    print("  • LLM Provider: zkh")
    print("  • LLM Model: ep_20251217_i18v (DeepSeek-V3)")
    print("  • 无需本地部署，工具调用能力强")
    
    print("\n" + "=" * 70)
    print("⚙️  可选: 尝试修改系统提示词（实验性）")
    print("=" * 70)
    print("  在 Agent 配置的 'Extend system prompt' 中添加:")
    print("""
  你必须严格按照以下 JSON 格式输出动作：
  {"action": [{"click_element_by_index": {"index": 121}}]}
  
  不要输出空的 action {}，必须包含具体的操作。
  """)
    
    print("\n" + "=" * 70)
    print("📊 各模型工具调用能力对比:")
    print("  qwen3.5-9b       ⭐⭐     较弱，不推荐用于 browser-use")
    print("  qwen2.5-7b       ⭐⭐⭐   一般，可能需要多次尝试")
    print("  qwen2.5-14b      ⭐⭐⭐⭐  良好，推荐用于本地部署")
    print("  DeepSeek-V3(API) ⭐⭐⭐⭐⭐ 优秀，最稳定")
    print("=" * 70)

if __name__ == "__main__":
    analyze()
