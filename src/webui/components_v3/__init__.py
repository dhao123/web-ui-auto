"""
WebUI V3 组件包
基于ui-ux skill的企业级设计体系
"""

from .home_dashboard import create_home_dashboard
from .agent_settings_v3 import create_agent_settings_tab_v3
from .browser_settings_v3 import create_browser_settings_tab_v3
from .browser_use_agent_v3 import create_browser_use_agent_tab_v3
from .task_history_panel import create_task_history_panel
from .realtime_monitor_panel import create_realtime_monitor_panel
from .config_template_panel import create_config_template_panel
from .zkh_mcp_config_panel import create_zkh_mcp_config_panel

__all__ = [
    "create_home_dashboard",
    "create_agent_settings_tab_v3",
    "create_browser_settings_tab_v3",
    "create_browser_use_agent_tab_v3",
    "create_task_history_panel",
    "create_realtime_monitor_panel",
    "create_config_template_panel",
    "create_zkh_mcp_config_panel",
]
