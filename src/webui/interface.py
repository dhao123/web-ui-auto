import gradio as gr

from src.webui.webui_manager import WebuiManager
from src.webui.components.agent_settings_tab import create_agent_settings_tab
from src.webui.components.browser_settings_tab import create_browser_settings_tab
from src.webui.components.browser_use_agent_tab import create_browser_use_agent_tab
from src.webui.components.deep_research_agent_tab import create_deep_research_agent_tab
from src.webui.components.load_save_config_tab import create_load_save_config_tab

theme_map = {
    "Default": gr.themes.Default(),
    "Soft": gr.themes.Soft(),
    "Monochrome": gr.themes.Monochrome(),
    "Glass": gr.themes.Glass(),
    "Origin": gr.themes.Origin(),
    "Citrus": gr.themes.Citrus(),
    "Ocean": gr.themes.Ocean(),
    "Base": gr.themes.Base()
}


def create_ui(theme_name="Ocean"):
    css = """
    /* 全局容器样式 - 参考AI测试者平台 */
    .gradio-container {
        width: 90vw !important; 
        max-width: 90% !important; 
        margin-left: auto !important;
        margin-right: auto !important;
        padding-top: 10px !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    /* 头部样式 */
    .header-text {
        text-align: center;
        margin-bottom: 20px;
        color: white !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .header-text h1 {
        font-size: 2.5em !important;
        font-weight: 700 !important;
        margin-bottom: 10px !important;
    }
    
    .header-text h3 {
        font-size: 1.2em !important;
        font-weight: 400 !important;
        opacity: 0.9;
    }
    
    /* Tab样式 - 浅色背景 */
    .tab-nav {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 12px !important;
        padding: 8px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }
    
    .tab-nav button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .tab-nav button.selected {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    /* 卡片样式 */
    .metric-card {
        background: white !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
        margin-bottom: 16px !important;
        border: 1px solid #e5e7eb !important;
        transition: all 0.3s ease !important;
        height: 180px !important;  /* 使用固定高度而不是min-height */
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important;
        overflow: hidden !important;  /* 防止内容溢出 */
    }
    
    .metric-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.12) !important;
        transform: translateY(-2px) !important;
    }
    
    .metric-card h3 {
        color: #667eea !important;
        font-weight: 700 !important;
        margin-bottom: 12px !important;
        font-size: 16px !important;  /* 减小标题字体 */
        line-height: 1.2 !important;  /* 紧凑行高 */
    }
    
    .metric-card strong {
        color: #667eea !important;
        font-weight: 600 !important;
    }
    
    .metric-card ul {
        list-style: none !important;
        padding-left: 0 !important;
        margin: 0 !important;
    }
    
    .metric-card li {
        padding: 4px 0 !important;
        color: #374151 !important;
        line-height: 1.6 !important;
    }
    
    /* 确保Row中的Column高度一致 */
    .gr-row {
        align-items: stretch !important;
    }
    
    .gr-column {
        display: flex !important;
        flex-direction: column !important;
    }
    
    /* 指标卡片 - 不同颜色 */
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 16px !important;
        margin: 8px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }
    
    .stats-card-success {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%) !important;
    }
    
    .stats-card-warning {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%) !important;
    }
    
    .stats-card-info {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%) !important;
    }
    
    /* 按钮样式 */
    .btn-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 8px !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .btn-primary:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* 输入框样式 */
    .input-modern {
        border-radius: 8px !important;
        border: 2px solid #e5e7eb !important;
        padding: 12px !important;
        transition: all 0.3s ease !important;
        background: white !important;
    }
    
    .input-modern:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Chatbot样式 */
    #browser_use_chatbot {
        border-radius: 12px !important;
        border: 1px solid #e5e7eb !important;
        background: white !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
    }
    
    /* Group样式 */
    .gr-group {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
        border: 1px solid #e5e7eb !important;
        margin-bottom: 16px !important;
    }
    
    /* Slider样式 */
    .gr-slider input[type="range"] {
        accent-color: #667eea !important;
    }
    
    /* Dropdown样式 */
    .gr-dropdown {
        border-radius: 8px !important;
        border: 2px solid #e5e7eb !important;
    }
    
    /* 侧边栏样式 */
    .sidebar {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
    }
    
    /* 文件上传区域 */
    .gr-file {
        border-radius: 8px !important;
        border: 2px dashed #e5e7eb !important;
        background: white !important;
    }
    
    /* Markdown内容样式 */
    .markdown-text {
        line-height: 1.6 !important;
        color: #374151 !important;
    }
    
    .markdown-text strong {
        color: #667eea !important;
    }
    
    /* 浏览器视图和历史记录的标题样式 - 更紧凑 */
    .markdown-text h3 {
        font-size: 16px !important;
        font-weight: 600 !important;
        margin: 0 0 8px 0 !important;  /* 减小底部间距 */
        padding: 8px 12px !important;  /* 减小内边距 */
        color: #667eea !important;
        background: rgba(102, 126, 234, 0.05) !important;
        border-radius: 8px !important;
        line-height: 1.2 !important;
    }
    """

    # 移除dark mode强制设置，使用浅色主题
    js_func = """
    function refresh() {
        const url = new URL(window.location);
        // 移除dark mode，使用light mode
        if (url.searchParams.get('__theme') === 'dark') {
            url.searchParams.delete('__theme');
            window.location.href = url.href;
        }
    }
    """

    ui_manager = WebuiManager()

    with gr.Blocks(
            title="Browser Use WebUI", theme=theme_map[theme_name], css=css, js=js_func,
    ) as demo:
        with gr.Row():
            gr.Markdown(
                """
                # 🌐 AI测试平台 - Browser Use WebUI
                ### 智能浏览器自动化测试平台 | Control your browser with AI assistance
                """,
                elem_classes=["header-text"],
            )

        with gr.Tabs() as tabs:
            with gr.TabItem("⚙️ Agent Settings"):
                create_agent_settings_tab(ui_manager)

            with gr.TabItem("🌐 Browser Settings"):
                create_browser_settings_tab(ui_manager)

            with gr.TabItem("🤖 Run Agent"):
                create_browser_use_agent_tab(ui_manager)

            with gr.TabItem("🎁 Agent Marketplace"):
                gr.Markdown(
                    """
                    ### Agents built on Browser-Use
                    """,
                    elem_classes=["tab-header-text"],
                )
                with gr.Tabs():
                    with gr.TabItem("Deep Research"):
                        create_deep_research_agent_tab(ui_manager)

            with gr.TabItem("📁 Load & Save Config"):
                create_load_save_config_tab(ui_manager)

    return demo
