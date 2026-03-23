/**
 * BaseTable - 基础表格组件
 * 科技感表格样式
 */
import { Table } from 'antd';
import type { TableProps } from 'antd/es/table';

interface BaseTableProps<T> extends TableProps<T> {
  className?: string;
}

export function BaseTable<T extends object>({ 
  className = '',
  ...props 
}: BaseTableProps<T>) {
  return (
    <Table
      {...props}
      className={`base-table ${className}`}
      pagination={
        props.pagination === false
          ? false
          : {
              showSizeChanger: true,
              showQuickJumper: true,
              showTotal: (total) => `共 ${total} 条`,
              ...props.pagination,
            }
      }
    />
  );
}
