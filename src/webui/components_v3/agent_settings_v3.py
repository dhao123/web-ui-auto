"""
Agent配置组件 V3
基于ui-ux skill的企业级设计,使用卡片布局优化UI
"""
import json
import os
import gradio as gr
from gradio.components import Component
from typing import Any, Dict, Optional
from src.webui.webui_manager import WebuiManager
from src.utils import config
import logging
from functools import partial

logger = logging.getLogger(__name__)


def update_model_dropdown(llm_provider):
    """更新模型名称下拉列表"""
    if llm_provider in config.model_names:
        return gr.Dropdown(
            choices=config.model_names[llm_provider],
            value=config.model_names[llm_provider][0],
            interactive=True
        )
    else:
        return gr.Dropdown(choices=[], value="", interactive=True, allow_custom_value=True)


async def update_mcp_server(mcp_file: str, webui_manager: WebuiManager):
    """更新MCP服务器配置"""
    if hasattr(webui_manager, "bu_controller") and webui_manager.bu_controller:
        logger.warning("⚠️ Close controller because mcp file has changed!")
        await webui_manager.bu_controller.close_mcp_client()
        webui_manager.bu_controller = None

    if not mcp_file or not os.path.exists(mcp_file) or not mcp_file.endswith('.json'):
        logger.warning(f"{mcp_file} is not a valid MCP file.")
        return None, gr.update(visible=False)

    with open(mcp_file, 'r') as f:
        mcp_server = json.load(f)

    return json.dumps(mcp_server, indent=2), gr.update(visible=True)


def create_agent_settings_tab_v3(webui_manager: WebuiManager):
    """创建Agent配置页面 - V3优化版"""
    tab_components = {}

    # === 系统Prompt配置卡片 ===
    with gr.Group(elem_classes=["card"]):
        gr.Markdown("### 📝 系统Prompt配置")
        override_system_prompt = gr.Textbox(
            label="覆盖系统Prompt",
            lines=4,
            placeholder="输入自定义的系统提示词,将完全替换默认提示词...",
            interactive=True
        )
        extend_system_prompt = gr.Textbox(
            label="扩展系统Prompt",
            lines=4,
            placeholder="输入额外的提示词,将追加到默认提示词后面...",
            interactive=True
        )

    # === MCP服务器配置卡片 ===
    with gr.Group(elem_classes=["card"]):
        gr.Markdown("### 🔧 MCP服务器配置")
        mcp_json_file = gr.File(
            label="MCP配置文件",
            interactive=True,
            file_types=[".json"]
        )
        mcp_server_config = gr.Textbox(
            label="MCP服务器配置",
            lines=6,
            interactive=True,
            visible=False
        )

    # === 主LLM配置卡片 ===
    with gr.Group(elem_classes=["card"]):
        gr.Markdown("### 🤖 主LLM配置")
        
        with gr.Row():
            llm_provider = gr.Dropdown(
                choices=[provider for provider, model in config.model_names.items()],
                label="LLM Provider",
                value=os.getenv("DEFAULT_LLM", "openai"),
                info="选择LLM服务提供商",
                interactive=True
            )
            llm_model_name = gr.Dropdown(
                label="LLM Model",
                choices=config.model_names[os.getenv("DEFAULT_LLM", "openai")],
                value=config.model_names[os.getenv("DEFAULT_LLM", "openai")][0],
                interactive=True,
                allow_custom_value=True,
                info="选择模型或输入自定义模型名称"
            )
        
        with gr.Row():
            llm_temperature = gr.Slider(
                minimum=0.0,
                maximum=2.0,
                value=0.6,
                step=0.1,
                label="Temperature",
                info="控制模型输出的随机性 (0=确定性, 2=高随机性)",
                interactive=True
            )
            use_vision = gr.Checkbox(
                label="启用Vision",
                value=True,
                info="将高亮截图输入LLM进行视觉分析",
                interactive=True
            )
            ollama_num_ctx = gr.Slider(
                minimum=2 ** 8,
                maximum=2 ** 16,
                value=16000,
                step=1,
                label="Ollama上下文长度",
                info="控制最大上下文长度(越小越快)",
                visible=False,
                interactive=True
            )

        with gr.Row():
            llm_base_url = gr.Textbox(
                label="Base URL",
                value="",
                placeholder="https://api.openai.com/v1",
                info="API端点URL(可选)"
            )
            llm_api_key = gr.Textbox(
                label="API Key",
                type="password",
                value="",
                placeholder="sk-...",
                info="API密钥(留空使用.env配置)"
            )

    # === Planner LLM配置卡片 ===
    with gr.Group(elem_classes=["card"]):
        gr.Markdown("### 🎯 Planner LLM配置")
        gr.Markdown("*可选:为规划任务配置独立的LLM模型*")
        
        with gr.Row():
            planner_llm_provider = gr.Dropdown(
                choices=[provider for provider, model in config.model_names.items()],
                label="Planner LLM Provider",
                info="选择规划器LLM服务提供商",
                value=None,
                interactive=True
            )
            planner_llm_model_name = gr.Dropdown(
                label="Planner LLM Model",
                interactive=True,
                allow_custom_value=True,
                info="选择模型或输入自定义模型名称"
            )
        
        with gr.Row():
            planner_llm_temperature = gr.Slider(
                minimum=0.0,
                maximum=2.0,
                value=0.6,
                step=0.1,
                label="Temperature",
                info="控制规划器模型的随机性",
                interactive=True
            )
            planner_use_vision = gr.Checkbox(
                label="启用Vision(Planner)",
                value=False,
                info="为规划器启用视觉分析",
                interactive=True
            )
            planner_ollama_num_ctx = gr.Slider(
                minimum=2 ** 8,
                maximum=2 ** 16,
                value=16000,
                step=1,
                label="Ollama上下文长度",
                info="控制最大上下文长度",
                visible=False,
                interactive=True
            )

        with gr.Row():
            planner_llm_base_url = gr.Textbox(
                label="Base URL",
                value="",
                placeholder="https://api.openai.com/v1",
                info="API端点URL(可选)"
            )
            planner_llm_api_key = gr.Textbox(
                label="API Key",
                type="password",
                value="",
                placeholder="sk-...",
                info="API密钥(留空使用.env配置)"
            )

    # === Agent参数配置卡片 ===
    with gr.Group(elem_classes=["card"]):
        gr.Markdown("### ⚡ Agent执行参数")
        
        with gr.Row():
            max_steps = gr.Slider(
                minimum=1,
                maximum=1000,
                value=30,
                step=1,
                label="最大执行步数",
                info="Agent执行的最大步数(步数熔断阈值)",
                interactive=True
            )
            max_actions = gr.Slider(
                minimum=1,
                maximum=100,
                value=10,
                step=1,
                label="每步最大动作数",
                info="每个步骤中Agent可执行的最大动作数",
                interactive=True
            )

        with gr.Row():
            max_input_tokens = gr.Number(
                label="最大输入Token数",
                value=128000,
                precision=0,
                info="限制输入Token数量",
                interactive=True
            )
            tool_calling_method = gr.Dropdown(
                label="工具调用方法",
                value="auto",
                interactive=True,
                allow_custom_value=True,
                choices=['function_calling', 'json_mode', 'raw', 'auto', 'tools', "None"],
                info="选择工具调用的方式",
                visible=True
            )

    # 注册组件到manager
    tab_components.update(dict(
        override_system_prompt=override_system_prompt,
        extend_system_prompt=extend_system_prompt,
        llm_provider=llm_provider,
        llm_model_name=llm_model_name,
        llm_temperature=llm_temperature,
        use_vision=use_vision,
        ollama_num_ctx=ollama_num_ctx,
        llm_base_url=llm_base_url,
        llm_api_key=llm_api_key,
        planner_llm_provider=planner_llm_provider,
        planner_llm_model_name=planner_llm_model_name,
        planner_llm_temperature=planner_llm_temperature,
        planner_use_vision=planner_use_vision,
        planner_ollama_num_ctx=planner_ollama_num_ctx,
        planner_llm_base_url=planner_llm_base_url,
        planner_llm_api_key=planner_llm_api_key,
        max_steps=max_steps,
        max_actions=max_actions,
        max_input_tokens=max_input_tokens,
        tool_calling_method=tool_calling_method,
        mcp_json_file=mcp_json_file,
        mcp_server_config=mcp_server_config,
    ))
    webui_manager.add_components("agent_settings", tab_components)

    # === 事件绑定 ===
    # LLM Provider变化时更新Ollama上下文长度可见性
    llm_provider.change(
        fn=lambda x: gr.update(visible=x == "ollama"),
        inputs=llm_provider,
        outputs=ollama_num_ctx
    )
    # LLM Provider变化时更新模型下拉列表
    llm_provider.change(
        lambda provider: update_model_dropdown(provider),
        inputs=[llm_provider],
        outputs=[llm_model_name]
    )
    
    # Planner LLM Provider变化时更新Ollama上下文长度可见性
    planner_llm_provider.change(
        fn=lambda x: gr.update(visible=x == "ollama"),
        inputs=[planner_llm_provider],
        outputs=[planner_ollama_num_ctx]
    )
    # Planner LLM Provider变化时更新模型下拉列表
    planner_llm_provider.change(
        lambda provider: update_model_dropdown(provider),
        inputs=[planner_llm_provider],
        outputs=[planner_llm_model_name]
    )

    # MCP配置文件变化时更新配置显示
    async def update_wrapper(mcp_file):
        """MCP配置更新包装函数"""
        update_dict = await update_mcp_server(mcp_file, webui_manager)
        yield update_dict

    mcp_json_file.change(
        update_wrapper,
        inputs=[mcp_json_file],
        outputs=[mcp_server_config, mcp_server_config]
    )
