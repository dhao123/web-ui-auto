/**
 * TaskHistory - 任务历史页面
 */
import { useState } from 'react';
import { Tag, Space, Button, Input, Select, DatePicker, message, Modal } from 'antd';
import { Icon } from '@iconify/react';
import type { ColumnsType } from 'antd/es/table';

import { BaseTable } from '@/components';
import type { Task, TaskStatus } from '@/types/common';

const { RangePicker } = DatePicker;

// 模拟更多任务数据
const mockTasks: Task[] = Array.from({ length: 50 }, (_, i) => ({
  id: `${i + 1}`,
  name: `任务 ${i + 1} - ${['搜索GitHub项目', '填写表单', '抓取数据', '自动登录', '导出报告'][i % 5]}`,
  status: ['completed', 'failed', 'running', 'pending', 'cancelled'][i % 5] as TaskStatus,
  startTime: `2026-02-${String(12 - (i % 7)).padStart(2, '0')} ${String(10 + (i % 12)).padStart(2, '0')}:${String(i % 60).padStart(2, '0')}:00`,
  duration: i % 5 === 1 ? undefined : Math.floor(Math.random() * 300) + 10,
  tokenUsed: Math.floor(Math.random() * 5000) + 100,
  error: i % 5 === 1 ? '执行超时' : undefined,
  result: i % 5 === 0 ? '任务执行成功，已获取数据' : undefined,
}));

// 状态标签映射
const statusConfig: Record<TaskStatus, { color: string; text: string }> = {
  pending: { color: 'default', text: '等待中' },
  running: { color: 'processing', text: '运行中' },
  completed: { color: 'success', text: '已完成' },
  failed: { color: 'error', text: '失败' },
  cancelled: { color: 'warning', text: '已取消' },
};

// 状态选项
const statusOptions = [
  { label: '全部状态', value: '' },
  { label: '等待中', value: 'pending' },
  { label: '运行中', value: 'running' },
  { label: '已完成', value: 'completed' },
  { label: '失败', value: 'failed' },
  { label: '已取消', value: 'cancelled' },
];

export function TaskHistory() {
  const [tasks, setTasks] = useState<Task[]>(mockTasks);
  const [loading] = useState(false);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [searchName, setSearchName] = useState('');
  const [filterStatus, setFilterStatus] = useState('');
  const [detailModal, setDetailModal] = useState<{ visible: boolean; task?: Task }>({ visible: false });

  // 过滤数据
  const filteredTasks = tasks.filter(task => {
    const nameMatch = !searchName || task.name.toLowerCase().includes(searchName.toLowerCase());
    const statusMatch = !filterStatus || task.status === filterStatus;
    return nameMatch && statusMatch;
  });

  // 分页数据
  const paginatedTasks = filteredTasks.slice((page - 1) * pageSize, page * pageSize);

  // 查看详情
  const handleViewDetail = (task: Task) => {
    setDetailModal({ visible: true, task });
  };

  // 停止任务
  const handleStopTask = (task: Task) => {
    Modal.confirm({
      title: '确认停止',
      content: `确定要停止任务 "${task.name}" 吗？`,
      okText: '确定',
      cancelText: '取消',
      onOk: () => {
        message.success('任务已停止');
        // 更新任务状态
        setTasks(prev => prev.map(t => 
          t.id === task.id ? { ...t, status: 'cancelled' as TaskStatus } : t
        ));
      },
    });
  };

  // 重新运行
  const handleRerunTask = (task: Task) => {
    message.info(`重新运行任务: ${task.name}`);
  };

  // 表格列配置
  const columns: ColumnsType<Task> = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: '任务名称',
      dataIndex: 'name',
      key: 'name',
      width: 250,
      ellipsis: true,
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
      title: '耗时',
      dataIndex: 'duration',
      key: 'duration',
      width: 100,
      render: (duration?: number) => {
        if (!duration) return '-';
        if (duration < 60) return `${duration}秒`;
        return `${Math.floor(duration / 60)}分${duration % 60}秒`;
      },
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
      width: 180,
      render: (_, record) => (
        <Space size="middle">
          <a onClick={() => handleViewDetail(record)}>详情</a>
          {record.status === 'running' && (
            <a className="text-red-500" onClick={() => handleStopTask(record)}>停止</a>
          )}
          {(record.status === 'failed' || record.status === 'cancelled') && (
            <a onClick={() => handleRerunTask(record)}>重试</a>
          )}
        </Space>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      {/* 页面标题 */}
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <Icon icon="mdi:history" className="text-[24px] text-[#676BEF] mr-3" />
          <h1 className="text-[20px] font-bold text-[#333]">任务历史</h1>
        </div>
        <Button 
          type="primary" 
          icon={<Icon icon="mdi:plus" />}
          onClick={() => message.info('创建新任务')}
        >
          创建任务
        </Button>
      </div>

      {/* 搜索和筛选 */}
      <div className="bg-white rounded-[8px] p-4 card-shadow">
        <div className="flex items-center gap-4 flex-wrap">
          <Input
            placeholder="搜索任务名称"
            prefix={<Icon icon="mdi:magnify" className="text-[#9297A9]" />}
            value={searchName}
            onChange={(e) => setSearchName(e.target.value)}
            className="w-[240px]"
            allowClear
          />
          <Select
            placeholder="任务状态"
            value={filterStatus}
            onChange={setFilterStatus}
            options={statusOptions}
            className="w-[150px]"
          />
          <RangePicker 
            placeholder={['开始日期', '结束日期']}
            className="w-[280px]"
          />
          <Button onClick={() => {
            setSearchName('');
            setFilterStatus('');
          }}>
            重置
          </Button>
        </div>
      </div>

      {/* 任务列表 */}
      <div className="bg-white rounded-[8px] p-6 card-shadow">
        <BaseTable
          columns={columns}
          dataSource={paginatedTasks}
          loading={loading}
          rowKey="id"
          pagination={{
            current: page,
            pageSize,
            total: filteredTasks.length,
            onChange: (newPage, newPageSize) => {
              setPage(newPage);
              setPageSize(newPageSize);
            },
          }}
        />
      </div>

      {/* 任务详情弹窗 */}
      <Modal
        title={
          <div className="flex items-center">
            <Icon icon="mdi:file-document-outline" className="mr-2 text-[#676BEF]" />
            任务详情
          </div>
        }
        open={detailModal.visible}
        onCancel={() => setDetailModal({ visible: false })}
        footer={null}
        width={600}
      >
        {detailModal.task && (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <span className="text-[#9297A9]">任务ID：</span>
                <span className="text-[#333]">{detailModal.task.id}</span>
              </div>
              <div>
                <span className="text-[#9297A9]">状态：</span>
                <Tag color={statusConfig[detailModal.task.status].color}>
                  {statusConfig[detailModal.task.status].text}
                </Tag>
              </div>
              <div className="col-span-2">
                <span className="text-[#9297A9]">任务名称：</span>
                <span className="text-[#333]">{detailModal.task.name}</span>
              </div>
              <div>
                <span className="text-[#9297A9]">开始时间：</span>
                <span className="text-[#333]">{detailModal.task.startTime}</span>
              </div>
              <div>
                <span className="text-[#9297A9]">耗时：</span>
                <span className="text-[#333]">
                  {detailModal.task.duration ? `${detailModal.task.duration}秒` : '-'}
                </span>
              </div>
              <div>
                <span className="text-[#9297A9]">Token消耗：</span>
                <span className="text-[#333]">
                  {detailModal.task.tokenUsed?.toLocaleString() || '-'}
                </span>
              </div>
            </div>
            {detailModal.task.result && (
              <div className="bg-[#f6ffed] p-4 rounded-lg border border-[#b7eb8f]">
                <div className="text-[12px] text-[#52c41a] mb-1">执行结果</div>
                <div className="text-[#333]">{detailModal.task.result}</div>
              </div>
            )}
            {detailModal.task.error && (
              <div className="bg-[#fff2f0] p-4 rounded-lg border border-[#ffccc7]">
                <div className="text-[12px] text-[#F35859] mb-1">错误信息</div>
                <div className="text-[#333]">{detailModal.task.error}</div>
              </div>
            )}
          </div>
        )}
      </Modal>
    </div>
  );
}

export default TaskHistory;
