#!/usr/bin/env python3
"""
验证 LM Studio 配置是否正确加载
"""
import sys

def verify_config():
    print("=" * 60)
    print("🔍 验证 LM Studio 配置")
    print("=" * 60)
    
    # 强制重新加载模块（避免缓存）
    if 'src.utils.config' in sys.modules:
        del sys.modules['src.utils.config']
    
    from src.utils import config
    
    print("\n📋 已配置的 LLM Providers:")
    for provider, display_name in config.PROVIDER_DISPLAY_NAMES.items():
        status = "✅" if provider in config.model_names else "❌"
        print(f"  {status} {provider}: {display_name}")
    
    print("\n🤖 LM Studio 可用模型:")
    if 'lmstudio' in config.model_names:
        for model in config.model_names['lmstudio']:
            print(f"  • {model}")
    else:
        print("  ❌ lmstudio 不在 model_names 中")
    
    print("\n🌐 环境变量配置:")
    import os
    endpoint = os.getenv('LMSTUDIO_ENDPOINT', '未设置')
    api_key = os.getenv('LMSTUDIO_API_KEY', '未设置')
    print(f"  LMSTUDIO_ENDPOINT: {endpoint}")
    print(f"  LMSTUDIO_API_KEY: {'已设置' if api_key else '未设置 (允许空)'}")
    
    print("\n" + "=" * 60)
    if 'lmstudio' in config.model_names:
        print("✅ LM Studio 配置正确！")
        print("\n⚠️  如果 WebUI 仍不显示 lmstudio，请执行：")
        print("   1. 完全停止 WebUI 服务 (Ctrl+C)")
        print("   2. 重新启动: python webui_enterprise.py 或 python webui.py")
    else:
        print("❌ LM Studio 配置缺失，请检查 src/utils/config.py")
    print("=" * 60)

if __name__ == "__main__":
    verify_config()
