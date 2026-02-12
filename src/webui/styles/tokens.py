"""
设计Token定义 - 明暗主题
统一管理所有CSS变量,确保设计一致性
"""

# 浅色主题Token
LIGHT_THEME = {
    # === 品牌色 ===
    "--primary": "#5B6BD1",
    "--primary-hover": "#4A5AB8",
    "--primary-light": "#7B8BE8",
    "--primary-dark": "#4A5AB8",
    "--primary-gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "--primary-alpha": "rgba(103, 107, 239, 0.1)",
    "--primary-alpha-hover": "rgba(103, 107, 239, 0.08)",
    
    # === 功能色 ===
    "--success": "#52C41A",
    "--success-bg": "#F6FFED",
    "--success-border": "#B7EB8F",
    "--warning": "#FAAD14",
    "--warning-bg": "#FFFBE6",
    "--warning-border": "#FFE58F",
    "--danger": "#F5222D",
    "--danger-bg": "#FFF2F0",
    "--danger-border": "#FFCCC7",
    "--info": "#4A90E2",
    "--info-bg": "#E6F7FF",
    "--info-border": "#91D5FF",
    
    # === 背景色 ===
    "--bg-page": "#F5F7FA",
    "--bg-content": "#FFFFFF",
    "--bg-card": "#FFFFFF",
    "--bg-hover": "rgba(103, 107, 239, 0.08)",
    "--bg-active": "rgba(103, 107, 239, 0.05)",
    "--bg-sidebar": "rgba(255, 255, 255, 0.95)",
    "--bg-header": "rgba(255, 255, 255, 0.98)",
    "--bg-input": "#FFFFFF",
    "--bg-table-header": "#FAFAFA",
    "--bg-table-hover": "#F5F7FA",
    
    # === 文字色 ===
    "--text-primary": "#262626",
    "--text-secondary": "#595959",
    "--text-tertiary": "#8C8C8C",
    "--text-disabled": "#BFBFBF",
    "--text-placeholder": "#BFBFBF",
    "--text-inverse": "#FFFFFF",
    
    # === 边框色 ===
    "--border-light": "#E8E8E8",
    "--border-normal": "#D9D9D9",
    "--border-dark": "#BFBFBF",
    "--border-primary": "rgba(103, 107, 239, 0.2)",
    "--border-focus": "rgba(103, 107, 239, 0.3)",
    
    # === 阴影 ===
    "--shadow-sm": "0 2px 8px rgba(0, 0, 0, 0.08)",
    "--shadow-md": "0 4px 16px rgba(0, 0, 0, 0.12)",
    "--shadow-lg": "0 8px 32px rgba(0, 0, 0, 0.15)",
    "--shadow-primary": "0 4px 16px rgba(103, 107, 239, 0.4)",
    "--shadow-primary-sm": "0 4px 12px rgba(103, 107, 239, 0.1)",
    "--shadow-sidebar": "4px 0 16px rgba(0, 0, 0, 0.05)",
    "--shadow-header": "0 2px 16px rgba(0, 0, 0, 0.05)",
    
    # === 间距 ===
    "--spacing-xs": "4px",
    "--spacing-sm": "8px",
    "--spacing-md": "16px",
    "--spacing-lg": "24px",
    "--spacing-xl": "32px",
    "--spacing-2xl": "40px",
    
    # === 圆角 ===
    "--radius-xs": "4px",
    "--radius-sm": "6px",
    "--radius-md": "8px",
    "--radius-lg": "12px",
    "--radius-xl": "16px",
    "--radius-full": "9999px",
    
    # === 过渡 ===
    "--transition-fast": "150ms",
    "--transition-normal": "300ms",
    "--transition-slow": "500ms",
    "--ease-default": "cubic-bezier(0.4, 0, 0.2, 1)",
    "--ease-bounce": "cubic-bezier(0.68, -0.55, 0.265, 1.55)",
    
    # === 字体 ===
    "--font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif",
    "--font-family-mono": "'Monaco', 'Courier New', monospace",
    
    # === 字号 ===
    "--font-size-xs": "11px",
    "--font-size-sm": "12px",
    "--font-size-base": "14px",
    "--font-size-lg": "16px",
    "--font-size-xl": "18px",
    "--font-size-2xl": "20px",
    "--font-size-3xl": "24px",
    "--font-size-4xl": "28px",
    "--font-size-5xl": "32px",
    
    # === 字重 ===
    "--font-weight-normal": "400",
    "--font-weight-medium": "500",
    "--font-weight-semibold": "600",
    "--font-weight-bold": "700",
    "--font-weight-extrabold": "800",
    
    # === 行高 ===
    "--line-height-tight": "1.2",
    "--line-height-normal": "1.5",
    "--line-height-relaxed": "1.6",
    
    # === 布局尺寸 ===
    "--sidebar-width": "180px",
    "--sidebar-width-collapsed": "160px",
    "--header-height": "90px",
    "--page-min-width": "1260px",
    "--content-padding-x": "40px",
    "--content-padding-y": "24px",
    
    # === 组件尺寸 ===
    "--input-height": "42px",
    "--input-height-sm": "36px",
    "--input-height-lg": "48px",
    "--button-height": "42px",
    "--button-height-sm": "32px",
    "--button-height-lg": "48px",
    
    # === 滚动条 ===
    "--scrollbar-width": "8px",
    "--scrollbar-track": "#f1f3fa",
    "--scrollbar-thumb": "linear-gradient(180deg, var(--primary) 0%, var(--info) 100%)",
    "--scrollbar-thumb-hover": "linear-gradient(180deg, #5a5fd8 0%, #4286ed 100%)",
    
    # === 图表颜色 ===
    "--chart-primary": "#5B6BD1",
    "--chart-success": "#52C41A",
    "--chart-warning": "#FAAD14",
    "--chart-danger": "#F5222D",
    "--chart-info": "#4A90E2",
    "--chart-area-start": "rgba(91, 107, 209, 0.3)",
    "--chart-area-end": "rgba(91, 107, 209, 0.05)",
    "--chart-grid": "#F0F0F0",
    "--chart-axis": "#E8E8E8",
    "--chart-label": "#8C8C8C",
}

# 深色主题Token
DARK_THEME = {
    # === 品牌色 ===
    "--primary": "#7B8BE8",
    "--primary-hover": "#8F9DEF",
    "--primary-light": "#9AA8F2",
    "--primary-dark": "#6A7AD8",
    "--primary-gradient": "linear-gradient(135deg, #7B8BE8 0%, #9D7BDE 100%)",
    "--primary-alpha": "rgba(123, 139, 232, 0.15)",
    "--primary-alpha-hover": "rgba(123, 139, 232, 0.1)",
    
    # === 功能色 ===
    "--success": "#73D13D",
    "--success-bg": "rgba(115, 209, 61, 0.1)",
    "--success-border": "rgba(115, 209, 61, 0.3)",
    "--warning": "#FFD666",
    "--warning-bg": "rgba(255, 214, 102, 0.1)",
    "--warning-border": "rgba(255, 214, 102, 0.3)",
    "--danger": "#FF7875",
    "--danger-bg": "rgba(255, 120, 117, 0.1)",
    "--danger-border": "rgba(255, 120, 117, 0.3)",
    "--info": "#69C0FF",
    "--info-bg": "rgba(105, 192, 255, 0.1)",
    "--info-border": "rgba(105, 192, 255, 0.3)",
    
    # === 背景色 ===
    "--bg-page": "#0F0F0F",
    "--bg-content": "#1A1A1A",
    "--bg-card": "#2D2D2D",
    "--bg-hover": "rgba(123, 139, 232, 0.1)",
    "--bg-active": "rgba(123, 139, 232, 0.08)",
    "--bg-sidebar": "rgba(26, 26, 26, 0.95)",
    "--bg-header": "rgba(26, 26, 26, 0.98)",
    "--bg-input": "#2D2D2D",
    "--bg-table-header": "#252525",
    "--bg-table-hover": "#333333",
    
    # === 文字色 ===
    "--text-primary": "#E8E8E8",
    "--text-secondary": "#ACACAC",
    "--text-tertiary": "#8C8C8C",
    "--text-disabled": "#5C5C5C",
    "--text-placeholder": "#6C6C6C",
    "--text-inverse": "#1A1A1A",
    
    # === 边框色 ===
    "--border-light": "#404040",
    "--border-normal": "#4A4A4A",
    "--border-dark": "#5C5C5C",
    "--border-primary": "rgba(123, 139, 232, 0.3)",
    "--border-focus": "rgba(123, 139, 232, 0.5)",
    
    # === 阴影 ===
    "--shadow-sm": "0 2px 8px rgba(0, 0, 0, 0.3)",
    "--shadow-md": "0 4px 16px rgba(0, 0, 0, 0.4)",
    "--shadow-lg": "0 8px 32px rgba(0, 0, 0, 0.5)",
    "--shadow-primary": "0 4px 16px rgba(123, 139, 232, 0.3)",
    "--shadow-primary-sm": "0 4px 12px rgba(123, 139, 232, 0.15)",
    "--shadow-sidebar": "4px 0 16px rgba(0, 0, 0, 0.3)",
    "--shadow-header": "0 2px 16px rgba(0, 0, 0, 0.3)",
    
    # === 间距 (与浅色主题相同) ===
    "--spacing-xs": "4px",
    "--spacing-sm": "8px",
    "--spacing-md": "16px",
    "--spacing-lg": "24px",
    "--spacing-xl": "32px",
    "--spacing-2xl": "40px",
    
    # === 圆角 (与浅色主题相同) ===
    "--radius-xs": "4px",
    "--radius-sm": "6px",
    "--radius-md": "8px",
    "--radius-lg": "12px",
    "--radius-xl": "16px",
    "--radius-full": "9999px",
    
    # === 过渡 (与浅色主题相同) ===
    "--transition-fast": "150ms",
    "--transition-normal": "300ms",
    "--transition-slow": "500ms",
    "--ease-default": "cubic-bezier(0.4, 0, 0.2, 1)",
    "--ease-bounce": "cubic-bezier(0.68, -0.55, 0.265, 1.55)",
    
    # === 字体 (与浅色主题相同) ===
    "--font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif",
    "--font-family-mono": "'Monaco', 'Courier New', monospace",
    
    # === 字号 (与浅色主题相同) ===
    "--font-size-xs": "11px",
    "--font-size-sm": "12px",
    "--font-size-base": "14px",
    "--font-size-lg": "16px",
    "--font-size-xl": "18px",
    "--font-size-2xl": "20px",
    "--font-size-3xl": "24px",
    "--font-size-4xl": "28px",
    "--font-size-5xl": "32px",
    
    # === 字重 (与浅色主题相同) ===
    "--font-weight-normal": "400",
    "--font-weight-medium": "500",
    "--font-weight-semibold": "600",
    "--font-weight-bold": "700",
    "--font-weight-extrabold": "800",
    
    # === 行高 (与浅色主题相同) ===
    "--line-height-tight": "1.2",
    "--line-height-normal": "1.5",
    "--line-height-relaxed": "1.6",
    
    # === 布局尺寸 (与浅色主题相同) ===
    "--sidebar-width": "180px",
    "--sidebar-width-collapsed": "160px",
    "--header-height": "90px",
    "--page-min-width": "1260px",
    "--content-padding-x": "40px",
    "--content-padding-y": "24px",
    
    # === 组件尺寸 (与浅色主题相同) ===
    "--input-height": "42px",
    "--input-height-sm": "36px",
    "--input-height-lg": "48px",
    "--button-height": "42px",
    "--button-height-sm": "32px",
    "--button-height-lg": "48px",
    
    # === 滚动条 ===
    "--scrollbar-width": "8px",
    "--scrollbar-track": "#252525",
    "--scrollbar-thumb": "linear-gradient(180deg, #7B8BE8 0%, #69C0FF 100%)",
    "--scrollbar-thumb-hover": "linear-gradient(180deg, #8F9DEF 0%, #85CFFF 100%)",
    
    # === 图表颜色 ===
    "--chart-primary": "#7B8BE8",
    "--chart-success": "#73D13D",
    "--chart-warning": "#FFD666",
    "--chart-danger": "#FF7875",
    "--chart-info": "#69C0FF",
    "--chart-area-start": "rgba(123, 139, 232, 0.3)",
    "--chart-area-end": "rgba(123, 139, 232, 0.05)",
    "--chart-grid": "#333333",
    "--chart-axis": "#404040",
    "--chart-label": "#8C8C8C",
}


def get_theme(mode: str = "light") -> dict:
    """获取指定模式的主题Token"""
    return LIGHT_THEME if mode == "light" else DARK_THEME


def generate_css_variables(mode: str = "light") -> str:
    """生成CSS变量定义字符串"""
    theme = get_theme(mode)
    lines = [":root {"]
    for key, value in theme.items():
        lines.append(f"    {key}: {value};")
    lines.append("}")
    return "\n".join(lines)
