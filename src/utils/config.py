PROVIDER_DISPLAY_NAMES = {
    "zkh": "ZKH AI Gateway",
    "openai": "OpenAI",
    "deepseek": "DeepSeek",
    "ollama": "Ollama (本地模型)",
}

# Predefined model names for common providers
# ZKH 模型按工具调用支持情况排序
model_names = {
    "zkh": [
        # ✅ 支持工具调用 - 可用于 Browser-Use Agent
        "ep_20250805_urdq",   # GPT-4o
        "ep_20251217_i18v",   # DeepSeek-V3 (推荐)
        "ep_20250805_4q5l",   # GPT-4o-mini
        "ep_20250805_ur59",   # 通义千问VL-Max-Latest (支持视觉)
        "ep_20250731_vzaa",   # 通义千问3-235B-A22B-Instruct
        "ep_20250728_izkl",   # 通义千问-Max-Latest
        "ep_20250718_zoiz",   # ZKH-LLM
        "ep_20250904_slsu",   # Qwen-Long
        # ⚠️ 不支持工具调用 - 不推荐用于 Browser-Use Agent
        # "ep_20250815_yc11", # 通义千问vl max (旧版本，工具调用不支持)
        # "ep_20250908_1pgk", # DeepSeek-V3.1 (工具调用不支持)
        # "ep_20251217_hr5x", # DeepSeek-R1 (推理模型，不支持工具调用)
        # "ep_20250718_qj6v", # Doubao-1.5-pro-32k (工具调用不支持)
    ],
    "openai": ["gpt-4o", "gpt-4", "gpt-3.5-turbo", "o3-mini"],
    "deepseek": ["deepseek-chat", "deepseek-reasoner"],
    "ollama": [
        "qwen2.5:7b", "qwen2.5:14b", "qwen2.5:32b",
        "qwen2.5-coder:14b", "qwen2.5-coder:32b",
        "llama2:7b", "deepseek-r1:14b", "deepseek-r1:32b"
    ],
}
