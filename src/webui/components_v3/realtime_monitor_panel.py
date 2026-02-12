"""
实时执行监控面板
显示Agent执行状态、Token消耗、步骤进度
"""
import gradio as gr
from src.webui.webui_manager import WebuiManager


def create_realtime_monitor_panel(webui_manager: WebuiManager):
    """创建实时监控面板"""
    
    # === 整体状态卡片 ===
    with gr.Group(elem_classes=["card", "status-card"]):
        gr.Markdown("### 🎯 执行状态")
        status_display = gr.Markdown("**当前状态**: 空闲\n\n*等待Agent任务启动...*")
    
    # === 执行指标卡片 ===
    with gr.Row():
        # Token消耗卡片
        with gr.Column(scale=1):
            with gr.Group(elem_classes=["card", "metric-card"]):
                gr.Markdown("### 💰 Token消耗")
                token_display = gr.Markdown("""
**Token使用情况**:
- Prompt Tokens: 0
- Completion Tokens: 0
- 总计: 0
                """)
        
        # 执行进度卡片
        with gr.Column(scale=1):
            with gr.Group(elem_classes=["card", "metric-card"]):
                gr.Markdown("### ⏱️ 执行进度")
                progress_display = gr.Markdown("""
**执行统计**:
- 当前步数: 0 / 30
- 总耗时: 0.0秒
- 平均步骤耗时: 0.0秒
                """)
        
        # 重试统计卡片
        with gr.Column(scale=1):
            with gr.Group(elem_classes=["card", "metric-card"]):
                gr.Markdown("### 🔄 重试统计")
                retry_display = gr.Markdown("""
**重试记录**:
- 系统级重试: 0
- 业务级重试: 0
- 总重试次数: 0
                """)
    
    # === 步骤历史时间线 ===
    with gr.Group(elem_classes=["card"]):
        gr.Markdown("### 📋 执行步骤历史")
        steps_timeline = gr.Markdown("""
*暂无执行记录*

当Agent开始执行时,此处将显示每个步骤的详细信息。
        """)
    
    # === 使用说明 ===
    with gr.Group(elem_classes=["card"]):
        gr.Markdown("""
### 💡 监控面板说明

此面板用于实时查看Agent执行状态。主要指标包括:

- **执行状态**: 显示Agent当前状态(运行中/暂停/完成)
- **Token消耗**: 实时统计Prompt和Completion Token使用量
- **执行进度**: 显示当前执行步数和平均耗时
- **重试统计**: 记录系统级和业务级重试次数
- **步骤历史**: 按时间线展示每个步骤的详细操作

**注意**: 监控数据在"执行Agent"页面运行任务时实时更新。
        """)
    
    # 返回组件以便在browser_use_agent中更新
    return {
        "status_display": status_display,
        "token_display": token_display,
        "progress_display": progress_display,
        "retry_display": retry_display,
        "steps_timeline": steps_timeline,
    }
