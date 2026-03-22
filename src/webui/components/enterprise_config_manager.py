"""
Enterprise Config Manager Component
企业级配置管理组件
"""

import os
import json
import glob
from datetime import datetime
import gradio as gr
from typing import Literal, List, Tuple

from src.webui.webui_manager import WebuiManager


def get_config_history(save_dir: str = "./tmp/webui_settings", limit: int = 5) -> List[Tuple[str, str, str]]:
    """获取配置历史记录"""
    if not os.path.exists(save_dir):
        return []
    
    config_files = glob.glob(os.path.join(save_dir, "*.json"))
    config_files.sort(key=os.path.getmtime, reverse=True)
    
    history = []
    for filepath in config_files[:limit]:
        filename = os.path.basename(filepath)
        # Parse timestamp from filename (format: YYYYMMDD-HHMMSS.json)
        try:
            timestamp = filename.replace(".json", "")
            dt = datetime.strptime(timestamp, "%Y%m%d-%H%M%S")
            display_time = dt.strftime("%Y-%m-%d %H:%M")
        except:
            display_time = filename
        
        # Try to get config name from content
        config_name = "未命名配置"
        try:
            with open(filepath, 'r') as f:
                content = json.load(f)
                # Try to find a name from provider settings
                if "agent_settings.llm_provider" in content:
                    provider = content.get("agent_settings.llm_provider", "")
                    model = content.get("agent_settings.llm_model_name", "")
                    if provider and model:
                        config_name = f"{provider}-{model}"
        except:
            pass
        
        history.append((config_name, display_time, filepath))
    
    return history


def format_config_list(history: List[Tuple[str, str, str]], lang: str = "zh") -> str:
    """格式化配置列表为 Markdown"""
    if not history:
        return "暂无保存的配置" if lang == "zh" else "No saved configurations"
    
    items = []
    for name, time, path in history:
        items.append(f"• **{name}** · {time}")
    
    return "\n".join(items)


def create_enterprise_config_manager(ui_manager: WebuiManager, lang: Literal["zh", "en"] = "zh"):
    """创建企业级配置管理界面"""
    
    texts = {
        "zh": {
            "title": "配置管理",
            "subtitle": "保存和加载界面配置",
            "history_title": "📚 配置历史",
            "history_empty": "暂无保存的配置",
            "history_desc": "最近保存的配置文件",
            "load_title": "📂 从文件加载",
            "save_title": "💾 保存当前配置",
            "config_name": "配置名称",
            "config_name_placeholder": "输入配置名称（可选）...",
            "select_file": "选择配置文件",
            "load_btn": "加载配置",
            "save_btn": "保存配置",
            "status": "状态",
            "status_ready": "就绪",
            "load_success": "✅ 配置加载成功",
            "save_success": "✅ 配置保存成功",
            "file_required": "请选择配置文件",
            "save_path": "保存路径",
            "refresh_btn": "🔄 刷新列表",
        },
        "en": {
            "title": "Config Manager",
            "subtitle": "Save and load UI configurations",
            "history_title": "📚 Config History",
            "history_empty": "No saved configurations",
            "history_desc": "Recently saved configuration files",
            "load_title": "📂 Load from File",
            "save_title": "💾 Save Current Config",
            "config_name": "Config Name",
            "config_name_placeholder": "Enter config name (optional)...",
            "select_file": "Select Config File",
            "load_btn": "Load Config",
            "save_btn": "Save Config",
            "status": "Status",
            "status_ready": "Ready",
            "load_success": "✅ Config loaded successfully",
            "save_success": "✅ Config saved successfully",
            "file_required": "Please select a config file",
            "save_path": "Save Path",
            "refresh_btn": "🔄 Refresh List",
        }
    }
    
    t = texts[lang]
    tab_components = {}
    
    # Get initial config history
    config_history = get_config_history()
    config_list_md = format_config_list(config_history, lang)
    
    with gr.Column(elem_classes=["ep-content"]):
        
        # ==================== Config History Card ====================
        with gr.Column(elem_classes=["ep-card", "ep-mb-4"]):
            with gr.Row(elem_classes=["ep-card-header"]):
                gr.Markdown(f"**{t['history_title']}**")
                refresh_btn = gr.Button(
                    t["refresh_btn"],
                    size="sm",
                    elem_classes=["ep-btn", "ep-btn-sm", "ep-btn-ghost"]
                )
            
            with gr.Column(elem_classes=["ep-card-body"]):
                gr.Markdown(f"<span class='ep-text-xs ep-text-gray'>{t['history_desc']}</span>")
                config_list_display = gr.Markdown(
                    value=config_list_md,
                    elem_classes=["ep-config-list"]
                )
        
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
                with gr.Row():
                    with gr.Column(scale=2):
                        config_name_input = gr.Textbox(
                            label=t["config_name"],
                            placeholder=t["config_name_placeholder"],
                            elem_classes=["ep-input"]
                        )
                    with gr.Column(scale=1):
                        gr.Markdown("")  # Spacer
                        save_config_button = gr.Button(
                            t["save_btn"],
                            variant="primary",
                            elem_classes=["ep-btn", "ep-btn-primary"]
                        )
                
                with gr.Row():
                    gr.Markdown(f"<span class='ep-text-xs ep-text-gray'>{t['save_path']}: `./tmp/webui_settings/`</span>")
        
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
        "config_name_input": config_name_input,
    })
    
    ui_manager.add_components("load_save_config", tab_components)
    
    # Custom save function with name support
    def save_config_with_name(components: dict, config_name: str = "") -> str:
        """Save config with optional name"""
        # Generate filename with optional name
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        if config_name.strip():
            # Sanitize name for filesystem
            safe_name = "".join(c for c in config_name.strip() if c.isalnum() or c in "-_ ").replace(" ", "_")
            filename = f"{timestamp}_{safe_name}.json"
        else:
            filename = f"{timestamp}.json"
        
        # Get current settings from all components
        cur_settings = {}
        for comp in components:
            if not isinstance(comp, gr.Button) and not isinstance(comp, gr.File):
                try:
                    comp_id = ui_manager.get_id_by_component(comp)
                    cur_settings[comp_id] = components[comp]
                except:
                    pass
        
        # Add metadata
        save_data = {
            "_metadata": {
                "saved_at": timestamp,
                "name": config_name.strip() or "Unnamed",
                "version": "1.0"
            },
            "settings": cur_settings
        }
        
        save_path = os.path.join("./tmp/webui_settings", filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        with open(save_path, "w") as fw:
            json.dump(save_data, fw, indent=4, ensure_ascii=False)
        
        return f"✅ {t['save_success']}: {filename}"
    
    # Refresh config list function
    def refresh_config_list():
        history = get_config_history()
        md = format_config_list(history, lang)
        return md
    
    # Connect events
    save_config_button.click(
        fn=lambda *args: save_config_with_name(
            {comp: val for comp, val in zip(ui_manager.get_components(), args[:-1])},
            args[-1]
        ),
        inputs=list(ui_manager.get_components()) + [config_name_input],
        outputs=[config_status]
    ).then(
        fn=refresh_config_list,
        outputs=[config_list_display]
    )
    
    load_config_button.click(
        fn=ui_manager.load_config,
        inputs=[config_file],
        outputs=ui_manager.get_components()
    )
    
    refresh_btn.click(
        fn=refresh_config_list,
        outputs=[config_list_display]
    )
