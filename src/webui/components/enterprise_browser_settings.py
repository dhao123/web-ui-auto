"""
Enterprise Browser Settings Component
企业级浏览器配置组件
"""

import os
from distutils.util import strtobool
import gradio as gr
from typing import Literal

from src.webui.webui_manager import WebuiManager


def create_enterprise_browser_settings(ui_manager: WebuiManager, lang: Literal["zh", "en"] = "zh"):
    """创建企业级浏览器配置界面"""
    
    texts = {
        "zh": {
            "title": "浏览器配置",
            "subtitle": "配置浏览器实例和行为",
            "basic_config": "🔧 基础配置",
            "advanced_config": "⚙️ 高级配置",
            "save_config": "💾 保存配置",
            "window_config": "📐 窗口配置",
            "remote_config": "🌐 远程连接配置",
            "browser_path": "浏览器路径",
            "user_data": "用户数据目录",
            "use_own": "使用自有浏览器",
            "keep_open": "保持浏览器打开",
            "headless": "无头模式",
            "disable_security": "禁用安全策略",
            "window_width": "窗口宽度",
            "window_height": "窗口高度",
            "cdp_url": "CDP 调试 URL",
            "wss_url": "WSS 调试 URL",
            "recording_path": "录制保存路径",
            "trace_path": "Trace 保存路径",
            "history_path": "历史记录路径",
            "download_path": "下载文件路径",
            "hints": {
                "use_own": "使用本地已安装的浏览器实例",
                "keep_open": "任务完成后保持浏览器打开",
                "headless": "在后台运行，不显示界面",
                "disable_security": "禁用 CORS 和 CSP 策略（仅用于测试）",
            }
        },
        "en": {
            "title": "Browser Settings",
            "subtitle": "Configure browser instance and behavior",
            "basic_config": "🔧 Basic Configuration",
            "advanced_config": "⚙️ Advanced Configuration",
            "save_config": "💾 Save Configuration",
            "window_config": "📐 Window Configuration",
            "remote_config": "🌐 Remote Connection",
            "browser_path": "Browser Path",
            "user_data": "User Data Directory",
            "use_own": "Use Own Browser",
            "keep_open": "Keep Browser Open",
            "headless": "Headless Mode",
            "disable_security": "Disable Security",
            "window_width": "Window Width",
            "window_height": "Window Height",
            "cdp_url": "CDP Debug URL",
            "wss_url": "WSS Debug URL",
            "recording_path": "Recording Path",
            "trace_path": "Trace Path",
            "history_path": "History Path",
            "download_path": "Download Path",
            "hints": {
                "use_own": "Use locally installed browser instance",
                "keep_open": "Keep browser open after task completion",
                "headless": "Run in background without GUI",
                "disable_security": "Disable CORS and CSP (testing only)",
            }
        }
    }
    
    t = texts[lang]
    tab_components = {}
    
    with gr.Column(elem_classes=["ep-content"]):
        
        # ==================== Basic Configuration Card ====================
        with gr.Column(elem_classes=["ep-card", "ep-mb-4"]):
            with gr.Row(elem_classes=["ep-card-header"]):
                gr.Markdown(f"**{t['basic_config']}**")
            
            with gr.Column(elem_classes=["ep-card-body"]):
                # Browser paths
                with gr.Row():
                    with gr.Column(scale=1):
                        browser_binary_path = gr.Textbox(
                            label=t["browser_path"],
                            placeholder="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                            elem_classes=["ep-input"]
                        )
                    with gr.Column(scale=1):
                        browser_user_data_dir = gr.Textbox(
                            label=t["user_data"],
                            placeholder="/Users/username/Library/Application Support/Google/Chrome",
                            elem_classes=["ep-input"]
                        )
                
                # Checkboxes
                with gr.Row():
                    with gr.Column(scale=1):
                        use_own_browser = gr.Checkbox(
                            label=t["use_own"],
                            value=bool(strtobool(os.getenv("USE_OWN_BROWSER", "false"))),
                            elem_classes=["ep-checkbox"]
                        )
                        gr.Markdown(f"<span class='ep-text-xs ep-text-gray'>{t['hints']['use_own']}</span>")
                    with gr.Column(scale=1):
                        keep_browser_open = gr.Checkbox(
                            label=t["keep_open"],
                            value=bool(strtobool(os.getenv("KEEP_BROWSER_OPEN", "true"))),
                            elem_classes=["ep-checkbox"]
                        )
                        gr.Markdown(f"<span class='ep-text-xs ep-text-gray'>{t['hints']['keep_open']}</span>")
                    with gr.Column(scale=1):
                        headless = gr.Checkbox(
                            label=t["headless"],
                            value=False,
                            elem_classes=["ep-checkbox"]
                        )
                        gr.Markdown(f"<span class='ep-text-xs ep-text-gray'>{t['hints']['headless']}</span>")
                    with gr.Column(scale=1):
                        disable_security = gr.Checkbox(
                            label=t["disable_security"],
                            value=False,
                            elem_classes=["ep-checkbox"]
                        )
                        gr.Markdown(f"<span class='ep-text-xs ep-text-gray'>{t['hints']['disable_security']}</span>")
        
        # ==================== Window Configuration Card ====================
        with gr.Column(elem_classes=["ep-card", "ep-mb-4"]):
            with gr.Row(elem_classes=["ep-card-header"]):
                gr.Markdown(f"**{t['window_config']}**")
            
            with gr.Column(elem_classes=["ep-card-body"]):
                with gr.Row():
                    with gr.Column(scale=1):
                        window_w = gr.Number(
                            label=t["window_width"],
                            value=1280,
                            precision=0,
                            elem_classes=["ep-input"]
                        )
                    with gr.Column(scale=1):
                        window_h = gr.Number(
                            label=t["window_height"],
                            value=1100,
                            precision=0,
                            elem_classes=["ep-input"]
                        )
        
        # ==================== Remote Connection Card ====================
        with gr.Column(elem_classes=["ep-card", "ep-mb-4"]):
            with gr.Row(elem_classes=["ep-card-header"]):
                gr.Markdown(f"**{t['remote_config']}** (可选)")
            
            with gr.Column(elem_classes=["ep-card-body"]):
                with gr.Row():
                    with gr.Column(scale=1):
                        cdp_url = gr.Textbox(
                            label=t["cdp_url"],
                            value=os.getenv("BROWSER_CDP", ""),
                            placeholder="http://localhost:9222",
                            elem_classes=["ep-input"]
                        )
                    with gr.Column(scale=1):
                        wss_url = gr.Textbox(
                            label=t["wss_url"],
                            placeholder="ws://localhost:9222/devtools/page/...",
                            elem_classes=["ep-input"]
                        )
        
        # ==================== Save Configuration Card ====================
        with gr.Column(elem_classes=["ep-card"]):
            with gr.Row(elem_classes=["ep-card-header"]):
                gr.Markdown(f"**{t['save_config']}**")
            
            with gr.Column(elem_classes=["ep-card-body"]):
                with gr.Row():
                    with gr.Column(scale=1):
                        save_recording_path = gr.Textbox(
                            label=t["recording_path"],
                            placeholder="./tmp/recordings",
                            elem_classes=["ep-input"]
                        )
                    with gr.Column(scale=1):
                        save_trace_path = gr.Textbox(
                            label=t["trace_path"],
                            placeholder="./tmp/traces",
                            elem_classes=["ep-input"]
                        )
                
                with gr.Row():
                    with gr.Column(scale=1):
                        save_agent_history_path = gr.Textbox(
                            label=t["history_path"],
                            value="./tmp/agent_history",
                            elem_classes=["ep-input"]
                        )
                    with gr.Column(scale=1):
                        save_download_path = gr.Textbox(
                            label=t["download_path"],
                            value="./tmp/downloads",
                            elem_classes=["ep-input"]
                        )
    
    # Store components
    tab_components.update({
        "browser_binary_path": browser_binary_path,
        "browser_user_data_dir": browser_user_data_dir,
        "use_own_browser": use_own_browser,
        "keep_browser_open": keep_browser_open,
        "headless": headless,
        "disable_security": disable_security,
        "window_w": window_w,
        "window_h": window_h,
        "cdp_url": cdp_url,
        "wss_url": wss_url,
        "save_recording_path": save_recording_path,
        "save_trace_path": save_trace_path,
        "save_agent_history_path": save_agent_history_path,
        "save_download_path": save_download_path,
    })
    
    ui_manager.add_components("browser_settings", tab_components)
    
    # Event handlers - close browser when critical settings change
    async def close_browser():
        if ui_manager.bu_current_task and not ui_manager.bu_current_task.done():
            ui_manager.bu_current_task.cancel()
            ui_manager.bu_current_task = None
        
        if ui_manager.bu_browser_context:
            await ui_manager.bu_browser_context.close()
            ui_manager.bu_browser_context = None
        
        if ui_manager.bu_browser:
            await ui_manager.bu_browser.close()
            ui_manager.bu_browser = None
    
    headless.change(fn=close_browser, inputs=None, outputs=None)
    keep_browser_open.change(fn=close_browser, inputs=None, outputs=None)
    disable_security.change(fn=close_browser, inputs=None, outputs=None)
    use_own_browser.change(fn=close_browser, inputs=None, outputs=None)
