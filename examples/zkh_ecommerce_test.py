"""
震坤行电商测试示例 - MCP+Skills+Agent方案演示

测试用例:
打开震坤行官网zkh.com，用账号18614277918，密码test.123登录,
搜索"AIGO/爱国者 鼠标 Q710 黑色 1个" 找到未税价格并加购，
判断未税价格是否是18.50，加购是否成功。
如果其中任意一项不符合，就返回case验证不通过，否则返回case验证成功
"""
import asyncio
import logging
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig

from src.agent.browser_use.enhanced_browser_use_agent import EnhancedBrowserUseAgent
from src.controller.custom_controller import CustomController
from src.utils.llm_provider import get_llm_model

load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def run_zkh_test():
    """运行震坤行电商测试"""
    
    # 测试用例定义
    test_case = {
        "name": "震坤行商品搜索加购测试",
        "url": "https://www.zkh.com",
        "username": "18614277918",
        "password": "test.123",
        "search_keyword": "AIGO/爱国者 鼠标 Q710 黑色",
        "expected_price": 18.50,
        "expected_cart_success": True
    }
    
    logger.info("=" * 80)
    logger.info(f"🧪 测试用例: {test_case['name']}")
    logger.info(f"🔗 目标网站: {test_case['url']}")
    logger.info(f"🔍 搜索关键词: {test_case['search_keyword']}")
    logger.info(f"💰 期望未税价: {test_case['expected_price']}")
    logger.info("=" * 80)
    
    # 构建任务描述（注入技能提示）
    task = f"""
请按照以下步骤完成震坤行电商测试任务：

## 任务目标
验证震坤行网站的登录、搜索、价格提取和加购功能是否正常。

## 执行步骤（使用技能库）

### 步骤1: 登录 (使用 zkh_login_skill)
- 打开 {test_case['url']}
- 使用账号 {test_case['username']} 和密码 {test_case['password']} 登录
- 验证登录成功（检查是否出现用户信息或退出按钮）

### 步骤2: 搜索商品 (使用 zkh_search_skill)
- 在搜索框输入关键词: {test_case['search_keyword']}
- 点击搜索或按Enter
- 等待搜索结果页面加载完成

### 步骤3: 提取未税价格 (使用 zkh_extract_price 工具)
- 在搜索结果中找到目标商品
- 使用 zkh_extract_price 工具提取未税价格
- 记录提取到的价格值

### 步骤4: 加购商品 (使用 zkh_add_to_cart_skill)
- 点击商品进入详情页（如果需要）
- 点击"加入购物车"按钮
- 等待加购反馈

### 步骤5: 验证结果 (使用 zkh_verify_cart_status 和 zkh_verify_skill)
- 使用 zkh_verify_cart_status 验证购物车状态
- 比对实际价格与期望价格 {test_case['expected_price']}
- 验证加购是否成功

## 验证标准
1. 未税价格 = {test_case['expected_price']} 元
2. 加购成功（购物车中有商品或出现成功提示）

## 最终输出
如果所有验证通过，返回: "✅ Case验证成功"
如果任意验证失败，返回: "❌ Case验证不通过: [失败原因]"

## 注意事项
- 优先使用MCP工具（zkh_extract_price, zkh_verify_cart_status）
- 遇到动态元素使用 zkh_wait_for_element
- 如遇验证码或异常，使用 ask_for_assistant 请求人工协助
- 失败时使用 zkh_capture_network 捕获网络请求辅助分析
"""
    
    # 初始化LLM（使用震坤行大模型）
    logger.info("🤖 初始化震坤行大模型...")
    llm = get_llm_model(
        provider="zkh",
        model_name="ep_20251217_i18v",  # DeepSeek-V3，支持工具调用
        temperature=0.0
    )
    
    # 初始化浏览器
    logger.info("🌐 初始化浏览器...")
    browser = Browser(
        config=BrowserConfig(
            headless=False,  # 显示浏览器窗口以便观察
            disable_security=True,
        )
    )
    
    # 初始化Controller（已集成MCP工具）
    logger.info("🛠️ 初始化Controller（集成MCP工具）...")
    controller = CustomController()
    
    # 初始化增强的Agent（集成Skills）
    logger.info("🚀 初始化Enhanced Agent（集成Skills）...")
    agent = EnhancedBrowserUseAgent(
        task=task,
        llm=llm,
        browser=browser,
        controller=controller,
        browser_context=BrowserContextConfig(
            trace_path="./tmp/zkh_test_trace",
            save_recording_path="./tmp/zkh_test_recording.webm",
        ),
    )
    
    try:
        # 执行测试
        logger.info("▶️ 开始执行测试...")
        result = await agent.run(max_steps=30)
        
        # 输出结果
        logger.info("=" * 80)
        logger.info("📋 测试执行完成")
        logger.info(f"📊 总步数: {len(result.history)}")
        
        # 提取最终结果
        if result.history:
            final_step = result.history[-1]
            if final_step.result:
                final_message = final_step.result[0].extracted_content or ""
                logger.info(f"🎯 最终结果: {final_message}")
                
                # 判断测试是否通过
                if "验证成功" in final_message or "✅" in final_message:
                    logger.info("✅ 测试通过！")
                    return True
                else:
                    logger.error("❌ 测试失败！")
                    return False
        
        logger.warning("⚠️ 无法确定测试结果")
        return False
        
    except Exception as e:
        logger.error(f"❌ 测试执行异常: {e}", exc_info=True)
        return False
    
    finally:
        # 清理资源
        logger.info("🧹 清理资源...")
        await browser.close()


async def main():
    """主函数"""
    success = await run_zkh_test()
    
    if success:
        logger.info("=" * 80)
        logger.info("🎉 震坤行电商测试完成 - 成功")
        logger.info("=" * 80)
        sys.exit(0)
    else:
        logger.error("=" * 80)
        logger.error("💥 震坤行电商测试完成 - 失败")
        logger.error("=" * 80)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
