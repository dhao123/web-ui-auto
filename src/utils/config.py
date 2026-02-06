PROVIDER_DISPLAY_NAMES = {
    "zkh": "ZKH AI Gateway",
    "openai": "OpenAI",
    "deepseek": "DeepSeek",
    "ollama": "Ollama (本地模型)",
}

# Predefined model names for common providers
model_names = {
    "zkh": [
        
        "ep_20251217_i18v",   # deepseek-v3-百炼
        "ep_20250908_1pgk",   # DeepSeek-V3.1-百炼
        "ep_20251217_hr5x",   # deepseek-r1-百炼
        "ep_20250815_yc11",   # 通义千问vl max
    ],
    "openai": ["gpt-4o", "gpt-4", "gpt-3.5-turbo", "o3-mini"],
    "deepseek": ["deepseek-chat", "deepseek-reasoner"],
    "ollama": [
        "qwen2.5:7b", "qwen2.5:14b", "qwen2.5:32b",
        "qwen2.5-coder:14b", "qwen2.5-coder:32b",
        "llama2:7b", "deepseek-r1:14b", "deepseek-r1:32b"
    ],
}
