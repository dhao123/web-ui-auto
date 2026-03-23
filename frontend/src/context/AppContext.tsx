/**
 * AppContext - 全局应用状态管理
 */
import { createContext, useContext, useState, useCallback, type ReactNode } from 'react';
import type { MenuGroup, AgentConfig, BrowserConfig, LLMConfig } from '@/types/common';

// =============================================================================
// Types
// =============================================================================

interface AppState {
  // 全局加载状态
  globalLoading: boolean;
  setGlobalLoading: (loading: boolean) => void;
  
  // 当前任务状态
  currentTaskId: string | null;
  setCurrentTaskId: (taskId: string | null) => void;
  
  // 任务执行状态
  taskStatus: 'idle' | 'running' | 'paused' | 'completed' | 'error';
  setTaskStatus: (status: 'idle' | 'running' | 'paused' | 'completed' | 'error') => void;
  
  // 配置
  agentConfig: AgentConfig;
  setAgentConfig: (config: AgentConfig) => void;
  browserConfig: BrowserConfig;
  setBrowserConfig: (config: BrowserConfig) => void;
  llmConfig: LLMConfig;
  setLLMConfig: (config: LLMConfig) => void;
  
  // 菜单
  menuList: MenuGroup[];
  
  // 刷新任务列表
  refreshTaskList: () => void;
  taskListVersion: number;
}

// =============================================================================
// Default Configs
// =============================================================================

const defaultAgentConfig: AgentConfig = {
  agentType: 'custom',
  maxSteps: 100,
  useVision: true,
  maxActionsPerStep: 10,
  toolCallInContent: true,
  maxInputTokens: 128000,
  toolCallingMethod: 'auto',
  overrideSystemPrompt: '',
  extendSystemPrompt: '',
};

const defaultBrowserConfig: BrowserConfig = {
  headless: false,
  disableSecurity: true,
  windowWidth: 1280,
  windowHeight: 1100,
  saveRecordingPath: './tmp/recordings',
  saveTracePath: './tmp/traces',
  useOwnBrowser: false,
  keepBrowserOpen: true,
  browserBinaryPath: '',
  browserUserDataDir: '',
  cdpUrl: '',
  wssUrl: '',
};

const defaultLLMConfig: LLMConfig = {
  provider: 'openai',
  modelName: 'gpt-4o',
  temperature: 0.6,
  baseUrl: '',
  apiKey: '',
  plannerEnabled: false,
  plannerProvider: 'openai',
  plannerModelName: 'gpt-4o-mini',
  plannerTemperature: 0.7,
};

// =============================================================================
// Context
// =============================================================================

const AppContext = createContext<AppState | undefined>(undefined);

// =============================================================================
// Provider
// =============================================================================

interface AppProviderProps {
  children: ReactNode;
  menuList: MenuGroup[];
}

export function AppProvider({ children, menuList }: AppProviderProps) {
  const [globalLoading, setGlobalLoading] = useState(false);
  const [currentTaskId, setCurrentTaskId] = useState<string | null>(null);
  const [taskStatus, setTaskStatus] = useState<'idle' | 'running' | 'paused' | 'completed' | 'error'>('idle');
  const [taskListVersion, setTaskListVersion] = useState(0);
  
  const [agentConfig, setAgentConfig] = useState<AgentConfig>(defaultAgentConfig);
  const [browserConfig, setBrowserConfig] = useState<BrowserConfig>(defaultBrowserConfig);
  const [llmConfig, setLLMConfig] = useState<LLMConfig>(defaultLLMConfig);
  
  const refreshTaskList = useCallback(() => {
    setTaskListVersion(v => v + 1);
  }, []);

  const value: AppState = {
    globalLoading,
    setGlobalLoading,
    currentTaskId,
    setCurrentTaskId,
    taskStatus,
    setTaskStatus,
    agentConfig,
    setAgentConfig,
    browserConfig,
    setBrowserConfig,
    llmConfig,
    setLLMConfig,
    menuList,
    refreshTaskList,
    taskListVersion,
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
}

// =============================================================================
// Hook
// =============================================================================

export function useApp() {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
}
