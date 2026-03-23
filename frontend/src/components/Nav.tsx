/**
 * Nav - 侧边导航组件
 */
import { Menu } from 'antd';
import { Icon } from '@iconify/react';
import { useNavigate, useLocation } from 'react-router-dom';

import type { MenuGroup } from '@/types/common';

interface NavProps {
  menuList: MenuGroup[];
  collapsed?: boolean;
}

export function Nav({ menuList, collapsed = false }: NavProps) {
  const navigate = useNavigate();
  const location = useLocation();

  // 获取当前选中的菜单项
  const getSelectedKey = () => {
    const path = location.pathname;
    if (path === '/') return 'dashboard';
    return path.slice(1);
  };

  // 构建菜单项
  const buildMenuItems = () => {
    const items: any[] = [];
    
    menuList.forEach((group, groupIndex) => {
      items.push({
        type: 'group',
        label: collapsed ? null : (
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            {group.name}
          </span>
        ),
        key: `group-${groupIndex}`,
        children: group.children.map((item) => {
          const key = item.link === '/' ? 'dashboard' : item.link.slice(1);
          return {
            key,
            icon: <Icon icon={item.icon} className="text-lg" />,
            label: <span className="font-medium">{item.name}</span>,
            onClick: () => navigate(item.link),
          };
        }),
      });
    });
    
    return items;
  };

  return (
    <Menu
      mode="inline"
      selectedKeys={[getSelectedKey()]}
      items={buildMenuItems()}
      style={{
        background: 'transparent',
        border: 'none',
        padding: '16px 12px',
      }}
    />
  );
}
