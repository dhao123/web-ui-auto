"""
WebUI V3 主界面
基于ui-ux skill的企业级设计体系
采用左侧导航 + 右侧内容区的布局结构
支持明暗主题切换
"""
import gradio as gr
from src.webui.webui_manager import WebuiManager
from src.webui.components_v3 import (
    create_home_dashboard,
    create_agent_settings_tab_v3,
    create_browser_settings_tab_v3,
    create_browser_use_agent_tab_v3,
    create_task_history_panel,
    create_realtime_monitor_panel,
    create_config_template_panel,
    create_zkh_mcp_config_panel,
)
from src.webui.styles import build_css, get_theme_toggle_js


def create_ui_v3(theme_name="Soft", theme_mode="light"):
    """创建V3主界面
    
    Args:
        theme_name: Gradio主题名称 (Default, Soft, Monochrome, Glass, Origin, Citrus, Ocean, Base)
        theme_mode: 颜色模式 (light, dark)
    """
    
    # 使用模块化样式系统构建CSS
    css = build_css(theme_mode)
    
    # 创建UI管理器
    ui_manager = WebuiManager()
    
    # 主题映射
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
        title="AI浏览器自动化测试平台 - WebUI V3",
        theme=theme_map.get(theme_name, gr.themes.Soft()),
        css=css
    ) as demo:
        
        # 主题状态
        current_theme = gr.State(value=theme_mode)
        
        with gr.Row(elem_classes=["main-layout"]):
            # ========== 左侧导航栏 ==========
            with gr.Column(scale=0, min_width=180, elem_classes=["sidebar"]):
                # Logo区域
                gr.HTML("""
                    <div class="logo-section">
                        <div class="logo-title">🌐 AI测试平台</div>
                        <div class="logo-subtitle">Browser Automation</div>
                    </div>
                """)
                
                # 导航菜单
                with gr.Group(elem_classes=["nav-container"]):
                    nav_selection = gr.Radio(
                        choices=[
                            "🏠 首页",
                            "⚙️ Agent配置",
                            "🌐 浏览器配置",
                            "🤖 执行Agent",
                            "📜 任务历史",
                            "📊 实时监控",
                            "💾 配置管理",
                            "🛒 震坤行MCP"
                        ],
                        value="🏠 首页",
                        label="",
                        show_label=False,
                        interactive=True
                    )
            
            # ========== 右侧内容区 ==========
            with gr.Column(scale=1, elem_classes=["content-area"]):
                # 页面头部
                with gr.Row(elem_classes=["page-header"]):
                    page_title = gr.HTML("""
                        <div>
                            <h1>🏠 首页</h1>
                            <p>平台数据总览 | Dashboard Overview</p>
                        </div>
                    """)
                    
                    # 主题切换按钮
                    theme_toggle = gr.Button(
                        value="🌙",
                        elem_classes=["theme-toggle"],
                        min_width=40,
                        scale=0
                    )
                
                # 主内容区 - 使用Column切换,而不是Tabs
                with gr.Column(elem_classes=["page-content"]):
                    # Page 0: 首页 - 仪表盘(累计统计+历史任务)
                    page_home = gr.Column(visible=True, elem_classes=["single-page"])
                    with page_home:
                        home_dashboard_data = create_home_dashboard(ui_manager)
                    
                    # Page 1: Agent配置
                    page_agent = gr.Column(visible=False, elem_classes=["single-page"])
                    with page_agent:
                        create_agent_settings_tab_v3(ui_manager)
                    
                    # Page 2: 浏览器配置
                    page_browser = gr.Column(visible=False, elem_classes=["single-page"])
                    with page_browser:
                        create_browser_settings_tab_v3(ui_manager)
                    
                    # Page 3: 执行Agent
                    page_execute = gr.Column(visible=False, elem_classes=["single-page"])
                    with page_execute:
                        create_browser_use_agent_tab_v3(ui_manager)
                    
                    # Page 4: 任务历史
                    page_history = gr.Column(visible=False, elem_classes=["single-page"])
                    with page_history:
                        create_task_history_panel(ui_manager)
                    
                    # Page 5: 实时监控
                    page_monitor = gr.Column(visible=False, elem_classes=["single-page"])
                    with page_monitor:
                        create_realtime_monitor_panel(ui_manager)
                    
                    # Page 6: 配置管理
                    page_config = gr.Column(visible=False, elem_classes=["single-page"])
                    with page_config:
                        create_config_template_panel(ui_manager)
                    
                    # Page 7: 震坤行MCP
                    page_zkh = gr.Column(visible=False, elem_classes=["single-page"])
                    with page_zkh:
                        create_zkh_mcp_config_panel(ui_manager)
        
        # ========== 导航切换逻辑 ==========
        def update_page(selection):
            """更新页面内容和标题 - 返回各页面的显示状态"""
            page_map = {
                "🏠 首页": (
                    """<div><h1>🏠 首页</h1><p>欢迎使用AI浏览器自动化测试平台</p></div>""",
                    [True, False, False, False, False, False, False, False]
                ),
                "⚙️ Agent配置": (
                    """<div><h1>⚙️ Agent配置</h1><p>配置LLM模型、MCP服务器和Agent参数</p></div>""",
                    [False, True, False, False, False, False, False, False]
                ),
                "🌐 浏览器配置": (
                    """<div><h1>🌐 浏览器配置</h1><p>配置浏览器行为、窗口尺寸和高级选项</p></div>""",
                    [False, False, True, False, False, False, False, False]
                ),
                "🤖 执行Agent": (
                    """<div><h1>🤖 执行Agent</h1><p>智能浏览器自动化测试 | Browser-Use Agent Execution</p></div>""",
                    [False, False, False, True, False, False, False, False]
                ),
                "📜 任务历史": (
                    """<div><h1>📜 任务历史</h1><p>查看和管理历史执行记录</p></div>""",
                    [False, False, False, False, True, False, False, False]
                ),
                "📊 实时监控": (
                    """<div><h1>📊 实时监控</h1><p>实时显示Agent执行状态和性能指标</p></div>""",
                    [False, False, False, False, False, True, False, False]
                ),
                "💾 配置管理": (
                    """<div><h1>💾 配置管理</h1><p>保存和加载配置模板,快速切换测试场景</p></div>""",
                    [False, False, False, False, False, False, True, False]
                ),
                "🛒 震坤行MCP": (
                    """<div><h1>🛒 震坤行MCP</h1><p>电商场景专属配置和优化 | ZKH E-commerce</p></div>""",
                    [False, False, False, False, False, False, False, True]
                )
            }
            
            title_html, visibility = page_map.get(selection, page_map["🏠 首页"])
            
            # 返回: 标题HTML + 8个页面的visible状态
            return [
                title_html,
                gr.Column(visible=visibility[0]),
                gr.Column(visible=visibility[1]),
                gr.Column(visible=visibility[2]),
                gr.Column(visible=visibility[3]),
                gr.Column(visible=visibility[4]),
                gr.Column(visible=visibility[5]),
                gr.Column(visible=visibility[6]),
                gr.Column(visible=visibility[7])
            ]
        
        # ========== 主题切换逻辑 ==========
        def toggle_theme(current):
            """切换明暗主题"""
            new_mode = "dark" if current == "light" else "light"
            new_icon = "☀️" if new_mode == "dark" else "🌙"
            return new_mode, new_icon
        
        # 绑定导航切换事件
        nav_selection.change(
            fn=update_page,
            inputs=[nav_selection],
            outputs=[page_title, page_home, page_agent, page_browser, page_execute, 
                    page_history, page_monitor, page_config, page_zkh]
        )
        
        # 绑定主题切换事件
        theme_toggle.click(
            fn=toggle_theme,
            inputs=[current_theme],
            outputs=[current_theme, theme_toggle]
        )
        
        # 页面加载时初始化首页数据
        demo.load(
            fn=home_dashboard_data["init_fn"],
            outputs=home_dashboard_data["outputs"]
        )
    
    return demo


def create_ui_v3_dark(theme_name="Soft"):
    """创建深色主题的V3界面"""
    return create_ui_v3(theme_name=theme_name, theme_mode="dark")


if __name__ == "__main__":
    demo = create_ui_v3()
    demo.launch()
