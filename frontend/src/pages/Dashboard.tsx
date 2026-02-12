/**
 * Dashboard - 首页仪表盘
 */
import { useState } from 'react';
import { Tag, Space, Button, message } from 'antd';
import ReactECharts from 'echarts-for-react';
import { Icon } from '@iconify/react';
import type { ColumnsType } from 'antd/es/table';

import { StatCard, BaseTable } from '@/components';
import type { Task, TaskStatus, Statistics, TokenTrend, TaskAnalysis } from '@/types/common';

// 模拟数据
const mockStatistics: Statistics = {
  totalTasks: 1234,
  completedTasks: 1089,
  failedTasks: 98,
  runningTasks: 47,
  totalTokens: 2456789,
  successRate: 88.3,
};

const mockTokenTrend: TokenTrend[] = [
  { date: '02-06', tokens: 45000 },
  { date: '02-07', tokens: 52000 },
  { date: '02-08', tokens: 48000 },
  { date: '02-09', tokens: 61000 },
  { date: '02-10', tokens: 55000 },
  { date: '02-11', tokens: 67000 },
  { date: '02-12', tokens: 58000 },
];

const mockTaskAnalysis: TaskAnalysis = {
  successCount: 1089,
  failedCount: 98,
  durationDistribution: [
    { range: '0-30s', count: 320 },
    { range: '30-60s', count: 450 },
    { range: '1-5min', count: 280 },
    { range: '5-10min', count: 120 },
    { range: '>10min', count: 17 },
  ],
};

const mockTasks: Task[] = [
  { id: '1', name: '搜索GitHub项目', status: 'completed', startTime: '2026-02-12 10:30:00', duration: 45, tokenUsed: 1234 },
  { id: '2', name: '填写表单并提交', status: 'running', startTime: '2026-02-12 11:00:00', tokenUsed: 567 },
  { id: '3', name: '抓取商品信息', status: 'failed', startTime: '2026-02-12 09:15:00', duration: 120, tokenUsed: 890, error: '页面加载超时' },
  { id: '4', name: '自动登录测试', status: 'completed', startTime: '2026-02-12 08:30:00', duration: 30, tokenUsed: 456 },
  { id: '5', name: '数据导出任务', status: 'pending', startTime: '2026-02-12 11:30:00' },
];

// 状态标签映射
const statusConfig: Record<TaskStatus, { color: string; text: string }> = {
  pending: { color: 'default', text: '等待中' },
  running: { color: 'processing', text: '运行中' },
  completed: { color: 'success', text: '已完成' },
  failed: { color: 'error', text: '失败' },
  cancelled: { color: 'warning', text: '已取消' },
};

export function Dashboard() {
  const [statistics] = useState<Statistics>(mockStatistics);
  const [tokenTrend] = useState<TokenTrend[]>(mockTokenTrend);
  const [taskAnalysis] = useState<TaskAnalysis>(mockTaskAnalysis);
  const [tasks] = useState<Task[]>(mockTasks);
  const [loading] = useState(false);

  // Token趋势图表配置
  const tokenChartOption = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#E6E9FD',
      borderWidth: 1,
      textStyle: { color: '#333' },
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '10%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: tokenTrend.map(item => item.date),
      axisLine: { lineStyle: { color: '#E6E9FD' } },
      axisLabel: { color: '#9297A9' },
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      splitLine: { lineStyle: { color: '#F0F0F0' } },
      axisLabel: { color: '#9297A9' },
    },
    series: [{
      data: tokenTrend.map(item => item.tokens),
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 8,
      lineStyle: { color: '#676BEF', width: 3 },
      itemStyle: { color: '#676BEF' },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(103, 107, 239, 0.3)' },
            { offset: 1, color: 'rgba(103, 107, 239, 0.05)' },
          ],
        },
      },
    }],
  };

  // 任务成功率饼图配置
  const pieChartOption = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#E6E9FD',
      borderWidth: 1,
      textStyle: { color: '#333' },
    },
    legend: {
      orient: 'vertical',
      right: '5%',
      top: 'center',
      textStyle: { color: '#666' },
    },
    series: [{
      type: 'pie',
      radius: ['55%', '75%'],
      center: ['35%', '50%'],
      avoidLabelOverlap: false,
      label: {
        show: true,
        position: 'center',
        formatter: () => `${statistics.successRate}%\n成功率`,
        fontSize: 16,
        fontWeight: 'bold',
        color: '#333',
      },
      data: [
        { value: taskAnalysis.successCount, name: '成功', itemStyle: { color: '#52c41a' } },
        { value: taskAnalysis.failedCount, name: '失败', itemStyle: { color: '#F35859' } },
      ],
    }],
  };

  // 任务耗时分布柱状图
  const barChartOption = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#E6E9FD',
      borderWidth: 1,
      textStyle: { color: '#333' },
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '10%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: taskAnalysis.durationDistribution.map(item => item.range),
      axisLine: { lineStyle: { color: '#E6E9FD' } },
      axisLabel: { color: '#9297A9' },
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      splitLine: { lineStyle: { color: '#F0F0F0' } },
      axisLabel: { color: '#9297A9' },
    },
    series: [{
      data: taskAnalysis.durationDistribution.map(item => item.count),
      type: 'bar',
      barWidth: '50%',
      itemStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: '#676BEF' },
            { offset: 1, color: '#9D34FE' },
          ],
        },
        borderRadius: [4, 4, 0, 0],
      },
    }],
  };

  // 任务表格列配置
  const columns: ColumnsType<Task> = [
    {
      title: '任务名称',
      dataIndex: 'name',
      key: 'name',
      width: 200,
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status: TaskStatus) => (
        <Tag color={statusConfig[status].color}>{statusConfig[status].text}</Tag>
      ),
    },
    {
      title: '开始时间',
      dataIndex: 'startTime',
      key: 'startTime',
      width: 180,
    },
    {
      title: '耗时(秒)',
      dataIndex: 'duration',
      key: 'duration',
      width: 100,
      render: (duration?: number) => duration ? `${duration}s` : '-',
    },
    {
      title: 'Token消耗',
      dataIndex: 'tokenUsed',
      key: 'tokenUsed',
      width: 120,
      render: (tokens?: number) => tokens ? tokens.toLocaleString() : '-',
    },
    {
      title: '操作',
      key: 'action',
      width: 150,
      render: (_, record) => (
        <Space size="middle">
          <a onClick={() => message.info(`查看任务: ${record.name}`)}>详情</a>
          {record.status === 'running' && (
            <a className="text-red-500" onClick={() => message.warning(`停止任务: ${record.name}`)}>停止</a>
          )}
        </Space>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      {/* 欢迎区域 */}
      <div className="bg-gradient-to-r from-[#3462FE] to-[#9D34FE] rounded-[12px] p-8 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-[28px] font-bold mb-2">AI Browser Automation</h1>
            <p className="text-[16px] opacity-90">智能浏览器自动化平台，让AI帮你完成复杂的网页操作任务</p>
          </div>
          <Button 
            type="primary" 
            size="large"
            className="bg-white text-[#676BEF] border-none hover:bg-gray-100"
            icon={<Icon icon="mdi:plus" />}
          >
            创建新任务
          </Button>
        </div>
      </div>

      {/* 统计卡片 */}
      <div className="grid grid-cols-4 gap-6">
        <StatCard
          title="总任务数"
          value={statistics.totalTasks.toLocaleString()}
          icon="mdi:clipboard-list-outline"
          iconColor="#676BEF"
          iconBg="#E6E9FD"
        />
        <StatCard
          title="已完成"
          value={statistics.completedTasks.toLocaleString()}
          icon="mdi:check-circle-outline"
          iconColor="#52c41a"
          iconBg="#f6ffed"
          trend={{ value: 12.5, isUp: true }}
        />
        <StatCard
          title="失败任务"
          value={statistics.failedTasks}
          icon="mdi:alert-circle-outline"
          iconColor="#F35859"
          iconBg="#fff2f0"
          trend={{ value: 3.2, isUp: false }}
        />
        <StatCard
          title="Token消耗"
          value={(statistics.totalTokens / 1000000).toFixed(2)}
          suffix="M"
          icon="mdi:currency-usd"
          iconColor="#faad14"
          iconBg="#fffbe6"
        />
      </div>

      {/* 图表区域 */}
      <div className="grid grid-cols-2 gap-6">
        {/* Token趋势 */}
        <div className="bg-white rounded-[8px] p-6 card-shadow">
          <h3 className="text-[16px] font-bold text-[#333] mb-4">
            <Icon icon="mdi:chart-line" className="inline mr-2 text-[#676BEF]" />
            Token消耗趋势
          </h3>
          <ReactECharts option={tokenChartOption} style={{ height: '280px' }} />
        </div>

        {/* 任务分析 */}
        <div className="bg-white rounded-[8px] p-6 card-shadow">
          <h3 className="text-[16px] font-bold text-[#333] mb-4">
            <Icon icon="mdi:chart-pie" className="inline mr-2 text-[#676BEF]" />
            任务执行分析
          </h3>
          <div className="grid grid-cols-2 gap-4">
            <ReactECharts option={pieChartOption} style={{ height: '250px' }} />
            <ReactECharts option={barChartOption} style={{ height: '250px' }} />
          </div>
        </div>
      </div>

      {/* 最近任务 */}
      <div className="bg-white rounded-[8px] p-6 card-shadow">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-[16px] font-bold text-[#333]">
            <Icon icon="mdi:history" className="inline mr-2 text-[#676BEF]" />
            最近任务
          </h3>
          <Button type="link" className="text-[#676BEF]">
            查看全部 <Icon icon="mdi:arrow-right" className="inline ml-1" />
          </Button>
        </div>
        <BaseTable
          columns={columns}
          dataSource={tasks}
          loading={loading}
          rowKey="id"
          pagination={false}
        />
      </div>
    </div>
  );
}

export default Dashboard;
