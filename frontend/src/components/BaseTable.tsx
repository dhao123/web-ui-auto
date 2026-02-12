/**
 * BaseTable - 统一表格组件
 */
import { Table, Spin } from 'antd';
import type { TableProps } from 'antd';
import { Icon } from '@iconify/react';

export interface BaseTableProps<T> extends TableProps<T> {
  xScroll?: string | number;
}

// 自定义加载指示器
const spinIndicator = (
  <Icon icon="eos-icons:loading" className="text-[24px] text-[#676BEF] animate-spin" />
);

export function BaseTable<T extends object>({
  columns,
  loading,
  pagination,
  xScroll = 'max-content',
  ...props
}: BaseTableProps<T>) {
  // 处理列配置
  const processedColumns = columns?.map((col) => ({
    ...col,
    align: col.align || 'center' as const,
    ellipsis: col.ellipsis !== false,
  }));

  // 处理分页配置
  const processedPagination = pagination === false ? false : {
    showQuickJumper: true,
    showSizeChanger: true,
    showTotal: (total: number) => `共 ${total} 条`,
    ...pagination,
  };

  return (
    <Spin spinning={!!loading} indicator={spinIndicator}>
      <Table
        columns={processedColumns}
        pagination={processedPagination}
        scroll={{ x: xScroll }}
        size="large"
        bordered={false}
        {...props}
      />
    </Spin>
  );
}

export default BaseTable;
