/**
 * Dashboard - 首页仪表盘
 * 专业级设计，无重叠问题
 */
import { useState, useEffect } from 'react';
import { Button, Tag, Space, message, Card, Row, Col } from 'antd';
import { Icon } from '@iconify/react';
import ReactECharts from 'echarts-for-react';
import type { ColumnsType } from 'antd/es/table';

import { BaseTable } from '@/components';
import type { Task, TaskStatus, TaskStatistics, TokenTrend, TaskAnalysis } from '@/types/common';
import { api } from '@/utils/api';

// 状态标签映射
const statusConfig: Record<TaskStatus, { color: string; text: string; icon: string }> = {
  pending: { color: '#f59e0b', text: '等待中', icon: 'mdi:clock-outline' },
  running: { color: '#6366f1', text: '运行中', icon: 'mdi:loading' },
  completed: { color: '#22c55e', text: '已完成', icon: 'mdi:check-circle' },
  failed: { color: '#ef4444', text: '失败', icon: 'mdi:alert-circle' },
  cancelled: { color: '#64748b', text: '已取消', icon: 'mdi:cancel' },
};

// 统计卡片组件
function StatCard({ 
  title, 
  value, 
  suffix, 
  icon, 
  iconBg, 
  iconColor,
  trend,
  loading 
}: { 
  title: string;
  value: string | number;
  suffix?: string;
  icon: string;
  iconBg: string;
  iconColor: string;
  trend?: { value: number; isUp: boolean };
  loading?: boolean;
}) {
  return (
    <div className="stat-card" style={{ height: '100%' }}>
      <div className="stat-card-header">
        <div className="stat-card-icon" style={{ background: iconBg }}>
          <Icon icon={icon} style={{ fontSize: 22, color: iconColor }} />
        </div>
        {trend && (
          <div 
            className="stat-card-trend"
            style={{
              background: trend.isUp ? 'rgba(34, 197, 94, 0.15)' : 'rgba(239, 68, 68, 0.15)',
              color: trend.isUp ? '#22c55e' : '#ef4444',
            }}
          >
            <Icon icon={trend.isUp ? 'mdi:trending-up' : 'mdi:trending-down'} style={{ fontSize: 14 }} />
            {trend.value}%
          </div>
        )}
      </div>
      <div className="stat-card-label">{title}</div>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 4 }}>
        <span className="stat-card-value">{loading ? '-' : value}</span>
        {suffix && <span className="stat-card-suffix">{suffix}</span>}
      </div>
    </div>
  );
}

export function Dashboard() {
  const [statistics, setStatistics] = useState<TaskStatistics | null>(null);
  const [tokenTrend, setTokenTrend] = useState<TokenTrend[]>([]);
  const [taskAnalysis, setTaskAnalysis] = useState<TaskAnalysis | null>(null);
  const [recentTasks, setRecentTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        const [statsRes, trendRes, analysisRes, tasksRes] = await Promise.all([
          api.getStatistics(),
          api.getTokenTrend(),
          api.getTaskAnalysis(),
          api.getTasks({ page: 1, pageSize: 5 }),
        ]);

        if (statsRes.code === 0 && statsRes.data) setStatistics(statsRes.data);
        if (trendRes.code === 0 && trendRes.data) setTokenTrend(trendRes.data.trends || []);
        if (analysisRes.code === 0 && analysisRes.data) setTaskAnalysis(analysisRes.data);
        if (tasksRes.code === 0 && tasksRes.data) setRecentTasks(tasksRes.data.list || []);
      } catch {
        message.error('加载数据失败');
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  // Token趋势图表配置
  const tokenChartOption = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(28, 35, 51, 0.95)',
      borderColor: '#2d3748',
      borderWidth: 1,
      textStyle: { color: '#ffffff', fontSize: 13 },
      padding: [12, 16],
    },
    grid: {
      left: 16,
      right: 16,
      bottom: 16,
      top: 24,
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: tokenTrend.map(item => item.date),
      axisLine: { lineStyle: { color: '#2d3748' } },
      axisLabel: { color: '#8b95a5', fontSize: 12 },
      axisTick: { show: false },
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      splitLine: { lineStyle: { color: '#2d3748', type: 'dashed' } },
      axisLabel: { color: '#8b95a5', fontSize: 12 },
    },
    series: [{
      data: tokenTrend.map(item => item.tokens),
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 8,
      lineStyle: { 
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 1, y2: 0,
          colorStops: [{ offset: 0, color: '#6366f1' }, { offset: 1, color: '#a855f7' }],
        },
        width: 3,
      },
      itemStyle: { color: '#6366f1', borderWidth: 2, borderColor: '#1c2333' },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [{ offset: 0, color: 'rgba(99, 102, 241, 0.3)' }, { offset: 1, color: 'rgba(99, 102, 241, 0)' }],
        },
      },
    }],
  };

  // 饼图配置
  const pieChartOption = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(28, 35, 51, 0.95)',
      borderColor: '#2d3748',
      borderWidth: 1,
      textStyle: { color: '#ffffff', fontSize: 13 },
    },
    legend: {
      orient: 'vertical',
      right: 16,
      top: 'center',
      textStyle: { color: '#b8c0cc', fontSize: 13 },
      itemWidth: 12,
      itemHeight: 12,
      itemGap: 16,
    },
    series: [{
      type: 'pie',
      radius: ['50%', '70%'],
      center: ['35%', '50%'],
      avoidLabelOverlap: false,
      label: {
        show: true,
        position: 'center',
        formatter: `{a|${statistics?.successRate || 0}%}\n{b|成功率}`,
        rich: {
          a: { fontSize: 28, fontWeight: 'bold', color: '#ffffff', lineHeight: 36 },
          b: { fontSize: 12, color: '#8b95a5' }
        }
      },
      labelLine: { show: false },
      data: [
        { 
          value: taskAnalysis?.successCount || 0, 
          name: '成功', 
          itemStyle: { color: '#22c55e' } 
        },
        { 
          value: taskAnalysis?.failedCount || 0, 
          name: '失败', 
          itemStyle: { color: '#ef4444' } 
        },
      ],
    }],
  };

  // 柱状图配置
  const barChartOption = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(28, 35, 51, 0.95)',
      borderColor: '#2d3748',
      borderWidth: 1,
      textStyle: { color: '#ffffff', fontSize: 13 },
    },
    grid: {
      left: 16,
      right: 16,
      bottom: 16,
      top: 24,
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: taskAnalysis?.durationDistribution.map(item => item.range) || [],
      axisLine: { lineStyle: { color: '#2d3748' } },
      axisLabel: { color: '#8b95a5', fontSize: 11 },
      axisTick: { show: false },
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      splitLine: { lineStyle: { color: '#2d3748', type: 'dashed' } },
      axisLabel: { color: '#8b95a5', fontSize: 12 },
    },
    series: [{
      data: taskAnalysis?.durationDistribution.map(item => item.count) || [],
      type: 'bar',
      barWidth: '50%',
      itemStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [{ offset: 0, color: '#6366f1' }, { offset: 1, color: '#a855f7' }],
        },
        borderRadius: [4, 4, 0, 0],
      },
    }],
  };

  // 表格列
  const columns: ColumnsType<Task> = [
    {
      title: '任务名称',
      dataIndex: 'name',
      key: 'name',
      width: 200,
      render: (text) => <span style={{ color: '#ffffff', fontWeight: 500 }}>{text}</span>,
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status: TaskStatus) => (
        <Tag 
          style={{
            backgroundColor: `${statusConfig[status].color}15`,
            borderColor: `${statusConfig[status].color}40`,
            color: statusConfig[status].color,
            borderWidth: 1,
            margin: 0,
          }}
        >
          <Icon icon={statusConfig[status].icon} style={{ marginRight: 4 }} className={status === 'running' ? 'animate-spin' : ''} />
          {statusConfig[status].text}
        </Tag>
      ),
    },
    {
      title: '开始时间',
      dataIndex: 'startTime',
      key: 'startTime',
      width: 160,
      render: (text) => <span style={{ color: '#8b95a5' }}>{text}</span>,
    },
    {
      title: '耗时',
      dataIndex: 'duration',
      key: 'duration',
      width: 80,
      render: (duration?: number) => (
        <span style={{ color: '#b8c0cc' }}>{duration ? `${duration}s` : '-'}</span>
      ),
    },
    {
      title: 'Token消耗',
      dataIndex: 'tokenUsed',
      key: 'tokenUsed',
      width: 110,
      render: (tokens?: number) => (
        <span style={{ color: '#818cf8', fontFamily: 'JetBrains Mono, monospace' }}>
          {tokens ? tokens.toLocaleString() : '-'}
        </span>
      ),
    },
    {
      title: '操作',
      key: 'action',
      width: 80,
      render: (_, record) => (
        <Button 
          type="text" 
          size="small"
          icon={<Icon icon="mdi:eye-outline" />}
          onClick={() => message.info(`查看任务: ${record.name}`)}
          style={{ color: '#818cf8' }}
        >
          详情
        </Button>
      ),
    },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      {/* Hero Banner */}
      <div className="hero-banner">
        <h1 className="hero-title">AI Browser Automation</h1>
        <p className="hero-description">
          智能浏览器自动化平台，让AI帮你完成复杂的网页操作任务
        </p>
        <Space size={12}>
          <Button 
            type="primary" 
            size="large"
            icon={<Icon icon="mdi:rocket-launch" />}
            onClick={() => window.location.href = '/execute'}
            style={{ height: 44, padding: '0 24px', fontSize: 15 }}
          >
            开始新任务
          </Button>
          <Button 
            size="large"
            icon={<Icon icon="mdi:book-open" />}
            onClick={() => message.info('查看文档')}
            style={{ height: 44, padding: '0 24px', fontSize: 15 }}
          >
            查看文档
          </Button>
        </Space>
      </div>

      {/* 统计卡片 */}
      <Row gutter={[24, 24]}>
        <Col xs={24} sm={12} lg={6}>
          <StatCard
            title="总任务数"
            value={statistics?.totalTasks.toLocaleString() || '0'}
            icon="mdi:clipboard-list-outline"
            iconColor="#6366f1"
            iconBg="rgba(99, 102, 241, 0.15)"
            loading={loading}
          />
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <StatCard
            title="已完成"
            value={statistics?.completedTasks.toLocaleString() || '0'}
            icon="mdi:check-circle-outline"
            iconColor="#22c55e"
            iconBg="rgba(34, 197, 94, 0.15)"
            trend={{ value: 12.5, isUp: true }}
            loading={loading}
          />
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <StatCard
            title="失败任务"
            value={statistics?.failedTasks || '0'}
            icon="mdi:alert-circle-outline"
            iconColor="#ef4444"
            iconBg="rgba(239, 68, 68, 0.15)"
            trend={{ value: 3.2, isUp: false }}
            loading={loading}
          />
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <StatCard
            title="Token消耗"
            value={statistics ? (statistics.totalTokens / 1000000).toFixed(2) : '0.00'}
            suffix="M"
            icon="mdi:lightning-bolt"
            iconColor="#f59e0b"
            iconBg="rgba(245, 158, 11, 0.15)"
            loading={loading}
          />
        </Col>
      </Row>

      {/* 图表区域 */}
      <Row gutter={[24, 24]}>
        <Col xs={24} lg={12}>
          <Card 
            title={
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <Icon icon="mdi:chart-line" style={{ color: '#818cf8', fontSize: 18 }} />
                <span style={{ fontSize: 15, fontWeight: 600, color: '#ffffff' }}>Token消耗趋势</span>
              </div>
            }
          >
            <ReactECharts option={tokenChartOption} style={{ height: 300 }} />
          </Card>
        </Col>
        <Col xs={24} lg={12}>
          <Card 
            title={
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <Icon icon="mdi:chart-pie" style={{ color: '#818cf8', fontSize: 18 }} />
                <span style={{ fontSize: 15, fontWeight: 600, color: '#ffffff' }}>任务执行分析</span>
              </div>
            }
          >
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
              <ReactECharts option={pieChartOption} style={{ height: 280 }} />
              <ReactECharts option={barChartOption} style={{ height: 280 }} />
            </div>
          </Card>
        </Col>
      </Row>

      {/* 最近任务 */}
      <Card 
        title={
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <Icon icon="mdi:history" style={{ color: '#818cf8', fontSize: 18 }} />
              <span style={{ fontSize: 15, fontWeight: 600, color: '#ffffff' }}>最近任务</span>
            </div>
            <Button type="link" onClick={() => window.location.href = '/tasks'} style={{ color: '#818cf8' }}>
              查看全部 <Icon icon="mdi:arrow-right" style={{ marginLeft: 4 }} />
            </Button>
          </div>
        }
      >
        <BaseTable
          columns={columns}
          dataSource={recentTasks}
          loading={loading}
          rowKey="id"
          pagination={false}
        />
      </Card>
    </div>
  );
}

export default Dashboard;
