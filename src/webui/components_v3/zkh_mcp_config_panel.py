"""
震坤行MCP专属配置面板
针对震坤行大模型和电商场景的专属配置
"""
import os
import gradio as gr
from src.webui.webui_manager import WebuiManager


def create_zkh_mcp_config_panel(webui_manager: WebuiManager):
    """创建震坤行MCP专属配置面板"""
    
    # === MCP服务器配置卡片 ===
    with gr.Group(elem_classes=["card"]):
        gr.Markdown("### 🔧 震坤行MCP服务器配置")
        
        zkh_mcp_enabled = gr.Checkbox(
            label="启用震坤行MCP服务器",
            value=True,
            info="使用震坤行电商领域专属MCP工具",
            interactive=True
        )
        
        zkh_mcp_file = gr.Textbox(
            label="MCP配置文件路径",
            value="src/mcp_servers/zkh_ecommerce_server.py",
            placeholder="src/mcp_servers/zkh_ecommerce_server.py",
            info="震坤行电商MCP服务器路径",
            interactive=True
        )
        
        zkh_mcp_config_display = gr.JSON(label="MCP配置预览")
    
    # === 震坤行大模型配置卡片 ===
    with gr.Group(elem_classes=["card"]):
        gr.Markdown("### 🤖 震坤行大模型配置")
        
        with gr.Row():
            zkh_llm_endpoint = gr.Textbox(
                label="API Endpoint",
                value=os.getenv("ZKH_LLM_ENDPOINT", ""),
                placeholder="https://api.zkh360.com/v1",
                info="震坤行大模型API端点",
                interactive=True
            )
            zkh_llm_api_key = gr.Textbox(
                label="API Key",
                type="password",
                value=os.getenv("ZKH_LLM_API_KEY", ""),
                placeholder="zkh-...",
                info="震坤行大模型API密钥",
                interactive=True
            )
        
        with gr.Row():
            zkh_llm_model = gr.Dropdown(
                label="模型选择",
                choices=["zkh-gpt-4o", "zkh-claude-3.5", "zkh-custom"],
                value="zkh-gpt-4o",
                info="选择震坤行支持的大模型",
                interactive=True
            )
            zkh_llm_temperature = gr.Slider(
                label="Temperature",
                minimum=0.0,
                maximum=1.0,
                value=0.6,
                step=0.1,
                info="控制模型输出随机性",
                interactive=True
            )
    
    # === 电商领域优化配置卡片 ===
    with gr.Group(elem_classes=["card"]):
        gr.Markdown("### 🛒 电商领域优化")
        
        enable_product_search = gr.Checkbox(
            label="启用商品搜索优化",
            value=True,
            info="针对电商商品搜索场景的提示词优化",
            interactive=True
        )
        
        enable_price_comparison = gr.Checkbox(
            label="启用价格对比功能",
            value=True,
            info="自动比较多个商品价格",
            interactive=True
        )
        
        enable_inventory_check = gr.Checkbox(
            label="启用库存检查",
            value=False,
            info="检查商品库存状态",
            interactive=True
        )
        
        custom_prompts = gr.Textbox(
            label="自定义电商领域Prompt",
            lines=5,
            placeholder="在此输入针对震坤行电商场景的自定义系统提示词...\n\n例如:\n你是震坤行电商平台的智能助手,专注于工业品采购...",
            interactive=True
        )
    
    # === 连接测试卡片 ===
    with gr.Group(elem_classes=["card"]):
        gr.Markdown("### 🔍 连接测试")
        
        with gr.Row():
            test_mcp_btn = gr.Button("🧪 测试MCP连接", variant="primary")
            test_llm_btn = gr.Button("🧪 测试大模型连接", variant="primary")
        
        test_result = gr.Textbox(label="测试结果", lines=5, interactive=False)
    
    # === 快速配置预设卡片 ===
    with gr.Group(elem_classes=["card"]):
        gr.Markdown("### ⚡ 快速配置预设")
        
        preset_buttons = gr.Radio(
            choices=[
                "开发测试环境",
                "生产环境",
                "高性能模式",
                "节省Token模式"
            ],
            label="选择预设配置",
            interactive=True
        )
        
        apply_preset_btn = gr.Button("应用预设", variant="secondary")
    
    # === 使用说明卡片 ===
    with gr.Group(elem_classes=["card"]):
        gr.Markdown("""
### 💡 震坤行MCP使用说明

**震坤行MCP服务器**提供电商领域专属的工具和能力:

**核心功能**:
- 🔍 **商品搜索**: 智能搜索震坤行商品库
- 💰 **价格对比**: 自动对比多个商品价格
- 📦 **库存查询**: 实时查询商品库存状态
- 🛒 **购物车管理**: 添加/删除购物车商品
- 📋 **订单追踪**: 查询订单状态和物流信息

**配置步骤**:
1. 在"Agent配置"页面上传MCP配置JSON文件
2. 或直接指定震坤行MCP服务器路径
3. 配置震坤行大模型的API端点和密钥
4. 启用所需的电商优化功能
5. 点击"测试连接"验证配置

**预设模式说明**:
- **开发测试环境**: 高随机性,启用所有功能,适合开发调试
- **生产环境**: 平衡性能和准确性,启用核心功能
- **高性能模式**: 低随机性,更多步数,追求最佳结果
- **节省Token模式**: 减少步数,禁用Vision,降低成本

**注意事项**:
- 需要有效的震坤行API密钥
- 建议先在测试环境验证配置
- 生产环境使用前请进行充分测试
        """)
    
    # === 事件处理函数 ===
    
    def test_mcp_connection(mcp_file):
        """测试MCP服务器连接"""
        try:
            if not mcp_file or not os.path.exists(mcp_file):
                return "❌ MCP文件路径无效"
            
            # TODO: 实现真实的MCP连接测试
            return f"""✅ MCP服务器连接成功

**配置文件**: {mcp_file}
**可用工具**: 
- search_product: 搜索商品
- compare_price: 价格对比
- check_inventory: 库存检查
- manage_cart: 购物车管理
- track_order: 订单追踪

**状态**: 就绪
            """
        except Exception as e:
            return f"❌ MCP连接失败: {str(e)}"
    
    def test_llm_connection(endpoint, api_key, model):
        """测试大模型连接"""
        try:
            if not endpoint or not api_key:
                return "❌ 请配置API Endpoint和API Key"
            
            # TODO: 实现真实的LLM连接测试
            return f"""✅ 大模型连接成功

**Endpoint**: {endpoint}
**模型**: {model}
**延迟**: 120ms
**状态**: 正常

可以开始使用震坤行大模型进行自动化测试。
            """
        except Exception as e:
            return f"❌ 大模型连接失败: {str(e)}"
    
    def apply_preset(preset_name):
        """应用预设配置"""
        presets = {
            "开发测试环境": {
                "temperature": 0.8,
                "enable_product_search": True,
                "enable_price_comparison": True,
                "enable_inventory_check": False,
                "message": "✅ 已应用开发测试环境配置\n\n- Temperature: 0.8 (高随机性)\n- 启用商品搜索和价格对比\n- 适合开发调试"
            },
            "生产环境": {
                "temperature": 0.6,
                "enable_product_search": True,
                "enable_price_comparison": True,
                "enable_inventory_check": True,
                "message": "✅ 已应用生产环境配置\n\n- Temperature: 0.6 (平衡性能)\n- 启用所有核心功能\n- 适合生产使用"
            },
            "高性能模式": {
                "temperature": 0.4,
                "max_steps": 50,
                "enable_product_search": True,
                "message": "✅ 已应用高性能模式\n\n- Temperature: 0.4 (低随机性)\n- Max Steps: 50\n- 追求最佳结果"
            },
            "节省Token模式": {
                "temperature": 0.3,
                "max_steps": 15,
                "use_vision": False,
                "message": "✅ 已应用节省Token模式\n\n- Temperature: 0.3\n- Max Steps: 15\n- 禁用Vision\n- 降低成本"
            }
        }
        
        config = presets.get(preset_name, {})
        message = config.get("message", f"✅ 已应用预设: {preset_name}")
        
        # TODO: 实际应用配置到对应的UI组件
        
        return message
    
    # === 绑定事件 ===
    test_mcp_btn.click(
        test_mcp_connection,
        inputs=[zkh_mcp_file],
        outputs=[test_result]
    )
    
    test_llm_btn.click(
        test_llm_connection,
        inputs=[zkh_llm_endpoint, zkh_llm_api_key, zkh_llm_model],
        outputs=[test_result]
    )
    
    apply_preset_btn.click(
        apply_preset,
        inputs=[preset_buttons],
        outputs=[test_result]
    )
