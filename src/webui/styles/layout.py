"""
布局样式 - 侧边栏、头部、内容区
"""


def get_layout_styles() -> str:
    """获取布局样式"""
    return """
    /* === 主布局容器 === */
    .main-layout {
        display: flex !important;
        height: 100vh !important;
        overflow: hidden !important;
    }

    /* === 侧边栏 === */
    .sidebar {
        width: var(--sidebar-width) !important;
        min-width: var(--sidebar-width) !important;
        max-width: var(--sidebar-width) !important;
        background: var(--bg-sidebar) !important;
        backdrop-filter: blur(10px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(10px) saturate(180%) !important;
        border-right: 1px solid var(--border-primary) !important;
        box-shadow: var(--shadow-sidebar), inset -1px 0 0 var(--primary-alpha) !important;
        overflow-y: auto !important;
        height: 100vh !important;
        flex-shrink: 0 !important;
        position: relative !important;
    }
    
    /* 侧边栏顶部装饰条 */
    .sidebar::before {
        content: "" !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 4px !important;
        background: var(--primary-gradient) !important;
        background-size: 200% 100% !important;
        animation: shimmer 3s linear infinite !important;
    }

    /* === 内容区域 === */
    .content-area {
        flex: 1 !important;
        display: flex !important;
        flex-direction: column !important;
        overflow: hidden !important;
        min-width: 0 !important;
    }

    /* === 页面头部 === */
    .page-header {
        height: var(--header-height) !important;
        background: var(--bg-header) !important;
        backdrop-filter: blur(10px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(10px) saturate(180%) !important;
        border-bottom: 1px solid var(--border-primary) !important;
        box-shadow: var(--shadow-header), inset 0 -1px 0 var(--primary-alpha) !important;
        padding: 0 var(--content-padding-x) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        flex-shrink: 0 !important;
        position: relative !important;
        z-index: 10 !important;
    }
    
    /* 头部底部装饰线 */
    .page-header::after {
        content: "" !important;
        position: absolute !important;
        bottom: -2px !important;
        left: 0 !important;
        right: 0 !important;
        height: 2px !important;
        background: linear-gradient(90deg, 
            transparent 0%, 
            var(--primary) 50%, 
            transparent 100%) !important;
        opacity: 0.3 !important;
    }

    .page-header h1 {
        font-size: var(--font-size-3xl) !important;
        font-weight: var(--font-weight-bold) !important;
        background: var(--primary-gradient) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        margin: 0 !important;
        text-shadow: 0 0 30px var(--primary-alpha) !important;
    }

    .page-header p {
        font-size: var(--font-size-base) !important;
        color: var(--text-secondary) !important;
        margin: 5px 0 0 0 !important;
    }

    /* === 页面内容区 === */
    .page-content {
        flex: 1 !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
        padding: var(--content-padding-y) var(--content-padding-x) var(--content-padding-x) !important;
        background-color: transparent !important;
        min-height: 0 !important;
        max-height: calc(100vh - var(--header-height)) !important;
        scrollbar-width: thin !important;
        scrollbar-color: var(--primary) var(--scrollbar-track) !important;
    }
    
    /* 页面容器 */
    .page-content > .block {
        width: 100% !important;
        height: auto !important;
        min-height: calc(100vh - 180px) !important;
        margin-bottom: 0 !important;
    }
    
    /* 单个页面Column样式 */
    .page-content .block > .block {
        width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* 隐藏的页面不占用空间 */
    .page-content .block[style*="display: none"] {
        height: 0 !important;
        overflow: hidden !important;
        padding: 0 !important;
        margin: 0 !important;
        visibility: hidden !important;
    }
    
    /* 单个页面样式 */
    .single-page {
        width: 100% !important;
        min-height: calc(100vh - 180px) !important;
        padding-bottom: var(--content-padding-x) !important;
    }
    
    .single-page > * {
        margin-bottom: 20px !important;
        position: relative !important;
        z-index: 1 !important;
    }
    
    .single-page > *:last-child {
        margin-bottom: 0 !important;
    }

    /* === Logo区域 === */
    .logo-section {
        padding: 20px 12px !important;
        text-align: center !important;
        border-bottom: 1px solid var(--border-light) !important;
    }

    .logo-title {
        font-size: var(--font-size-xl) !important;
        font-weight: var(--font-weight-bold) !important;
        color: var(--primary) !important;
        margin-bottom: 4px !important;
    }

    .logo-subtitle {
        font-size: var(--font-size-xs) !important;
        color: var(--text-secondary) !important;
    }

    /* === 主题切换按钮 === */
    .theme-toggle {
        width: 40px !important;
        height: 40px !important;
        border-radius: var(--radius-md) !important;
        background: var(--bg-card) !important;
        border: 1px solid var(--border-light) !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 18px !important;
        transition: all var(--transition-normal) var(--ease-default) !important;
    }

    .theme-toggle:hover {
        border-color: var(--primary) !important;
        box-shadow: var(--shadow-primary-sm) !important;
        transform: scale(1.05) !important;
    }

    /* === 响应式布局 === */
    @media (max-width: 1600px) {
        .sidebar {
            width: var(--sidebar-width-collapsed) !important;
            min-width: var(--sidebar-width-collapsed) !important;
            max-width: var(--sidebar-width-collapsed) !important;
        }
        
        .page-content {
            padding: 20px 30px !important;
        }
    }
    """
