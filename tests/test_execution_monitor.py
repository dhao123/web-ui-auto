"""
测试执行监控器功能
"""
import pytest
import time
from src.utils.execution_monitor import (
    ExecutionMonitor,
    ExecutionStatus,
    RetryRecord,
    TokenUsage,
    StepMetrics
)


def test_execution_monitor_initialization():
    """测试执行监控器初始化"""
    monitor = ExecutionMonitor(max_steps=30, task_id="test_task_001")
    
    assert monitor.max_steps == 30
    assert monitor.task_id == "test_task_001"
    assert monitor.current_step == 0
    assert monitor.status == ExecutionStatus.RUNNING
    assert monitor.token_usage.total_tokens == 0
    assert len(monitor.retry_records) == 0
    assert len(monitor.step_metrics) == 0


def test_step_execution():
    """测试步骤执行"""
    monitor = ExecutionMonitor(max_steps=5)
    
    # 执行3个步骤
    for i in range(3):
        assert monitor.start_step(f"action_{i}") is True
        time.sleep(0.1)  # 模拟执行时间
        monitor.finish_step(success=True)
    
    assert monitor.current_step == 3
    assert len(monitor.step_metrics) == 3
    assert all(m.success for m in monitor.step_metrics)


def test_step_limit_exceeded():
    """测试步数熔断"""
    monitor = ExecutionMonitor(max_steps=3)
    
    # 执行3个步骤
    for i in range(3):
        assert monitor.start_step(f"action_{i}") is True
        monitor.finish_step(success=True)
    
    # 第4个步骤应该被熔断
    assert monitor.start_step("action_4") is False
    assert monitor.status == ExecutionStatus.STEP_LIMIT_EXCEEDED


def test_retry_tracking():
    """测试重试追踪"""
    monitor = ExecutionMonitor(max_steps=10)
    
    monitor.start_step("action_1")
    
    # 记录系统级重试
    monitor.record_retry("system", "Network timeout")
    monitor.record_retry("system", "Connection error")
    
    # 记录业务级重试
    monitor.record_retry("business", "Validation failed")
    
    monitor.finish_step(success=True)
    
    assert monitor.system_retry_count == 2
    assert monitor.business_retry_count == 1
    assert len(monitor.retry_records) == 3
    
    # 验证重试记录
    assert monitor.retry_records[0].retry_type == "system"
    assert monitor.retry_records[0].reason == "Network timeout"
    assert monitor.retry_records[2].retry_type == "business"


def test_token_usage():
    """测试Token统计"""
    monitor = ExecutionMonitor(max_steps=10)
    
    # 记录多次Token使用
    monitor.record_tokens(prompt_tokens=100, completion_tokens=50)
    monitor.record_tokens(prompt_tokens=200, completion_tokens=100)
    monitor.record_tokens(prompt_tokens=150, completion_tokens=75)
    
    assert monitor.token_usage.prompt_tokens == 450
    assert monitor.token_usage.completion_tokens == 225
    assert monitor.token_usage.total_tokens == 675


def test_duration_metrics():
    """测试耗时度量"""
    monitor = ExecutionMonitor(max_steps=5)
    
    # 执行3个步骤，每个步骤耗时不同
    for i in range(3):
        monitor.start_step(f"action_{i}")
        time.sleep(0.1 * (i + 1))  # 0.1s, 0.2s, 0.3s
        monitor.finish_step(success=True)
    
    # 验证总耗时
    total_duration = monitor.get_total_duration()
    assert total_duration >= 0.6  # 至少0.6秒
    
    # 验证平均步骤耗时
    avg_duration = monitor.get_average_step_duration()
    assert 0.15 <= avg_duration <= 0.25  # 平均约0.2秒


def test_execution_summary():
    """测试执行摘要"""
    monitor = ExecutionMonitor(max_steps=10, task_id="test_summary")
    
    # 执行一些步骤
    for i in range(3):
        monitor.start_step(f"action_{i}")
        time.sleep(0.05)
        monitor.record_tokens(prompt_tokens=100, completion_tokens=50)
        if i == 1:
            monitor.record_retry("system", "Timeout")
        monitor.finish_step(success=True)
    
    monitor.finish(ExecutionStatus.SUCCESS)
    
    # 获取摘要
    summary = monitor.get_summary()
    
    assert summary["task_id"] == "test_summary"
    assert summary["status"] == "SUCCESS"
    assert summary["execution"]["current_step"] == 3
    assert summary["execution"]["max_steps"] == 10
    assert summary["tokens"]["total_tokens"] == 450
    assert summary["retries"]["system_retry_count"] == 1
    assert len(summary["steps"]) == 3


def test_metrics_display():
    """测试指标显示文本"""
    monitor = ExecutionMonitor(max_steps=30, task_id="test_display")
    
    # 执行一些操作
    monitor.start_step("action_1")
    monitor.record_tokens(prompt_tokens=500, completion_tokens=200)
    monitor.record_retry("business", "Validation failed")
    monitor.finish_step(success=True)
    
    # 获取显示文本
    display_text = monitor.get_metrics_display()
    
    assert "状态" in display_text
    assert "RUNNING" in display_text
    assert "1 / 30" in display_text
    assert "500" in display_text  # prompt tokens
    assert "200" in display_text  # completion tokens
    assert "700" in display_text  # total tokens


def test_step_failure():
    """测试步骤失败"""
    monitor = ExecutionMonitor(max_steps=10)
    
    monitor.start_step("action_1")
    monitor.finish_step(success=False, error="Action failed")
    
    assert len(monitor.step_metrics) == 1
    assert monitor.step_metrics[0].success is False
    assert monitor.step_metrics[0].error == "Action failed"


def test_execution_status_transitions():
    """测试执行状态转换"""
    monitor = ExecutionMonitor(max_steps=5)
    
    # 初始状态
    assert monitor.status == ExecutionStatus.RUNNING
    
    # 成功完成
    monitor.finish(ExecutionStatus.SUCCESS)
    assert monitor.status == ExecutionStatus.SUCCESS
    assert monitor.end_time is not None
    
    # 新任务 - 失败
    monitor2 = ExecutionMonitor(max_steps=5)
    monitor2.finish(ExecutionStatus.FAILED)
    assert monitor2.status == ExecutionStatus.FAILED
    
    # 新任务 - 取消
    monitor3 = ExecutionMonitor(max_steps=5)
    monitor3.finish(ExecutionStatus.CANCELLED)
    assert monitor3.status == ExecutionStatus.CANCELLED


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
