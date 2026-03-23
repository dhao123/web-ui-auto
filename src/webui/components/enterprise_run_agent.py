"""
Enterprise Run Agent Component
企业级运行 Agent 组件 - 核心功能界面
"""

import gradio as gr
from typing import Literal

from src.webui.webui_manager import WebuiManager


def create_enterprise_run_agent(ui_manager: WebuiManager, lang: Literal["zh", "en"] = "zh"):
    """创建企业级运行 Agent 界面"""
    
    texts = {
        "zh": {
            "title": "运行任务",
            "subtitle": "运行浏览器自动化任务",
            "metrics": {
                "execution": "执行统计",
                "tokens": "Token 消耗",
                "retries": "重试统计",
                "status": "状态",
                "current_step": "当前步数",
                "max_steps": "最大步数",
                "duration": "总耗时",
                "avg_step": "平均步骤耗时",
                "prompt_tokens": "Prompt Tokens",
                "completion_tokens": "Completion Tokens",
                "total_tokens": "总 Token",
                "system_retries": "系统级重试",
                "business_retries": "业务级重试",
                "total_retries": "总重试",
                "waiting": "等待任务",
            },
            "task_input": "📝 任务输入",
            "placeholder": "输入您的任务指令，例如：打开 Google 并搜索最新的人工智能新闻...",
            "quick_tips": "💡 提示：按 Enter 快速提交任务",
            "submit": "▶ 提交任务",
            "stop": "⏹ 停止",
            "pause": "⏸ 暂停",
            "resume": "▶ 继续",
            "clear": "🗑 清空",
            "browser_view": "🌐 浏览器实时视图",
            "execution_log": "📋 执行日志",
            "outputs": "📁 任务输出",
            "history_file": "执行历史 JSON",
            "recording": "录制 GIF",
        },
        "en": {
            "title": "Run Task",
            "subtitle": "Execute browser automation tasks",
            "metrics": {
                "execution": "Execution Stats",
                "tokens": "Token Usage",
                "retries": "Retry Stats",
                "status": "Status",
                "current_step": "Current Step",
                "max_steps": "Max Steps",
                "duration": "Duration",
                "avg_step": "Avg Step Time",
                "prompt_tokens": "Prompt Tokens",
                "completion_tokens": "Completion Tokens",
                "total_tokens": "Total Tokens",
                "system_retries": "System Retries",
                "business_retries": "Business Retries",
                "total_retries": "Total Retries",
                "waiting": "Waiting",
            },
            "task_input": "📝 Task Input",
            "placeholder": "Enter your task, e.g., Open Google and search for latest AI news...",
            "quick_tips": "💡 Tip: Press Enter to submit quickly",
            "submit": "▶ Submit Task",
            "stop": "⏹ Stop",
            "pause": "⏸ Pause",
            "resume": "▶ Resume",
            "clear": "🗑 Clear",
            "browser_view": "🌐 Browser Live View",
            "execution_log": "📋 Execution Log",
            "outputs": "📁 Task Outputs",
            "history_file": "History JSON",
            "recording": "Recording GIF",
        }
    }
    
    t = texts[lang]
    tab_components = {}
    
    # Initialize agent
    ui_manager.init_browser_use_agent()
    
    with gr.Column(elem_classes=["ep-content"]):
        
        # ==================== Metrics Cards ====================
        with gr.Row(elem_classes=["ep-stats-grid", "ep-mb-4"]):
            # Execution Stats Card
            with gr.Column(scale=1, elem_classes=["ep-stat-card", "primary"]):
                with gr.Row(elem_classes=["ep-stat-header"]):
                    gr.Markdown(f"📊 **{t['metrics']['execution']}**")
                    gr.Markdown("⏱️", elem_classes=["ep-stat-icon"])
                metrics_execution = gr.Markdown(f"""
                <div class="ep-stat-label">{t['metrics']['status']}</div>
                <div class="ep-stat-value">{t['metrics']['waiting']}</div>
                <div class="ep-stat-desc">- / - {t['metrics']['current_step']}</div>
                """)
            
            # Token Usage Card
            with gr.Column(scale=1, elem_classes=["ep-stat-card", "info"]):
                with gr.Row(elem_classes=["ep-stat-header"]):
                    gr.Markdown(f"🔤 **{t['metrics']['tokens']}**")
                    gr.Markdown("🪙", elem_classes=["ep-stat-icon"])
                metrics_tokens = gr.Markdown(f"""
                <div class="ep-stat-label">Total</div>
                <div class="ep-stat-value">0</div>
                <div class="ep-stat-desc">0 / 0 tokens</div>
                """)
            
            # Retry Stats Card
            with gr.Column(scale=1, elem_classes=["ep-stat-card", "warning"]):
                with gr.Row(elem_classes=["ep-stat-header"]):
                    gr.Markdown(f"🔄 **{t['metrics']['retries']}**")
                    gr.Markdown("🔄", elem_classes=["ep-stat-icon"])
                metrics_retries = gr.Markdown(f"""
                <div class="ep-stat-label">Total</div>
                <div class="ep-stat-value">0</div>
                <div class="ep-stat-desc">0 / 0 retries</div>
                """)
        
        # ==================== Task Input Section ====================
        with gr.Column(elem_classes=["ep-card", "ep-mb-4"]):
            with gr.Row(elem_classes=["ep-card-header"]):
                gr.Markdown(f"**{t['task_input']}**")
            
            with gr.Column(elem_classes=["ep-card-body"]):
                user_input = gr.Textbox(
                    label="",
                    placeholder=t["placeholder"],
                    lines=3,
                    elem_classes=["ep-input", "ep-textarea-lg"]
                )
                gr.Markdown(f"<span class='ep-text-xs ep-text-gray' style='margin-top: -0.5rem; display: block;'>{t['quick_tips']}</span>")
                
                # Primary Button - Full Width
                run_button = gr.Button(
                    t["submit"],
                    variant="primary",
                    elem_classes=["ep-btn", "ep-btn-primary", "ep-btn-lg"]
                )
                
                # Secondary Actions Row
                with gr.Row():
                    stop_button = gr.Button(
                        t["stop"],
                        variant="stop",
                        interactive=False,
                        elem_classes=["ep-btn", "ep-btn-danger"]
                    )
                    pause_resume_button = gr.Button(
                        t["pause"],
                        interactive=False,
                        elem_classes=["ep-btn", "ep-btn-secondary"]
                    )
                    clear_button = gr.Button(
                        t["clear"],
                        elem_classes=["ep-btn", "ep-btn-secondary"]
                    )
        
        # ==================== Browser View & Logs ====================
        with gr.Row():
            # Browser View
            with gr.Column(scale=1):
                with gr.Column(elem_classes=["ep-card"]):
                    with gr.Row(elem_classes=["ep-card-header"]):
                        gr.Markdown(f"**{t['browser_view']}**")
                    
                    with gr.Column(elem_classes=["ep-card-body"]):
                        browser_view = gr.HTML(
                            value="""
                            <div class="ep-browser-frame">
                                <div class="ep-browser-header">
                                    <div class="ep-browser-dots">
                                        <span class="ep-browser-dot red"></span>
                                        <span class="ep-browser-dot yellow"></span>
                                        <span class="ep-browser-dot green"></span>
                                    </div>
                                    <div class="ep-browser-address">about:blank</div>
                                </div>
                                <div class="ep-browser-content">
                                    <div style="text-align: center; color: #94a3b8;">
                                        <div style="font-size: 32px; margin-bottom: 1rem;">🌐</div>
                                        <p>等待任务启动...</p>
                                    </div>
                                </div>
                            </div>
                            """,
                            elem_classes=["ep-browser-frame"]
                        )
            
            # Execution Log
            with gr.Column(scale=1):
                with gr.Column(elem_classes=["ep-card"]):
                    with gr.Row(elem_classes=["ep-card-header"]):
                        gr.Markdown(f"**{t['execution_log']}**")
                    
                    with gr.Column(elem_classes=["ep-card-body"]):
                        chatbot = gr.Chatbot(
                            label="",
                            type="messages",
                            height=500,
                            show_copy_button=True,
                            elem_classes=["ep-chat-messages"]
                        )
        
        # ==================== Task Outputs ====================
        with gr.Column(elem_classes=["ep-card"]):
            with gr.Row(elem_classes=["ep-card-header"]):
                gr.Markdown(f"**{t['outputs']}**")
            
            with gr.Column(elem_classes=["ep-card-body"]):
                with gr.Row():
                    with gr.Column(scale=1):
                        agent_history_file = gr.File(
                            label=t["history_file"],
                            interactive=False
                        )
                    with gr.Column(scale=1):
                        recording_gif = gr.Image(
                            label=t["recording"],
                            format="gif",
                            interactive=False
                        )
    
    # Store components
    tab_components.update({
        "chatbot": chatbot,
        "user_input": user_input,
        "run_button": run_button,
        "stop_button": stop_button,
        "pause_resume_button": pause_resume_button,
        "clear_button": clear_button,
        "browser_view": browser_view,
        "agent_history_file": agent_history_file,
        "recording_gif": recording_gif,
        "metrics_execution": metrics_execution,
        "metrics_tokens": metrics_tokens,
        "metrics_retries": metrics_retries,
    })
    
    ui_manager.add_components("browser_use_agent", tab_components)
    
    # Import and connect event handlers from original implementation
    from src.webui.components.browser_use_agent_tab import (
        handle_submit, handle_stop, handle_pause_resume, handle_clear
    )
    from typing import Dict, Any, AsyncGenerator
    from gradio.components import Component
    
    all_managed_components = set(ui_manager.get_components())
    run_tab_outputs = list(tab_components.values())
    
    async def submit_wrapper(
        components_dict: Dict[Component, Any]
    ) -> AsyncGenerator[Dict[Component, Any], None]:
        async for update in handle_submit(ui_manager, components_dict):
            yield update
    
    async def stop_wrapper() -> AsyncGenerator[Dict[Component, Any], None]:
        update_dict = await handle_stop(ui_manager)
        yield update_dict
    
    async def pause_resume_wrapper() -> AsyncGenerator[Dict[Component, Any], None]:
        update_dict = await handle_pause_resume(ui_manager)
        yield update_dict
    
    async def clear_wrapper() -> AsyncGenerator[Dict[Component, Any], None]:
        update_dict = await handle_clear(ui_manager)
        yield update_dict
    
    # Connect events
    run_button.click(
        fn=submit_wrapper,
        inputs=all_managed_components,
        outputs=run_tab_outputs,
        trigger_mode="multiple"
    )
    user_input.submit(
        fn=submit_wrapper,
        inputs=all_managed_components,
        outputs=run_tab_outputs
    )
    stop_button.click(fn=stop_wrapper, inputs=None, outputs=run_tab_outputs)
    pause_resume_button.click(fn=pause_resume_wrapper, inputs=None, outputs=run_tab_outputs)
    clear_button.click(fn=clear_wrapper, inputs=None, outputs=run_tab_outputs)
