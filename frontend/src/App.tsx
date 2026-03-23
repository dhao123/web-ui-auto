/**
 * App - AI Browser Automation Platform
 * 科技感、现代化、专业级设计
 */
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider, theme } from 'antd';
import zhCN from 'antd/locale/zh_CN';

import { Layout } from '@/components/Layout';
import { 
  Dashboard, 
  AgentRun, 
  Settings, 
  TaskHistory,
  DeepResearch,
  ConfigTemplates,
  ZKHConfig 
} from '@/pages';
import { AppProvider } from '@/context/AppContext';
import type { MenuGroup } from '@/types/common';

// 菜单配置 - 与V1功能对应
const menuList: MenuGroup[] = [
  {
    name: '任务中心',
    icon: 'mdi:rocket-launch',
    children: [
      { name: '仪表盘', icon: 'mdi:view-dashboard', link: '/' },
      { name: '执行任务', icon: 'mdi:play-circle', link: '/execute' },
      { name: '深度研究', icon: 'mdi:brain', link: '/research' },
      { name: '任务历史', icon: 'mdi:history', link: '/tasks' },
    ],
  },
  {
    name: '配置管理',
    icon: 'mdi:cog',
    children: [
      { name: '系统配置', icon: 'mdi:tune', link: '/settings' },
      { name: '配置模板', icon: 'mdi:content-save', link: '/templates' },
      { name: '震坤行MCP', icon: 'mdi:store', link: '/zkh' },
    ],
  },
];

// Ant Design 深色科技主题配置
const antdTheme = {
  algorithm: theme.darkAlgorithm,
  token: {
    colorPrimary: '#6366f1',
    colorPrimaryHover: '#818cf8',
    colorPrimaryActive: '#4f46e5',
    colorSuccess: '#10b981',
    colorWarning: '#f59e0b',
    colorError: '#ef4444',
    colorInfo: '#06b6d4',
    colorBgBase: '#0f172a',
    colorBgContainer: '#1e293b',
    colorBgElevated: '#334155',
    colorText: '#f8fafc',
    colorTextSecondary: '#cbd5e1',
    colorTextTertiary: '#94a3b8',
    colorBorder: 'rgba(148, 163, 184, 0.2)',
    borderRadius: 10,
    borderRadiusLG: 16,
    fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
    fontSize: 14,
    controlHeight: 40,
  },
  components: {
    Layout: {
      siderBg: '#1e293b',
      headerBg: '#0f172a',
      bodyBg: '#0f172a',
    },
    Menu: {
      itemBg: 'transparent',
      itemSelectedBg: 'rgba(99, 102, 241, 0.15)',
      itemHoverBg: 'rgba(148, 163, 184, 0.1)',
      itemColor: '#94a3b8',
      itemSelectedColor: '#818cf8',
      itemHoverColor: '#cbd5e1',
    },
    Card: {
      colorBgContainer: 'rgba(30, 41, 59, 0.8)',
      colorBorderSecondary: 'rgba(148, 163, 184, 0.2)',
    },
    Table: {
      colorBgContainer: 'transparent',
      headerBg: '#1e293b',
      headerColor: '#cbd5e1',
      rowHoverBg: 'rgba(51, 65, 85, 0.5)',
    },
    Button: {
      primaryShadow: '0 0 20px rgba(99, 102, 241, 0.3)',
    },
  },
};

function App() {
  return (
    <ConfigProvider locale={zhCN} theme={antdTheme}>
      <AppProvider menuList={menuList}>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Layout />}>
              <Route index element={<Dashboard />} />
              <Route path="execute" element={<AgentRun />} />
              <Route path="research" element={<DeepResearch />} />
              <Route path="tasks" element={<TaskHistory />} />
              <Route path="settings" element={<Settings />} />
              <Route path="templates" element={<ConfigTemplates />} />
              <Route path="zkh" element={<ZKHConfig />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </AppProvider>
    </ConfigProvider>
  );
}

export default App;
