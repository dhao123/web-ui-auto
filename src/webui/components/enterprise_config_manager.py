"""
Enterprise Config Manager Component
企业级配置管理组件
"""

import gradio as gr
from typing import Literal

from src.webui.webui_manager import WebuiManager


def create_enterprise_config_manager(ui_manager: WebuiManager, lang: Literal["zh", "en"] = "zh"):
    """创建企业级配置管理界面"""
    
    texts = {
        "zh": {
            "title": "配置管理",
            "subtitle": "保存和加载界面配置",
            "load_title": "📂 加载配置",
            "save_title": "💾 保存当前配置",
            "select_file": "选择配置文件",
            "load_btn": "加载配置",
            "save_btn": "保存配置",
            "status": "状态",
            "status_ready": "就绪",
            "load_success": "✅ 配置加载成功",
            "save_success": "✅ 配置保存成功",
            "file_required": "请选择配置文件",
        },
        "en": {
            "title": "Config Manager",
            "subtitle": "Save and load UI configurations",
            "load_title": "📂 Load Config",
            "save_title": "💾 Save Current Config",
            "select_file": "Select Config File",
            "load_btn": "Load Config",
            "save_btn": "Save Config",
            "status": "Status",
            "status_ready": "Ready",
            "load_success": "✅ Config loaded successfully",
            "save_success": "✅ Config saved successfully",
            "file_required": "Please select a config file",
        }
    }
    
    t = texts[lang]
    tab_components = {}
    
    with gr.Column(elem_classes=["ep-content"]):
        
        # ==================== Load Config Card ====================
        with gr.Column(elem_classes=["ep-card", "ep-mb-4"]):
            with gr.Row(elem_classes=["ep-card-header"]):
                gr.Markdown(f"**{t['load_title']}**")
            
            with gr.Column(elem_classes=["ep-card-body"]):
                with gr.Row():
                    with gr.Column(scale=2):
                        config_file = gr.File(
                            label=t["select_file"],
                            file_types=[".json"],
                            elem_classes=["ep-input"]
                        )
                    with gr.Column(scale=1):
                        gr.Markdown("")  # Spacer
                        load_config_button = gr.Button(
                            t["load_btn"],
                            variant="primary",
                            elem_classes=["ep-btn", "ep-btn-primary"]
                        )
        
        # ==================== Save Config Card ====================
        with gr.Column(elem_classes=["ep-card", "ep-mb-4"]):
            with gr.Row(elem_classes=["ep-card-header"]):
                gr.Markdown(f"**{t['save_title']}**")
            
            with gr.Column(elem_classes=["ep-card-body"]):
                save_config_button = gr.Button(
                    t["save_btn"],
                    variant="primary",
                    elem_classes=["ep-btn", "ep-btn-primary"]
                )
        
        # ==================== Status Card ====================
        with gr.Column(elem_classes=["ep-card"]):
            with gr.Row(elem_classes=["ep-card-header"]):
                gr.Markdown(f"**{t['status']}**")
            
            with gr.Column(elem_classes=["ep-card-body"]):
                config_status = gr.Textbox(
                    label="",
                    value=t["status_ready"],
                    interactive=False,
                    elem_classes=["ep-input"]
                )
    
    # Store components
    tab_components.update({
        "config_file": config_file,
        "load_config_button": load_config_button,
        "save_config_button": save_config_button,
        "config_status": config_status,
    })
    
    ui_manager.add_components("load_save_config", tab_components)
    
    # Connect events
    save_config_button.click(
        fn=ui_manager.save_config,
        inputs=set(ui_manager.get_components()),
        outputs=[config_status]
    )
    
    load_config_button.click(
        fn=ui_manager.load_config,
        inputs=[config_file],
        outputs=ui_manager.get_components()
    )
