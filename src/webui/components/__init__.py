"""
WebUI Components Module
WebUI 组件模块

包含所有 UI 组件的实现
"""

# Original components (keep for backward compatibility)
from .agent_settings_tab import create_agent_settings_tab
from .browser_settings_tab import create_browser_settings_tab
from .browser_use_agent_tab import create_browser_use_agent_tab
from .deep_research_agent_tab import create_deep_research_agent_tab
from .load_save_config_tab import create_load_save_config_tab

# Enterprise components (new enterprise-grade UI)
from .enterprise_agent_settings import create_enterprise_agent_settings
from .enterprise_browser_settings import create_enterprise_browser_settings
from .enterprise_run_agent import create_enterprise_run_agent
from .enterprise_deep_research import create_enterprise_deep_research
from .enterprise_config_manager import create_enterprise_config_manager

__all__ = [
    # Original components
    "create_agent_settings_tab",
    "create_browser_settings_tab",
    "create_browser_use_agent_tab",
    "create_deep_research_agent_tab",
    "create_load_save_config_tab",
    # Enterprise components
    "create_enterprise_agent_settings",
    "create_enterprise_browser_settings",
    "create_enterprise_run_agent",
    "create_enterprise_deep_research",
    "create_enterprise_config_manager",
]
