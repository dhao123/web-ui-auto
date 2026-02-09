"""
执行监控模块 - Execution Monitor
提供步数熔断、重试追踪、Token统计、耗时度量等可观测性功能
"""
import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class ExecutionStatus(Enum):
    """执行状态枚举"""
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    STEP_LIMIT_EXCEEDED = "STEP_LIMIT_EXCEEDED"
    CANCELLED = "CANCELLED"


@dataclass
class RetryRecord:
    """重试记录"""
    step_number: int
    retry_type: str  # "system" or "business"
    reason: str
    timestamp: float = field(default_factory=time.time)


@dataclass
class TokenUsage:
    """Token使用统计"""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    
    def add(self, prompt: int = 0, completion: int = 0):
        """累加Token"""
        self.prompt_tokens += prompt
        self.completion_tokens += completion
        self.total_tokens = self.prompt_tokens + self.completion_tokens


@dataclass
class StepMetrics:
    """单步执行指标"""
    step_number: int
    action_type: str
    start_time: float
    end_time: Optional[float] = None
    duration: Optional[float] = None
    success: bool = True
    error: Optional[str] = None
    
    def finish(self, success: bool = True, error: Optional[str] = None):
        """完成步骤"""
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        self.success = success
        self.error = error


class ExecutionMonitor:
    """执行监控器"""
    
    def __init__(self, max_steps: int = 30, task_id: Optional[str] = None):
        """
        初始化执行监控器
        
        Args:
            max_steps: 最大步数限制
            task_id: 任务ID
        """
        self.max_steps = max_steps
        self.task_id = task_id or f"task_{int(time.time())}"
        
        # 执行状态
        self.status = ExecutionStatus.RUNNING
        self.current_step = 0
        self.start_time = time.time()
        self.end_time: Optional[float] = None
        
        # Token统计
        self.token_usage = TokenUsage()
        
        # 重试追踪
        self.retry_records: List[RetryRecord] = []
        self.system_retry_count = 0
        self.business_retry_count = 0
        
        # 步骤指标
        self.step_metrics: List[StepMetrics] = []
        self.current_step_metric: Optional[StepMetrics] = None
        
        logger.info(f"ExecutionMonitor initialized: task_id={self.task_id}, max_steps={self.max_steps}")
    
    def start_step(self, action_type: str) -> bool:
        """
        开始新步骤
        
        Args:
            action_type: 动作类型
            
        Returns:
            是否允许继续执行（未超过步数限制）
        """
        self.current_step += 1
        
        # 检查步数熔断
        if self.current_step > self.max_steps:
            self.status = ExecutionStatus.STEP_LIMIT_EXCEEDED
            logger.warning(
                f"Step limit exceeded: current_step={self.current_step}, "
                f"max_steps={self.max_steps}"
            )
            return False
        
        # 创建步骤指标
        self.current_step_metric = StepMetrics(
            step_number=self.current_step,
            action_type=action_type,
            start_time=time.time()
        )
        
        logger.debug(f"Step {self.current_step} started: action_type={action_type}")
        return True
    
    def finish_step(self, success: bool = True, error: Optional[str] = None):
        """
        完成当前步骤
        
        Args:
            success: 是否成功
            error: 错误信息
        """
        if self.current_step_metric:
            self.current_step_metric.finish(success=success, error=error)
            self.step_metrics.append(self.current_step_metric)
            
            logger.debug(
                f"Step {self.current_step} finished: "
                f"duration={self.current_step_metric.duration:.2f}s, "
                f"success={success}"
            )
            
            self.current_step_metric = None
    
    def record_retry(self, retry_type: str, reason: str):
        """
        记录重试
        
        Args:
            retry_type: 重试类型 ("system" 或 "business")
            reason: 重试原因
        """
        record = RetryRecord(
            step_number=self.current_step,
            retry_type=retry_type,
            reason=reason
        )
        self.retry_records.append(record)
        
        if retry_type == "system":
            self.system_retry_count += 1
        elif retry_type == "business":
            self.business_retry_count += 1
        
        logger.info(
            f"Retry recorded: step={self.current_step}, "
            f"type={retry_type}, reason={reason}"
        )
    
    def record_tokens(self, prompt_tokens: int = 0, completion_tokens: int = 0):
        """
        记录Token使用
        
        Args:
            prompt_tokens: 提示Token数
            completion_tokens: 完成Token数
        """
        self.token_usage.add(prompt=prompt_tokens, completion=completion_tokens)
        
        logger.debug(
            f"Tokens recorded: prompt={prompt_tokens}, "
            f"completion={completion_tokens}, "
            f"total={self.token_usage.total_tokens}"
        )
    
    def finish(self, status: ExecutionStatus = ExecutionStatus.SUCCESS):
        """
        完成执行
        
        Args:
            status: 最终状态
        """
        self.end_time = time.time()
        self.status = status
        
        logger.info(
            f"Execution finished: status={status.value}, "
            f"duration={self.get_total_duration():.2f}s, "
            f"steps={self.current_step}/{self.max_steps}"
        )
    
    def get_total_duration(self) -> float:
        """获取总耗时（秒）"""
        if self.end_time:
            return self.end_time - self.start_time
        return time.time() - self.start_time
    
    def get_average_step_duration(self) -> float:
        """获取平均步骤耗时（秒）"""
        if not self.step_metrics:
            return 0.0
        
        total_duration = sum(
            m.duration for m in self.step_metrics if m.duration is not None
        )
        return total_duration / len(self.step_metrics)
    
    def get_summary(self) -> Dict[str, Any]:
        """
        获取执行摘要
        
        Returns:
            包含所有监控指标的字典
        """
        return {
            "task_id": self.task_id,
            "status": self.status.value,
            "execution": {
                "current_step": self.current_step,
                "max_steps": self.max_steps,
                "total_duration": round(self.get_total_duration(), 2),
                "average_step_duration": round(self.get_average_step_duration(), 2),
                "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
                "end_time": datetime.fromtimestamp(self.end_time).isoformat() if self.end_time else None,
            },
            "tokens": {
                "prompt_tokens": self.token_usage.prompt_tokens,
                "completion_tokens": self.token_usage.completion_tokens,
                "total_tokens": self.token_usage.total_tokens,
            },
            "retries": {
                "system_retry_count": self.system_retry_count,
                "business_retry_count": self.business_retry_count,
                "total_retry_count": len(self.retry_records),
                "retry_details": [
                    {
                        "step": r.step_number,
                        "type": r.retry_type,
                        "reason": r.reason,
                        "timestamp": datetime.fromtimestamp(r.timestamp).isoformat(),
                    }
                    for r in self.retry_records
                ],
            },
            "steps": [
                {
                    "step": m.step_number,
                    "action": m.action_type,
                    "duration": round(m.duration, 2) if m.duration else None,
                    "success": m.success,
                    "error": m.error,
                }
                for m in self.step_metrics
            ],
        }
    
    def get_metrics_display(self) -> str:
        """
        获取用于UI显示的指标文本
        
        Returns:
            格式化的指标文本
        """
        summary = self.get_summary()
        
        text = f"""
### 📊 执行指标

**状态**: {summary['status']}

**执行统计**:
- 当前步数: {summary['execution']['current_step']} / {summary['execution']['max_steps']}
- 总耗时: {summary['execution']['total_duration']}秒
- 平均步骤耗时: {summary['execution']['average_step_duration']}秒

**Token消耗**:
- Prompt Tokens: {summary['tokens']['prompt_tokens']}
- Completion Tokens: {summary['tokens']['completion_tokens']}
- 总Token数: {summary['tokens']['total_tokens']}

**重试统计**:
- 系统级重试: {summary['retries']['system_retry_count']}
- 业务级重试: {summary['retries']['business_retry_count']}
- 总重试次数: {summary['retries']['total_retry_count']}
"""
        return text.strip()
