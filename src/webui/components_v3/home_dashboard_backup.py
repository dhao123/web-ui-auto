"""
首页仪表盘 - 显示累计统计和历史任务
整合实时监控总量和任务历史记录
"""
import gradio as gr
import os
import json
from datetime import datetime
from src.webui.webui_manager import WebuiManager


def create_home_dashboard(webui_manager: WebuiManager):
    """创建首页仪表盘"""
    
    # === 历史累计统计 - 单个大卡片 ===
    with gr.Group(elem_classes=["card", "dashboard-stats-card"]):
        gr.Markdown("## 📊 历史累计统计", elem_classes=["stats-title"])
        
        stats_display = gr.Markdown("""
<div class="stats-grid">
    <div class="stat-item">
        <div class="stat-label">累计Token消耗</div>
        <div class="stat-value">0</div>
        <div class="stat-detail">Prompt: 0 | Completion: 0</div>
    </div>
    <div class="stat-item">
        <div class="stat-label">总任务数</div>
        <div class="stat-value">0</div>
        <div class="stat-detail">成功: 0 | 失败: 0</div>
    </div>
    <div class="stat-item">
        <div class="stat-label">累计运行时长</div>
        <div class="stat-value">0.0 小时</div>
        <div class="stat-detail">平均: 0.0秒 | 最长: 0.0秒</div>
    </div>
</div>
        """)
    
    # === 最近任务历史 ===
    with gr.Group(elem_classes=["card", "task-history-card"]):
        gr.Markdown("## 📜 最近任务历史", elem_classes=["history-title"])
        
        # 筛选工具栏 - 优化按钮大小
        with gr.Row(elem_classes=["filter-toolbar"]):
            refresh_btn = gr.Button("🔄 刷新数据", size="lg", variant="primary", scale=0, min_width=140)
            date_filter = gr.Dropdown(
                choices=["全部", "今天", "最近7天", "最近30天"],
                value="最近7天",
                label="📅 时间筛选",
                scale=1,
                min_width=160,
                elem_classes=["filter-dropdown"]
            )
            status_filter = gr.Dropdown(
                choices=["全部", "成功", "失败", "运行中"],
                value="全部",
                label="🎯 状态筛选",
                scale=1,
                min_width=160,
                elem_classes=["filter-dropdown"]
            )
        
        # 任务列表
        task_table = gr.Dataframe(
            headers=["任务ID", "创建时间", "任务描述", "状态", "耗时(秒)", "Token消耗"],
            datatype=["str", "str", "str", "str", "number", "number"],
            row_count=8,
            col_count=(6, "fixed"),
            interactive=False,
            wrap=True,
            elem_classes=["task-table"]
        )
    
    # === 任务详情面板 ===
    with gr.Group(elem_classes=["card", "task-detail-card"]):
        gr.Markdown("## 📋 任务详情", elem_classes=["detail-title"])
        
        with gr.Row():
            with gr.Column(scale=1):
                task_stats_md = gr.Markdown("""
<div class="detail-placeholder">
    <div class="placeholder-icon">📊</div>
    <div class="placeholder-text">选择任务查看详情</div>
    <div class="placeholder-hint">点击上方任务列表查看完整信息</div>
</div>
                """, elem_classes=["task-stats"])
            
            with gr.Column(scale=1):
                task_gif_display = gr.Image(
                    label="📹 任务执行回放",
                    visible=True,
                    height=350,
                    elem_classes=["task-gif"]
                )
        
        # 详细配置信息(折叠)
        with gr.Accordion("🔧 任务配置详情", open=False):
            task_detail_json = gr.JSON(label="配置信息", visible=True)
    
    # === 数据加载函数 ===
    def load_statistics():
        """加载累计统计数据"""
        history_dir = "tmp/agent_history"
        
        if not os.path.exists(history_dir):
            return """
<div class="stats-grid">
    <div class="stat-item">
        <div class="stat-label">累计Token消耗</div>
        <div class="stat-value">0</div>
        <div class="stat-detail">Prompt: 0 | Completion: 0</div>
    </div>
    <div class="stat-item">
        <div class="stat-label">总任务数</div>
        <div class="stat-value">0</div>
        <div class="stat-detail">成功: 0 | 失败: 0</div>
    </div>
    <div class="stat-item">
        <div class="stat-label">累计运行时长</div>
        <div class="stat-value">0.0 小时</div>
        <div class="stat-detail">平均: 0.0秒 | 最长: 0.0秒</div>
    </div>
</div>
            """
        
        total_prompt = 0
        total_completion = 0
        total_tasks = 0
        success_tasks = 0
        failed_tasks = 0
        total_duration = 0.0
        max_duration = 0.0
        
        for task_dir in os.listdir(history_dir):
            task_path = os.path.join(history_dir, task_dir)
            if not os.path.isdir(task_path):
                continue
            
            json_file = os.path.join(task_path, f"{task_dir}.json")
            if os.path.exists(json_file):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        total_tasks += 1
                        
                        # Token统计
                        if 'token_usage' in data:
                            total_prompt += data['token_usage'].get('total_prompt_tokens', 0)
                            total_completion += data['token_usage'].get('total_completion_tokens', 0)
                        
                        # 状态统计
                        if data.get('final_result', {}).get('is_done'):
                            success_tasks += 1
                        else:
                            failed_tasks += 1
                        
                        # 时长统计
                        duration = data.get('total_duration', 0)
                        total_duration += duration
                        max_duration = max(max_duration, duration)
                except:
                    continue
        
        total_tokens = total_prompt + total_completion
        avg_duration = total_duration / total_tasks if total_tasks > 0 else 0
        total_hours = total_duration / 3600
        
        return f"""
<div class="stats-grid">
    <div class="stat-item">
        <div class="stat-label">💰 累计Token消耗</div>
        <div class="stat-value">{total_tokens:,}</div>
        <div class="stat-detail">Prompt: {total_prompt:,} | Completion: {total_completion:,}</div>
    </div>
    <div class="stat-item">
        <div class="stat-label">🎯 总任务数</div>
        <div class="stat-value">{total_tasks}</div>
        <div class="stat-detail">成功: {success_tasks} | 失败: {failed_tasks}</div>
    </div>
    <div class="stat-item">
        <div class="stat-label">⏱️ 累计运行时长</div>
        <div class="stat-value">{total_hours:.2f} 小时</div>
        <div class="stat-detail">平均: {avg_duration:.1f}秒 | 最长: {max_duration:.1f}秒</div>
    </div>
</div>
        """
    
    def load_task_history(date_filter_val, status_filter_val):
        """加载任务历史列表"""
        history_dir = "tmp/agent_history"
        
        if not os.path.exists(history_dir):
            return []
        
        tasks = []
        for task_dir in os.listdir(history_dir):
            task_path = os.path.join(history_dir, task_dir)
            if not os.path.isdir(task_path):
                continue
            
            json_file = os.path.join(task_path, f"{task_dir}.json")
            if os.path.exists(json_file):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                        task_id = task_dir[:8] + "..."
                        created_at = data.get('created_at', 'Unknown')
                        description = data.get('task', '')[:40] + "..." if len(data.get('task', '')) > 40 else data.get('task', '')
                        is_done = data.get('final_result', {}).get('is_done', False)
                        status = "✅ 成功" if is_done else "❌ 失败"
                        duration = round(data.get('total_duration', 0), 2)
                        
                        total_tokens = 0
                        if 'token_usage' in data:
                            total_tokens = data['token_usage'].get('total_prompt_tokens', 0) + \
                                          data['token_usage'].get('total_completion_tokens', 0)
                        
                        tasks.append([task_id, created_at, description, status, duration, total_tokens])
                except:
                    continue
        
        # 按创建时间排序(最新的在前)
        tasks.sort(key=lambda x: x[1], reverse=True)
        
        # 应用筛选
        if date_filter_val == "今天":
            today = datetime.now().strftime("%Y-%m-%d")
            tasks = [t for t in tasks if t[1].startswith(today)]
        elif date_filter_val == "最近7天":
            tasks = tasks[:50]
        elif date_filter_val == "最近30天":
            tasks = tasks[:200]
        
        if status_filter_val != "全部":
            filter_status = "✅ 成功" if status_filter_val == "成功" else "❌ 失败"
            tasks = [t for t in tasks if t[3] == filter_status]
        
        return tasks[:8]
    
    def load_task_detail(evt: gr.SelectData, date_filter_val, status_filter_val):
        """加载任务详情"""
        if evt is None:
            return None, """
<div class="detail-placeholder">
    <div class="placeholder-icon">📊</div>
    <div class="placeholder-text">选择任务查看详情</div>
    <div class="placeholder-hint">点击上方任务列表查看完整信息</div>
</div>
            """, None
        
        # 获取选中行的数据
        tasks = load_task_history(date_filter_val, status_filter_val)
        if evt.index[0] >= len(tasks):
            return None, "**任务不存在**", None
        
        task_id_short = tasks[evt.index[0]][0].replace("...", "")
        
        # 查找完整任务ID
        history_dir = "tmp/agent_history"
        full_task_id = None
        for task_dir in os.listdir(history_dir):
            if task_dir.startswith(task_id_short):
                full_task_id = task_dir
                break
        
        if not full_task_id:
            return None, "**任务数据未找到**", None
        
        json_file = os.path.join(history_dir, full_task_id, f"{full_task_id}.json")
        gif_file = os.path.join(history_dir, full_task_id, f"{full_task_id}.gif")
        
        task_data = None
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as f:
                task_data = json.load(f)
        
        # 生成统计信息
        stats_html = """
<div class="task-detail-stats">
    <div class="detail-header">任务详细信息</div>
"""
        if task_data:
            stats_html += f"""
    <div class="detail-row">
        <span class="detail-label">任务ID:</span>
        <span class="detail-value">{full_task_id}</span>
    </div>
    <div class="detail-row">
        <span class="detail-label">创建时间:</span>
        <span class="detail-value">{task_data.get('created_at', 'Unknown')}</span>
    </div>
    <div class="detail-row">
        <span class="detail-label">总耗时:</span>
        <span class="detail-value">{task_data.get('total_duration', 0):.2f} 秒</span>
    </div>
    <div class="detail-row">
        <span class="detail-label">步骤数:</span>
        <span class="detail-value">{len(task_data.get('history', []))}</span>
    </div>
"""
            
            if 'token_usage' in task_data:
                token_usage = task_data['token_usage']
                total_tokens = token_usage.get('total_prompt_tokens', 0) + token_usage.get('total_completion_tokens', 0)
                stats_html += f"""
    <div class="detail-divider"></div>
    <div class="detail-row">
        <span class="detail-label">Token消耗:</span>
        <span class="detail-value highlight">{total_tokens:,}</span>
    </div>
    <div class="detail-row sub">
        <span class="detail-label">Prompt:</span>
        <span class="detail-value">{token_usage.get('total_prompt_tokens', 0):,}</span>
    </div>
    <div class="detail-row sub">
        <span class="detail-label">Completion:</span>
        <span class="detail-value">{token_usage.get('total_completion_tokens', 0):,}</span>
    </div>
"""
        
        stats_html += "</div>"
        
        gif_path = gif_file if os.path.exists(gif_file) else None
        
        return task_data, stats_html, gif_path
    
    # 绑定事件
    refresh_btn.click(
        fn=load_statistics,
        outputs=[stats_display]
    ).then(
        fn=load_task_history,
        inputs=[date_filter, status_filter],
        outputs=[task_table]
    )
    
    date_filter.change(
        fn=load_task_history,
        inputs=[date_filter, status_filter],
        outputs=[task_table]
    )
    
    status_filter.change(
        fn=load_task_history,
        inputs=[date_filter, status_filter],
        outputs=[task_table]
    )
    
    task_table.select(
        fn=load_task_detail,
        inputs=[date_filter, status_filter],
        outputs=[task_detail_json, task_stats_md, task_gif_display]
    )
    
    return {
        "refresh_btn": refresh_btn,
        "stats_display": stats_display,
    }
