"""
WebUI V3 样式系统

统一的设计Token系统，支持明暗主题切换

使用示例:
    from src.webui.styles import build_css, build_light_css, build_dark_css
    
    # 在 Gradio Blocks 中使用
    with gr.Blocks(css=build_css("light")) as demo:
        ...
    
    # 或使用预构建的浅色/深色主题
    css = build_light_css()  # 浅色主题
    css = build_dark_css()   # 深色主题

模块结构:
    - tokens.py: 设计Token定义 (LIGHT_THEME, DARK_THEME)
    - base.py: 全局基础样式 (重置、滚动条等)
    - layout.py: 布局样式 (侧边栏、头部、内容区)
    - components.py: 组件样式 (卡片、表单、表格、导航等)
    - animations.py: 动画效果 (@keyframes)
    - charts.py: 图表主题配置 (ECharts)
    - builder.py: 样式构建工具
"""

# 主要导出
from .builder import (
    build_css,
    build_light_css,
    build_dark_css,
    get_cached_css,
    clear_css_cache,
    get_theme_toggle_js,
    get_theme_toggle_button_html,
    get_css_with_theme_support,
    get_css_stats,
)

# Token导出
from .tokens import (
    LIGHT_THEME,
    DARK_THEME,
    get_theme,
    generate_css_variables,
)

# 样式模块导出
from .base import get_base_styles
from .layout import get_layout_styles
from .components import (
    get_component_styles,
    get_navigation_styles,
    get_card_styles,
    get_metric_card_styles,
    get_form_styles,
    get_button_styles,
    get_table_styles,
    get_status_styles,
    get_chart_container_styles,
)
from .animations import get_animation_styles

# 图表工具导出
from .charts import (
    get_echarts_theme,
    build_line_chart_option,
    build_pie_chart_option,
    build_bar_chart_option,
    build_gauge_chart_option,
    generate_chart_html,
    generate_line_chart_html,
    generate_pie_chart_html,
    generate_bar_chart_html,
)

__all__ = [
    # 主要构建函数
    "build_css",
    "build_light_css",
    "build_dark_css",
    "get_cached_css",
    "clear_css_cache",
    "get_css_with_theme_support",
    "get_theme_toggle_js",
    "get_theme_toggle_button_html",
    "get_css_stats",
    
    # Token
    "LIGHT_THEME",
    "DARK_THEME",
    "get_theme",
    "generate_css_variables",
    
    # 样式模块
    "get_base_styles",
    "get_layout_styles",
    "get_component_styles",
    "get_navigation_styles",
    "get_card_styles",
    "get_metric_card_styles",
    "get_form_styles",
    "get_button_styles",
    "get_table_styles",
    "get_status_styles",
    "get_chart_container_styles",
    "get_animation_styles",
    
    # 图表
    "get_echarts_theme",
    "build_line_chart_option",
    "build_pie_chart_option",
    "build_bar_chart_option",
    "build_gauge_chart_option",
    "generate_chart_html",
    "generate_line_chart_html",
    "generate_pie_chart_html",
    "generate_bar_chart_html",
]

__version__ = "1.0.0"
