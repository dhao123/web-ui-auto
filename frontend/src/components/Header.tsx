/**
 * Header - 顶部导航组件
 */
import { Avatar, Dropdown } from 'antd';
import { Icon } from '@iconify/react';

interface HeaderProps {
  user?: {
    username: string;
    nickname: string;
    avatar?: string;
  };
  isLogin?: boolean;
}

export function Header({ user, isLogin = false }: HeaderProps) {
  const userMenuItems = [
    {
      key: 'profile',
      icon: <Icon icon="mdi:account" />,
      label: '个人资料',
    },
    {
      key: 'settings',
      icon: <Icon icon="mdi:cog" />,
      label: '系统设置',
    },
    {
      type: 'divider' as const,
    },
    {
      key: 'logout',
      icon: <Icon icon="mdi:logout" />,
      label: '退出登录',
      danger: true,
    },
  ];

  return (
    <header 
      className="h-16 px-6 flex items-center justify-between"
      style={{
        background: 'rgba(15, 23, 42, 0.8)',
        backdropFilter: 'blur(12px)',
        borderBottom: '1px solid rgba(99, 102, 241, 0.1)',
      }}
    >
      {/* 左侧 - 面包屑/标题 */}
      <div className="flex items-center gap-4">
        <h2 className="text-lg font-semibold text-white">AI Browser Automation</h2>
      </div>

      {/* 右侧 - 操作区 */}
      <div className="flex items-center gap-4">
        {/* 通知 */}
        <button className="w-10 h-10 rounded-lg flex items-center justify-center transition-all duration-300 hover:bg-white/5 relative">
          <Icon icon="mdi:bell-outline" className="text-xl text-slate-400" />
          <span className="absolute top-2 right-2 w-2 h-2 rounded-full bg-rose-500 animate-pulse" />
        </button>

        {/* 帮助 */}
        <button className="w-10 h-10 rounded-lg flex items-center justify-center transition-all duration-300 hover:bg-white/5">
          <Icon icon="mdi:help-circle-outline" className="text-xl text-slate-400" />
        </button>

        {/* 用户菜单 */}
        {isLogin && user && (
          <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
            <div className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer transition-all duration-300 hover:bg-white/5">
              <Avatar 
                size={36}
                src={user.avatar}
                icon={!user.avatar && <Icon icon="mdi:account" />}
                style={{ 
                  background: 'linear-gradient(135deg, #6366f1 0%, #a855f7 100%)',
                }}
              />
              <div className="hidden md:block">
                <p className="text-sm font-medium text-white leading-tight">{user.nickname}</p>
                <p className="text-xs text-slate-400">{user.username}</p>
              </div>
              <Icon icon="mdi:chevron-down" className="text-slate-400" />
            </div>
          </Dropdown>
        )}
      </div>
    </header>
  );
}
