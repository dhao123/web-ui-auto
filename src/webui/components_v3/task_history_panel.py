"""
任务历史记录面板
展示历史执行任务列表,支持查看/导出
"""
import os
import json
import gradio as gr
from datetime import datetime, timedelta
from src.webui.webui_manager import WebuiManager
import logging

logger = logging.getLogger(__name__)


def create_task_history_panel(webui_manager: WebuiManager):
    """创建任务历史管理面板"""
    
    # === 任务列表卡片 ===
    with gr.Group(elem_classes=["card"]):
        gr.Markdown("### 📜 历史任务列表")
        
        # 筛选条件
        with gr.Row():
            date_filter = gr.Dropdown(
                label="时间范围",
                choices=["今天", "最近7天", "最近30天", "全部"],
                value="最近7天",
                interactive=True
            )
            status_filter = gr.Dropdown(
                label="状态筛选",
                choices=["全部", "成功", "失败", "取消"],
                value="全部",
                interactive=True
            )
            refresh_btn = gr.Button("🔄 刷新列表", size="sm")
        
        # 任务列表(使用Dataframe)
        task_table = gr.Dataframe(
            headers=["任务ID", "创建时间", "任务描述", "状态", "耗时(秒)", "Token消耗"],
            datatype=["str", "str", "str", "str", "number", "number"],
            interactive=False,
            wrap=True,
            max_height=400
        )
    
    # === 任务详情卡片 ===
    with gr.Group(elem_classes=["card"]):
        gr.Markdown("### 🔍 任务详情")
        
        selected_task_id = gr.Textbox(label="当前选中任务ID", value="", interactive=False)
        
        with gr.Tabs():
            with gr.Tab("执行日志"):
                log_display = gr.JSON(label="Agent History")
            
            with gr.Tab("执行录像"):
                gif_display = gr.Image(label="Task Recording", type="filepath")
            
            with gr.Tab("统计信息"):
                stats_display = gr.Markdown("*请选择任务查看详情*")
        
        with gr.Row():
            download_json_btn = gr.Button("📥 下载JSON", size="sm")
            download_gif_btn = gr.Button("📥 下载录像", size="sm")
            delete_btn = gr.Button("🗑️ 删除记录", variant="stop", size="sm")
        
        operation_status = gr.Textbox(label="操作状态", interactive=False)
    
    # === 事件处理函数 ===
    
    def load_task_history(date_filter_val, status_filter_val):
        """加载任务历史列表"""
        history_dir = "tmp/agent_history"
        
        if not os.path.exists(history_dir):
            logger.warning(f"History directory not found: {history_dir}")
            return []
        
        tasks = []
        
        # 计算时间过滤范围
        now = datetime.now()
        if date_filter_val == "今天":
            time_limit = now - timedelta(days=1)
        elif date_filter_val == "最近7天":
            time_limit = now - timedelta(days=7)
        elif date_filter_val == "最近30天":
            time_limit = now - timedelta(days=30)
        else:
            time_limit = None
        
        # 扫描目录
        for item in os.listdir(history_dir):
            item_path = os.path.join(history_dir, item)
            if os.path.isdir(item_path):
                json_file = os.path.join(item_path, f"{item}.json")
                if os.path.exists(json_file):
                    try:
                        with open(json_file, 'r') as f:
                            data = json.load(f)
                        
                        # 提取任务信息
                        task_id = item
                        created_time = datetime.fromtimestamp(os.path.getctime(json_file))
                        
                        # 时间过滤
                        if time_limit and created_time < time_limit:
                            continue
                        
                        # 从JSON中提取信息
                        history_list = data.get("history", [])
                        task_desc = history_list[0].get("task", "无描述") if history_list else "无描述"
                        
                        # 判断状态
                        errors = data.get("errors", [])
                        if any(errors):
                            status = "失败"
                        elif data.get("final_result"):
                            status = "成功"
                        else:
                            status = "取消"
                        
                        # 状态过滤
                        if status_filter_val != "全部" and status != status_filter_val:
                            continue
                        
                        # 计算耗时和Token
                        duration = sum(item.get("duration", 0) for item in history_list)
                        input_tokens = data.get("total_input_tokens", 0)
                        
                        tasks.append([
                            task_id[:12] + "...",  # 缩短显示
                            created_time.strftime("%Y-%m-%d %H:%M:%S"),
                            task_desc[:50] + "..." if len(task_desc) > 50 else task_desc,
                            status,
                            round(duration, 2),
                            input_tokens
                        ])
                    except Exception as e:
                        logger.error(f"Error reading task history {item}: {e}")
                        continue
        
        # 按时间倒序排序
        tasks.sort(key=lambda x: x[1], reverse=True)
        
        return tasks
    
    def load_task_detail(evt: gr.SelectData, date_filter_val, status_filter_val):
        """加载任务详情"""
        if evt.index is None or len(evt.index) < 1:
            return None, None, "*未选中任务*", ""
        
        # 重新加载任务列表获取完整ID
        tasks = load_task_history(date_filter_val, status_filter_val)
        if evt.index[0] >= len(tasks):
            return None, None, "*任务不存在*", ""
        
        # 从短ID查找完整ID
        short_id = tasks[evt.index[0]][0].replace("...", "")
        history_dir = "tmp/agent_history"
        
        full_id = None
        for item in os.listdir(history_dir):
            if item.startswith(short_id):
                full_id = item
                break
        
        if not full_id:
            return None, None, "*任务ID未找到*", ""
        
        task_dir = os.path.join(history_dir, full_id)
        json_file = os.path.join(task_dir, f"{full_id}.json")
        gif_file = os.path.join(task_dir, f"{full_id}.gif")
        
        # 读取JSON
        json_data = None
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r') as f:
                    json_data = json.load(f)
            except Exception as e:
                logger.error(f"Error loading JSON: {e}")
        
        # 读取GIF
        gif_path = gif_file if os.path.exists(gif_file) else None
        
        # 生成统计信息
        stats_md = "### 📊 执行统计\n\n"
        if json_data:
            history_list = json_data.get("history", [])
            stats_md += f"- **总步数**: {len(history_list)}\n"
            stats_md += f"- **总耗时**: {sum(item.get('duration', 0) for item in history_list):.2f} 秒\n"
            stats_md += f"- **输入Token**: {json_data.get('total_input_tokens', 0)}\n"
            stats_md += f"- **最终结果**: {json_data.get('final_result', '无')}\n"
            
            errors = json_data.get("errors", [])
            if any(errors):
                stats_md += f"\n### ⚠️ 错误信息\n\n```\n{errors}\n```\n"
        else:
            stats_md += "*无法加载统计信息*"
        
        return json_data, gif_path, stats_md, full_id
    
    def download_json(task_id):
        """下载JSON文件"""
        if not task_id:
            return "请先选择任务"
        
        json_file = f"tmp/agent_history/{task_id}/{task_id}.json"
        if os.path.exists(json_file):
            return json_file
        return None
    
    def download_gif(task_id):
        """下载GIF文件"""
        if not task_id:
            return "请先选择任务"
        
        gif_file = f"tmp/agent_history/{task_id}/{task_id}.gif"
        if os.path.exists(gif_file):
            return gif_file
        return None
    
    def delete_task(task_id):
        """删除任务记录"""
        if not task_id:
            return "请先选择任务"
        
        task_dir = f"tmp/agent_history/{task_id}"
        if os.path.exists(task_dir):
            try:
                import shutil
                shutil.rmtree(task_dir)
                return f"✅ 已删除任务: {task_id}"
            except Exception as e:
                return f"❌ 删除失败: {str(e)}"
        return "❌ 任务目录不存在"
    
    # === 绑定事件 ===
    refresh_btn.click(
        load_task_history,
        inputs=[date_filter, status_filter],
        outputs=[task_table]
    )
    
    task_table.select(
        load_task_detail,
        inputs=[date_filter, status_filter],
        outputs=[log_display, gif_display, stats_display, selected_task_id]
    )
    
    download_json_btn.click(
        download_json,
        inputs=[selected_task_id],
        outputs=[operation_status]
    )
    
    download_gif_btn.click(
        download_gif,
        inputs=[selected_task_id],
        outputs=[operation_status]
    )
    
    delete_btn.click(
        delete_task,
        inputs=[selected_task_id],
        outputs=[operation_status]
    ).then(
        load_task_history,
        inputs=[date_filter, status_filter],
        outputs=[task_table]
    )
    
    # 初始加载
    date_filter.change(
        load_task_history,
        inputs=[date_filter, status_filter],
        outputs=[task_table]
    )
    status_filter.change(
        load_task_history,
        inputs=[date_filter, status_filter],
        outputs=[task_table]
    )
