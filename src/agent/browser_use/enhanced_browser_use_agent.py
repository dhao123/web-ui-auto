"""
增强的Browser Use Agent - 集成Skills和MCP工具
"""
from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Optional

from browser_use.agent.views import AgentHistoryList
from dotenv import load_dotenv

from src.agent.browser_use.browser_use_agent import BrowserUseAgent
from src.utils.execution_monitor import ExecutionStatus

load_dotenv()
logger = logging.getLogger(__name__)


class EnhancedBrowserUseAgent(BrowserUseAgent):
    """
    增强的Browser Use Agent
    
    特性:
    1. 自动加载震坤行电商技能库
    2. 集成MCP工具提示
    3. 增强的任务分解能力
    """
    
    def __init__(self, *args, **kwargs):
        # 加载技能库到系统提示
        skills_content = self._load_skills()
        
        # 将技能库添加到系统提示
        if 'system_prompt_class' in kwargs:
            original_prompt = kwargs['system_prompt_class']
            kwargs['system_prompt_class'] = self._enhance_system_prompt(
                original_prompt,
                skills_content
            )
        
        super().__init__(*args, **kwargs)
        logger.info("EnhancedBrowserUseAgent initialized with skills integration")
    
    def _load_skills(self) -> str:
        """加载技能库内容"""
        skills_path = Path(".kiro/skills/zkh_ecommerce_skills.md")
        
        if not skills_path.exists():
            logger.warning(f"Skills file not found: {skills_path}")
            return ""
        
        try:
            with open(skills_path, 'r', encoding='utf-8') as f:
                content = f.read()
            logger.info(f"Loaded skills from {skills_path}")
            return content
        except Exception as e:
            logger.error(f"Failed to load skills: {e}")
            return ""
    
    def _enhance_system_prompt(self, original_prompt, skills_content: str):
        """增强系统提示，注入技能库"""
        if not skills_content:
            return original_prompt
        
        # 创建增强的提示类
        class EnhancedSystemPrompt(original_prompt):
            def important_rules(self) -> str:
                base_rules = super().important_rules()
                
                skills_guidance = f"""

## 🎯 震坤行电商测试技能库集成

你现在拥有专门为震坤行（zkh.com）电商测试优化的技能库和MCP工具。

### 可用的结构化技能：
1. **zkh_login_skill**: 登录震坤行网站
2. **zkh_search_skill**: 搜索商品
3. **zkh_price_extract_skill**: 提取价格（未税价/含税价）
4. **zkh_add_to_cart_skill**: 加购商品
5. **zkh_verify_skill**: 验证测试结果

### 可用的MCP工具：
1. **zkh_extract_price**: 智能价格提取（支持多种格式）
2. **zkh_verify_cart_status**: 购物车状态验证
3. **zkh_wait_for_element**: 智能等待元素（处理动态加载）
4. **zkh_capture_network**: 网络请求捕获（调试用）

### 执行策略：
1. **任务分解**: 将复杂任务分解为技能序列（登录→搜索→提取→加购→验证）
2. **工具优先**: 优先使用MCP工具而非通用浏览器操作（如价格提取用zkh_extract_price）
3. **智能等待**: 遇到动态元素时使用zkh_wait_for_element
4. **验证确认**: 关键操作后使用zkh_verify_cart_status确认状态
5. **问题定位**: 失败时使用zkh_capture_network捕获网络请求辅助分析

### 示例执行流程（震坤行登录+搜索+加购）：
```
任务: "登录震坤行，搜索'AIGO鼠标'，提取未税价，加购并验证"

步骤1: 导航到zkh.com
步骤2: 点击登录，输入账号密码，提交
步骤3: 使用zkh_wait_for_element等待登录完成
步骤4: 在搜索框输入"AIGO鼠标"，点击搜索
步骤5: 使用zkh_extract_price提取未税价格
步骤6: 点击加购按钮
步骤7: 使用zkh_verify_cart_status验证加购成功
步骤8: 返回验证结果
```

### 详细技能文档：
{skills_content}

---
"""
                return base_rules + skills_guidance
        
        return EnhancedSystemPrompt
    
    async def run(
        self,
        max_steps: int = 100,
        on_step_start=None,
        on_step_end=None
    ) -> AgentHistoryList:
        """
        执行任务（覆盖父类方法以添加技能相关日志）
        """
        logger.info("=" * 60)
        logger.info("🚀 Enhanced Browser Use Agent 开始执行")
        logger.info(f"📋 任务: {self.task}")
        logger.info(f"🎯 最大步数: {max_steps}")
        logger.info(f"🛠️ 已加载震坤行电商技能库和MCP工具")
        logger.info("=" * 60)
        
        # 调用父类的run方法
        result = await super().run(
            max_steps=max_steps,
            on_step_start=on_step_start,
            on_step_end=on_step_end
        )
        
        # 输出执行摘要
        if self.execution_monitor:
            summary = self.execution_monitor.get_summary()
            logger.info("=" * 60)
            logger.info("📊 执行摘要")
            logger.info(f"状态: {summary['status']}")
            logger.info(f"步数: {summary['execution']['current_step']}/{summary['execution']['max_steps']}")
            logger.info(f"耗时: {summary['execution']['total_duration']}s")
            logger.info(f"Token: {summary['tokens']['total_tokens']}")
            logger.info(f"重试: 系统级{summary['retries']['system_retry_count']} + 业务级{summary['retries']['business_retry_count']}")
            logger.info("=" * 60)
        
        return result
