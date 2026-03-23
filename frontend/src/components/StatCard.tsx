/**
 * StatCard - 统计卡片组件
 * 科技感设计，支持趋势指示器
 */
import { Icon } from '@iconify/react';

interface StatCardProps {
  title: string;
  value: string | number;
  suffix?: string;
  icon: string;
  iconColor?: string;
  iconBg?: string;
  trend?: {
    value: number;
    isUp: boolean;
  };
  description?: string;
  loading?: boolean;
  className?: string;
}

export function StatCard({
  title,
  value,
  suffix,
  icon,
  iconColor = '#6366f1',
  iconBg = 'rgba(99, 102, 241, 0.1)',
  trend,
  description,
  loading = false,
  className = '',
}: StatCardProps) {
  if (loading) {
    return (
      <div 
        className={`rounded-2xl p-6 ${className}`}
        style={{
          background: 'rgba(30, 41, 59, 0.6)',
          border: '1px solid rgba(99, 102, 241, 0.1)',
          backdropFilter: 'blur(12px)',
        }}
      >
        <div className="animate-pulse">
          <div className="h-4 bg-slate-700 rounded w-1/3 mb-4" />
          <div className="h-8 bg-slate-700 rounded w-2/3" />
        </div>
      </div>
    );
  }

  return (
    <div 
      className={`rounded-2xl p-6 transition-all duration-300 hover:translate-y-[-2px] group ${className}`}
      style={{
        background: 'rgba(30, 41, 59, 0.6)',
        border: '1px solid rgba(99, 102, 241, 0.1)',
        backdropFilter: 'blur(12px)',
      }}
    >
      {/* 顶部：图标和标题 */}
      <div className="flex items-start justify-between mb-4">
        <div>
          <p className="text-sm text-slate-400 font-medium mb-1">{title}</p>
          <div className="flex items-baseline gap-1">
            <span className="text-2xl font-bold text-white">{value}</span>
            {suffix && (
              <span className="text-sm text-slate-400">{suffix}</span>
            )}
          </div>
        </div>
        <div 
          className="w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-300 group-hover:scale-110"
          style={{ 
            background: iconBg,
            boxShadow: `0 0 20px ${iconBg}`,
          }}
        >
          <Icon 
            icon={icon} 
            className="text-2xl"
            style={{ color: iconColor }}
          />
        </div>
      </div>

      {/* 底部：趋势和描述 */}
      <div className="flex items-center gap-3">
        {trend && (
          <div 
            className="flex items-center gap-1 px-2 py-1 rounded-lg text-xs font-medium"
            style={{
              background: trend.isUp 
                ? 'rgba(16, 185, 129, 0.1)' 
                : 'rgba(239, 68, 68, 0.1)',
              color: trend.isUp ? '#10b981' : '#ef4444',
            }}
          >
            <Icon 
              icon={trend.isUp ? 'mdi:trending-up' : 'mdi:trending-down'} 
              className="text-sm"
            />
            <span>{trend.value}%</span>
          </div>
        )}
        {description && (
          <p className="text-xs text-slate-500">{description}</p>
        )}
      </div>

      {/* 装饰性光效 */}
      <div 
        className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"
        style={{
          background: `radial-gradient(circle at top right, ${iconColor}10, transparent 50%)`,
        }}
      />
    </div>
  );
}
