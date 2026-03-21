/**
 * Nav - 侧边导航组件
 */
import { Icon } from '@iconify/react';
import { useMemo } from 'react';
import { NavLink } from 'react-router-dom';

import Logo from '@/assets/images/logo.png';
import MenuBg from '@/assets/images/menuBg.png';
import type { MenuItem, MenuGroup } from '@/types/common';

export interface NavProps {
  menuList?: MenuGroup[];
  logoLink?: string;
}

/**
 * 外部网站的打开新的tab窗口
 */
const targetType = (link?: string) => {
  return link &&
    (link.startsWith('http://') || link.startsWith('https://') || link.includes('open=true'))
    ? '_blank'
    : '_self';
};

/**
 * NavItem - 导航菜单项
 */
const NavItem = ({ icon, link, name }: MenuItem) => {
  const iconName =
    icon && !icon.includes(':') ? `mdi:${icon.replace('icon-', '')}` : (icon ?? '');

  return (
    <NavLink
      className={({ isActive }) =>
        [
          isActive ? 'active bg-[#676BEF] text-white' : '',
        ].join(' ') + ' flex items-center h-[30px] px-[10px] leading-[30px] rounded-[5px] mb-1'
      }
      target={targetType(link)}
      to={link ?? ''}>
      {iconName && <Icon className="text-[16px] w-[16px]" icon={iconName} />}
      <span className="ml-[10px]">{name}</span>
    </NavLink>
  );
};

export function Nav({ menuList = [], logoLink = '/' }: NavProps) {
  const filteredMenuList = useMemo(() => {
    return menuList.filter((item) => item.children && item.children.length > 0);
  }, [menuList]);

  return (
    <nav
      className="bg-white h-full px-[12px] overflow-y-auto bg-cover"
      style={{ backgroundImage: `url(${MenuBg})` }}>
      {/* Logo */}
      <NavLink className="h-[75px] flex items-center" to={logoLink}>
        <img alt="Logo" src={Logo} className="h-[40px]" />
      </NavLink>

      {/* 分割线 */}
      <div className="h-[1px] bg-[#D7DEF4] mb-[20px]"></div>

      {/* 固定菜单项 */}
      <div className="text-[14px] text-[#333]">
        <NavItem icon="mdi:home" link="/" name="首页" />
      </div>

      {/* 动态菜单分组 */}
      {filteredMenuList.map((group) => {
        return (
          <div key={group.name}>
            {/* 分组标题 */}
            <div className="px-[10px] mt-[26px] mb-[14px] text-[12px] text-[#9297A9]">
              {group.name}
            </div>

            {/* 菜单项 */}
            {(group.children ?? []).map((child) => {
              return (
                <div className="text-[14px] text-[#333]" key={child.name}>
                  <NavItem icon={child.icon} link={child.link} name={child.name} />
                </div>
              );
            })}
          </div>
        );
      })}
    </nav>
  );
}

export default Nav;
