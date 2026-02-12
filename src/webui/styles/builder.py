"""
样式构建工具 - 动态组装CSS字符串
"""
from .tokens import generate_css_variables, get_theme, LIGHT_THEME, DARK_THEME
from .base import get_base_styles
from .layout import get_layout_styles
from .components import get_component_styles
from .animations import get_animation_styles


def build_css(theme_mode: str = "light") -> str:
    """构建完整CSS字符串
    
    Args:
        theme_mode: 主题模式，"light" 或 "dark"
    
    Returns:
        完整的CSS字符串，可直接用于 gr.Blocks(css=...)
    """
    # 1. 生成CSS变量定义
    css_variables = generate_css_variables(theme_mode)
    
    # 2. 拼接各模块样式
    all_styles = [
        f"/* === CSS Variables ({theme_mode} theme) === */",
        css_variables,
        "",
        "/* === Base Styles === */",
        get_base_styles(),
        "",
        "/* === Layout Styles === */",
        get_layout_styles(),
        "",
        "/* === Component Styles === */",
        get_component_styles(),
        "",
        "/* === Animation Styles === */",
        get_animation_styles(),
    ]
    
    return "\n".join(all_styles)


def build_light_css() -> str:
    """构建浅色主题CSS"""
    return build_css("light")


def build_dark_css() -> str:
    """构建深色主题CSS"""
    return build_css("dark")


def get_theme_toggle_js() -> str:
    """获取主题切换的JavaScript代码
    
    用于在前端动态切换主题，无需重新加载页面
    """
    light_vars = "\n".join([f"    '{k}': '{v}'," for k, v in LIGHT_THEME.items()])
    dark_vars = "\n".join([f"    '{k}': '{v}'," for k, v in DARK_THEME.items()])
    
    return f"""
    <script>
    (function() {{
        const lightTheme = {{
{light_vars}
        }};
        
        const darkTheme = {{
{dark_vars}
        }};
        
        window.toggleTheme = function(mode) {{
            const theme = mode === 'dark' ? darkTheme : lightTheme;
            const root = document.documentElement;
            
            for (const [key, value] of Object.entries(theme)) {{
                root.style.setProperty(key, value);
            }}
            
            // 保存主题偏好
            localStorage.setItem('theme-mode', mode);
            
            // 触发自定义事件
            window.dispatchEvent(new CustomEvent('themechange', {{ detail: {{ mode }} }}));
        }};
        
        window.getCurrentTheme = function() {{
            return localStorage.getItem('theme-mode') || 'light';
        }};
        
        // 页面加载时应用保存的主题
        document.addEventListener('DOMContentLoaded', function() {{
            const savedTheme = localStorage.getItem('theme-mode');
            if (savedTheme) {{
                window.toggleTheme(savedTheme);
            }}
        }});
    }})();
    </script>
    """


def get_theme_toggle_button_html(current_mode: str = "light") -> str:
    """获取主题切换按钮HTML
    
    Args:
        current_mode: 当前主题模式
    """
    icon = "🌙" if current_mode == "light" else "☀️"
    next_mode = "dark" if current_mode == "light" else "light"
    
    return f"""
    <button 
        class="theme-toggle" 
        onclick="window.toggleTheme('{next_mode}'); this.textContent = '{next_mode == 'light' and '🌙' or '☀️'}'"
        title="切换到{next_mode == 'dark' and '深色' or '浅色'}模式"
    >
        {icon}
    </button>
    """


def get_css_with_theme_support() -> str:
    """获取带主题切换支持的CSS
    
    包含基础样式和主题切换JavaScript
    """
    return build_light_css() + "\n" + get_theme_toggle_js()


# 预构建的CSS缓存
_css_cache = {
    "light": None,
    "dark": None,
}


def get_cached_css(theme_mode: str = "light") -> str:
    """获取缓存的CSS（提高性能）
    
    首次调用时构建CSS并缓存，后续调用直接返回缓存
    """
    if _css_cache[theme_mode] is None:
        _css_cache[theme_mode] = build_css(theme_mode)
    return _css_cache[theme_mode]


def clear_css_cache():
    """清除CSS缓存"""
    _css_cache["light"] = None
    _css_cache["dark"] = None


def get_css_stats() -> dict:
    """获取CSS统计信息"""
    light_css = build_css("light")
    dark_css = build_css("dark")
    
    return {
        "light_css_length": len(light_css),
        "dark_css_length": len(dark_css),
        "light_css_lines": light_css.count("\n") + 1,
        "dark_css_lines": dark_css.count("\n") + 1,
        "token_count": {
            "light": len(LIGHT_THEME),
            "dark": len(DARK_THEME),
        },
    }
