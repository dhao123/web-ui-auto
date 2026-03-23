/**
 * AgentRun - 任务执行页面
 * 专业级设计，无重叠问题
 */
import { useState, useRef, useEffect, useCallback } from 'react';
import { Button, Input, message, Tag, Empty, Card, Progress } from 'antd';
import { Icon } from '@iconify/react';

import { useApp } from '@/context/AppContext';
import { api } from '@/utils/api';
import type { ChatMessage, ExecutionMetrics } from '@/types/common';

const { TextArea } = Input;

type RunStatus = 'idle' | 'running' | 'paused' | 'stopped' | 'completed' | 'error';

const statusConfig: Record<RunStatus, { color: string; bgColor: string; text: string; icon: string }> = {
  idle: { color: '#64748b', bgColor: 'rgba(100, 116, 139, 0.15)', text: '等待任务', icon: 'mdi:clock-outline' },
  running: { color: '#6366f1', bgColor: 'rgba(99, 102, 241, 0.15)', text: '运行中', icon: 'mdi:loading' },
  paused: { color: '#f59e0b', bgColor: 'rgba(245, 158, 11, 0.15)', text: '已暂停', icon: 'mdi:pause-circle' },
  stopped: { color: '#ef4444', bgColor: 'rgba(239, 68, 68, 0.15)', text: '已停止', icon: 'mdi:stop-circle' },
  completed: { color: '#22c55e', bgColor: 'rgba(34, 197, 94, 0.15)', text: '已完成', icon: 'mdi:check-circle' },
  error: { color: '#ef4444', bgColor: 'rgba(239, 68, 68, 0.15)', text: '执行失败', icon: 'mdi:alert-circle' },
};

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

// 指标行组件
function MetricRow({ label, value, highlight }: { label: string; value: string | number; highlight?: boolean }) {
  return (
    <div className="metric-row">
      <span className="metric-label">{label}</span>
      <span className="metric-value" style={{ color: highlight ? '#818cf8' : undefined }}>{value}</span>
    </div>
  );
}

// 指标卡片组件
function MetricCard({ 
  title, 
  icon, 
  iconBg, 
  iconColor,
  headerRight,
  children,
}: { 
  title: string;
  icon: string;
  iconBg: string;
  iconColor: string;
  headerRight?: React.ReactNode;
  children: React.ReactNode;
}) {
  return (
    <div className="metric-card">
      <div className="metric-card-header">
        <div className="metric-card-icon" style={{ background: iconBg }}>
          <Icon icon={icon} style={{ fontSize: 20, color: iconColor }} />
        </div>
        <span className="metric-card-title">{title}</span>
        {headerRight}
      </div>
      <div className="metric-card-body">
        {children}
      </div>
    </div>
  );
}

export function AgentRun() {
  const { setCurrentTaskId, setTaskStatus: setGlobalTaskStatus, refreshTaskList } = useApp();
  const [taskInput, setTaskInput] = useState('');
  const [runStatus, setRunStatus] = useState<RunStatus>('idle');
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [metrics, setMetrics] = useState<ExecutionMetrics>(defaultMetrics);
  const [browserScreenshot, setBrowserScreenshot] = useState<string | null>(null);
  const [taskId, setTaskId] = useState<string | null>(null);
  const pollingRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory]);

  useEffect(() => {
    return () => {
      if (pollingRef.current) clearInterval(pollingRef.current);
    };
  }, []);

  const startPolling = useCallback((id: string) => {
    if (pollingRef.current) clearInterval(pollingRef.current);

    const poll = async () => {
      try {
        const res = await api.getAgentRunStatus(id);
        if (res.code === 0 && res.data) {
          const d = res.data;
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
          setRunStatus(d.status as RunStatus);
          
          const globalStatus = d.status === 'stopped' ? 'idle' : d.status as 'idle' | 'running' | 'paused' | 'completed' | 'error';
          setGlobalTaskStatus(globalStatus);

          if (d.chatHistory) setChatHistory(d.chatHistory);
          if (d.screenshot) setBrowserScreenshot(d.screenshot);

          if (['completed', 'stopped', 'error'].includes(d.status)) {
            if (pollingRef.current) {
              clearInterval(pollingRef.current);
              pollingRef.current = null;
            }
            setCurrentTaskId(null);
            refreshTaskList();
          }
        }
      } catch {}
    };

    poll();
    pollingRef.current = setInterval(poll, 1000);
  }, [setCurrentTaskId, setGlobalTaskStatus, refreshTaskList]);

  const handleSubmit = async () => {
    const task = taskInput.trim();
    if (!task) {
      message.warning('请输入任务描述');
      return;
    }

    setRunStatus('running');
    setGlobalTaskStatus('running');
    setChatHistory([{ role: 'user', content: task, timestamp: new Date().toLocaleTimeString() }]);
    setBrowserScreenshot(null);
    setMetrics({ ...defaultMetrics, status: 'running' });

    try {
      const res = await api.startAgentRun(task);
      if (res.code === 0 && res.data?.taskId) {
        setTaskId(res.data.taskId);
        setCurrentTaskId(res.data.taskId);
        setTaskInput('');
        message.success('任务已提交');
        startPolling(res.data.taskId);
      } else {
        message.error(res.message || '任务提交失败');
        setRunStatus('error');
        setGlobalTaskStatus('idle');
      }
    } catch {
      message.error('网络错误，请检查后端服务');
      setRunStatus('error');
      setGlobalTaskStatus('idle');
    }
  };

  const handleStop = async () => {
    if (!taskId) return;
    try {
      await api.stopAgentRun(taskId);
      setRunStatus('stopped');
      setGlobalTaskStatus('idle');
      message.info('已发送停止信号');
    } catch {
      message.error('停止请求失败');
    }
  };

  const handlePauseResume = async () => {
    if (!taskId) return;
    const action = runStatus === 'paused' ? 'resume' : 'pause';
    try {
      if (action === 'pause') {
        await api.pauseAgentRun(taskId);
        setRunStatus('paused');
        setGlobalTaskStatus('paused');
      } else {
        await api.resumeAgentRun(taskId);
        setRunStatus('running');
        setGlobalTaskStatus('running');
      }
    } catch {
      message.error('操作失败');
    }
  };

  const handleClear = () => {
    if (pollingRef.current) {
      clearInterval(pollingRef.current);
      pollingRef.current = null;
    }
    setTaskInput('');
    setRunStatus('idle');
    setGlobalTaskStatus('idle');
    setChatHistory([]);
    setMetrics(defaultMetrics);
    setBrowserScreenshot(null);
    setTaskId(null);
    setCurrentTaskId(null);
    message.success('已清空');
  };

  const isRunning = runStatus === 'running' || runStatus === 'paused';
  const progressPercent = metrics.maxSteps > 0 ? Math.round((metrics.currentStep / metrics.maxSteps) * 100) : 0;
  const status = statusConfig[runStatus];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      {/* 页面标题 */}
      <div className="page-header">
        <div className="page-header-title">
          <div className="page-header-icon">
            <Icon icon="mdi:robot" />
          </div>
          <div className="page-header-text">
            <h1>任务执行</h1>
            <p>智能浏览器自动化测试平台</p>
          </div>
        </div>
        <Tag
          style={{
            backgroundColor: status.bgColor,
            borderColor: `${status.color}50`,
            color: status.color,
            borderWidth: 1,
            padding: '6px 16px',
            fontSize: 14,
            fontWeight: 600,
            margin: 0,
          }}
        >
          <Icon icon={status.icon} style={{ marginRight: 6 }} className={runStatus === 'running' ? 'animate-spin' : ''} />
          {status.text}
        </Tag>
      </div>

      {/* 指标卡片 */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 24 }}>
        <MetricCard
          title="执行统计"
          icon="mdi:chart-timeline-variant"
          iconColor="#6366f1"
          iconBg="rgba(99, 102, 241, 0.15)"
          headerRight={metrics.maxSteps > 0 && (
            <span style={{ fontSize: 13, color: '#818cf8', fontFamily: 'JetBrains Mono, monospace' }}>{progressPercent}%</span>
          )}
        >
          {/* 进度条 - 运行时显示动态效果 */}
          <div style={{ marginBottom: 16 }}>
            {runStatus === 'running' ? (
              <Progress 
                percent={100} 
                size="small"
                showInfo={false}
                strokeColor={{ '0%': '#6366f1', '100%': '#a855f7' }}
                status="active"
              />
            ) : metrics.maxSteps > 0 ? (
              <Progress 
                percent={progressPercent} 
                size="small"
                showInfo={false}
                strokeColor={{ '0%': '#6366f1', '100%': '#a855f7' }}
              />
            ) : (
              <div style={{ height: 6, background: 'rgba(99, 102, 241, 0.1)', borderRadius: 3, overflow: 'hidden' }}>
                <div 
                  style={{ 
                    height: '100%', 
                    width: runStatus === 'idle' ? '0%' : '100%',
                    background: 'linear-gradient(90deg, #6366f1, #a855f7)',
                    borderRadius: 3,
                    transition: 'width 0.3s ease'
                  }} 
                />
              </div>
            )}
          </div>
          <MetricRow label="当前步数" value={`${metrics.currentStep} / ${metrics.maxSteps || '-'}`} />
          <MetricRow label="总耗时" value={`${metrics.totalDuration.toFixed(2)}s`} />
          <MetricRow label="平均步骤耗时" value={`${metrics.avgStepDuration.toFixed(2)}s`} />
        </MetricCard>

        <MetricCard
          title="Token 消耗"
          icon="mdi:lightning-bolt"
          iconColor="#f59e0b"
          iconBg="rgba(245, 158, 11, 0.15)"
        >
          {/* 动态进度条 */}
          <div style={{ marginBottom: 16 }}>
            {runStatus === 'running' ? (
              <Progress 
                percent={100} 
                size="small"
                showInfo={false}
                strokeColor={{ '0%': '#f59e0b', '100%': '#f97316' }}
                status="active"
              />
            ) : (
              <div style={{ height: 6, background: 'rgba(245, 158, 11, 0.1)', borderRadius: 3, overflow: 'hidden' }}>
                <div 
                  style={{ 
                    height: '100%', 
                    width: runStatus === 'idle' ? '0%' : '100%',
                    background: 'linear-gradient(90deg, #f59e0b, #f97316)',
                    borderRadius: 3,
                    transition: 'width 0.3s ease'
                  }} 
                />
              </div>
            )}
          </div>
          <MetricRow label="Prompt Tokens" value={metrics.promptTokens.toLocaleString()} />
          <MetricRow label="Completion Tokens" value={metrics.completionTokens.toLocaleString()} />
          <MetricRow label="总 Token" value={metrics.totalTokens.toLocaleString()} highlight />
        </MetricCard>

        <MetricCard
          title="重试统计"
          icon="mdi:refresh"
          iconColor="#ef4444"
          iconBg="rgba(239, 68, 68, 0.15)"
        >
          {/* 动态进度条 */}
          <div style={{ marginBottom: 16 }}>
            {runStatus === 'running' ? (
              <Progress 
                percent={100} 
                size="small"
                showInfo={false}
                strokeColor={{ '0%': '#ef4444', '100%': '#f97316' }}
                status="active"
              />
            ) : (
              <div style={{ height: 6, background: 'rgba(239, 68, 68, 0.1)', borderRadius: 3, overflow: 'hidden' }}>
                <div 
                  style={{ 
                    height: '100%', 
                    width: runStatus === 'idle' ? '0%' : '100%',
                    background: 'linear-gradient(90deg, #ef4444, #f97316)',
                    borderRadius: 3,
                    transition: 'width 0.3s ease'
                  }} 
                />
              </div>
            )}
          </div>
          <MetricRow label="系统级重试" value={metrics.systemRetries} />
          <MetricRow label="业务级重试" value={metrics.businessRetries} />
          <MetricRow label="总重试" value={metrics.totalRetries} highlight />
        </MetricCard>
      </div>

      {/* 任务输入 */}
      <Card>
        <div style={{ marginBottom: 16 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 }}>
            <div style={{ 
              width: 32, height: 32, borderRadius: 8, 
              background: 'rgba(99, 102, 241, 0.15)',
              display: 'flex', alignItems: 'center', justifyContent: 'center'
            }}>
              <Icon icon="mdi:text-box-edit" style={{ color: '#818cf8' }} />
            </div>
            <span style={{ fontSize: 15, fontWeight: 600, color: '#ffffff' }}>任务描述</span>
          </div>
          <TextArea
            value={taskInput}
            onChange={(e) => setTaskInput(e.target.value)}
            placeholder={isRunning ? 'Agent 正在执行中...' : '请输入任务描述，例如：打开百度搜索"AI浏览器自动化"并获取前5个结果的标题'}
            rows={4}
            disabled={isRunning}
            onPressEnter={(e) => {
              if (!e.shiftKey && !isRunning) {
                e.preventDefault();
                handleSubmit();
              }
            }}
            style={{ marginBottom: 16 }}
          />
          <div style={{ display: 'flex', gap: 12 }}>
            <Button
              type="primary"
              size="large"
              icon={<Icon icon="mdi:play" />}
              onClick={handleSubmit}
              disabled={isRunning || !taskInput.trim()}
              style={{ minWidth: 140, height: 44 }}
            >
              提交任务
            </Button>
            <Button
              danger
              size="large"
              icon={<Icon icon="mdi:stop" />}
              onClick={handleStop}
              disabled={!isRunning}
              style={{ height: 44 }}
            >
              停止
            </Button>
            <Button
              size="large"
              icon={<Icon icon={runStatus === 'paused' ? 'mdi:play' : 'mdi:pause'} />}
              onClick={handlePauseResume}
              disabled={!isRunning}
              style={{ height: 44 }}
            >
              {runStatus === 'paused' ? '恢复' : '暂停'}
            </Button>
            <Button
              size="large"
              icon={<Icon icon="mdi:delete-outline" />}
              onClick={handleClear}
              disabled={isRunning}
              style={{ height: 44 }}
            >
              清空
            </Button>
          </div>
        </div>
      </Card>

      {/* 浏览器视图 + 执行历史 */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 24 }}>
        <Card
          title={
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <div style={{ 
                width: 32, height: 32, borderRadius: 8, 
                background: 'rgba(99, 102, 241, 0.15)',
                display: 'flex', alignItems: 'center', justifyContent: 'center'
              }}>
                <Icon icon="mdi:web" style={{ color: '#818cf8' }} />
              </div>
              <span style={{ fontSize: 15, fontWeight: 600, color: '#ffffff' }}>浏览器实时视图</span>
              {isRunning && (
                <span style={{ 
                  display: 'flex', alignItems: 'center', gap: 4,
                  padding: '4px 10px', borderRadius: 4,
                  background: 'rgba(34, 197, 94, 0.15)',
                  color: '#22c55e',
                  fontSize: 12,
                  fontWeight: 600,
                  marginLeft: 'auto'
                }}>
                  <span style={{ width: 6, height: 6, borderRadius: '50%', background: '#22c55e', animation: 'pulse 1.5s infinite' }} />
                  实时
                </span>
              )}
            </div>
          }
        >
          {browserScreenshot ? (
            <img
              src={`data:image/svg+xml;base64,${browserScreenshot}`}
              alt="Browser"
              style={{ 
                width: '100%', borderRadius: 8, minHeight: 400, maxHeight: '55vh',
                objectFit: 'contain', background: '#0f141f', border: '1px solid #2d3748'
              }}
            />
          ) : (
            <div style={{ 
              width: '100%', minHeight: 400, display: 'flex', flexDirection: 'column',
              alignItems: 'center', justifyContent: 'center',
              background: '#0f141f', border: '2px dashed #2d3748',
              borderRadius: 8
            }}>
              <Icon icon="mdi:monitor-screenshot" style={{ fontSize: 64, color: '#3d4757', marginBottom: 16 }} />
              <span style={{ color: '#5a6478' }}>
                {isRunning ? '正在等待浏览器响应...' : '提交任务后将在此显示浏览器视图'}
              </span>
            </div>
          )}
        </Card>

        <Card
          title={
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <div style={{ 
                  width: 32, height: 32, borderRadius: 8, 
                  background: 'rgba(99, 102, 241, 0.15)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center'
                }}>
                  <Icon icon="mdi:message-text" style={{ color: '#818cf8' }} />
                </div>
                <span style={{ fontSize: 15, fontWeight: 600, color: '#ffffff' }}>执行历史记录</span>
              </div>
              <span style={{ 
                padding: '4px 10px', borderRadius: 4, background: '#151b2b',
                color: '#8b95a5', fontSize: 12, fontWeight: 500
              }}>
                {chatHistory.length} 条消息
              </span>
            </div>
          }
        >
          <div style={{ 
            maxHeight: 'calc(55vh + 70px)', overflow: 'auto', minHeight: 400,
            display: 'flex', flexDirection: 'column', gap: 12
          }}>
            {chatHistory.length === 0 ? (
              <Empty description="暂无执行记录" image={Empty.PRESENTED_IMAGE_SIMPLE} style={{ marginTop: 100 }} />
            ) : (
              chatHistory.map((msg, idx) => (
                <div
                  key={idx}
                  style={{ 
                    alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                    maxWidth: '85%'
                  }}
                >
                  <div
                    style={{
                      padding: '12px 16px',
                      borderRadius: 12,
                      background: msg.role === 'user'
                        ? 'linear-gradient(135deg, #6366f1 0%, #a855f7 100%)'
                        : msg.role === 'system'
                        ? 'rgba(245, 158, 11, 0.1)'
                        : '#242b3d',
                      border: msg.role === 'system' ? '1px solid rgba(245, 158, 11, 0.3)' : msg.role !== 'user' ? '1px solid #2d3748' : 'none',
                      color: msg.role === 'user' ? '#ffffff' : msg.role === 'system' ? '#f59e0b' : '#b8c0cc',
                      fontSize: 14,
                      lineHeight: 1.6,
                    }}
                  >
                    {msg.role !== 'user' && (
                      <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 6, opacity: 0.8 }}>
                        <Icon icon={msg.role === 'system' ? 'mdi:information' : 'mdi:robot'} style={{ fontSize: 14 }} />
                        <span style={{ fontSize: 12, fontWeight: 500 }}>{msg.role === 'system' ? '系统' : 'Agent'}</span>
                        {msg.timestamp && <span style={{ fontSize: 11, opacity: 0.6, marginLeft: 'auto' }}>{msg.timestamp}</span>}
                      </div>
                    )}
                    <div dangerouslySetInnerHTML={{ __html: msg.content }} />
                  </div>
                </div>
              ))
            )}
            <div ref={chatEndRef} />
          </div>
        </Card>
      </div>
    </div>
  );
}

export default AgentRun;
