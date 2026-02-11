from __future__ import annotations

import asyncio
import logging
import os

# from lmnr.sdk.decorators import observe
from browser_use.agent.gif import create_history_gif
from browser_use.agent.service import Agent, AgentHookFunc
from browser_use.agent.views import (
    ActionResult,
    AgentHistory,
    AgentHistoryList,
    AgentStepInfo,
    ToolCallingMethod,
)
from browser_use.browser.views import BrowserStateHistory
from browser_use.utils import time_execution_async
from dotenv import load_dotenv
from browser_use.agent.message_manager.utils import is_model_without_tool_support
from src.utils.execution_monitor import ExecutionMonitor, ExecutionStatus

load_dotenv()
logger = logging.getLogger(__name__)

SKIP_LLM_API_KEY_VERIFICATION = (
        os.environ.get("SKIP_LLM_API_KEY_VERIFICATION", "false").lower()[0] in "ty1"
)


class BrowserUseAgent(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初始化执行监控器
        self.execution_monitor: ExecutionMonitor | None = None
    
    def _set_tool_calling_method(self) -> ToolCallingMethod | None:
        tool_calling_method = self.settings.tool_calling_method
        if tool_calling_method == 'auto':
            if is_model_without_tool_support(self.model_name):
                return 'raw'
            elif self.chat_model_library == 'ChatGoogleGenerativeAI':
                return None
            elif self.chat_model_library == 'ChatOpenAI':
                return 'function_calling'
            elif self.chat_model_library == 'AzureChatOpenAI':
                return 'function_calling'
            # 支持 ZKH AI Gateway (ZKHChatOpenAI 继承自 ChatOpenAI)
            elif self.chat_model_library == 'ZKHChatOpenAI':
                return 'function_calling'
            else:
                return None
        else:
            return tool_calling_method

    @time_execution_async("--run (agent)")
    async def run(
            self, max_steps: int = 100, on_step_start: AgentHookFunc | None = None,
            on_step_end: AgentHookFunc | None = None
    ) -> AgentHistoryList:
        """Execute the task with maximum number of steps"""

        # 初始化执行监控器
        self.execution_monitor = ExecutionMonitor(
            max_steps=max_steps,
            task_id=getattr(self.state, 'agent_id', None)
        )

        loop = asyncio.get_event_loop()

        # Set up the Ctrl+C signal handler with callbacks specific to this agent
        from browser_use.utils import SignalHandler

        signal_handler = SignalHandler(
            loop=loop,
            pause_callback=self.pause,
            resume_callback=self.resume,
            custom_exit_callback=None,  # No special cleanup needed on forced exit
            exit_on_second_int=True,
        )
        signal_handler.register()

        try:
            self._log_agent_run()

            # Execute initial actions if provided
            if self.initial_actions:
                result = await self.multi_act(self.initial_actions, check_for_new_elements=False)
                self.state.last_result = result

            for step in range(max_steps):
                # 检查步数熔断
                if not self.execution_monitor.start_step(f"step_{step}"):
                    error_message = f'Step limit exceeded: {step}/{max_steps}'
                    self.state.history.history.append(
                        AgentHistory(
                            model_output=None,
                            result=[ActionResult(error=error_message, include_in_memory=True)],
                            state=BrowserStateHistory(
                                url='',
                                title='',
                                tabs=[],
                                interacted_element=[],
                                screenshot=None,
                            ),
                            metadata=None,
                        )
                    )
                    logger.error(f'❌ {error_message}')
                    self.execution_monitor.finish(ExecutionStatus.STEP_LIMIT_EXCEEDED)
                    break
                
                # Check if waiting for user input after Ctrl+C
                if self.state.paused:
                    signal_handler.wait_for_resume()
                    signal_handler.reset()

                # Check if we should stop due to too many failures
                if self.state.consecutive_failures >= self.settings.max_failures:
                    logger.error(f'❌ Stopping due to {self.settings.max_failures} consecutive failures')
                    self.execution_monitor.finish_step(success=False, error='Too many consecutive failures')
                    self.execution_monitor.finish(ExecutionStatus.FAILED)
                    break

                # Check control flags before each step
                if self.state.stopped:
                    logger.info('Agent stopped')
                    self.execution_monitor.finish_step(success=False, error='Agent stopped')
                    self.execution_monitor.finish(ExecutionStatus.CANCELLED)
                    break

                while self.state.paused:
                    await asyncio.sleep(0.2)  # Small delay to prevent CPU spinning
                    if self.state.stopped:  # Allow stopping while paused
                        break

                if on_step_start is not None:
                    await on_step_start(self)

                step_info = AgentStepInfo(step_number=step, max_steps=max_steps)
                
                # 记录步骤开始前的失败次数
                failures_before = self.state.consecutive_failures
                
                try:
                    await self.step(step_info)
                    self.execution_monitor.finish_step(success=True)
                except Exception as e:
                    logger.error(f"Step {step} failed: {e}")
                    self.execution_monitor.finish_step(success=False, error=str(e))
                    # 记录系统级重试（步骤失败但会继续）
                    if step < max_steps - 1:
                        self.execution_monitor.record_retry("system", f"Step exception: {str(e)}")

                # 检查是否有新的失败（即使没有抛出异常）
                failures_after = self.state.consecutive_failures
                if failures_after > failures_before:
                    # 失败次数增加，说明步骤执行有问题，记录为系统级重试
                    if step < max_steps - 1:
                        for i in range(failures_after - failures_before):
                            self.execution_monitor.record_retry("system", f"Action execution failed (failure #{failures_after})")

                if on_step_end is not None:
                    await on_step_end(self)

                if self.state.history.is_done():
                    if self.settings.validate_output and step < max_steps - 1:
                        if not await self._validate_output():
                            # 记录业务级重试
                            self.execution_monitor.record_retry("business", "Output validation failed")
                            continue

                    await self.log_completion()
                    self.execution_monitor.finish(ExecutionStatus.SUCCESS)
                    break
            else:
                error_message = 'Failed to complete task in maximum steps'

                self.state.history.history.append(
                    AgentHistory(
                        model_output=None,
                        result=[ActionResult(error=error_message, include_in_memory=True)],
                        state=BrowserStateHistory(
                            url='',
                            title='',
                            tabs=[],
                            interacted_element=[],
                            screenshot=None,
                        ),
                        metadata=None,
                    )
                )

                logger.info(f'❌ {error_message}')
                self.execution_monitor.finish(ExecutionStatus.FAILED)

            return self.state.history

        except KeyboardInterrupt:
            # Already handled by our signal handler, but catch any direct KeyboardInterrupt as well
            logger.info('Got KeyboardInterrupt during execution, returning current history')
            return self.state.history

        finally:
            # Unregister signal handlers before cleanup
            signal_handler.unregister()

            if self.settings.save_playwright_script_path:
                logger.info(
                    f'Agent run finished. Attempting to save Playwright script to: {self.settings.save_playwright_script_path}'
                )
                try:
                    # Extract sensitive data keys if sensitive_data is provided
                    keys = list(self.sensitive_data.keys()) if self.sensitive_data else None
                    # Pass browser and context config to the saving method
                    self.state.history.save_as_playwright_script(
                        self.settings.save_playwright_script_path,
                        sensitive_data_keys=keys,
                        browser_config=self.browser.config,
                        context_config=self.browser_context.config,
                    )
                except Exception as script_gen_err:
                    # Log any error during script generation/saving
                    logger.error(f'Failed to save Playwright script: {script_gen_err}', exc_info=True)

            await self.close()

            if self.settings.generate_gif:
                output_path: str = 'agent_history.gif'
                if isinstance(self.settings.generate_gif, str):
                    output_path = self.settings.generate_gif

                create_history_gif(task=self.task, history=self.state.history, output_path=output_path)
