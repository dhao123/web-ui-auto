"""
浏览器配置组件 V3
基于ui-ux skill的企业级设计,使用卡片布局优化UI
"""
import os
from distutils.util import strtobool
import gradio as gr
import logging
from gradio.components import Component
from src.webui.webui_manager import WebuiManager
from src.utils import config

logger = logging.getLogger(__name__)


async def close_browser(webui_manager: WebuiManager):
    """关闭浏览器"""
    if webui_manager.bu_current_task and not webui_manager.bu_current_task.done():
        webui_manager.bu_current_task.cancel()
        webui_manager.bu_current_task = None

    if webui_manager.bu_browser_context:
        logger.info("⚠️ Closing browser context when changing browser config.")
        await webui_manager.bu_browser_context.close()
        webui_manager.bu_browser_context = None

    if webui_manager.bu_browser:
        logger.info("⚠️ Closing browser when changing browser config.")
        await webui_manager.bu_browser.close()
        webui_manager.bu_browser = None


def create_browser_settings_tab_v3(webui_manager: WebuiManager):
    """创建浏览器配置页面 - V3优化版"""
    tab_components = {}

    # === 浏览器路径配置卡片 ===
    with gr.Group(elem_classes=["card"]):
        gr.Markdown("### 📁 浏览器路径配置")
        with gr.Row():
            browser_binary_path = gr.Textbox(
                label="浏览器可执行文件路径",
                lines=1,
                interactive=True,
                placeholder="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            )
            browser_user_data_dir = gr.Textbox(
                label="用户数据目录",
                lines=1,
                interactive=True,
                placeholder="留空使用默认用户数据目录",
            )

    # === 浏览器基础配置卡片 ===
    with gr.Group(elem_classes=["card"]):
        gr.Markdown("### ⚙️ 浏览器基础配置")
        with gr.Row():
            use_own_browser = gr.Checkbox(
                label="使用已有浏览器",
                value=bool(strtobool(os.getenv("USE_OWN_BROWSER", "false"))),
                info="挂载到已启动的浏览器实例",
                interactive=True
            )
            keep_browser_open = gr.Checkbox(
                label="保持浏览器开启",
                value=bool(strtobool(os.getenv("KEEP_BROWSER_OPEN", "true"))),
                info="任务间保持浏览器开启",
                interactive=True
            )
            headless = gr.Checkbox(
                label="无头模式",
                value=True,
                info="后台运行浏览器(仅在实时视图显示)",
                interactive=True
            )
            disable_security = gr.Checkbox(
                label="禁用安全特性",
                value=False,
                info="禁用浏览器安全限制",
                interactive=True
            )

    # === 窗口尺寸配置卡片 ===
    with gr.Group(elem_classes=["card"]):
        gr.Markdown("### 📐 窗口尺寸配置")
        with gr.Row():
            window_w = gr.Number(
                label="窗口宽度",
                value=1280,
                info="浏览器窗口宽度(像素)",
                interactive=True
            )
            window_h = gr.Number(
                label="窗口高度",
                value=1100,
                info="浏览器窗口高度(像素)",
                interactive=True
            )

    # === 远程调试配置卡片 ===
    with gr.Group(elem_classes=["card"]):
        gr.Markdown("### 🔗 远程调试配置")
        with gr.Row():
            cdp_url = gr.Textbox(
                label="CDP URL",
                value=os.getenv("BROWSER_CDP", ""),
                placeholder="ws://localhost:9222/devtools/browser/...",
                info="Chrome DevTools Protocol URL",
                interactive=True,
            )
            wss_url = gr.Textbox(
                label="WSS URL",
                value=os.getenv("BROWSER_WSS", ""),
                placeholder="wss://chrome.browserless.io?token=...",
                info="WebSocket URL for remote browser",
                interactive=True,
            )

    # === 高级配置卡片 ===
    with gr.Group(elem_classes=["card"]):
        gr.Markdown("### 🔧 高级配置")
        
        with gr.Row():
            proxy = gr.Textbox(
                label="代理服务器",
                value="",
                placeholder="http://proxy.example.com:8080",
                info="HTTP/HTTPS代理配置",
                interactive=True
            )
            extra_chromium_args = gr.Textbox(
                label="额外Chromium参数",
                value="",
                placeholder="--arg1 --arg2=value",
                info="空格分隔的额外启动参数",
                interactive=True
            )
        
        with gr.Row():
            save_agent_history_path = gr.Textbox(
                label="Agent历史保存路径",
                value="tmp/agent_history",
                info="Agent执行历史JSON文件保存目录",
                interactive=True
            )
        
        with gr.Row():
            save_recording_path = gr.Textbox(
                label="录像保存路径",
                value="",
                placeholder="tmp/recordings",
                info="GIF录像文件保存目录(留空不录制)",
                interactive=True
            )
            save_trace_path = gr.Textbox(
                label="Trace保存路径",
                value="",
                placeholder="tmp/traces",
                info="Playwright trace文件保存目录(留空不记录)",
                interactive=True
            )
        
        with gr.Row():
            save_download_path = gr.Textbox(
                label="下载文件保存路径",
                value="tmp/downloads",
                info="浏览器下载文件保存目录",
                interactive=True
            )
            minimum_wait_page_load_time = gr.Number(
                label="最小页面加载等待时间(秒)",
                value=0.5,
                info="页面加载后的最小等待时间",
                interactive=True
            )

    # 注册组件到manager
    tab_components.update(dict(
        browser_binary_path=browser_binary_path,
        browser_user_data_dir=browser_user_data_dir,
        use_own_browser=use_own_browser,
        keep_browser_open=keep_browser_open,
        headless=headless,
        disable_security=disable_security,
        window_w=window_w,
        window_h=window_h,
        cdp_url=cdp_url,
        wss_url=wss_url,
        proxy=proxy,
        extra_chromium_args=extra_chromium_args,
        save_agent_history_path=save_agent_history_path,
        save_recording_path=save_recording_path,
        save_trace_path=save_trace_path,
        save_download_path=save_download_path,
        minimum_wait_page_load_time=minimum_wait_page_load_time,
    ))
    webui_manager.add_components("browser_settings", tab_components)

    # === 事件绑定 ===
    # 浏览器配置变化时关闭现有浏览器
    async def browser_config_changed_wrapper():
        """浏览器配置变化包装函数"""
        await close_browser(webui_manager)
        return gr.update()

    # 监听关键配置项变化
    for comp in [use_own_browser, headless, browser_binary_path, cdp_url, wss_url]:
        comp.change(
            browser_config_changed_wrapper,
            inputs=None,
            outputs=[]
        )
