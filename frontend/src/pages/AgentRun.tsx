/**
 * AgentRun - 任务执行页面
 * 对应原Gradio WebUI的runAgent功能，提供Agent任务提交、实时监控、执行控制
 */
import { useState, useRef, useEffect, useCallback } from 'react';
import { Button, Input, message, Tag, Tooltip, Empty } from 'antd';
import { Icon } from '@iconify/react';

const { TextArea } = Input;

// 执行状态
type RunStatus = 'idle' | 'running' | 'paused' | 'stopped' | 'completed' | 'error';

// 聊天消息
interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
}

// 执行指标
interface ExecutionMetrics {
  status: RunStatus;
  currentStep: number;
  maxSteps: number;
  totalDuration: number;
  avgStepDuration: number;
  promptTokens: number;
  completionTokens: number;
  totalTokens: number;
  systemRetries: number;
  businessRetries: number;
  totalRetries: number;
}

// 状态显示配置
const statusConfig: Record<RunStatus, { color: string; text: string; icon: string }> = {
  idle: { color: 'default', text: '等待任务', icon: 'mdi:clock-outline' },
  running: { color: 'processing', text: '运行中', icon: 'mdi:loading' },
  paused: { color: 'warning', text: '已暂停', icon: 'mdi:pause-circle' },
  stopped: { color: 'error', text: '已停止', icon: 'mdi:stop-circle' },
  completed: { color: 'success', text: '已完成', icon: 'mdi:check-circle' },
  error: { color: 'error', text: '执行失败', icon: 'mdi:alert-circle' },
};

// 默认指标
const defaultMetrics: ExecutionMetrics = {
  status: 'idle',
  currentStep: 0,
  maxSteps: 0,
  totalDuration: 0,
  avgStepDuration: 0,
  promptTokens: 0,
  completionTokens: 0,
  totalTokens: 0,
  systemRetries: 0,
  businessRetries: 0,
  totalRetries: 0,
};

export function AgentRun() {
  // 任务输入
  const [taskInput, setTaskInput] = useState('');
  // 执行状态
  const [runStatus, setRunStatus] = useState<RunStatus>('idle');
  // 聊天历史
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  // 执行指标
  const [metrics, setMetrics] = useState<ExecutionMetrics>(defaultMetrics);
  // 浏览器截图 (base64)
  const [browserScreenshot, setBrowserScreenshot] = useState<string | null>(null);
  // 任务ID
  const [taskId, setTaskId] = useState<string | null>(null);
  // 轮询定时器
  const pollingRef = useRef<ReturnType<typeof setInterval> | null>(null);
  // 聊天区域滚动
  const chatEndRef = useRef<HTMLDivElement>(null);

  // 自动滚动聊天到底部
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory]);

  // 清理轮询
  useEffect(() => {
    return () => {
      if (pollingRef.current) {
        clearInterval(pollingRef.current);
      }
    };
  }, []);

  // 轮询任务状态
  const startPolling = useCallback((id: string) => {
    if (pollingRef.current) {
      clearInterval(pollingRef.current);
    }

    const poll = async () => {
      try {
        const response = await fetch(`/api/agent/run/${id}/status`);
        if (!response.ok) return;
        const data = await response.json();
        if (data.code === 0 && data.data) {
          const d = data.data;
          setMetrics({
            status: d.status,
            currentStep: d.currentStep ?? 0,
            maxSteps: d.maxSteps ?? 0,
            totalDuration: d.totalDuration ?? 0,
            avgStepDuration: d.avgStepDuration ?? 0,
            promptTokens: d.promptTokens ?? 0,
            completionTokens: d.completionTokens ?? 0,
            totalTokens: d.totalTokens ?? 0,
            systemRetries: d.systemRetries ?? 0,
            businessRetries: d.businessRetries ?? 0,
            totalRetries: d.totalRetries ?? 0,
          });
          setRunStatus(d.status);

          // 更新聊天历史
          if (d.chatHistory && Array.isArray(d.chatHistory)) {
            setChatHistory(d.chatHistory);
          }

          // 更新截图
          if (d.screenshot) {
            setBrowserScreenshot(d.screenshot);
          }

          // 任务结束时停止轮询
          if (['completed', 'stopped', 'error'].includes(d.status)) {
            if (pollingRef.current) {
              clearInterval(pollingRef.current);
              pollingRef.current = null;
            }
          }
        }
      } catch {
        // 网络错误静默处理
      }
    };

    // 立即执行一次
    poll();
    pollingRef.current = setInterval(poll, 1000);
  }, []);

  // 提交任务
  const handleSubmit = async () => {
    const task = taskInput.trim();
    if (!task) {
      message.warning('请输入任务描述');
      return;
    }

    setRunStatus('running');
    setChatHistory([{ role: 'user', content: task, timestamp: new Date().toLocaleTimeString() }]);
    setBrowserScreenshot(null);
    setMetrics({ ...defaultMetrics, status: 'running' });

    try {
      const response = await fetch('/api/agent/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task }),
      });
      const data = await response.json();
      if (data.code === 0 && data.data?.taskId) {
        setTaskId(data.data.taskId);
        setTaskInput('');
        message.success('任务已提交');
        startPolling(data.data.taskId);
      } else {
        message.error(data.message || '任务提交失败');
        setRunStatus('error');
      }
    } catch {
      message.error('网络错误，请检查后端服务');
      setRunStatus('error');
    }
  };

  // 停止任务
  const handleStop = async () => {
    if (!taskId) return;
    try {
      await fetch(`/api/agent/run/${taskId}/stop`, { method: 'POST' });
      setRunStatus('stopped');
      message.info('已发送停止信号');
    } catch {
      message.error('停止请求失败');
    }
  };

  // 暂停/恢复
  const handlePauseResume = async () => {
    if (!taskId) return;
    const action = runStatus === 'paused' ? 'resume' : 'pause';
    try {
      await fetch(`/api/agent/run/${taskId}/${action}`, { method: 'POST' });
      setRunStatus(action === 'pause' ? 'paused' : 'running');
    } catch {
      message.error('操作失败');
    }
  };

  // 清空
  const handleClear = () => {
    if (pollingRef.current) {
      clearInterval(pollingRef.current);
      pollingRef.current = null;
    }
    setTaskInput('');
    setRunStatus('idle');
    setChatHistory([]);
    setMetrics(defaultMetrics);
    setBrowserScreenshot(null);
    setTaskId(null);
    message.success('已清空');
  };

  const isRunning = runStatus === 'running' || runStatus === 'paused';

  return (
    <div className="space-y-5">
      {/* 页面标题 */}
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <Icon icon="mdi:robot" className="text-[24px] text-[#676BEF] mr-3" />
          <h1 className="text-[20px] font-bold text-[#333]">任务执行</h1>
        </div>
        <Tag
          color={statusConfig[runStatus].color}
          icon={<Icon icon={statusConfig[runStatus].icon} className={runStatus === 'running' ? 'animate-spin' : ''} />}
          className="text-[14px] px-3 py-1"
        >
          {statusConfig[runStatus].text}
        </Tag>
      </div>

      {/* 执行指标卡片 - 三列 */}
      <div className="grid grid-cols-3 gap-4">
        {/* 执行统计 */}
        <div className="bg-white rounded-[8px] p-5 card-shadow">
          <div className="flex items-center mb-3">
            <div className="w-[32px] h-[32px] rounded-[6px] bg-[#EEF0FD] flex items-center justify-center mr-3">
              <Icon icon="mdi:chart-timeline-variant" className="text-[18px] text-[#676BEF]" />
            </div>
            <span className="text-[14px] font-semibold text-[#333]">执行统计</span>
          </div>
          <div className="space-y-2 text-[13px]">
            <div className="flex justify-between">
              <span className="text-[#9297A9]">当前步数</span>
              <span className="text-[#333] font-medium">{metrics.currentStep} / {metrics.maxSteps || '-'}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#9297A9]">总耗时</span>
              <span className="text-[#333] font-medium">{metrics.totalDuration.toFixed(2)}秒</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#9297A9]">平均步骤耗时</span>
              <span className="text-[#333] font-medium">{metrics.avgStepDuration.toFixed(2)}秒</span>
            </div>
          </div>
        </div>

        {/* Token消耗 */}
        <div className="bg-white rounded-[8px] p-5 card-shadow">
          <div className="flex items-center mb-3">
            <div className="w-[32px] h-[32px] rounded-[6px] bg-[#FFF4E6] flex items-center justify-center mr-3">
              <Icon icon="mdi:lightning-bolt" className="text-[18px] text-[#F5A623]" />
            </div>
            <span className="text-[14px] font-semibold text-[#333]">Token 消耗</span>
          </div>
          <div className="space-y-2 text-[13px]">
            <div className="flex justify-between">
              <span className="text-[#9297A9]">Prompt Tokens</span>
              <span className="text-[#333] font-medium">{metrics.promptTokens.toLocaleString()}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#9297A9]">Completion Tokens</span>
              <span className="text-[#333] font-medium">{metrics.completionTokens.toLocaleString()}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#9297A9]">总 Token</span>
              <span className="text-[#333] font-medium font-bold">{metrics.totalTokens.toLocaleString()}</span>
            </div>
          </div>
        </div>

        {/* 重试统计 */}
        <div className="bg-white rounded-[8px] p-5 card-shadow">
          <div className="flex items-center mb-3">
            <div className="w-[32px] h-[32px] rounded-[6px] bg-[#FDE8E8] flex items-center justify-center mr-3">
              <Icon icon="mdi:refresh" className="text-[18px] text-[#F35859]" />
            </div>
            <span className="text-[14px] font-semibold text-[#333]">重试统计</span>
          </div>
          <div className="space-y-2 text-[13px]">
            <div className="flex justify-between">
              <span className="text-[#9297A9]">系统级重试</span>
              <span className="text-[#333] font-medium">{metrics.systemRetries}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#9297A9]">业务级重试</span>
              <span className="text-[#333] font-medium">{metrics.businessRetries}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#9297A9]">总重试</span>
              <span className="text-[#333] font-medium">{metrics.totalRetries}</span>
            </div>
          </div>
        </div>
      </div>

      {/* 任务输入区域 */}
      <div className="bg-white rounded-[8px] p-5 card-shadow">
        <div className="flex items-center mb-3">
          <Icon icon="mdi:text-box-edit" className="text-[16px] text-[#676BEF] mr-2" />
          <span className="text-[14px] font-semibold text-[#333]">任务描述</span>
        </div>
        <TextArea
          value={taskInput}
          onChange={(e) => setTaskInput(e.target.value)}
          placeholder={isRunning ? 'Agent 正在执行中...' : '请输入任务描述，例如：打开百度搜索"AI浏览器自动化"并获取前5个结果的标题'}
          rows={3}
          disabled={isRunning}
          onPressEnter={(e) => {
            if (!e.shiftKey && !isRunning) {
              e.preventDefault();
              handleSubmit();
            }
          }}
          className="mb-4"
        />
        <div className="flex items-center gap-3">
          <Button
            type="primary"
            size="large"
            icon={<Icon icon="mdi:play" />}
            onClick={handleSubmit}
            disabled={isRunning || !taskInput.trim()}
            className="flex-1 max-w-[200px]"
          >
            提交任务
          </Button>
          <Tooltip title="停止当前任务">
            <Button
              danger
              size="large"
              icon={<Icon icon="mdi:stop" />}
              onClick={handleStop}
              disabled={!isRunning}
            >
              停止
            </Button>
          </Tooltip>
          <Tooltip title={runStatus === 'paused' ? '恢复执行' : '暂停执行'}>
            <Button
              size="large"
              icon={<Icon icon={runStatus === 'paused' ? 'mdi:play' : 'mdi:pause'} />}
              onClick={handlePauseResume}
              disabled={!isRunning}
            >
              {runStatus === 'paused' ? '恢复' : '暂停'}
            </Button>
          </Tooltip>
          <Tooltip title="清空所有状态">
            <Button
              size="large"
              icon={<Icon icon="mdi:delete-outline" />}
              onClick={handleClear}
              disabled={isRunning}
            >
              清空
            </Button>
          </Tooltip>
        </div>
      </div>

      {/* 主内容区域: 浏览器视图 + 执行历史 */}
      <div className="grid grid-cols-2 gap-5">
        {/* 左侧: 浏览器实时视图 */}
        <div className="bg-white rounded-[8px] card-shadow overflow-hidden">
          <div className="flex items-center px-5 py-3 border-b border-[#f0f0f0]">
            <Icon icon="mdi:web" className="text-[16px] text-[#676BEF] mr-2" />
            <span className="text-[14px] font-semibold text-[#333]">浏览器实时视图</span>
            {isRunning && (
              <span className="ml-2 flex items-center text-[12px] text-[#52c41a]">
                <span className="w-[6px] h-[6px] rounded-full bg-[#52c41a] mr-1 animate-pulse"></span>
                实时
              </span>
            )}
          </div>
          <div className="p-3">
            {browserScreenshot ? (
              <img
                src={`data:image/jpeg;base64,${browserScreenshot}`}
                alt="Browser View"
                className="w-full rounded-[6px] border border-[#e5e7eb]"
                style={{ minHeight: '400px', maxHeight: '60vh', objectFit: 'contain', background: '#f9fafb' }}
              />
            ) : (
              <div
                className="w-full flex flex-col items-center justify-center rounded-[6px] border-2 border-dashed border-[#e5e7eb] bg-[#f9fafb]"
                style={{ minHeight: '400px' }}
              >
                <Icon icon="mdi:monitor-screenshot" className="text-[48px] text-[#d1d5db] mb-3" />
                <p className="text-[14px] text-[#9ca3af]">
                  {isRunning ? '正在等待浏览器响应...' : '提交任务后将在此显示浏览器视图'}
                </p>
              </div>
            )}
          </div>
        </div>

        {/* 右侧: 执行历史记录 */}
        <div className="bg-white rounded-[8px] card-shadow overflow-hidden flex flex-col" style={{ maxHeight: 'calc(60vh + 56px)' }}>
          <div className="flex items-center justify-between px-5 py-3 border-b border-[#f0f0f0]">
            <div className="flex items-center">
              <Icon icon="mdi:message-text" className="text-[16px] text-[#676BEF] mr-2" />
              <span className="text-[14px] font-semibold text-[#333]">执行历史记录</span>
            </div>
            <span className="text-[12px] text-[#9297A9]">{chatHistory.length} 条消息</span>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-3" style={{ minHeight: '400px' }}>
            {chatHistory.length === 0 ? (
              <div className="h-full flex items-center justify-center">
                <Empty description="暂无执行记录" image={Empty.PRESENTED_IMAGE_SIMPLE} />
              </div>
            ) : (
              chatHistory.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[85%] rounded-[8px] px-4 py-3 text-[13px] leading-[1.6] ${
                      msg.role === 'user'
                        ? 'bg-[#676BEF] text-white'
                        : msg.role === 'system'
                        ? 'bg-[#FFF4E6] text-[#F5A623] border border-[#F5A623]/20'
                        : 'bg-[#f5f5f5] text-[#333]'
                    }`}
                  >
                    {msg.role !== 'user' && (
                      <div className="flex items-center mb-1.5">
                        <Icon
                          icon={msg.role === 'system' ? 'mdi:information' : 'mdi:robot'}
                          className="text-[14px] mr-1"
                        />
                        <span className="text-[11px] font-medium opacity-70">
                          {msg.role === 'system' ? '系统' : 'Agent'}
                        </span>
                        {msg.timestamp && (
                          <span className="text-[10px] ml-2 opacity-50">{msg.timestamp}</span>
                        )}
                      </div>
                    )}
                    <div
                      className="whitespace-pre-wrap break-words"
                      dangerouslySetInnerHTML={{ __html: msg.content }}
                    />
                  </div>
                </div>
              ))
            )}
            <div ref={chatEndRef} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default AgentRun;
