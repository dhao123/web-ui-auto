"""
Browser Use Agent执行组件 V3
基于ui-ux skill的企业级设计
保持原有功能不变,优化UI布局
"""
# 直接复用原有的browser_use_agent_tab,因为它已经实现了完整的功能
# V3主要是添加卡片样式,核心逻辑保持不变
from src.webui.components.browser_use_agent_tab import create_browser_use_agent_tab

def create_browser_use_agent_tab_v3(webui_manager):
    """
    创建Browser Use Agent执行页面 - V3版本
    保持原有功能不变,通过CSS优化UI
    """
    # 直接调用原有实现,CSS样式已在interface_v3.py中统一处理
    return create_browser_use_agent_tab(webui_manager)
