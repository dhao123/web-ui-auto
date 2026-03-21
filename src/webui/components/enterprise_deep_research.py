"""
Enterprise Deep Research Component
企业级深度研究组件
"""

import gradio as gr
from typing import Literal

from src.webui.webui_manager import WebuiManager


def create_enterprise_deep_research(ui_manager: WebuiManager, lang: Literal["zh", "en"] = "zh"):
    """创建企业级深度研究界面"""
    
    texts = {
        "zh": {
            "title": "深度研究",
            "subtitle": "执行深度研究任务",
            "task_input": "📝 研究任务",
            "placeholder": "输入研究主题，例如：瑞士 6 月 1-10 日的详细旅行计划...",
            "resume_task": "恢复任务 ID",
            "parallel": "并行代理数",
            "save_dir": "保存目录",
            "run": "▶ 开始研究",
            "stop": "⏹ 停止",
            "report": "📄 研究报告",
            "download": "下载报告",
            "mcp_config": "🔌 MCP 配置",
            "mcp_file": "MCP 配置文件",
        },
        "en": {
            "title": "Deep Research",
            "subtitle": "Execute deep research tasks",
            "task_input": "📝 Research Task",
            "placeholder": "Enter research topic, e.g., Detailed travel plan to Switzerland from June 1-10...",
            "resume_task": "Resume Task ID",
            "parallel": "Parallel Agents",
            "save_dir": "Save Directory",
            "run": "▶ Start Research",
            "stop": "⏹ Stop",
            "report": "📄 Research Report",
            "download": "Download Report",
            "mcp_config": "🔌 MCP Config",
            "mcp_file": "MCP Config File",
        }
    }
    
    t = texts[lang]
    tab_components = {}
    
    # Initialize deep research agent
    ui_manager.init_deep_research_agent()
    
    with gr.Column(elem_classes=["ep-content"]):
        
        # ==================== MCP Config ====================
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
                            lines=4,
                            visible=False,
                            elem_classes=["ep-input"]
                        )
        
        # ==================== Task Input ====================
        with gr.Column(elem_classes=["ep-card", "ep-mb-4"]):
            with gr.Row(elem_classes=["ep-card-header"]):
                gr.Markdown(f"**{t['task_input']}**")
            
            with gr.Column(elem_classes=["ep-card-body"]):
                research_task = gr.Textbox(
                    label="",
                    placeholder=t["placeholder"],
                    lines=5,
                    elem_classes=["ep-input", "ep-textarea-lg"]
                )
                
                with gr.Row():
                    with gr.Column(scale=1):
                        resume_task_id = gr.Textbox(
                            label=t["resume_task"],
                            placeholder="输入之前的任务 ID 以恢复",
                            elem_classes=["ep-input"]
                        )
                    with gr.Column(scale=1):
                        parallel_num = gr.Number(
                            label=t["parallel"],
                            value=1,
                            precision=0,
                            minimum=1,
                            maximum=10,
                            elem_classes=["ep-input"]
                        )
                    with gr.Column(scale=1):
                        max_query = gr.Textbox(
                            label=t["save_dir"],
                            value="./tmp/deep_research",
                            elem_classes=["ep-input"]
                        )
                
                with gr.Row():
                    stop_button = gr.Button(
                        t["stop"],
                        variant="stop",
                        interactive=False,
                        elem_classes=["ep-btn", "ep-btn-danger"]
                    )
                    start_button = gr.Button(
                        t["run"],
                        variant="primary",
                        elem_classes=["ep-btn", "ep-btn-primary", "ep-btn-lg"]
                    )
        
        # ==================== Report Output ====================
        with gr.Column(elem_classes=["ep-card"]):
            with gr.Row(elem_classes=["ep-card-header"]):
                gr.Markdown(f"**{t['report']}**")
            
            with gr.Column(elem_classes=["ep-card-body"]):
                markdown_display = gr.Markdown(
                    label="",
                    value="*研究报告将在此显示*"
                )
                markdown_download = gr.File(
                    label=t["download"],
                    interactive=False
                )
    
    # Store components
    tab_components.update({
        "research_task": research_task,
        "resume_task_id": resume_task_id,
        "parallel_num": parallel_num,
        "max_query": max_query,
        "start_button": start_button,
        "stop_button": stop_button,
        "markdown_display": markdown_display,
        "markdown_download": markdown_download,
        "mcp_json_file": mcp_json_file,
        "mcp_server_config": mcp_server_config,
    })
    
    ui_manager.add_components("deep_research_agent", tab_components)
    
    # Import and connect event handlers
    from src.webui.components.deep_research_agent_tab import (
        run_deep_research, stop_deep_research, update_mcp_server
    )
    from typing import Dict, Any, AsyncGenerator
    from gradio.components import Component
    import json
    
    dr_tab_outputs = list(tab_components.values())
    all_managed_inputs = set(ui_manager.get_components())
    
    async def start_wrapper(comps: Dict[Component, Any]) -> AsyncGenerator[Dict[Component, Any], None]:
        async for update in run_deep_research(ui_manager, comps):
            yield update
    
    async def stop_wrapper() -> AsyncGenerator[Dict[Component, Any], None]:
        update_dict = await stop_deep_research(ui_manager)
        yield update_dict
    
    async def update_mcp_wrapper(mcp_file):
        if hasattr(ui_manager, "dr_agent") and ui_manager.dr_agent:
            await ui_manager.dr_agent.close_mcp_client()
        
        if not mcp_file:
            return None, gr.update(visible=False)
        
        try:
            import os
            if not os.path.exists(mcp_file) or not mcp_file.endswith('.json'):
                return None, gr.update(visible=False)
            with open(mcp_file, 'r') as f:
                mcp_server = json.load(f)
            return json.dumps(mcp_server, indent=2), gr.update(visible=True)
        except Exception as e:
            return f"Error: {e}", gr.update(visible=False)
    
    # Connect events
    start_button.click(
        fn=start_wrapper,
        inputs=all_managed_inputs,
        outputs=dr_tab_outputs
    )
    stop_button.click(
        fn=stop_wrapper,
        inputs=None,
        outputs=dr_tab_outputs
    )
    mcp_json_file.change(
        fn=update_mcp_wrapper,
        inputs=mcp_json_file,
        outputs=[mcp_server_config, mcp_server_config]
    )
