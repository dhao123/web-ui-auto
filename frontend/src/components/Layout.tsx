/**
 * Layout - 布局组件
 */
import type { ReactNode } from 'react';
import { Outlet } from 'react-router-dom';

import Header, { type HeaderProps } from './Header';
import Nav, { type NavProps } from './Nav';

import headerBg from '@/assets/images/headerBg.png';

export interface LayoutProps {
  children?: ReactNode;
  mode?: 'common' | 'simple';
  navProps?: NavProps;
  headerProps?: HeaderProps;
  useOutlet?: boolean;
}

/**
 * CommonLayout - 完整布局
 */
export function CommonLayout({
  children,
  navProps,
  headerProps,
  useOutlet = true,
}: Omit<LayoutProps, 'mode'>) {
  return (
    <div className="h-[100vh] flex">
      {/* 左侧导航 - 固定宽度 */}
      <div className="w-[180px] shrink-0">
        <Nav {...navProps} />
      </div>

      {/* 右侧内容区 - 自适应 */}
      <div 
        className="flex-1 w-full overflow-y-hidden overflow-x-auto min-w-[1080px] bg-[#F1F3FA] bg-no-repeat bg-contain"
        style={{ backgroundImage: `url(${headerBg})` }}
      >
        <Header mode="common" {...headerProps} />
        <div className="w-full px-[40px] pb-[20px] h-[calc(100vh-90px)] max-h-[calc(100vh-90px)]">
          <div className="h-full overflow-y-auto">
            {useOutlet ? <Outlet /> : children}
          </div>
        </div>
      </div>
    </div>
  );
}

/**
 * SimpleLayout - 简化布局
 */
export function SimpleLayout({
  children,
  headerProps,
  useOutlet = true,
}: Omit<LayoutProps, 'mode' | 'navProps'>) {
  return (
    <div 
      className="h-[100vh] overflow-y-hidden overflow-x-auto min-w-[1080px] bg-[#F1F3FA] bg-no-repeat bg-contain"
      style={{ backgroundImage: `url(${headerBg})` }}
    >
      <Header mode="simple" {...headerProps} />
      <div className="w-full px-[40px] pb-[20px] h-[calc(100vh-90px)] max-h-[calc(100vh-90px)]">
        <div className="h-full overflow-y-auto">
          {useOutlet ? <Outlet /> : children}
        </div>
      </div>
    </div>
  );
}

/**
 * Layout - 自动布局组件
 */
export function Layout({ mode = 'common', ...props }: LayoutProps) {
  if (mode === 'simple') {
    return <SimpleLayout {...props} />;
  }
  return <CommonLayout {...props} />;
}

export default Layout;
