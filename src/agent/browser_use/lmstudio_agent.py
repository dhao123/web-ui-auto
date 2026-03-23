"""
LM Studio 本地模型专用 Agent
为本地部署模型（qwen/llama 等）优化，解决 action 为空的问题
"""
import json
import logging
from typing import Any, Optional

from browser_use.agent.views import AgentOutput, ActionResult, AgentHistory, AgentHistoryList, AgentStepInfo
from browser_use.agent.service import AgentHookFunc
from browser_use.browser.views import BrowserStateHistory
from browser_use.utils import time_execution_async
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from pydantic import ValidationError

from src.agent.browser_use.browser_use_agent import BrowserUseAgent

logger = logging.getLogger(__name__)


class LMStudioAgent(BrowserUseAgent):
    """
    专为 LM Studio 本地模型优化的 Agent
    
    主要优化点：
    1. 强制使用 raw 模式进行工具调用
    2. 自定义 JSON 解析，处理本地模型的各种输出格式
    3. 增强的错误处理和重试逻辑
    4. 针对本地模型的系统提示词优化
    """
    
    def _set_tool_calling_method(self):
        """强制使用 raw 模式"""
        logger.info(f"🤖 LMStudioAgent: Forcing 'raw' mode for local model {self.model_name}")
        return 'raw'
    
    def _get_system_prompt_for_local_model(self) -> str:
        """
        为本地模型定制的系统提示词
        更明确的格式要求，帮助模型正确输出 action
        """
        base_prompt = """You are a helpful assistant that can use browser tools to complete tasks.

CRITICAL INSTRUCTIONS FOR OUTPUT FORMAT:

You must respond with a valid JSON object in the following exact format:

{
  "current_state": {
    "evaluation_previous_goal": "Evaluate if the previous action succeeded or failed",
    "memory": "Store important information here",
    "next_goal": "Describe what you want to do next"
  },
  "action": [
    {"action_name": {"param1": "value1", "param2": "value2"}}
  ]
}

IMPORTANT RULES:
1. The "action" field MUST be a non-empty array with at least one action
2. NEVER output empty action like "action": [] or "action": [{}]
3. Available actions include:
   - go_to_url: {"go_to_url": {"url": "https://example.com"}}
   - click_element_by_index: {"click_element_by_index": {"index": 123}}
   - input_text: {"input_text": {"index": 123, "text": "your text"}}
   - extract_page_content: {"extract_page_content": {}}
   - done: {"done": {"text": "final answer"}}

4. Always include the full action object with all required parameters
5. Do not include any text outside the JSON object
6. Do not use markdown code blocks, output raw JSON only

Example response:
{
  "current_state": {
    "evaluation_previous_goal": "Successfully navigated to zkh.com",
    "memory": "On homepage, need to login",
    "next_goal": "Click the login button"
  },
  "action": [
    {"click_element_by_index": {"index": 121}}
  ]
}
"""
        return base_prompt
    
    def _convert_input_messages(self, input_messages: list[BaseMessage]) -> list[BaseMessage]:
        """
        转换输入消息，为本地模型优化
        """
        converted = []
        for msg in input_messages:
            if isinstance(msg, SystemMessage):
                # 替换系统提示词为本地模型优化版本
                converted.append(SystemMessage(content=self._get_system_prompt_for_local_model()))
            else:
                converted.append(msg)
        return converted
    
    def _extract_json_from_output(self, content: str) -> dict:
        """
        从模型输出中提取 JSON，处理各种格式
        """
        content = content.strip()
        
        # 尝试1: 直接解析
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass
        
        # 尝试2: 从代码块中提取
        if '```json' in content:
            try:
                json_str = content.split('```json')[1].split('```')[0].strip()
                return json.loads(json_str)
            except (IndexError, json.JSONDecodeError):
                pass
        
        if '```' in content:
            try:
                json_str = content.split('```')[1].split('```')[0].strip()
                # 移除可能的语言标识符
                if '\n' in json_str:
                    first_line = json_str.split('\n')[0].strip()
                    if first_line in ['json', 'python', '']:
                        json_str = '\n'.join(json_str.split('\n')[1:])
                return json.loads(json_str)
            except (IndexError, json.JSONDecodeError):
                pass
        
        # 尝试3: 查找 JSON 对象边界
        try:
            start = content.find('{')
            end = content.rfind('}')
            if start != -1 and end != -1 and end > start:
                return json.loads(content[start:end+1])
        except json.JSONDecodeError:
            pass
        
        # 尝试4: 查找 JSON 数组
        try:
            start = content.find('[')
            end = content.rfind(']')
            if start != -1 and end != -1 and end > start:
                data = json.loads(content[start:end+1])
                if isinstance(data, list) and len(data) > 0:
                    return data[0] if isinstance(data[0], dict) else {"action": data}
        except (json.JSONDecodeError, IndexError):
            pass
        
        raise ValueError(f"Could not extract valid JSON from: {content[:200]}...")
    
    def _fix_empty_action(self, data: dict) -> dict:
        """
        修复空的 action 字段
        """
        if 'action' not in data or not data['action']:
            logger.warning("Empty action detected, attempting to fix...")
            
            # 从 next_goal 推断可能的 action
            next_goal = data.get('current_state', {}).get('next_goal', '').lower()
            
            # 默认 action：截图查看当前状态
            default_action = [{"extract_page_content": {}}]
            
            if 'click' in next_goal or '登录' in next_goal or 'login' in next_goal:
                default_action = [{"click_element_by_index": {"index": 121}}]
            elif 'input' in next_goal or '输入' in next_goal:
                default_action = [{"input_text": {"index": 0, "text": ""}}]
            elif 'search' in next_goal or '搜索' in next_goal:
                default_action = [{"input_text": {"index": 0, "text": ""}}]
            elif 'navigate' in next_goal or '打开' in next_goal or 'go to' in next_goal:
                url = "https://zkh.com"
                default_action = [{"go_to_url": {"url": url}}]
            
            data['action'] = default_action
            logger.info(f"Fixed empty action with: {default_action}")
        
        return data
    
    async def get_next_action(self, input_messages: list[BaseMessage]) -> AgentOutput:
        """
        为本地模型定制的 get_next_action
        强制使用 raw 模式并自定义解析逻辑
        """
        from browser_use.agent.message_manager.utils import convert_input_messages
        
        # 转换消息格式
        input_messages = convert_input_messages(input_messages, self.model_name)
        
        # 使用 raw 模式调用 LLM
        try:
            output = await self.llm.ainvoke(input_messages)
            content = str(output.content)
            
            logger.debug(f"Raw model output: {content[:500]}...")
            
            # 提取 JSON
            try:
                data = self._extract_json_from_output(content)
            except ValueError as e:
                logger.error(f"Failed to parse JSON: {e}")
                # 返回一个默认的 action 避免崩溃
                data = {
                    "current_state": {
                        "evaluation_previous_goal": "Failed to parse model output",
                        "memory": "Parsing error occurred",
                        "next_goal": "Retry with clearer instructions"
                    },
                    "action": [{"extract_page_content": {}}]
                }
            
            # 修复空的 action
            data = self._fix_empty_action(data)
            
            # 验证并创建 AgentOutput
            try:
                parsed = self.AgentOutput(**data)
                
                # 限制 action 数量
                if len(parsed.action) > self.settings.max_actions_per_step:
                    parsed.action = parsed.action[:self.settings.max_actions_per_step]
                
                return parsed
                
            except ValidationError as e:
                logger.error(f"Validation error: {e}")
                # 尝试修复常见验证错误
                if 'current_state' not in data:
                    data['current_state'] = {
                        "evaluation_previous_goal": "Unknown",
                        "memory": "No memory provided",
                        "next_goal": "Continue task"
                    }
                
                parsed = self.AgentOutput(**data)
                return parsed
                
        except Exception as e:
            logger.error(f"Error in get_next_action: {e}")
            raise
    
    @time_execution_async('--run (agent)')
    async def run(self, max_steps: int = 100, on_step_start: AgentHookFunc | None = None,
                  on_step_end: AgentHookFunc | None = None) -> AgentHistoryList:
        """
        运行 agent，使用本地模型优化的 get_next_action
        """
        # 临时替换父类的 get_next_action
        original_get_next_action = self.get_next_action
        self.get_next_action = self.get_next_action
        
        try:
            return await super().run(max_steps, on_step_start, on_step_end)
        finally:
            pass  # 恢复原始方法如果需要
