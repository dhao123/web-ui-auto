/**
 * Layout - 主布局组件
 * 专业级设计系统
 */
import { useState } from 'react';
import { Layout as AntLayout, Menu, Badge, Avatar, Dropdown } from 'antd';
import { Outlet, useLocation, useNavigate } from 'react-router-dom';
import { Icon } from '@iconify/react';

import { useApp } from '@/context/AppContext';

const { Sider, Header, Content } = AntLayout;

const userMenuItems = [
  { key: 'profile', icon: <Icon icon="mdi:account" style={{ fontSize: 16 }} />, label: '个人资料' },
  { key: 'settings', icon: <Icon icon="mdi:cog" style={{ fontSize: 16 }} />, label: '系统设置' },
  { type: 'divider' as const },
  { key: 'logout', icon: <Icon icon="mdi:logout" style={{ fontSize: 16 }} />, label: '退出登录', danger: true },
];

export function Layout() {
  const [collapsed, setCollapsed] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const { menuList, taskStatus } = useApp();

  const getSelectedKey = () => {
    const path = location.pathname;
    if (path === '/') return 'dashboard';
    return path.slice(1);
  };

  const buildMenuItems = () => {
    const items: any[] = [];
    menuList.forEach((group, groupIndex) => {
      items.push({
        type: 'group',
        label: collapsed ? null : (
          <span style={{ fontSize: 11, fontWeight: 600, color: '#5a6478', textTransform: 'uppercase', letterSpacing: 0.5 }}>
            {group.name}
          </span>
        ),
        key: `group-${groupIndex}`,
        children: group.children.map((item) => {
          const key = item.link === '/' ? 'dashboard' : item.link.slice(1);
          return {
            key,
            icon: <Icon icon={item.icon} style={{ fontSize: 20 }} />,
            label: <span style={{ fontWeight: 500, fontSize: 14 }}>{item.name}</span>,
            onClick: () => navigate(item.link),
          };
        }),
      });
    });
    return items;
  };

  return (
    <AntLayout style={{ minHeight: '100vh', background: '#0b0f19' }}>
      {/* 侧边栏 */}
      <Sider
        trigger={null}
        collapsible
        collapsed={collapsed}
        width={260}
        collapsedWidth={80}
        style={{
          background: '#151b2b',
          borderRight: '1px solid #2d3748',
        }}
      >
        {/* Logo区域 */}
        <div 
          style={{ 
            height: 72, display: 'flex', alignItems: 'center', justifyContent: 'center',
            borderBottom: '1px solid #2d3748', padding: '0 16px'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <div 
              style={{
                width: 42, height: 42, borderRadius: 10,
                background: 'linear-gradient(135deg, #6366f1 0%, #a855f7 100%)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                boxShadow: '0 0 20px rgba(99, 102, 241, 0.3)',
              }}
            >
              <Icon icon="mdi:robot" style={{ fontSize: 22, color: '#ffffff' }} />
            </div>
            {!collapsed && (
              <div>
                <h1 style={{ fontSize: 16, fontWeight: 700, color: '#ffffff', margin: 0, lineHeight: 1.3 }}>
                  AI Browser
                </h1>
                <p style={{ fontSize: 11, color: '#8b95a5', margin: 0 }}>Automation Platform</p>
              </div>
            )}
          </div>
        </div>

        {/* 菜单 */}
        <Menu
          mode="inline"
          selectedKeys={[getSelectedKey()]}
          items={buildMenuItems()}
          style={{
            background: 'transparent',
            border: 'none',
            padding: '12px',
          }}
        />

        {/* 折叠按钮 */}
        <div style={{ position: 'absolute', bottom: 16, left: 12, right: 12 }}>
          <button
            onClick={() => setCollapsed(!collapsed)}
            style={{
              width: '100%', height: 40, borderRadius: 8,
              border: '1px solid #2d3748', background: 'transparent',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              cursor: 'pointer', transition: 'all 0.2s',
            }}
            onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(99, 102, 241, 0.1)'}
            onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
          >
            <Icon 
              icon={collapsed ? 'mdi:chevron-right' : 'mdi:chevron-left'} 
              style={{ fontSize: 20, color: '#8b95a5' }}
            />
          </button>
        </div>
      </Sider>

      <AntLayout style={{ background: '#0b0f19' }}>
        {/* 顶部导航 */}
        <Header 
          style={{
            display: 'flex', alignItems: 'center', justifyContent: 'space-between',
            padding: '0 24px', height: 72,
            background: '#0b0f19',
            borderBottom: '1px solid #2d3748',
          }}
        >
          {/* 左侧 - 页面标题 */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
            <h2 style={{ fontSize: 18, fontWeight: 600, color: '#ffffff', margin: 0 }}>
              {menuList.flatMap(g => g.children).find(item => item.link === location.pathname)?.name || '仪表盘'}
            </h2>
            {taskStatus === 'running' && (
              <Badge 
                status="processing" 
                text={<span style={{ color: '#22c55e', fontSize: 13 }}>任务运行中</span>}
              />
            )}
          </div>

          {/* 右侧 - 操作区 */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            {/* 通知 */}
            <button style={{
              width: 40, height: 40, borderRadius: 8, border: 'none', background: 'transparent',
              display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer',
              position: 'relative',
            }}>
              <Icon icon="mdi:bell-outline" style={{ fontSize: 20, color: '#8b95a5' }} />
              <span style={{
                position: 'absolute', top: 8, right: 8, width: 8, height: 8, borderRadius: '50%',
                background: '#ef4444'
              }} />
            </button>

            {/* 帮助 */}
            <button style={{
              width: 40, height: 40, borderRadius: 8, border: 'none', background: 'transparent',
              display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer',
            }}>
              <Icon icon="mdi:help-circle-outline" style={{ fontSize: 20, color: '#8b95a5' }} />
            </button>

            {/* 用户菜单 */}
            <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
              <div style={{
                display: 'flex', alignItems: 'center', gap: 10, padding: '6px 12px',
                borderRadius: 8, cursor: 'pointer', border: '1px solid #2d3748',
              }}>
                <Avatar 
                  size={32}
                  icon={<Icon icon="mdi:account" />}
                  style={{ background: 'linear-gradient(135deg, #6366f1 0%, #a855f7 100%)' }}
                />
                <div style={{ display: collapsed ? 'none' : 'block' }}>
                  <p style={{ fontSize: 13, fontWeight: 500, color: '#ffffff', margin: 0, lineHeight: 1.3 }}>管理员</p>
                  <p style={{ fontSize: 11, color: '#8b95a5', margin: 0 }}>admin@zkh.com</p>
                </div>
                <Icon icon="mdi:chevron-down" style={{ color: '#8b95a5', fontSize: 16 }} />
              </div>
            </Dropdown>
          </div>
        </Header>

        {/* 主内容区 */}
        <Content style={{ padding: 24, overflow: 'auto', background: '#0b0f19' }}>
          <Outlet />
        </Content>
      </AntLayout>
    </AntLayout>
  );
}
