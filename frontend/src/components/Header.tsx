/**
 * Header - 头部导航组件
 */
import { Icon } from '@iconify/react';
import { Dropdown } from 'antd';
import { useMemo } from 'react';
import { NavLink } from 'react-router-dom';
import type { MenuProps } from 'antd';
import type { UserInfo } from '@/types/common';

import Logo from '@/assets/images/logo.png';

export interface HeaderMenuItem {
  icon: string;
  link: string;
  title: string;
}

export type HeaderMode = 'common' | 'simple';

export interface HeaderProps {
  mode?: HeaderMode;
  user?: UserInfo;
  isLogin?: boolean;
  headerMenu?: HeaderMenuItem[];
  onLogout?: () => void;
  logoUrl?: string;
  defaultAvatarUrl?: string;
}

// 默认占位图片
const DEFAULT_AVATAR = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzYiIGhlaWdodD0iMzYiIHZpZXdCb3g9IjAgMCAzNiAzNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSIxOCIgY3k9IjE4IiByPSIxOCIgZmlsbD0iI0UwRTBFMCIvPjxjaXJjbGUgY3g9IjE4IiBjeT0iMTQiIHI9IjYiIGZpbGw9IiM5OTkiLz48cGF0aCBkPSJNNiAzMmMwLTYuNjI3IDUuMzczLTEyIDEyLTEyczEyIDUuMzczIDEyIDEyIiBmaWxsPSIjOTk5Ii8+PC9zdmc+';

export function Header({
  mode = 'common',
  user,
  isLogin = false,
  headerMenu = [
    {
      icon: 'mdi:file-document-outline',
      link: '#',
      title: '文档',
    },
  ],
  onLogout,
  logoUrl,
  defaultAvatarUrl = DEFAULT_AVATAR,
}: HeaderProps) {
  // 用户菜单项
  const dropdownItems: MenuProps['items'] = useMemo(() => {
    return [
      {
        key: '1',
        label: (
          <a
            onClick={() => {
              if (isLogin && onLogout) {
                onLogout();
              }
            }}
            rel="noopener noreferrer">
            {isLogin ? '登出' : '登录'}
          </a>
        ),
      },
    ];
  }, [isLogin, onLogout]);

  return (
    <header className="h-[90px] px-[40px] flex flex-row items-center justify-between">
      {/* 左侧：Logo */}
      <div>
        {mode === 'simple' && (
          <NavLink className="h-[75px] flex items-center" to="/">
            <img alt="Logo" src={logoUrl || Logo} className="h-[40px]" />
          </NavLink>
        )}
        {mode === 'common' && (
          <div className="text-[20px] font-bold text-[#333]">
            AI Browser Automation
          </div>
        )}
      </div>

      {/* 右侧：导航菜单 + 用户信息 */}
      <div className="flex-1 flex items-center justify-end">
        {/* 导航菜单 */}
        <div className="flex text-[14px] text-[#5F626D]">
          {headerMenu.map((item) => {
            return (
              <a
                className="mr-[40px] flex items-center hover:text-[#676BEF]"
                href={item.link}
                key={item.title}
                target="_blank"
                rel="noopener noreferrer">
                <Icon className="text-[16px]" icon={item.icon} />
                <span className="ml-[8px]">{item.title}</span>
              </a>
            );
          })}
        </div>

        {/* 用户信息 */}
        {user && (
          <>
            <div className="text-right mr-[15px]">
              <div className="text-[#333333] text-[14px] font-bold">
                {user.nickname || user.username}
              </div>
              <div className="text-[#666666] text-[12px] mt-[5px] font-normal">
                {user.username}
              </div>
            </div>

            {/* 用户头像下拉菜单 */}
            <Dropdown menu={{ items: dropdownItems }} placement="bottomRight">
              <img
                alt="User Avatar"
                className="w-[36px] h-[36px] cursor-pointer rounded-full"
                src={user.avatar || defaultAvatarUrl}
              />
            </Dropdown>
          </>
        )}
      </div>
    </header>
  );
}

export default Header;
