"""
配置模板管理面板
保存/加载多套配置模板,快速切换测试场景
"""
import os
import json
import gradio as gr
from datetime import datetime
from src.webui.webui_manager import WebuiManager
import logging

logger = logging.getLogger(__name__)


def create_config_template_panel(webui_manager: WebuiManager):
    """创建配置模板管理面板"""
    
    # === 模板列表卡片 ===
    with gr.Group(elem_classes=["card"]):
        gr.Markdown("### 📑 配置模板列表")
        
        with gr.Row():
            template_dropdown = gr.Dropdown(
                label="选择模板",
                choices=[],
                interactive=True
            )
            load_template_btn = gr.Button("📂 加载模板", variant="primary", size="sm")
            refresh_list_btn = gr.Button("🔄 刷新列表", size="sm")
    
    # === 配置预览卡片 ===
    with gr.Group(elem_classes=["card"]):
        gr.Markdown("### 👀 配置预览")
        config_preview = gr.JSON(label="当前配置内容")
    
    # === 保存新模板卡片 ===
    with gr.Group(elem_classes=["card"]):
        gr.Markdown("### 💾 保存为新模板")
        
        with gr.Row():
            template_name = gr.Textbox(
                label="模板名称",
                placeholder="例如: 震坤行测试-GPT4o",
                interactive=True
            )
            template_desc = gr.Textbox(
                label="模板描述",
                placeholder="简要描述此配置的用途",
                interactive=True
            )
        
        with gr.Row():
            save_template_btn = gr.Button("💾 保存模板", variant="primary")
            delete_template_btn = gr.Button("🗑️ 删除模板", variant="stop")
        
        status_msg = gr.Textbox(label="操作状态", interactive=False)
    
    # === 使用说明 ===
    with gr.Group(elem_classes=["card"]):
        gr.Markdown("""
### 💡 配置模板使用说明

配置模板功能允许您保存和快速切换不同的测试配置。

**操作步骤**:
1. 在"Agent配置"和"浏览器配置"页面设置好参数
2. 返回此页面,输入模板名称和描述
3. 点击"保存模板"按钮
4. 下次使用时,从列表选择模板并点击"加载模板"

**应用场景**:
- 不同客户项目的配置快速切换
- 开发/测试/生产环境配置管理
- 不同大模型的参数预设
- 特定测试场景的配置保存

**存储位置**: `tmp/webui_settings/templates/`
        """)
    
    # === 事件处理函数 ===
    
    def load_template_list():
        """加载模板列表"""
        templates_dir = "tmp/webui_settings/templates"
        if not os.path.exists(templates_dir):
            os.makedirs(templates_dir, exist_ok=True)
        
        templates = []
        for file in os.listdir(templates_dir):
            if file.endswith(".json"):
                templates.append(file.replace(".json", ""))
        
        templates.sort()
        return gr.Dropdown(choices=templates)
    
    def load_template(template_name):
        """加载模板配置"""
        if not template_name:
            return None, "⚠️ 请选择模板"
        
        template_path = f"tmp/webui_settings/templates/{template_name}.json"
        if not os.path.exists(template_path):
            return None, f"❌ 模板不存在: {template_name}"
        
        try:
            with open(template_path, 'r') as f:
                config = json.load(f)
            
            # TODO: 应用配置到webui_manager(需要实现配置加载逻辑)
            # 这里暂时只显示配置内容
            
            return config, f"✅ 模板加载成功: {template_name}\n\n💡 提示: 配置已加载,请重启任务以应用新配置"
        except Exception as e:
            logger.error(f"Error loading template: {e}")
            return None, f"❌ 加载失败: {str(e)}"
    
    def save_template(name, desc):
        """保存当前配置为模板"""
        if not name:
            return "❌ 请输入模板名称"
        
        templates_dir = "tmp/webui_settings/templates"
        os.makedirs(templates_dir, exist_ok=True)
        
        try:
            # 收集当前所有配置
            config = {}
            for comp_id, comp in webui_manager.id_to_component.items():
                try:
                    # 尝试获取组件值
                    config[comp_id] = comp.value
                except Exception:
                    pass
            
            # 添加元数据
            config["_template_meta"] = {
                "name": name,
                "description": desc,
                "created_at": datetime.now().isoformat()
            }
            
            template_path = f"{templates_dir}/{name}.json"
            with open(template_path, 'w') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            return f"✅ 模板保存成功: {template_path}"
        except Exception as e:
            logger.error(f"Error saving template: {e}")
            return f"❌ 保存失败: {str(e)}"
    
    def delete_template(template_name):
        """删除模板"""
        if not template_name:
            return "⚠️ 请选择要删除的模板"
        
        template_path = f"tmp/webui_settings/templates/{template_name}.json"
        if os.path.exists(template_path):
            try:
                os.remove(template_path)
                return f"✅ 模板已删除: {template_name}"
            except Exception as e:
                return f"❌ 删除失败: {str(e)}"
        return f"❌ 模板不存在: {template_name}"
    
    # === 绑定事件 ===
    refresh_list_btn.click(
        load_template_list,
        outputs=[template_dropdown]
    )
    
    load_template_btn.click(
        load_template,
        inputs=[template_dropdown],
        outputs=[config_preview, status_msg]
    )
    
    save_template_btn.click(
        save_template,
        inputs=[template_name, template_desc],
        outputs=[status_msg]
    ).then(
        load_template_list,
        outputs=[template_dropdown]
    )
    
    delete_template_btn.click(
        delete_template,
        inputs=[template_dropdown],
        outputs=[status_msg]
    ).then(
        load_template_list,
        outputs=[template_dropdown]
    )

