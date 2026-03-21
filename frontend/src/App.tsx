/**
 * App - 应用入口
 */
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';

import { Layout } from '@/components';
import { Dashboard, AgentRun, Settings, TaskHistory } from '@/pages';
import { CommonContext, defaultContextValue } from '@/context';
import type { MenuGroup } from '@/types/common';

// 菜单配置
const menuList: MenuGroup[] = [
  {
    name: '任务管理',
    children: [
      { name: '任务执行', icon: 'mdi:robot', link: '/execute' },
      { name: '任务历史', icon: 'mdi:history', link: '/tasks' },
    ],
  },
  {
    name: '系统设置',
    children: [
      { name: '配置管理', icon: 'mdi:cog', link: '/settings' },
    ],
  },
];

// Context值
const contextValue = {
  ...defaultContextValue,
  user: {
    username: 'admin@example.com',
    nickname: '管理员',
  },
  menuList,
  routerList: ['/', '/execute', '/tasks', '/settings'],
};

// Ant Design主题配置
const antdTheme = {
  token: {
    colorPrimary: '#676BEF',
    colorLink: '#4F4FF6',
    colorSuccess: '#52c41a',
    colorError: '#F35859',
    colorWarning: '#faad14',
    borderRadius: 6,
    fontFamily: 'system-ui, Avenir, Helvetica, Arial, sans-serif',
  },
};

function App() {
  return (
    <ConfigProvider locale={zhCN} theme={antdTheme}>
      <CommonContext.Provider value={contextValue}>
        <BrowserRouter>
          <Routes>
            <Route
              path="/"
              element={
                <Layout
                  mode="common"
                  navProps={{ menuList }}
                  headerProps={{
                    user: contextValue.user,
                    isLogin: true,
                  }}
                />
              }
            >
              <Route index element={<Dashboard />} />
              <Route path="execute" element={<AgentRun />} />
              <Route path="tasks" element={<TaskHistory />} />
              <Route path="settings" element={<Settings />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </CommonContext.Provider>
    </ConfigProvider>
  );
}

export default App;
