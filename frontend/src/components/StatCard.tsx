/**
 * StatCard - 统计卡片组件
 */
import { Icon } from '@iconify/react';

export interface StatCardProps {
  title: string;
  value: number | string;
  icon: string;
  iconColor?: string;
  iconBg?: string;
  trend?: {
    value: number;
    isUp: boolean;
  };
  suffix?: string;
}

export function StatCard({
  title,
  value,
  icon,
  iconColor = '#676BEF',
  iconBg = '#E6E9FD',
  trend,
  suffix,
}: StatCardProps) {
  return (
    <div className="bg-white rounded-[8px] p-6 card-shadow hover:shadow-lg transition-shadow duration-300">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <div className="text-[14px] text-[#9297A9] mb-2">{title}</div>
          <div className="flex items-baseline">
            <span className="text-[28px] font-bold text-[#333]">{value}</span>
            {suffix && <span className="text-[14px] text-[#666] ml-1">{suffix}</span>}
          </div>
          {trend && (
            <div className={`flex items-center mt-2 text-[12px] ${trend.isUp ? 'text-[#52c41a]' : 'text-[#F35859]'}`}>
              <Icon 
                icon={trend.isUp ? 'mdi:arrow-up' : 'mdi:arrow-down'} 
                className="mr-1"
              />
              <span>{trend.value}%</span>
              <span className="text-[#999] ml-1">较上周</span>
            </div>
          )}
        </div>
        <div 
          className="w-[48px] h-[48px] rounded-[12px] flex items-center justify-center"
          style={{ backgroundColor: iconBg }}
        >
          <Icon icon={icon} className="text-[24px]" style={{ color: iconColor }} />
        </div>
      </div>
    </div>
  );
}

export default StatCard;
