"""
优化后的WebUI界面 - 采用左侧导航栏设计
参考UI/UX Skill设计规范 - 完全优化版本
"""
import gradio as gr
from src.webui.webui_manager import WebuiManager
from src.webui.components.agent_settings_tab import create_agent_settings_tab
from src.webui.components.browser_settings_tab import create_browser_settings_tab
from src.webui.components.browser_use_agent_tab import create_browser_use_agent_tab
from src.webui.components.deep_research_agent_tab import create_deep_research_agent_tab
from src.webui.components.load_save_config_tab import create_load_save_config_tab


def create_ui_v2(theme_name="Soft"):
    """创建优化后的UI界面"""
    
    # 完全优化的CSS
    css = """
    /* ========== 全局重置 ========== */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .gradio-container {
        width: 100vw !important;
        max-width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        background: #F1F3FA !important;
        height: 100vh !important;
        overflow: hidden !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif !important;
    }
    
    .gradio-container > div,
    .gradio-container .contain {
        gap: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* ========== 主布局 ========== */
    .app-container {
        display: flex !important;
        height: 100vh !important;
        overflow: hidden !important;
    }
    
    /* ========== 左侧导航栏 ========== */
    .sidebar {
        width: 260px !important;
        min-width: 260px !important;
        max-width: 260px !important;
        background: linear-gradient(180deg, #ffffff 0%, #fafbff 100%) !important;
        height: 100vh !important;
        overflow-y: auto !important;
        border-right: 2px solid #E6E9FD !important;
        box-shadow: 4px 0 24px rgba(52, 98, 254, 0.08) !important;
        position: relative !important;
        z-index: 100 !important;
    }
    
    /* Logo区域 */
    .logo-section {
        padding: 36px 24px 28px !important;
        text-align: center !important;
        background: linear-gradient(135deg, rgba(52, 98, 254, 0.06) 0%, rgba(157, 52, 254, 0.06) 100%) !important;
        border-bottom: 3px solid #E6E9FD !important;
        position: relative !important;
    }
    
    .logo-section::after {
        content: '' !important;
        position: absolute !important;
        bottom: 0 !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 60px !important;
        height: 3px !important;
        background: linear-gradient(90deg, #3462FE 0%, #9D34FE 100%) !important;
        border-radius: 3px 3px 0 0 !important;
    }
    
    .logo-title {
        font-size: 24px !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, #3462FE 0%, #9D34FE 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        margin-bottom: 8px !important;
        letter-spacing: -0.5px !important;
        line-height: 1.2 !important;
    }
    
    .logo-subtitle {
        font-size: 12px !important;
        color: #9297A9 !important;
        font-weight: 600 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
    }
    
    /* 导航菜单 */
    .nav-container {
        padding: 20px 16px !important;
    }
    
    /* 重写Radio组样式 */
    .sidebar .gr-radio-group {
        gap: 8px !important;
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    
    .sidebar .gr-radio-group label {
        display: flex !important;
        align-items: center !important;
        padding: 16px 20px !important;
        border-radius: 14px !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        color: #545E74 !important;
        background: transparent !important;
        border: 2px solid transparent !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        position: relative !important;
        overflow: hidden !important;
        margin: 0 !important;
    }
    
    .sidebar .gr-radio-group label::before {
        content: '' !important;
        position: absolute !important;
        left: 0 !important;
        top: 0 !important;
        width: 0 !important;
        height: 100% !important;
        background: linear-gradient(135deg, rgba(52, 98, 254, 0.12) 0%, rgba(157, 52, 254, 0.12) 100%) !important;
        transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        z-index: -1 !important;
    }
    
    .sidebar .gr-radio-group label:hover {
        color: #3462FE !important;
        background: linear-gradient(135deg, rgba(52, 98, 254, 0.06) 0%, rgba(157, 52, 254, 0.06) 100%) !important;
        transform: translateX(6px) !important;
        border-color: rgba(52, 98, 254, 0.2) !important;
    }
    
    .sidebar .gr-radio-group label:hover::before {
        width: 100% !important;
    }
    
    /* 选中状态 */
    .sidebar .gr-radio-group label.selected {
        background: linear-gradient(135deg, #E6E9FD 0%, #F0E9FD 100%) !important;
        color: #3462FE !important;
        font-weight: 800 !important;
        border-color: #9D34FE !important;
        box-shadow: 0 6px 20px rgba(52, 98, 254, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
        transform: translateX(6px) scale(1.02) !important;
    }
    
    .sidebar .gr-radio-group label.selected::after {
        content: '' !important;
        position: absolute !important;
        left: 0 !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        width: 5px !important;
        height: 60% !important;
        background: linear-gradient(180deg, #3462FE 0%, #9D34FE 100%) !important;
        border-radius: 0 4px 4px 0 !important;
        box-shadow: 2px 0 8px rgba(52, 98, 254, 0.4) !important;
    }
    
    /* 隐藏Radio原始按钮 */
    .sidebar .gr-radio-group input[type="radio"] {
        display: none !important;
    }
    
    /* ========== 右侧内容区 ========== */
    .content-wrapper {
        flex: 1 !important;
        display: flex !important;
        flex-direction: column !important;
        height: 100vh !important;
        overflow: hidden !important;
        background: #F1F3FA !important;
        min-width: 0 !important;
    }
    
    /* 头部 */
    .page-header {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%) !important;
        padding: 32px 56px !important;
        border-bottom: 3px solid #E6E9FD !important;
        box-shadow: 0 6px 24px rgba(52, 98, 254, 0.08) !important;
        position: relative !important;
        z-index: 50 !important;
    }
    
    .page-header::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 5px !important;
        background: linear-gradient(90deg, #3462FE 0%, #9D34FE 50%, #3462FE 100%) !important;
        background-size: 200% 100% !important;
        animation: gradientShift 3s ease infinite !important;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .page-header h1 {
        font-size: 36px !important;
        font-weight: 900 !important;
        color: #333333 !important;
        margin: 0 0 10px 0 !important;
        letter-spacing: -0.8px !important;
        line-height: 1.2 !important;
    }
    
    .page-header p {
        font-size: 16px !important;
        color: #545E74 !important;
        margin: 0 !important;
        font-weight: 500 !important;
        line-height: 1.6 !important;
    }
    
    /* 主内容 */
    .page-content {
        flex: 1 !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
        padding: 40px 56px !important;
    }
    
    /* ========== 卡片 ========== */
    .card {
        background: white !important;
        border-radius: 20px !important;
        padding: 36px !important;
        margin-bottom: 28px !important;
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.06) !important;
        border: 2px solid rgba(230, 233, 253, 0.6) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .card::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 4px !important;
        background: linear-gradient(90deg, #3462FE 0%, #9D34FE 100%) !important;
        opacity: 0 !important;
        transition: opacity 0.4s ease !important;
    }
    
    .card:hover {
        box-shadow: 0 12px 40px rgba(52, 98, 254, 0.15) !important;
        transform: translateY(-4px) !important;
        border-color: rgba(52, 98, 254, 0.4) !important;
    }
    
    .card:hover::before {
        opacity: 1 !important;
    }
    
    /* ========== 按钮 ========== */
    button, .btn {
        border-radius: 14px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        padding: 16px 36px !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        letter-spacing: 0.3px !important;
        border: none !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    button.primary, .btn-primary {
        background: linear-gradient(135deg, #3462FE 0%, #9D34FE 100%) !important;
        color: white !important;
        box-shadow: 0 8px 24px rgba(52, 98, 254, 0.35) !important;
    }
    
    button.primary::before, .btn-primary::before {
        content: '' !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        width: 0 !important;
        height: 0 !important;
        border-radius: 50% !important;
        background: rgba(255, 255, 255, 0.4) !important;
        transform: translate(-50%, -50%) !important;
        transition: width 0.6s, height 0.6s !important;
    }
    
    button.primary:hover, .btn-primary:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 12px 36px rgba(52, 98, 254, 0.45) !important;
    }
    
    button.primary:hover::before, .btn-primary:hover::before {
        width: 400px !important;
        height: 400px !important;
    }
    
    /* ========== 输入框 ========== */
    input, select, textarea, .gr-textbox, .gr-dropdown {
        border-radius: 14px !important;
        border: 2px solid #E6E9FD !important;
        padding: 14px 20px !important;
        font-size: 15px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        background: white !important;
        color: #333333 !important;
    }
    
    input:focus, select:focus, textarea:focus,
    .gr-textbox:focus, .gr-dropdown:focus {
        border-color: #676BEF !important;
        box-shadow: 0 0 0 5px rgba(103, 107, 239, 0.12) !important;
        outline: none !important;
        background: white !important;
    }
    
    input:hover, select:hover, textarea:hover,
    .gr-textbox:hover, .gr-dropdown:hover {
        border-color: #9D34FE !important;
    }
    
    /* ========== 滚动条 ========== */
    ::-webkit-scrollbar {
        width: 10px !important;
        height: 10px !important;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f3fa !important;
        border-radius: 10px !important;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #3462FE 0%, #9D34FE 100%) !important;
        border-radius: 10px !important;
        border: 2px solid #f1f3fa !important;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #2952ed 0%, #8c2ded 100%) !important;
    }
    
    /* ========== 响应式 ========== */
    @media (max-width: 1400px) {
        .sidebar {
            width: 220px !important;
            min-width: 220px !important;
            max-width: 220px !important;
        }
        
        .page-header, .page-content {
            padding-left: 40px !important;
            padding-right: 40px !important;
        }
    }
    
    /* ========== 隐藏Gradio默认元素 ========== */
    .gr-form, .gr-box {
        border: none !important;
        background: transparent !important;
    }
    
    /* ========== 动画 ========== */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .card, .sidebar .gr-radio-group label {
        animation: fadeIn 0.6s ease-out !important;
    }
    """
    
    ui_manager = WebuiManager()
    
    # 主题配置
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
    
    with gr.Blocks(
        title="AI测试平台 - Browser Use WebUI",
        theme=theme_map[theme_name],
        css=css
    ) as demo:
        
        with gr.Row(elem_classes=["app-container"]):
            # 左侧导航
            with gr.Column(scale=0, min_width=260, elem_classes=["sidebar"]):
                gr.HTML("""
                    <div class="logo-section">
                        <div class="logo-title">🌐 AI测试平台</div>
                        <div class="logo-subtitle">Browser Use WebUI</div>
                    </div>
                """)
                
                with gr.Group(elem_classes=["nav-container"]):
                    nav_selection = gr.Radio(
                        choices=[
                            "⚙️ Agent Settings",
                            "🌐 Browser Settings",
                            "🤖 Run Agent",
                            "🎁 Agent Marketplace",
                            "📁 Load & Save Config"
                        ],
                        value="🤖 Run Agent",
                        label="",
                        show_label=False,
                        interactive=True
                    )
            
            # 右侧内容
            with gr.Column(scale=1, elem_classes=["content-wrapper"]):
                # 头部
                page_title = gr.HTML("""
                    <div class="page-header">
                        <h1>🤖 Run Agent</h1>
                        <p>智能浏览器自动化测试平台 | Control your browser with AI assistance</p>
                    </div>
                """)
                
                # 内容区
                with gr.Column(elem_classes=["page-content"]):
                    with gr.Tabs(visible=False) as content_tabs:
                        with gr.TabItem("⚙️ Agent Settings", id=0):
                            with gr.Group(elem_classes=["card"]):
                                create_agent_settings_tab(ui_manager)
                        
                        with gr.TabItem("🌐 Browser Settings", id=1):
                            with gr.Group(elem_classes=["card"]):
                                create_browser_settings_tab(ui_manager)
                        
                        with gr.TabItem("🤖 Run Agent", id=2):
                            with gr.Group(elem_classes=["card"]):
                                create_browser_use_agent_tab(ui_manager)
                        
                        with gr.TabItem("🎁 Agent Marketplace", id=3):
                            with gr.Group(elem_classes=["card"]):
                                create_deep_research_agent_tab(ui_manager)
                        
                        with gr.TabItem("📁 Load & Save Config", id=4):
                            with gr.Group(elem_classes=["card"]):
                                create_load_save_config_tab(ui_manager)
        
        # 导航切换
        def update_page(selection):
            page_map = {
                "⚙️ Agent Settings": (0, """
                    <div class="page-header">
                        <h1>⚙️ Agent Settings</h1>
                        <p>配置AI Agent的模型、参数和MCP服务器</p>
                    </div>
                """),
                "🌐 Browser Settings": (1, """
                    <div class="page-header">
                        <h1>🌐 Browser Settings</h1>
                        <p>配置浏览器参数和行为设置</p>
                    </div>
                """),
                "🤖 Run Agent": (2, """
                    <div class="page-header">
                        <h1>🤖 Run Agent</h1>
                        <p>智能浏览器自动化测试平台 | Control your browser with AI assistance</p>
                    </div>
                """),
                "🎁 Agent Marketplace": (3, """
                    <div class="page-header">
                        <h1>🎁 Agent Marketplace</h1>
                        <p>探索和使用基于Browser-Use构建的专业Agent</p>
                    </div>
                """),
                "📁 Load & Save Config": (4, """
                    <div class="page-header">
                        <h1>📁 Load & Save Config</h1>
                        <p>保存和加载配置文件</p>
                    </div>
                """)
            }
            
            tab_index, title_html = page_map.get(selection, (2, ""))
            return gr.Tabs(selected=tab_index), gr.HTML(value=title_html)
        
        nav_selection.change(
            fn=update_page,
            inputs=[nav_selection],
            outputs=[content_tabs, page_title]
        )
    
    return demo


if __name__ == "__main__":
    demo = create_ui_v2()
    demo.launch()
