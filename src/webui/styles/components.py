"""
组件样式 - 卡片、表单、表格、导航、按钮等
"""


def get_navigation_styles() -> str:
    """获取导航组件样式"""
    return """
    /* === 导航容器 === */
    .nav-container {
        padding: 12px 8px !important;
    }

    .sidebar .gr-radio-group {
        gap: 6px !important;
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }

    .sidebar .gr-radio-group label {
        display: flex !important;
        align-items: center !important;
        padding: 12px 14px !important;
        border-radius: var(--radius-md) !important;
        font-size: var(--font-size-base) !important;
        font-weight: var(--font-weight-medium) !important;
        color: var(--text-primary) !important;
        background: transparent !important;
        border: 1px solid transparent !important;
        transition: all 0.4s var(--ease-default) !important;
        cursor: pointer !important;
        margin: 0 !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .sidebar .gr-radio-group label::before {
        content: "" !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        width: 0 !important;
        height: 0 !important;
        border-radius: 50% !important;
        background: radial-gradient(circle, var(--primary-alpha) 0%, transparent 70%) !important;
        transform: translate(-50%, -50%) !important;
        transition: width 0.6s ease, height 0.6s ease !important;
        pointer-events: none !important;
    }

    .sidebar .gr-radio-group label:hover {
        background: linear-gradient(135deg, var(--primary-alpha-hover) 0%, rgba(82, 147, 254, 0.08) 100%) !important;
        color: var(--primary) !important;
        border-color: var(--border-focus) !important;
        transform: translateX(4px) !important;
        box-shadow: var(--shadow-primary-sm), inset 0 0 0 1px var(--primary-alpha) !important;
    }
    
    .sidebar .gr-radio-group label:hover::before {
        width: 200% !important;
        height: 200% !important;
    }

    .sidebar .gr-radio-group label.selected {
        background: var(--primary-gradient) !important;
        color: var(--text-inverse) !important;
        font-weight: var(--font-weight-semibold) !important;
        border-color: transparent !important;
        box-shadow: var(--shadow-primary), 0 0 20px var(--primary-alpha), inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        transform: translateX(6px) scale(1.02) !important;
    }
    
    .sidebar .gr-radio-group label.selected::before {
        background: radial-gradient(circle, rgba(255, 255, 255, 0.2) 0%, transparent 70%) !important;
        width: 200% !important;
        height: 200% !important;
        animation: ripple 2s ease-in-out infinite !important;
    }

    .sidebar .gr-radio-group input[type="radio"] {
        display: none !important;
    }
    """


def get_card_styles() -> str:
    """获取卡片组件样式"""
    return """
    /* === 基础卡片样式 === */
    .card {
        background: var(--bg-card) !important;
        border-radius: var(--radius-md) !important;
        border: 1px solid var(--border-light) !important;
        box-shadow: var(--shadow-sm) !important;
        padding: var(--spacing-lg) !important;
        margin-bottom: 20px !important;
        transition: box-shadow var(--transition-normal) var(--ease-default) !important;
        position: relative !important;
    }

    .card:hover {
        box-shadow: var(--shadow-md) !important;
    }
    
    /* === 卡片内容样式 === */
    .card h1 {
        color: var(--primary) !important;
        font-size: var(--font-size-4xl) !important;
        margin-bottom: 20px !important;
        font-weight: var(--font-weight-bold) !important;
    }
    
    .card h2 {
        color: var(--text-primary) !important;
        font-size: var(--font-size-2xl) !important;
        margin-top: var(--spacing-lg) !important;
        margin-bottom: var(--spacing-md) !important;
        font-weight: var(--font-weight-semibold) !important;
        border-left: 4px solid var(--primary) !important;
        padding-left: 12px !important;
    }

    .card h3 {
        color: var(--text-primary) !important;
        font-size: var(--font-size-lg) !important;
        font-weight: var(--font-weight-semibold) !important;
        margin-bottom: var(--spacing-md) !important;
    }
    
    .card ul {
        list-style: none !important;
        padding-left: 0 !important;
    }
    
    .card li {
        padding: 8px 0 !important;
        color: var(--text-primary) !important;
        line-height: var(--line-height-relaxed) !important;
    }
    
    .card li strong {
        color: var(--primary) !important;
    }
    
    /* === 欢迎卡片特殊样式 === */
    .welcome-card {
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.98) 0%, 
            rgba(248, 249, 255, 0.95) 100%) !important;
        border: 2px solid transparent !important;
        background-clip: padding-box !important;
        position: relative !important;
        box-shadow: 
            0 8px 32px var(--primary-alpha),
            0 0 0 1px var(--border-primary),
            inset 0 1px 0 rgba(255, 255, 255, 1),
            0 0 60px rgba(103, 107, 239, 0.08) !important;
    }
    
    .welcome-card::before {
        content: "" !important;
        position: absolute !important;
        inset: -2px !important;
        border-radius: var(--radius-lg) !important;
        padding: 2px !important;
        background: linear-gradient(135deg, 
            rgba(103, 107, 239, 0.6) 0%, 
            rgba(82, 147, 254, 0.4) 50%,
            rgba(118, 75, 162, 0.5) 100%) !important;
        -webkit-mask: 
            linear-gradient(#fff 0 0) content-box, 
            linear-gradient(#fff 0 0) !important;
        -webkit-mask-composite: xor !important;
        mask-composite: exclude !important;
        opacity: 0.8 !important;
        animation: borderGlow 3s ease-in-out infinite !important;
    }
    
    .welcome-card h1 {
        background: var(--primary-gradient) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        position: relative !important;
        animation: titlePulse 2s ease-in-out infinite !important;
    }
    
    /* === 仪表盘统计卡片 === */
    .dashboard-stats-card {
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.98) 0%, 
            rgba(248, 249, 255, 0.98) 100%) !important;
        padding: var(--spacing-xl) !important;
        margin-bottom: var(--spacing-lg) !important;
    }
    
    .stats-title,
    .history-title,
    .detail-title {
        font-size: var(--font-size-2xl) !important;
        font-weight: var(--font-weight-bold) !important;
        margin: 0 0 20px 0 !important;
        padding-bottom: 12px !important;
        border-bottom: 2px solid var(--border-primary) !important;
        background: var(--primary-gradient) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }
    
    /* 统计网格布局 */
    .stats-grid {
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important;
        gap: var(--spacing-lg) !important;
        margin-top: var(--spacing-md) !important;
    }
    
    .stat-item {
        text-align: center !important;
        padding: 20px !important;
        background: var(--bg-active) !important;
        border-radius: var(--radius-md) !important;
        border: 1px solid var(--border-primary) !important;
        transition: all var(--transition-normal) var(--ease-default) !important;
    }
    
    .stat-item:hover {
        background: var(--bg-hover) !important;
        border-color: var(--border-focus) !important;
        transform: translateY(-2px) !important;
    }
    
    .stat-label {
        font-size: var(--font-size-base) !important;
        font-weight: var(--font-weight-semibold) !important;
        color: var(--text-secondary) !important;
        margin-bottom: 10px !important;
    }
    
    .stat-value {
        font-size: var(--font-size-5xl) !important;
        font-weight: var(--font-weight-extrabold) !important;
        background: var(--primary-gradient) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        margin: 8px 0 !important;
        line-height: var(--line-height-tight) !important;
    }
    
    .stat-detail {
        font-size: var(--font-size-sm) !important;
        color: var(--text-tertiary) !important;
        margin-top: 6px !important;
    }
    
    /* === 任务历史卡片 === */
    .task-history-card {
        padding: 28px !important;
        margin-bottom: 20px !important;
    }

    /* === 任务详情卡片 === */
    .task-detail-card {
        padding: 28px !important;
        margin-top: 20px !important;
    }
    
    /* 详情占位符 */
    .detail-placeholder {
        text-align: center !important;
        padding: 40px 20px !important;
    }
    
    .placeholder-icon {
        font-size: 48px !important;
        margin-bottom: 16px !important;
        opacity: 0.6 !important;
    }
    
    .placeholder-text {
        font-size: var(--font-size-lg) !important;
        font-weight: var(--font-weight-semibold) !important;
        color: var(--text-primary) !important;
        margin-bottom: 8px !important;
    }
    
    .placeholder-hint {
        font-size: var(--font-size-sm) !important;
        color: var(--text-tertiary) !important;
    }
    
    /* 任务详情统计 */
    .task-detail-stats {
        background: var(--bg-active) !important;
        border-radius: var(--radius-md) !important;
        padding: 20px !important;
        border: 1px solid var(--border-primary) !important;
    }
    
    .detail-header {
        font-size: var(--font-size-lg) !important;
        font-weight: var(--font-weight-bold) !important;
        margin-bottom: 16px !important;
        padding-bottom: 12px !important;
        border-bottom: 2px solid var(--border-primary) !important;
        background: var(--primary-gradient) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }
    
    .detail-row {
        display: flex !important;
        justify-content: space-between !important;
        padding: 8px 0 !important;
        border-bottom: 1px solid rgba(103, 107, 239, 0.08) !important;
    }
    
    .detail-row.sub {
        padding-left: 16px !important;
        font-size: var(--font-size-sm) !important;
    }
    
    .detail-row:last-child {
        border-bottom: none !important;
    }
    
    .detail-label {
        font-weight: var(--font-weight-semibold) !important;
        color: var(--text-secondary) !important;
        font-size: var(--font-size-base) !important;
    }
    
    .detail-value {
        font-weight: var(--font-weight-medium) !important;
        color: var(--text-primary) !important;
        font-size: var(--font-size-base) !important;
        font-family: var(--font-family-mono) !important;
    }
    
    .detail-value.highlight {
        color: var(--primary) !important;
        font-weight: var(--font-weight-bold) !important;
        font-size: var(--font-size-lg) !important;
    }
    
    .detail-divider {
        height: 12px !important;
        border-bottom: 2px dashed var(--border-primary) !important;
        margin: 12px 0 !important;
    }

    /* === 响应式卡片 === */
    @media (max-width: 1600px) {
        .metric-card-container {
            flex-direction: column !important;
            text-align: center !important;
        }
        
        .metric-icon {
            margin: 0 0 12px 0 !important;
        }
        
        .metric-content {
            text-align: center !important;
        }
    }
    
    @media (max-width: 1200px) {
        .stats-grid {
            grid-template-columns: repeat(2, 1fr) !important;
        }
    }
    """


def get_metric_card_styles() -> str:
    """获取指标卡片样式"""
    return """
    /* === 指标卡片 === */
    .metric-card {
        text-align: center !important;
        min-height: 120px !important;
    }

    .metric-card h3 {
        color: var(--text-secondary) !important;
        font-size: var(--font-size-base) !important;
        margin-bottom: 12px !important;
        font-weight: var(--font-weight-semibold) !important;
    }
    
    /* 指标卡片容器 */
    .metric-card-container {
        display: flex !important;
        align-items: center !important;
        padding: var(--spacing-lg) !important;
        background: var(--bg-card) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: var(--radius-md) !important;
        transition: all var(--transition-normal) var(--ease-default) !important;
        min-height: 120px !important;
    }
    
    .metric-card-container:hover {
        border-color: var(--primary) !important;
        box-shadow: var(--shadow-primary-sm) !important;
    }
    
    .metric-icon {
        width: 56px !important;
        height: 56px !important;
        border-radius: var(--radius-md) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 28px !important;
        margin-right: 16px !important;
        flex-shrink: 0 !important;
    }
    
    .metric-icon.token {
        background: linear-gradient(135deg, #E6F7FF 0%, #BAE7FF 100%) !important;
    }
    
    .metric-icon.tasks {
        background: linear-gradient(135deg, #F0F5FF 0%, #D6E4FF 100%) !important;
    }
    
    .metric-icon.success {
        background: linear-gradient(135deg, #F6FFED 0%, #D9F7BE 100%) !important;
    }
    
    .metric-icon.duration {
        background: linear-gradient(135deg, #FFF7E6 0%, #FFE7BA 100%) !important;
    }
    
    .metric-content {
        flex: 1 !important;
        text-align: left !important;
    }
    
    .metric-label {
        font-size: var(--font-size-base) !important;
        color: var(--text-tertiary) !important;
        margin-bottom: 8px !important;
        font-weight: var(--font-weight-medium) !important;
    }
    
    .metric-value {
        font-size: var(--font-size-5xl) !important;
        font-weight: var(--font-weight-bold) !important;
        color: var(--text-primary) !important;
        line-height: var(--line-height-tight) !important;
        margin-bottom: 4px !important;
    }
    
    .metric-trend {
        font-size: var(--font-size-sm) !important;
        margin-top: 4px !important;
        font-weight: var(--font-weight-medium) !important;
    }
    
    .metric-trend.up {
        color: var(--success) !important;
    }
    
    .metric-trend.down {
        color: var(--danger) !important;
    }
    
    .metric-trend.neutral {
        color: var(--text-tertiary) !important;
    }
    """


def get_form_styles() -> str:
    """获取表单组件样式"""
    return """
    /* === 表单输入框 === */
    .card input[type="text"],
    .card input[type="number"],
    .card textarea,
    .card select {
        min-height: var(--input-height) !important;
        padding: 10px 14px !important;
        font-size: var(--font-size-base) !important;
        line-height: var(--line-height-relaxed) !important;
        border-radius: var(--radius-sm) !important;
        border: 1.5px solid var(--border-primary) !important;
        background: var(--bg-input) !important;
        color: var(--text-primary) !important;
        transition: all var(--transition-normal) var(--ease-default) !important;
    }
    
    .card input[type="text"]:focus,
    .card input[type="number"]:focus,
    .card textarea:focus,
    .card select:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px var(--primary-alpha) !important;
        outline: none !important;
    }
    
    .card textarea {
        min-height: 100px !important;
        resize: vertical !important;
    }
    
    .card label {
        font-size: var(--font-size-base) !important;
        font-weight: var(--font-weight-semibold) !important;
        color: var(--text-primary) !important;
        margin-bottom: 8px !important;
        display: block !important;
    }
    
    .card .form-group {
        margin-bottom: 20px !important;
    }
    
    /* Dropdown优化 */
    .card .dropdown {
        min-height: var(--input-height) !important;
    }
    
    .card .dropdown-menu {
        border-radius: var(--radius-md) !important;
        box-shadow: var(--shadow-md) !important;
        background: var(--bg-card) !important;
        border: 1px solid var(--border-light) !important;
    }

    /* 全局表单元素 */
    input, select, textarea, .gr-textbox, .gr-dropdown {
        border: 1px solid var(--border-light) !important;
        border-radius: var(--radius-sm) !important;
        background: var(--bg-input) !important;
        color: var(--text-primary) !important;
        transition: all var(--transition-normal) var(--ease-default) !important;
    }

    input:focus, select:focus, textarea:focus,
    .gr-textbox:focus, .gr-dropdown:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px var(--primary-alpha) !important;
        outline: none !important;
    }

    input::placeholder,
    textarea::placeholder {
        color: var(--text-placeholder) !important;
    }
    
    /* 筛选工具栏 */
    .filter-toolbar {
        gap: 12px !important;
        margin-bottom: 16px !important;
        align-items: flex-end !important;
    }
    
    .filter-toolbar button {
        height: var(--input-height-lg) !important;
        font-size: 15px !important;
        font-weight: var(--font-weight-semibold) !important;
        padding: 0 24px !important;
    }
    
    .filter-dropdown label {
        font-size: var(--font-size-base) !important;
        font-weight: var(--font-weight-semibold) !important;
        margin-bottom: 6px !important;
    }
    
    .filter-dropdown select,
    .filter-dropdown .dropdown {
        height: var(--input-height-lg) !important;
        font-size: var(--font-size-base) !important;
        padding: 0 14px !important;
    }
    """


def get_button_styles() -> str:
    """获取按钮样式"""
    return """
    /* === 按钮样式 === */
    button {
        border-radius: var(--radius-sm) !important;
        font-weight: var(--font-weight-semibold) !important;
        transition: all var(--transition-normal) var(--ease-default) !important;
        cursor: pointer !important;
    }

    button.primary, .btn-primary {
        background-color: var(--primary) !important;
        color: var(--text-inverse) !important;
        border: none !important;
    }

    button.primary:hover, .btn-primary:hover {
        background-color: var(--primary-hover) !important;
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-primary-sm) !important;
    }

    button.secondary, .btn-secondary {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-light) !important;
    }

    button.secondary:hover, .btn-secondary:hover {
        border-color: var(--primary) !important;
        color: var(--primary) !important;
    }

    button:disabled {
        opacity: 0.5 !important;
        cursor: not-allowed !important;
        transform: none !important;
    }
    """


def get_table_styles() -> str:
    """获取表格样式"""
    return """
    /* === 任务表格 === */
    .task-table {
        margin-top: 12px !important;
    }
    
    .task-table table {
        font-size: var(--font-size-sm) !important;
        border-collapse: separate !important;
        border-spacing: 0 !important;
        width: 100% !important;
    }
    
    .task-table th {
        background: var(--bg-table-header) !important;
        font-weight: var(--font-weight-semibold) !important;
        font-size: var(--font-size-base) !important;
        color: var(--text-primary) !important;
        padding: 12px 16px !important;
        border-bottom: 2px solid var(--border-light) !important;
        text-align: left !important;
    }
    
    .task-table td {
        padding: 12px 16px !important;
        line-height: var(--line-height-normal) !important;
        border-bottom: 1px solid var(--border-light) !important;
        color: var(--text-primary) !important;
    }
    
    .task-table tr:hover {
        background: var(--bg-table-hover) !important;
        cursor: pointer !important;
    }

    /* === 通用数据表格 === */
    .data-table {
        width: 100% !important;
        border-collapse: collapse !important;
    }

    .data-table th,
    .data-table td {
        padding: 12px 16px !important;
        text-align: left !important;
        border-bottom: 1px solid var(--border-light) !important;
    }

    .data-table th {
        background: var(--bg-table-header) !important;
        font-weight: var(--font-weight-semibold) !important;
        color: var(--text-primary) !important;
    }

    .data-table tbody tr:hover {
        background: var(--bg-table-hover) !important;
    }

    /* === GIF显示优化 === */
    .task-gif {
        border-radius: var(--radius-md) !important;
        overflow: hidden !important;
    }
    
    .task-gif img {
        border-radius: var(--radius-md) !important;
        border: 2px solid var(--border-primary) !important;
    }
    
    /* TaskRecordingGif优化 */
    #task_recording_gif,
    .task-recording-container,
    .task-recording-container .image {
        min-height: 600px !important;
        max-height: 800px !important;
        height: auto !important;
    }
    
    .task-recording-container .image img {
        object-fit: contain !important;
        width: 100% !important;
        height: auto !important;
        border-radius: var(--radius-md) !important;
    }
    
    /* 旧样式兼容 */
    .stat-card,
    .history-card {
        margin-bottom: 16px !important;
    }
    
    .dashboard-title {
        display: none !important;
    }
    """


def get_status_styles() -> str:
    """获取状态标签样式"""
    return """
    /* === 状态标签 === */
    .status-badge {
        display: inline-block !important;
        padding: 4px 12px !important;
        border-radius: var(--radius-full) !important;
        font-size: var(--font-size-sm) !important;
        font-weight: var(--font-weight-semibold) !important;
    }

    .status-badge.success {
        background-color: var(--success-bg) !important;
        color: var(--success) !important;
    }

    .status-badge.error {
        background-color: var(--danger-bg) !important;
        color: var(--danger) !important;
    }

    .status-badge.running {
        background-color: var(--info-bg) !important;
        color: var(--info) !important;
    }

    .status-badge.warning {
        background-color: var(--warning-bg) !important;
        color: var(--warning) !important;
    }
    """


def get_chart_container_styles() -> str:
    """获取图表容器样式"""
    return """
    /* === 图表容器 === */
    .chart-container {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: var(--radius-md) !important;
        padding: var(--spacing-lg) !important;
        margin-bottom: 20px !important;
    }
    
    .chart-title {
        font-size: var(--font-size-lg) !important;
        font-weight: var(--font-weight-semibold) !important;
        color: var(--text-primary) !important;
        margin-bottom: 16px !important;
        padding-bottom: 12px !important;
        border-bottom: 1px solid var(--border-light) !important;
    }
    """


def get_component_styles() -> str:
    """获取所有组件样式的组合"""
    return "\n".join([
        get_navigation_styles(),
        get_card_styles(),
        get_metric_card_styles(),
        get_form_styles(),
        get_button_styles(),
        get_table_styles(),
        get_status_styles(),
        get_chart_container_styles(),
    ])
