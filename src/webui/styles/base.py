"""
全局基础样式 - 重置、滚动条、Gradio容器
"""


def get_base_styles() -> str:
    """获取全局基础样式"""
    return """
    /* === 全局重置 === */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* === Gradio容器样式 === */
    .gradio-container {
        font-family: var(--font-family) !important;
        background: var(--bg-page) !important;
        min-width: var(--page-min-width) !important;
        width: 100vw !important;
        max-width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }

    .gradio-container > div,
    .gradio-container .contain {
        gap: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* === 滚动条样式 === */
    ::-webkit-scrollbar {
        width: var(--scrollbar-width) !important;
        height: var(--scrollbar-width) !important;
    }

    ::-webkit-scrollbar-track {
        background: var(--scrollbar-track) !important;
        border-radius: var(--radius-xs) !important;
    }

    ::-webkit-scrollbar-thumb {
        background: var(--scrollbar-thumb) !important;
        border-radius: var(--radius-xs) !important;
        transition: background var(--transition-normal) var(--ease-default) !important;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--scrollbar-thumb-hover) !important;
    }
    
    /* Firefox滚动条 */
    * {
        scrollbar-width: thin;
        scrollbar-color: var(--primary) var(--scrollbar-track);
    }

    /* === 隐藏Gradio默认样式 === */
    .gr-form, .gr-box {
        border: none !important;
        background: transparent !important;
    }

    /* === 链接样式 === */
    a {
        color: var(--primary);
        text-decoration: none;
        transition: color var(--transition-fast) var(--ease-default);
    }

    a:hover {
        color: var(--primary-hover);
    }

    /* === 文本选中样式 === */
    ::selection {
        background-color: var(--primary-alpha);
        color: var(--text-primary);
    }

    ::-moz-selection {
        background-color: var(--primary-alpha);
        color: var(--text-primary);
    }
    """
