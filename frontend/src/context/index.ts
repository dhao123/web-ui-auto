/**
 * 全局Context
 */
import { createContext } from 'react';
import type { UserInfo, MenuGroup } from '@/types/common';

export interface ContextType {
  user?: UserInfo;
  menuList: MenuGroup[];
  routerList: string[];
}

export const defaultContextValue: ContextType = {
  user: undefined,
  menuList: [],
  routerList: ['/'],
};

export const CommonContext = createContext<ContextType>(defaultContextValue);
