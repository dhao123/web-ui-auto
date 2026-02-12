"""
优化后的WebUI界面 - 采用左侧导航栏设计
参考UI/UX Skill设计规范
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
    
    # 自定义CSS - 参考UI/UX Skill设计规范
    css = """
    /* ========== 全局样式 ========== */
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
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
    }
    
    /* ========== 布局容器 ========== */
    .main-layout {
        display: flex !important;
        height: 100vh !important;
        overflow: hidden !important;
        gap: 0 !important;
    }
    
    /* 隐藏Gradio默认的padding和margin */
    .gradio-container > div {
        gap: 0 !important;
    }
    
    .contain {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* ========== 左侧导航栏 ========== */
    .sidebar-nav {
        width: 240px !important;
        min-width: 240px !important;
        max-width: 240px !important;
        background: linear-gradient(180deg, #ffffff 0%, #f8f9ff 100%) !important;
        height: 100vh !important;
        overflow-y: auto !important;
        border-right: 1px solid #E6E9FD !important;
        padding: 0 !important;
        box-shadow: 4px 0 20px rgba(102, 126, 234, 0.08) !important;
        position: relative !important;
    }
    
    /* Logo区域 */
    .logo-area {
        text-align: center !important;
        padding: 32px 20px 24px !important;
        margin-bottom: 16px !important;
        border-bottom: 2px solid #E6E9FD !important;
        background: linear-gradient(135deg, rgba(52, 98, 254, 0.05) 0%, rgba(157, 52, 254, 0.05) 100%) !important;
    }
    
    .logo-area h2 {
        font-size: 22px !important;
        font-weight: 800 !important;
        color: #333333 !important;
        margin: 0 0 8px 0 !important;
        background: linear-gradient(135deg, #3462FE 0%, #9D34FE 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        letter-spacing: -0.5px !important;
    }
    
    .logo-area p {
        font-size: 11px !important;
        color: #9297A9 !important;
        margin: 0 !important;
        font-weight: 500 !important;
        letter-spacing: 0.5px !important;
    }
    
    /* 导航菜单容器 */
    .nav-menu-container {
        padding: 12px 16px !important;
    }
    
    /* Radio组件样式重写 */
    .sidebar-nav .gr-radio-group {
        gap: 6px !important;
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    
    .sidebar-nav .gr-radio-group label {
        display: flex !important;
        align-items: center !important;
        padding: 14px 16px !important;
        border-radius: 10px !important;
        color: #545E74 !important;
        text-decoration: none !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        background: transparent !important;
        border: 2px solid transparent !important;
        margin: 0 !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .sidebar-nav .gr-radio-group label::before {
        content: '' !important;
        position: absolute !important;
        left: 0 !important;
        top: 0 !important;
        height: 100% !important;
        width: 0 !important;
        background: linear-gradient(135deg, rgba(52, 98, 254, 0.1) 0%, rgba(157, 52, 254, 0.1) 100%) !important;
        transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        z-index: 0 !important;
    }
    
    .sidebar-nav .gr-radio-group label:hover {
        background: linear-gradient(135deg, rgba(52, 98, 254, 0.08) 0%, rgba(157, 52, 254, 0.08) 100%) !important;
        color: #3462FE !important;
        transform: translateX(4px) !important;
        border-color: rgba(52, 98, 254, 0.2) !important;
    }
    
    .sidebar-nav .gr-radio-group label:hover::before {
        width: 100% !important;
    }
    
    /* 选中状态 */
    .sidebar-nav .gr-radio-group label.selected {
        background: linear-gradient(135deg, #E6E9FD 0%, #F0E9FD 100%) !important;
        color: #3462FE !important;
        font-weight: 700 !important;
        border-color: #9D34FE !important;
        box-shadow: 0 4px 12px rgba(52, 98, 254, 0.15) !important;
        transform: translateX(4px) !important;
    }
    
    .sidebar-nav .gr-radio-group label.selected::after {
        content: '' !important;
        position: absolute !important;
        left: 0 !important;
        top: 0 !important;
        height: 100% !important;
        width: 4px !important;
        background: linear-gradient(180deg, #3462FE 0%, #9D34FE 100%) !important;
        border-radius: 0 4px 4px 0 !important;
    }
    
    /* 隐藏Radio的原始圆点 */
    .sidebar-nav .gr-radio-group input[type="radio"] {
        display: none !important;
    }
    
    /* 图标样式 */
    .nav-icon {
        margin-right: 12px !important;
        font-size: 18px !important;
        display: inline-block !important;
        width: 20px !important;
        text-align: center !important;
    }
    
    /* ========== 右侧内容区 ========== */
    .content-area {
        flex: 1 !important;
        display: flex !important;
        flex-direction: column !important;
        height: 100vh !important;
        overflow: hidden !important;
        background: #F1F3FA !important;
        min-width: 0 !important;
    }
    
    /* 头部区域 */
    .header-area {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%) !important;
        padding: 28px 48px !important;
        border-bottom: 2px solid #E6E9FD !important;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.08) !important;
        position: relative !important;
        z-index: 10 !important;
    }
    
    .header-area::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 4px !important;
        background: linear-gradient(90deg, #3462FE 0%, #9D34FE 100%) !important;
    }
    
    .header-title {
        font-size: 32px !important;
        font-weight: 800 !important;
        color: #333333 !important;
        margin: 0 0 8px 0 !important;
        letter-spacing: -0.5px !important;
        line-height: 1.2 !important;
    }
    
    .header-subtitle {
        font-size: 15px !important;
        color: #545E74 !important;
        margin: 0 !important;
        font-weight: 500 !important;
        line-height: 1.5 !important;
    }
    
    /* 主内容区 */
    .main-content {
        flex: 1 !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
        padding: 32px 48px !important;
    }
    
    /* ========== 卡片样式 ========== */
    .content-card {
        background: white !important;
        border-radius: 16px !important;
        padding: 32px !important;
        margin-bottom: 24px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06) !important;
        border: 1px solid rgba(230, 233, 253, 0.6) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .content-card::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 3px !important;
        background: linear-gradient(90deg, #3462FE 0%, #9D34FE 100%) !important;
        opacity: 0 !important;
        transition: opacity 0.3s ease !important;
    }
    
    .content-card:hover {
        box-shadow: 0 8px 30px rgba(52, 98, 254, 0.12) !important;
        transform: translateY(-2px) !important;
        border-color: rgba(52, 98, 254, 0.3) !important;
    }
    
    .content-card:hover::before {
        opacity: 1 !important;
    }
    
    .card-title {
        font-size: 20px !important;
        font-weight: 700 !important;
        color: #333333 !important;
        margin: 0 0 20px 0 !important;
        padding-bottom: 16px !important;
        border-bottom: 2px solid #E6E9FD !important;
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
    }
    
    /* ========== 统计卡片 ========== */
    .stats-grid {
        display: grid !important;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)) !important;
        gap: 20px !important;
        margin-bottom: 32px !important;
    }
    
    .stat-card {
        background: white !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06) !important;
        border-left: 5px solid #676BEF !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stat-card::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        right: 0 !important;
        width: 100px !important;
        height: 100px !important;
        background: radial-gradient(circle, rgba(103, 107, 239, 0.1) 0%, transparent 70%) !important;
        border-radius: 50% !important;
        transform: translate(30%, -30%) !important;
    }
    
    .stat-card:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 8px 30px rgba(103, 107, 239, 0.15) !important;
    }
    
    .stat-card.success {
        border-left-color: #52c41a !important;
    }
    
    .stat-card.success::before {
        background: radial-gradient(circle, rgba(82, 196, 26, 0.1) 0%, transparent 70%) !important;
    }
    
    .stat-card.warning {
        border-left-color: #faad14 !important;
    }
    
    .stat-card.warning::before {
        background: radial-gradient(circle, rgba(250, 173, 20, 0.1) 0%, transparent 70%) !important;
    }
    
    .stat-card.info {
        border-left-color: #1890ff !important;
    }
    
    .stat-card.info::before {
        background: radial-gradient(circle, rgba(24, 144, 255, 0.1) 0%, transparent 70%) !important;
    }
    
    .stat-label {
        font-size: 13px !important;
        color: #9297A9 !important;
        margin-bottom: 12px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .stat-value {
        font-size: 32px !important;
        font-weight: 800 !important;
        color: #333333 !important;
        line-height: 1 !important;
    }
    
    /* ========== 表单样式 ========== */
    .form-group {
        margin-bottom: 20px !important;
    }
    
    .form-label {
        display: block !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        color: #333333 !important;
        margin-bottom: 8px !important;
    }
    
    /* 输入框 */
    .gr-textbox, .gr-dropdown, .gr-number {
        border-radius: 8px !important;
        border: 1px solid #D7DEF4 !important;
        transition: all 0.3s ease !important;
    }
    
    .gr-textbox:focus, .gr-dropdown:focus, .gr-number:focus {
        border-color: #676BEF !important;
        box-shadow: 0 0 0 3px rgba(103, 107, 239, 0.1) !important;
    }
    
    /* 滑块 */
    .gr-slider input[type="range"] {
        accent-color: #676BEF !important;
    }
    
    /* ========== 按钮样式 ========== */
    .btn-primary, button.primary {
        background: linear-gradient(135deg, #3462FE 0%, #9D34FE 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 14px 32px !important;
        font-size: 15px !important;
        box-shadow: 0 6px 20px rgba(52, 98, 254, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        letter-spacing: 0.3px !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .btn-primary::before, button.primary::before {
        content: '' !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        width: 0 !important;
        height: 0 !important;
        border-radius: 50% !important;
        background: rgba(255, 255, 255, 0.3) !important;
        transform: translate(-50%, -50%) !important;
        transition: width 0.6s, height 0.6s !important;
    }
    
    .btn-primary:hover, button.primary:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 30px rgba(52, 98, 254, 0.4) !important;
    }
    
    .btn-primary:hover::before, button.primary:hover::before {
        width: 300px !important;
        height: 300px !important;
    }
    
    .btn-primary:active, button.primary:active {
        transform: translateY(-1px) !important;
    }
    
    .btn-secondary {
        background: white !important;
        border: 2px solid #676BEF !important;
        border-radius: 12px !important;
        color: #676BEF !important;
        font-weight: 700 !important;
        padding: 12px 32px !important;
        font-size: 15px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        letter-spacing: 0.3px !important;
    }
    
    .btn-secondary:hover {
        background: linear-gradient(135deg, rgba(52, 98, 254, 0.1) 0%, rgba(157, 52, 254, 0.1) 100%) !important;
        border-color: #9D34FE !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(103, 107, 239, 0.2) !important;
    }
    
    .btn-danger {
        background: linear-gradient(135deg, #F35859 0%, #e04748 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 14px 32px !important;
        font-size: 15px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 6px 20px rgba(243, 88, 89, 0.3) !important;
    }
    
    .btn-danger:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 30px rgba(243, 88, 89, 0.4) !important;
    }
    
    /* ========== Chatbot样式 ========== */
    .chatbot-container {
        border-radius: 12px !important;
        border: 1px solid #D7DEF4 !important;
        background: white !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
        overflow: hidden !important;
    }
    
    /* ========== 标签样式 ========== */
    .tag {
        display: inline-block !important;
        padding: 4px 12px !important;
        border-radius: 4px !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        margin-right: 8px !important;
    }
    
    .tag-success {
        background: #f6ffed !important;
        color: #52c41a !important;
        border: 1px solid #b7eb8f !important;
    }
    
    .tag-warning {
        background: #fffbe6 !important;
        color: #faad14 !important;
        border: 1px solid #ffe58f !important;
    }
    
    .tag-error {
        background: #fff2f0 !important;
        color: #ff4d4f !important;
        border: 1px solid #ffccc7 !important;
    }
    
    .tag-info {
        background: #e6f7ff !important;
        color: #1890ff !important;
        border: 1px solid #91d5ff !important;
    }
    
    /* ========== 滚动条美化 ========== */
    ::-webkit-scrollbar {
        width: 8px !important;
        height: 8px !important;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1 !important;
        border-radius: 4px !important;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c1c1c1 !important;
        border-radius: 4px !important;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8 !important;
    }
    
    /* ========== 响应式调整 ========== */
    @media (max-width: 1260px) {
        .sidebar-nav {
            width: 180px !important;
            min-width: 180px !important;
        }
        
        .main-content {
            padding: 20px 24px !important;
        }
    }
    
    /* ========== Group样式优化 ========== */
    .gr-group {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* ========== Accordion样式 ========== */
    .gr-accordion {
        border-radius: 12px !important;
        border: 1px solid #D7DEF4 !important;
        overflow: hidden !important;
        margin-bottom: 16px !important;
    }
    
    /* ========== 加载动画 ========== */
    .loading-spinner {
        border: 3px solid #f3f3f3 !important;
        border-top: 3px solid #676BEF !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        animation: spin 1s linear infinite !important;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    """
    
    # JavaScript for navigation
    js_func = """
    function initNavigation() {
        // 导航切换逻辑将由Gradio的Tab组件处理
        console.log('Navigation initialized');
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
        css=css,
        js=js_func
    ) as demo:
        
        # 使用Gradio的Column布局模拟左右分栏
        with gr.Row(elem_classes=["main-layout"]):
            # 左侧导航栏
            with gr.Column(scale=0, min_width=220, elem_classes=["sidebar-nav"]):
                # Logo区域
                gr.Markdown(
                    """
                    <div class="logo-area">
                        <h2>🌐 AI测试平台</h2>
                        <p>Browser Use WebUI</p>
                    </div>
                    """,
                    elem_classes=["logo-area"]
                )
                
                # 导航菜单 - 使用Radio实现导航切换
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
                    elem_classes=["nav-menu"],
                    interactive=True
                )
            
            # 右侧内容区
            with gr.Column(scale=1, elem_classes=["content-area"]):
                # 头部区域
                with gr.Row(elem_classes=["header-area"]):
                    page_title = gr.Markdown(
                        """
                        <h1 class="header-title">🤖 Run Agent</h1>
                        <p class="header-subtitle">智能浏览器自动化测试平台 | Control your browser with AI assistance</p>
                        """,
                        elem_classes=["header-area"]
                    )
                
                # 主内容区 - 使用Tabs但隐藏Tab头部
                with gr.Column(elem_classes=["main-content"]):
                    with gr.Tabs(visible=False) as content_tabs:
                        # Agent Settings页面
                        with gr.TabItem("⚙️ Agent Settings", id=0):
                            with gr.Column(elem_classes=["content-card"]):
                                gr.Markdown("### ⚙️ Agent Settings", elem_classes=["card-title"])
                                create_agent_settings_tab(ui_manager)
                        
                        # Browser Settings页面
                        with gr.TabItem("🌐 Browser Settings", id=1):
                            with gr.Column(elem_classes=["content-card"]):
                                gr.Markdown("### 🌐 Browser Settings", elem_classes=["card-title"])
                                create_browser_settings_tab(ui_manager)
                        
                        # Run Agent页面
                        with gr.TabItem("🤖 Run Agent", id=2):
                            with gr.Column(elem_classes=["content-card"]):
                                gr.Markdown("### 🤖 Run Agent", elem_classes=["card-title"])
                                create_browser_use_agent_tab(ui_manager)
                        
                        # Agent Marketplace页面
                        with gr.TabItem("🎁 Agent Marketplace", id=3):
                            with gr.Column(elem_classes=["content-card"]):
                                gr.Markdown("### 🎁 Agent Marketplace", elem_classes=["card-title"])
                                gr.Markdown("#### Deep Research Agent")
                                create_deep_research_agent_tab(ui_manager)
                        
                        # Load & Save Config页面
                        with gr.TabItem("📁 Load & Save Config", id=4):
                            with gr.Column(elem_classes=["content-card"]):
                                gr.Markdown("### 📁 Load & Save Config", elem_classes=["card-title"])
                                create_load_save_config_tab(ui_manager)
        
        # 导航切换逻辑
        def update_page(selection):
            page_map = {
                "⚙️ Agent Settings": (
                    0,
                    """<h1 class="header-title">⚙️ Agent Settings</h1>
                    <p class="header-subtitle">配置AI Agent的模型、参数和MCP服务器</p>"""
                ),
                "🌐 Browser Settings": (
                    1,
                    """<h1 class="header-title">🌐 Browser Settings</h1>
                    <p class="header-subtitle">配置浏览器参数和行为设置</p>"""
                ),
                "🤖 Run Agent": (
                    2,
                    """<h1 class="header-title">🤖 Run Agent</h1>
                    <p class="header-subtitle">智能浏览器自动化测试平台 | Control your browser with AI assistance</p>"""
                ),
                "🎁 Agent Marketplace": (
                    3,
                    """<h1 class="header-title">🎁 Agent Marketplace</h1>
                    <p class="header-subtitle">探索和使用基于Browser-Use构建的专业Agent</p>"""
                ),
                "📁 Load & Save Config": (
                    4,
                    """<h1 class="header-title">📁 Load & Save Config</h1>
                    <p class="header-subtitle">保存和加载配置文件</p>"""
                )
            }
            
            tab_index, title_html = page_map.get(selection, (2, ""))
            return gr.Tabs(selected=tab_index), gr.Markdown(value=title_html)
        
        nav_selection.change(
            fn=update_page,
            inputs=[nav_selection],
            outputs=[content_tabs, page_title]
        )
    
    return demo


if __name__ == "__main__":
    demo = create_ui_v2()
    demo.launch()
