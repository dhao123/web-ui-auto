/**
 * TaskHistory - 任务历史页面
 * 专业级设计，无重叠问题
 */
import { useState, useEffect } from 'react';
import { Button, Input, Select, DatePicker, message, Modal, Card, Popconfirm } from 'antd';
import { Icon } from '@iconify/react';
import type { ColumnsType } from 'antd/es/table';

import { BaseTable } from '@/components';
import { useApp } from '@/context/AppContext';
import { api } from '@/utils/api';
import type { Task, TaskStatus } from '@/types/common';

const { RangePicker } = DatePicker;
const { Search } = Input;

// 状态标签映射
const statusConfig: Record<TaskStatus, { color: string; text: string; icon: string; bgColor: string }> = {
  pending: { color: '#f59e0b', text: '等待中', icon: 'mdi:clock-outline', bgColor: 'rgba(245, 158, 11, 0.15)' },
  running: { color: '#6366f1', text: '运行中', icon: 'mdi:loading', bgColor: 'rgba(99, 102, 241, 0.15)' },
  completed: { color: '#22c55e', text: '已完成', icon: 'mdi:check-circle', bgColor: 'rgba(34, 197, 94, 0.15)' },
  failed: { color: '#ef4444', text: '失败', icon: 'mdi:alert-circle', bgColor: 'rgba(239, 68, 68, 0.15)' },
  cancelled: { color: '#64748b', text: '已取消', icon: 'mdi:cancel', bgColor: 'rgba(100, 116, 139, 0.15)' },
};

const statusOptions = [
  { label: '全部状态', value: '' },
  { label: '等待中', value: 'pending' },
  { label: '运行中', value: 'running' },
  { label: '已完成', value: 'completed' },
  { label: '失败', value: 'failed' },
  { label: '已取消', value: 'cancelled' },
];

// 统计卡片组件
function StatCard({ title, value, icon, iconBg, iconColor, isSpinning = false }: { 
  title: string; value: number; icon: string; iconBg: string; iconColor: string; isSpinning?: boolean;
}) {
  return (
    <Card bodyStyle={{ padding: 20 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
        <div style={{ 
          width: 52, height: 52, borderRadius: 12,
          background: iconBg,
          display: 'flex', alignItems: 'center', justifyContent: 'center'
        }}>
          <Icon icon={icon} className={isSpinning ? 'animate-spin' : ''} style={{ fontSize: 26, color: iconColor }} />
        </div>
        <div>
          <p style={{ fontSize: 13, color: '#8b95a5', margin: '0 0 4px 0', fontWeight: 500 }}>{title}</p>
          <p style={{ fontSize: 28, fontWeight: 700, color: '#ffffff', margin: 0 }}>{value}</p>
        </div>
      </div>
    </Card>
  );
}

export function TaskHistory() {
  const { taskListVersion, refreshTaskList } = useApp();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [total, setTotal] = useState(0);
  const [searchName, setSearchName] = useState('');
  const [filterStatus, setFilterStatus] = useState('');
  const [detailModal, setDetailModal] = useState<{ visible: boolean; task?: Task }>({ visible: false });
  const [stats, setStats] = useState({ completed: 0, failed: 0, running: 0, pending: 0 });

  useEffect(() => {
    loadTasks();
  }, [page, pageSize, taskListVersion]);

  const loadTasks = async () => {
    setLoading(true);
    try {
      const res = await api.getTasks({ page, pageSize });
      if (res.code === 0 && res.data) {
        setTasks(res.data.list);
        setTotal(res.data.total);
        const completed = res.data.list.filter(t => t.status === 'completed').length;
        const failed = res.data.list.filter(t => t.status === 'failed').length;
        const running = res.data.list.filter(t => t.status === 'running').length;
        const pending = res.data.list.filter(t => t.status === 'pending').length;
        setStats({ completed, failed, running, pending });
      }
    } catch {
      message.error('加载任务列表失败');
    } finally {
      setLoading(false);
    }
  };

  const filteredTasks = tasks.filter(task => {
    const nameMatch = !searchName || task.name.toLowerCase().includes(searchName.toLowerCase());
    const statusMatch = !filterStatus || task.status === filterStatus;
    return nameMatch && statusMatch;
  });

  const handleViewDetail = (task: Task) => setDetailModal({ visible: true, task });

  const handleStopTask = async (task: Task) => {
    try {
      const res = await api.stopTask(task.id);
      if (res.code === 0) {
        message.success('任务已停止');
        refreshTaskList();
      } else {
        message.error(res.message || '停止失败');
      }
    } catch {
      message.error('网络错误');
    }
  };

  const handleRerunTask = (task: Task) => {
    message.info(`重新运行任务: ${task.name}`);
    window.location.href = `/execute?task=${encodeURIComponent(task.name)}`;
  };

  const columns: ColumnsType<Task> = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 70,
      render: (text) => <span style={{ color: '#5a6478', fontFamily: 'JetBrains Mono, monospace', fontSize: 13 }}>#{text}</span>,
    },
    {
      title: '任务名称',
      dataIndex: 'name',
      key: 'name',
      width: 240,
      ellipsis: true,
      render: (text) => <span style={{ color: '#ffffff', fontWeight: 500, fontSize: 14 }}>{text}</span>,
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 110,
      render: (status: TaskStatus) => (
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 6,
            padding: '6px 10px',
            borderRadius: 6,
            backgroundColor: statusConfig[status].bgColor,
            border: `1px solid ${statusConfig[status].color}30`,
          }}
        >
          <Icon 
            icon={statusConfig[status].icon} 
            style={{ color: statusConfig[status].color, fontSize: 14 }}
            className={status === 'running' ? 'animate-spin' : ''}
          />
          <span style={{ color: statusConfig[status].color, fontSize: 13, fontWeight: 600 }}>
            {statusConfig[status].text}
          </span>
        </div>
      ),
    },
    {
      title: '开始时间',
      dataIndex: 'startTime',
      key: 'startTime',
      width: 160,
      render: (text) => <span style={{ color: '#8b95a5', fontSize: 13 }}>{text}</span>,
    },
    {
      title: '耗时',
      dataIndex: 'duration',
      key: 'duration',
      width: 80,
      render: (duration?: number) => (
        <span style={{ color: '#b8c0cc', fontSize: 13 }}>{duration ? `${duration}s` : '-'}</span>
      ),
    },
    {
      title: 'Token消耗',
      dataIndex: 'tokenUsed',
      key: 'tokenUsed',
      width: 110,
      render: (tokens?: number) => (
        <span style={{ color: '#818cf8', fontFamily: 'JetBrains Mono, monospace', fontSize: 13 }}>
          {tokens ? tokens.toLocaleString() : '-'}
        </span>
      ),
    },
    {
      title: '操作',
      key: 'action',
      width: 160,
      render: (_, record) => (
        <div style={{ display: 'flex', gap: 4 }}>
          <Button
            type="text"
            size="small"
            icon={<Icon icon="mdi:eye-outline" />}
            onClick={() => handleViewDetail(record)}
            style={{ color: '#818cf8' }}
          >
            详情
          </Button>
          {record.status === 'running' && (
            <Popconfirm
              title="确认停止"
              description={`确定要停止任务 "${record.name}" 吗？`}
              onConfirm={() => handleStopTask(record)}
              okText="确定"
              cancelText="取消"
            >
              <Button type="text" danger size="small" icon={<Icon icon="mdi:stop-circle-outline" />}>
                停止
              </Button>
            </Popconfirm>
          )}
          {(record.status === 'failed' || record.status === 'cancelled') && (
            <Button type="text" size="small" icon={<Icon icon="mdi:refresh" />} onClick={() => handleRerunTask(record)} style={{ color: '#818cf8' }}>
              重试
            </Button>
          )}
        </div>
      ),
    },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      {/* 页面标题 */}
      <div className="page-header">
        <div className="page-header-title">
          <div className="page-header-icon">
            <Icon icon="mdi:history" />
          </div>
          <div className="page-header-text">
            <h1>任务历史</h1>
            <p>查看和管理所有执行记录</p>
          </div>
        </div>
        <Button 
          type="primary" 
          size="large"
          icon={<Icon icon="mdi:plus" />}
          onClick={() => window.location.href = '/execute'}
          style={{ height: 44, padding: '0 24px' }}
        >
          创建任务
        </Button>
      </div>

      {/* 统计卡片 */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 20 }}>
        <StatCard
          title="已完成"
          value={stats.completed}
          icon="mdi:check-circle"
          iconColor="#22c55e"
          iconBg="rgba(34, 197, 94, 0.15)"
        />
        <StatCard
          title="失败"
          value={stats.failed}
          icon="mdi:alert-circle"
          iconColor="#ef4444"
          iconBg="rgba(239, 68, 68, 0.15)"
        />
        <StatCard
          title="运行中"
          value={stats.running}
          icon="mdi:loading"
          iconColor="#6366f1"
          iconBg="rgba(99, 102, 241, 0.15)"
          isSpinning
        />
        <StatCard
          title="等待中"
          value={stats.pending}
          icon="mdi:clock-outline"
          iconColor="#f59e0b"
          iconBg="rgba(245, 158, 11, 0.15)"
        />
      </div>

      {/* 搜索和筛选 */}
      <Card bodyStyle={{ padding: 20 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, flexWrap: 'wrap' }}>
          <Search
            placeholder="搜索任务名称"
            value={searchName}
            onChange={(e) => setSearchName(e.target.value)}
            style={{ width: 260 }}
            allowClear
          />
          <Select
            placeholder="任务状态"
            value={filterStatus}
            onChange={setFilterStatus}
            options={statusOptions}
            style={{ width: 140 }}
            allowClear
          />
          <RangePicker placeholder={['开始日期', '结束日期']} style={{ width: 260 }} />
          <Button onClick={() => { setSearchName(''); setFilterStatus(''); }}>
            重置
          </Button>
        </div>
      </Card>

      {/* 任务列表 */}
      <Card bodyStyle={{ padding: 24 }}>
        <BaseTable
          columns={columns}
          dataSource={filteredTasks}
          loading={loading}
          rowKey="id"
          pagination={{
            current: page,
            pageSize,
            total,
            showSizeChanger: true,
            showTotal: (t) => `共 ${t} 条记录`,
            onChange: (p, ps) => { setPage(p); setPageSize(ps || 10); },
          }}
        />
      </Card>

      {/* 任务详情弹窗 */}
      <Modal
        title={
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <div style={{ 
              width: 32, height: 32, borderRadius: 8,
              background: 'rgba(99, 102, 241, 0.15)',
              display: 'flex', alignItems: 'center', justifyContent: 'center'
            }}>
              <Icon icon="mdi:file-document-outline" style={{ color: '#818cf8' }} />
            </div>
            <span style={{ fontSize: 16, fontWeight: 600, color: '#ffffff' }}>任务详情</span>
          </div>
        }
        open={detailModal.visible}
        onCancel={() => setDetailModal({ visible: false })}
        footer={null}
        width={700}
      >
        {detailModal.task && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 12 }}>
              <div style={{ padding: 16, background: '#0f141f', borderRadius: 8, border: '1px solid #2d3748' }}>
                <span style={{ fontSize: 12, color: '#8b95a5', display: 'block', marginBottom: 4 }}>任务ID</span>
                <span style={{ color: '#ffffff', fontFamily: 'JetBrains Mono, monospace' }}>#{detailModal.task.id}</span>
              </div>
              <div style={{ padding: 16, background: '#0f141f', borderRadius: 8, border: '1px solid #2d3748' }}>
                <span style={{ fontSize: 12, color: '#8b95a5', display: 'block', marginBottom: 4 }}>状态</span>
                <div style={{ display: 'inline-flex', alignItems: 'center', gap: 6, padding: '4px 10px', borderRadius: 6, background: statusConfig[detailModal.task.status].bgColor }}>
                  <Icon icon={statusConfig[detailModal.task.status].icon} style={{ color: statusConfig[detailModal.task.status].color, fontSize: 14 }} />
                  <span style={{ color: statusConfig[detailModal.task.status].color, fontSize: 13, fontWeight: 600 }}>
                    {statusConfig[detailModal.task.status].text}
                  </span>
                </div>
              </div>
              <div style={{ padding: 16, background: '#0f141f', borderRadius: 8, border: '1px solid #2d3748', gridColumn: 'span 2' }}>
                <span style={{ fontSize: 12, color: '#8b95a5', display: 'block', marginBottom: 4 }}>任务名称</span>
                <span style={{ color: '#ffffff', fontSize: 15 }}>{detailModal.task.name}</span>
              </div>
              <div style={{ padding: 16, background: '#0f141f', borderRadius: 8, border: '1px solid #2d3748' }}>
                <span style={{ fontSize: 12, color: '#8b95a5', display: 'block', marginBottom: 4 }}>开始时间</span>
                <span style={{ color: '#ffffff' }}>{detailModal.task.startTime}</span>
              </div>
              <div style={{ padding: 16, background: '#0f141f', borderRadius: 8, border: '1px solid #2d3748' }}>
                <span style={{ fontSize: 12, color: '#8b95a5', display: 'block', marginBottom: 4 }}>耗时</span>
                <span style={{ color: '#ffffff' }}>{detailModal.task.duration ? `${detailModal.task.duration}秒` : '-'}</span>
              </div>
              <div style={{ padding: 16, background: '#0f141f', borderRadius: 8, border: '1px solid #2d3748' }}>
                <span style={{ fontSize: 12, color: '#8b95a5', display: 'block', marginBottom: 4 }}>Token消耗</span>
                <span style={{ color: '#818cf8', fontFamily: 'JetBrains Mono, monospace' }}>{detailModal.task.tokenUsed?.toLocaleString() || '-'}</span>
              </div>
            </div>

            {detailModal.task.result && (
              <div style={{ padding: 16, background: 'rgba(34, 197, 94, 0.1)', borderRadius: 8, border: '1px solid rgba(34, 197, 94, 0.3)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 8 }}>
                  <Icon icon="mdi:check-circle" style={{ color: '#22c55e' }} />
                  <span style={{ color: '#22c55e', fontWeight: 600 }}>执行结果</span>
                </div>
                <div style={{ color: '#b8c0cc' }}>{detailModal.task.result}</div>
              </div>
            )}

            {detailModal.task.error && (
              <div style={{ padding: 16, background: 'rgba(239, 68, 68, 0.1)', borderRadius: 8, border: '1px solid rgba(239, 68, 68, 0.3)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 8 }}>
                  <Icon icon="mdi:alert-circle" style={{ color: '#ef4444' }} />
                  <span style={{ color: '#ef4444', fontWeight: 600 }}>错误信息</span>
                </div>
                <div style={{ color: '#b8c0cc' }}>{detailModal.task.error}</div>
              </div>
            )}

            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 12, paddingTop: 16, borderTop: '1px solid #2d3748' }}>
              <Button onClick={() => setDetailModal({ visible: false })}>关闭</Button>
              {(detailModal.task.status === 'failed' || detailModal.task.status === 'cancelled') && (
                <Button 
                  type="primary"
                  icon={<Icon icon="mdi:refresh" />}
                  onClick={() => { setDetailModal({ visible: false }); handleRerunTask(detailModal.task!); }}
                >
                  重新运行
                </Button>
              )}
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}

export default TaskHistory;
