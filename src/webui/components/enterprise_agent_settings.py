"""
Enterprise Agent Settings Component
企业级 Agent 配置组件
"""

import os
import json
import gradio as gr
from typing import Literal

from src.webui.webui_manager import WebuiManager
from src.utils import config


def create_enterprise_agent_settings(ui_manager: WebuiManager, lang: Literal["zh", "en"] = "zh"):
    """创建企业级 Agent 配置界面"""
    
    texts = {
        "zh": {
            "title": "Agent 配置",
            "subtitle": "配置大语言模型和执行参数",
            "llm_config": "🤖 LLM 配置",
            "planner_config": "📋 Planner LLM 配置",
            "execution_config": "⚡ 执行配置",
            "mcp_config": "🔌 MCP 服务器配置",
            "prompt_config": "📝 提示词配置",
            "provider": "模型提供商",
            "model": "模型名称",
            "temperature": "温度参数",
            "base_url": "基础 URL",
            "api_key": "API 密钥",
            "use_vision": "启用视觉",
            "ollama_ctx": "上下文长度",
            "max_steps": "最大步数",
            "max_actions": "每步最大动作数",
            "max_tokens": "最大输入 Token",
            "tool_calling": "工具调用方式",
            "system_prompt": "系统提示词覆盖",
            "extend_prompt": "扩展提示词",
            "mcp_file": "MCP 配置文件",
            "hints": {
                "temperature": "控制输出的随机性 (0.0-2.0)",
                "use_vision": "将截图输入到 LLM 进行分析",
                "max_steps": "防止无限循环的步数限制",
                "ollama_ctx": "仅对 Ollama 提供商有效",
            }
        },
        "en": {
            "title": "Agent Settings",
            "subtitle": "Configure LLM and execution parameters",
            "llm_config": "🤖 LLM Configuration",
            "planner_config": "📋 Planner LLM Configuration",
            "execution_config": "⚡ Execution Configuration",
            "mcp_config": "🔌 MCP Server Configuration",
            "prompt_config": "📝 Prompt Configuration",
            "provider": "Provider",
            "model": "Model Name",
            "temperature": "Temperature",
            "base_url": "Base URL",
            "api_key": "API Key",
            "use_vision": "Enable Vision",
            "ollama_ctx": "Context Length",
            "max_steps": "Max Steps",
            "max_actions": "Max Actions per Step",
            "max_tokens": "Max Input Tokens",
            "tool_calling": "Tool Calling Method",
            "system_prompt": "Override System Prompt",
            "extend_prompt": "Extend Prompt",
            "mcp_file": "MCP Config File",
            "hints": {
                "temperature": "Controls output randomness (0.0-2.0)",
                "use_vision": "Feed screenshots to LLM for analysis",
                "max_steps": "Step limit to prevent infinite loops",
                "ollama_ctx": "Only valid for Ollama provider",
            }
        }
    }
    
    t = texts[lang]
    tab_components = {}
    
    with gr.Column(elem_classes=["ep-content"]):
        
        # ==================== LLM Configuration Card ====================
        with gr.Column(elem_classes=["ep-card", "ep-mb-4"]):
            with gr.Row(elem_classes=["ep-card-header"]):
                gr.Markdown(f"**{t['llm_config']}**")
            
            with gr.Column(elem_classes=["ep-card-body"]):
                # Provider & Model
                with gr.Row():
                    with gr.Column(scale=1):
                        llm_provider = gr.Dropdown(
                            label=t["provider"],
                            choices=list(config.model_names.keys()),
                            value=os.getenv("DEFAULT_LLM", "openai"),
                            elem_classes=["ep-input", "ep-select"]
                        )
                    with gr.Column(scale=1):
                        llm_model_name = gr.Dropdown(
                            label=t["model"],
                            choices=config.model_names[os.getenv("DEFAULT_LLM", "openai")],
                            value=config.model_names[os.getenv("DEFAULT_LLM", "openai")][0],
                            allow_custom_value=True,
                            elem_classes=["ep-input", "ep-select"]
                        )
                
                # Temperature & Vision
                with gr.Row():
                    with gr.Column(scale=2):
                        llm_temperature = gr.Slider(
                            label=t["temperature"],
                            minimum=0.0,
                            maximum=2.0,
                            value=0.6,
                            step=0.1,
                            elem_classes=["ep-slider"]
                        )
                        gr.Markdown(f"<span class='ep-text-xs ep-text-gray'>{t['hints']['temperature']}</span>")
                    with gr.Column(scale=1):
                        use_vision = gr.Checkbox(
                            label=t["use_vision"],
                            value=True,
                            elem_classes=["ep-checkbox"]
                        )
                        gr.Markdown(f"<span class='ep-text-xs ep-text-gray'>{t['hints']['use_vision']}</span>")
                
                # Base URL & API Key
                with gr.Row():
                    with gr.Column(scale=1):
                        llm_base_url = gr.Textbox(
                            label=t["base_url"],
                            placeholder="https://api.openai.com/v1",
                            elem_classes=["ep-input"]
                        )
                    with gr.Column(scale=1):
                        llm_api_key = gr.Textbox(
                            label=t["api_key"],
                            type="password",
                            placeholder="••••••••",
                            elem_classes=["ep-input"]
                        )
                
                # Ollama Context (hidden by default)
                ollama_num_ctx = gr.Slider(
                    label=t["ollama_ctx"],
                    minimum=256,
                    maximum=65536,
                    value=16000,
                    step=256,
                    visible=False,
                    elem_classes=["ep-slider"]
                )
        
        # ==================== Planner LLM Configuration Card ====================
        with gr.Column(elem_classes=["ep-card", "ep-mb-4"]):
            with gr.Row(elem_classes=["ep-card-header"]):
                gr.Markdown(f"**{t['planner_config']}** (可选)")
            
            with gr.Column(elem_classes=["ep-card-body"]):
                with gr.Row():
                    with gr.Column(scale=1):
                        planner_llm_provider = gr.Dropdown(
                            label=t["provider"],
                            choices=[""] + list(config.model_names.keys()),
                            value="",
                            elem_classes=["ep-input", "ep-select"]
                        )
                    with gr.Column(scale=1):
                        planner_llm_model_name = gr.Dropdown(
                            label=t["model"],
                            choices=[],
                            value="",
                            allow_custom_value=True,
                            elem_classes=["ep-input", "ep-select"]
                        )
                
                with gr.Row():
                    with gr.Column(scale=2):
                        planner_llm_temperature = gr.Slider(
                            label=t["temperature"],
                            minimum=0.0,
                            maximum=2.0,
                            value=0.6,
                            step=0.1,
                            elem_classes=["ep-slider"]
                        )
                    with gr.Column(scale=1):
                        planner_use_vision = gr.Checkbox(
                            label=t["use_vision"],
                            value=False,
                            elem_classes=["ep-checkbox"]
                        )
                
                with gr.Row():
                    with gr.Column(scale=1):
                        planner_llm_base_url = gr.Textbox(
                            label=t["base_url"],
                            elem_classes=["ep-input"]
                        )
                    with gr.Column(scale=1):
                        planner_llm_api_key = gr.Textbox(
                            label=t["api_key"],
                            type="password",
                            elem_classes=["ep-input"]
                        )
                
                planner_ollama_num_ctx = gr.Slider(
                    label=t["ollama_ctx"],
                    minimum=256,
                    maximum=65536,
                    value=16000,
                    step=256,
                    visible=False,
                    elem_classes=["ep-slider"]
                )
        
        # ==================== Execution Configuration Card ====================
        with gr.Column(elem_classes=["ep-card", "ep-mb-4"]):
            with gr.Row(elem_classes=["ep-card-header"]):
                gr.Markdown(f"**{t['execution_config']}**")
            
            with gr.Column(elem_classes=["ep-card-body"]):
                with gr.Row():
                    with gr.Column(scale=1):
                        max_steps = gr.Slider(
                            label=t["max_steps"],
                            minimum=1,
                            maximum=1000,
                            value=30,
                            step=1,
                            elem_classes=["ep-slider"]
                        )
                        gr.Markdown(f"<span class='ep-text-xs ep-text-gray'>{t['hints']['max_steps']}</span>")
                    with gr.Column(scale=1):
                        max_actions = gr.Slider(
                            label=t["max_actions"],
                            minimum=1,
                            maximum=100,
                            value=10,
                            step=1,
                            elem_classes=["ep-slider"]
                        )
                
                with gr.Row():
                    with gr.Column(scale=1):
                        max_input_tokens = gr.Number(
                            label=t["max_tokens"],
                            value=128000,
                            precision=0,
                            elem_classes=["ep-input"]
                        )
                    with gr.Column(scale=1):
                        tool_calling_method = gr.Dropdown(
                            label=t["tool_calling"],
                            choices=['function_calling', 'json_mode', 'raw', 'auto', 'tools', 'None'],
                            value="auto",
                            elem_classes=["ep-input", "ep-select"]
                        )
        
        # ==================== MCP Configuration Card ====================
        with gr.Column(elem_classes=["ep-card", "ep-mb-4"]):
            with gr.Row(elem_classes=["ep-card-header"]):
                gr.Markdown(f"**{t['mcp_config']}** (可选)")
            
            with gr.Column(elem_classes=["ep-card-body"]):
                with gr.Row():
                    with gr.Column(scale=1):
                        mcp_json_file = gr.File(
                            label=t["mcp_file"],
                            file_types=[".json"],
                            elem_classes=["ep-input"]
                        )
                    with gr.Column(scale=1):
                        mcp_server_config = gr.Textbox(
                            label="MCP Server JSON",
                            lines=6,
                            visible=False,
                            elem_classes=["ep-input", "ep-textarea-lg"]
                        )
        
        # ==================== Prompt Configuration Card ====================
        with gr.Column(elem_classes=["ep-card"]):
            with gr.Row(elem_classes=["ep-card-header"]):
                gr.Markdown(f"**{t['prompt_config']}** (可选)")
            
            with gr.Column(elem_classes=["ep-card-body"]):
                with gr.Row():
                    with gr.Column(scale=1):
                        override_system_prompt = gr.Textbox(
                            label=t["system_prompt"],
                            lines=4,
                            placeholder="输入自定义系统提示词...",
                            elem_classes=["ep-input", "ep-textarea-lg"]
                        )
                    with gr.Column(scale=1):
                        extend_system_prompt = gr.Textbox(
                            label=t["extend_prompt"],
                            lines=4,
                            placeholder="输入扩展提示词...",
                            elem_classes=["ep-input", "ep-textarea-lg"]
                        )
    
    # Store components
    tab_components.update({
        "llm_provider": llm_provider,
        "llm_model_name": llm_model_name,
        "llm_temperature": llm_temperature,
        "use_vision": use_vision,
        "llm_base_url": llm_base_url,
        "llm_api_key": llm_api_key,
        "ollama_num_ctx": ollama_num_ctx,
        "planner_llm_provider": planner_llm_provider,
        "planner_llm_model_name": planner_llm_model_name,
        "planner_llm_temperature": planner_llm_temperature,
        "planner_use_vision": planner_use_vision,
        "planner_llm_base_url": planner_llm_base_url,
        "planner_llm_api_key": planner_llm_api_key,
        "planner_ollama_num_ctx": planner_ollama_num_ctx,
        "max_steps": max_steps,
        "max_actions": max_actions,
        "max_input_tokens": max_input_tokens,
        "tool_calling_method": tool_calling_method,
        "mcp_json_file": mcp_json_file,
        "mcp_server_config": mcp_server_config,
        "override_system_prompt": override_system_prompt,
        "extend_system_prompt": extend_system_prompt,
    })
    
    ui_manager.add_components("agent_settings", tab_components)
    
    # Event handlers
    def update_model_dropdown(provider):
        if provider in config.model_names:
            return gr.Dropdown(choices=config.model_names[provider], value=config.model_names[provider][0])
        return gr.Dropdown(choices=[], value="")
    
    llm_provider.change(
        fn=lambda x: gr.update(visible=x == "ollama"),
        inputs=llm_provider,
        outputs=ollama_num_ctx
    )
    llm_provider.change(
        fn=update_model_dropdown,
        inputs=llm_provider,
        outputs=llm_model_name
    )
    
    planner_llm_provider.change(
        fn=lambda x: gr.update(visible=x == "ollama"),
        inputs=planner_llm_provider,
        outputs=planner_ollama_num_ctx
    )
    planner_llm_provider.change(
        fn=update_model_dropdown,
        inputs=planner_llm_provider,
        outputs=planner_llm_model_name
    )
    
    async def update_mcp_server(mcp_file):
        if hasattr(ui_manager, "bu_controller") and ui_manager.bu_controller:
            await ui_manager.bu_controller.close_mcp_client()
            ui_manager.bu_controller = None
        
        if not mcp_file:
            return None, gr.update(visible=False)
        
        try:
            with open(mcp_file, 'r') as f:
                mcp_server = json.load(f)
            return json.dumps(mcp_server, indent=2), gr.update(visible=True)
        except Exception as e:
            return f"Error: {e}", gr.update(visible=False)
    
    mcp_json_file.change(
        fn=update_mcp_server,
        inputs=mcp_json_file,
        outputs=[mcp_server_config, mcp_server_config]
    )
