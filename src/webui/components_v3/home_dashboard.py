"""
首页仪表盘 - 简约商务风格 + 大屏可视化
关键指标卡片 + ECharts图表 + 任务历史表格
使用模块化样式系统的图表配置
"""
import gradio as gr
import os
import json
from datetime import datetime, timedelta
from collections import defaultdict
from src.webui.webui_manager import WebuiManager
from src.webui.styles import (
    build_line_chart_option,
    build_pie_chart_option,
    build_bar_chart_option,
    generate_chart_html,
)


# ============= 数据处理函数 =============

def calculate_trend_data():
    """计算最近7天的Token消耗趋势"""
    history_dir = "tmp/agent_history"
    
    # 如果没有真实数据,返回Mock数据
    if not os.path.exists(history_dir) or len(os.listdir(history_dir)) == 0:
        end_date = datetime.now()
        dates = [(end_date - timedelta(days=6-i)).strftime("%m-%d") for i in range(7)]
        # Mock数据: 展示上升趋势
        values = [12500, 15200, 18900, 16300, 21400, 19800, 21580]
        return dates, values
    
    # 初始化最近7天的数据
    end_date = datetime.now()
    date_token_map = {}
    
    for i in range(7):
        date = (end_date - timedelta(days=6-i)).strftime("%Y-%m-%d")
        date_token_map[date] = 0
    
    # 统计每天的Token消耗
    for task_dir in os.listdir(history_dir):
        task_path = os.path.join(history_dir, task_dir)
        if not os.path.isdir(task_path):
            continue
        
        json_file = os.path.join(task_path, f"{task_dir}.json")
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    created_at = data.get('created_at', '')
                    if created_at:
                        date = created_at.split()[0]  # 提取日期部分
                        if date in date_token_map:
                            if 'token_usage' in data:
                                total_tokens = data['token_usage'].get('total_prompt_tokens', 0) + \
                                             data['token_usage'].get('total_completion_tokens', 0)
                                date_token_map[date] += total_tokens
            except:
                continue
    
    dates = sorted(date_token_map.keys())
    values = [date_token_map[d] for d in dates]
    
    return dates, values


def calculate_success_rate():
    """计算任务成功率"""
    history_dir = "tmp/agent_history"
    
    if not os.path.exists(history_dir):
        return 0, 0, 0.0
    
    success_count = 0
    total_count = 0
    
    for task_dir in os.listdir(history_dir):
        task_path = os.path.join(history_dir, task_dir)
        if not os.path.isdir(task_path):
            continue
        
        json_file = os.path.join(task_path, f"{task_dir}.json")
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    total_count += 1
                    if data.get('final_result', {}).get('is_done'):
                        success_count += 1
            except:
                continue
    
    percentage = (success_count / total_count * 100) if total_count > 0 else 0.0
    return success_count, total_count, percentage


def calculate_duration_distribution():
    """计算任务时长分布"""
    history_dir = "tmp/agent_history"
    
    # 如果没有真实数据,返回Mock数据
    if not os.path.exists(history_dir) or len(os.listdir(history_dir)) == 0:
        return {"<30s": 8, "30-60s": 5, "1-3min": 12, ">3min": 6}
    
    distribution = {"<30s": 0, "30-60s": 0, "1-3min": 0, ">3min": 0}
    
    for task_dir in os.listdir(history_dir):
        task_path = os.path.join(history_dir, task_dir)
        if not os.path.isdir(task_path):
            continue
        
        json_file = os.path.join(task_path, f"{task_dir}.json")
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    duration = data.get('total_duration', 0)
                    
                    if duration < 30:
                        distribution["<30s"] += 1
                    elif duration < 60:
                        distribution["30-60s"] += 1
                    elif duration < 180:
                        distribution["1-3min"] += 1
                    else:
                        distribution[">3min"] += 1
            except:
                continue
    
    return distribution


def calculate_statistics():
    """计算所有统计数据"""
    history_dir = "tmp/agent_history"
    
    # 如果没有真实数据,返回Mock数据用于展示
    if not os.path.exists(history_dir) or len(os.listdir(history_dir)) == 0:
        return {
            "total_tokens": 125680,
            "prompt_tokens": 89420,
            "completion_tokens": 36260,
            "total_tasks": 31,
            "success_tasks": 28,
            "failed_tasks": 3,
            "success_rate": 90.3,
            "total_duration": 4832.5,
            "avg_duration": 155.9,
            "max_duration": 428.6,
            "total_hours": 1.34
        }
    
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
    success_rate = (success_tasks / total_tasks * 100) if total_tasks > 0 else 0.0
    
    return {
        "total_tokens": total_tokens,
        "prompt_tokens": total_prompt,
        "completion_tokens": total_completion,
        "total_tasks": total_tasks,
        "success_tasks": success_tasks,
        "failed_tasks": failed_tasks,
        "success_rate": success_rate,
        "total_duration": total_duration,
        "avg_duration": avg_duration,
        "max_duration": max_duration,
        "total_hours": total_hours
    }


# ============= HTML生成函数 =============

def create_metric_card_html(icon, icon_class, label, value, trend_text=""):
    """生成关键指标卡片HTML"""
    return f"""
    <div class="metric-card-container">
        <div class="metric-icon {icon_class}">
            {icon}
        </div>
        <div class="metric-content">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {f'<div class="metric-trend neutral">{trend_text}</div>' if trend_text else ''}
        </div>
    </div>
    """


def create_token_trend_chart_html(dates, values, mode="light"):
    """生成Token消耗趋势折线图 - 使用模块化图表配置"""
    option = build_line_chart_option(dates, values, "Token消耗", mode, show_area=True)
    chart_html = generate_chart_html("token-trend-chart", option, height="320px")
    
    return f"""
    <div class="chart-container">
        <div class="chart-title">📈 Token消耗趋势</div>
        {chart_html}
    </div>
    """


def create_task_analysis_chart_html(success_count, failed_count, duration_dist, mode="light"):
    """生成任务执行分析图表(饼图+柱状图组合) - 使用模块化图表配置"""
    total = success_count + failed_count
    success_rate = (success_count / total * 100) if total > 0 else 0
    
    # 成功率饼图数据
    pie_data = [
        {"name": "成功", "value": success_count},
        {"name": "失败", "value": failed_count},
    ]
    
    # 时长分布柱状图数据
    duration_categories = list(duration_dist.keys())
    duration_values = list(duration_dist.values())
    
    # 使用模块化图表配置
    pie_option = build_pie_chart_option(pie_data, "任务成功率", mode, inner_radius="55%", outer_radius="75%")
    # 添加中心文字
    pie_option["title"] = {
        "text": f"{success_rate:.1f}%",
        "subtext": "成功率",
        "left": "center",
        "top": "center",
        "textStyle": {
            "fontSize": 32,
            "fontWeight": 700,
            "color": "#E8E8E8" if mode == "dark" else "#262626"
        },
        "subtextStyle": {
            "fontSize": 14,
            "color": "#8C8C8C"
        }
    }
    pie_option["series"][0]["center"] = ["50%", "45%"]
    pie_option["series"][0]["label"]["show"] = False
    pie_option["legend"]["bottom"] = "5%"
    # 设置成功/失败的颜色
    if len(pie_option["series"][0]["data"]) >= 2:
        pie_option["series"][0]["data"][0]["itemStyle"] = {"color": "#52C41A"}
        pie_option["series"][0]["data"][1]["itemStyle"] = {"color": "#F5222D"}
    
    bar_option = build_bar_chart_option(duration_categories, duration_values, "任务数量", mode)
    # 自定义柱状图渐变色
    bar_option["series"][0]["itemStyle"] = {
        "color": {
            "type": "linear",
            "x": 0, "y": 0, "x2": 0, "y2": 1,
            "colorStops": [
                {"offset": 0, "color": "#7B8BE8" if mode == "dark" else "#7B8BE8"},
                {"offset": 1, "color": "#5B6BD1" if mode == "dark" else "#5B6BD1"}
            ]
        },
        "borderRadius": [4, 4, 0, 0]
    }
    bar_option["series"][0]["barWidth"] = "50%"
    bar_option["grid"]["bottom"] = "15%"
    
    pie_html = generate_chart_html("success-rate-chart", pie_option, height="280px")
    bar_html = generate_chart_html("duration-dist-chart", bar_option, height="280px")
    
    return f"""
    <div class="chart-container">
        <div class="chart-title">🎯 任务执行分析</div>
        <div style="display: flex; gap: 20px;">
            <div style="flex: 1;">{pie_html}</div>
            <div style="flex: 1;">{bar_html}</div>
        </div>
    </div>
    """


# ============= 主界面创建函数 =============

def create_home_dashboard(webui_manager: WebuiManager):
    """创建首页仪表盘 - 简约商务风格"""
    
    # === 顶部关键指标卡片 ===
    with gr.Row():
        metric_token = gr.HTML()
        metric_tasks = gr.HTML()
        metric_success = gr.HTML()
        metric_duration = gr.HTML()
    
    # === 中部图表区域 ===
    with gr.Row():
        token_trend_chart = gr.HTML()
        task_analysis_chart = gr.HTML()
    
    # === 底部任务历史 ===
    with gr.Group(elem_classes=["card"]):
        gr.Markdown("## 📜 最近任务历史")
        
        # 筛选工具栏
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
    with gr.Group(elem_classes=["card"]):
        gr.Markdown("## 📋 任务详情")
        
        with gr.Row():
            with gr.Column(scale=1):
                task_stats_md = gr.Markdown("""
<div class="detail-placeholder">
    <div class="placeholder-icon">📊</div>
    <div class="placeholder-text">选择任务查看详情</div>
    <div class="placeholder-hint">点击上方任务列表查看完整信息</div>
</div>
                """)
            
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
    
    # ============= 数据加载函数 =============
    
    def load_all_data():
        """加载所有数据"""
        stats = calculate_statistics()
        dates, token_values = calculate_trend_data()
        duration_dist = calculate_duration_distribution()
        
        # 生成关键指标卡片
        token_card = create_metric_card_html(
            "💰", "token", "Token消耗总量",
            f"{stats['total_tokens']:,}",
            f"Prompt: {stats['prompt_tokens']:,} | Completion: {stats['completion_tokens']:,}"
        )
        
        tasks_card = create_metric_card_html(
            "🎯", "tasks", "任务总数",
            f"{stats['total_tasks']}",
            f"成功: {stats['success_tasks']} | 失败: {stats['failed_tasks']}"
        )
        
        success_card = create_metric_card_html(
            "✅", "success", "成功率",
            f"{stats['success_rate']:.1f}%",
            f"成功 {stats['success_tasks']}/{stats['total_tasks']} 个任务"
        )
        
        duration_card = create_metric_card_html(
            "⏱️", "duration", "平均时长",
            f"{stats['avg_duration']:.1f}秒",
            f"总计: {stats['total_hours']:.2f}小时 | 最长: {stats['max_duration']:.1f}秒"
        )
        
        # 生成图表
        trend_chart = create_token_trend_chart_html(dates, token_values)
        analysis_chart = create_task_analysis_chart_html(
            stats['success_tasks'],
            stats['failed_tasks'],
            duration_dist
        )
        
        return token_card, tasks_card, success_card, duration_card, trend_chart, analysis_chart
    
    def load_task_history(date_filter_val, status_filter_val):
        """加载任务历史列表"""
        history_dir = "tmp/agent_history"
        
        # 如果没有真实数据,返回Mock数据
        if not os.path.exists(history_dir) or len(os.listdir(history_dir)) == 0:
            now = datetime.now()
            mock_tasks = [
                ["a2b4c6d8...", (now - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"), 
                 "打开震坤行官网并搜索产品信息", "✅ 成功", 142.5, 4250],
                ["c3e5f7g9...", (now - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"), 
                 "登录电商平台并查看购物车详情", "✅ 成功", 186.3, 5680],
                ["d4f6h8j0...", (now - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S"), 
                 "自动填写表单并提交订单信息", "❌ 失败", 98.7, 3120],
                ["e5g7i9k1...", (now - timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S"), 
                 "批量下载产品图片到本地文件夹", "✅ 成功", 234.8, 7890],
                ["f6h8j0l2...", (now - timedelta(days=1, hours=2)).strftime("%Y-%m-%d %H:%M:%S"), 
                 "爬取竞品价格数据并生成对比报告", "✅ 成功", 312.4, 9850],
                ["g7i9k1m3...", (now - timedelta(days=1, hours=6)).strftime("%Y-%m-%d %H:%M:%S"), 
                 "验证用户注册流程的完整性测试", "✅ 成功", 89.2, 2340],
                ["h8j0l2n4...", (now - timedelta(days=2, hours=3)).strftime("%Y-%m-%d %H:%M:%S"), 
                 "测试搜索功能的响应速度和准确性", "❌ 失败", 67.5, 1890],
                ["i9k1m3o5...", (now - timedelta(days=2, hours=10)).strftime("%Y-%m-%d %H:%M:%S"), 
                 "自动生成测试报告并发送邮件通知", "✅ 成功", 156.9, 4560],
            ]
            
            # 应用筛选
            if status_filter_val != "全部":
                filter_status = "✅ 成功" if status_filter_val == "成功" else "❌ 失败"
                mock_tasks = [t for t in mock_tasks if t[3] == filter_status]
            
            if date_filter_val == "今天":
                today = now.strftime("%Y-%m-%d")
                mock_tasks = [t for t in mock_tasks if t[1].startswith(today)]
            
            return mock_tasks[:8]
        
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
    
    # ============= 事件绑定 =============
    
    # 页面加载时初始化数据
    def init_dashboard():
        """初始化仪表盘数据"""
        token_card, tasks_card, success_card, duration_card, trend_chart, analysis_chart = load_all_data()
        history_data = load_task_history("最近7天", "全部")
        return token_card, tasks_card, success_card, duration_card, trend_chart, analysis_chart, history_data
    
    # 刷新按钮 - 加载所有数据
    refresh_btn.click(
        fn=load_all_data,
        outputs=[metric_token, metric_tasks, metric_success, metric_duration, 
                token_trend_chart, task_analysis_chart]
    ).then(
        fn=load_task_history,
        inputs=[date_filter, status_filter],
        outputs=[task_table]
    )
    
    # 筛选器变化
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
    
    # 选择任务行
    task_table.select(
        fn=load_task_detail,
        inputs=[date_filter, status_filter],
        outputs=[task_detail_json, task_stats_md, task_gif_display]
    )
    
    return {
        "init_fn": init_dashboard,
        "outputs": [metric_token, metric_tasks, metric_success, metric_duration, 
                   token_trend_chart, task_analysis_chart, task_table],
        "refresh_btn": refresh_btn,
    }
