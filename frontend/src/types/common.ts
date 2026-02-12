/**
 * 通用类型定义
 */

// 菜单项类型
export interface MenuItem {
  name: string;
  link?: string;
  icon?: string;
  children?: MenuItem[];
}

// 菜单分组类型
export interface MenuGroup {
  name: string;
  children: MenuItem[];
}

// 用户信息类型
export interface UserInfo {
  username: string;
  nickname?: string;
  avatar?: string;
}

// 任务状态
export type TaskStatus = 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';

// 任务数据
export interface Task {
  id: string;
  name: string;
  status: TaskStatus;
  startTime: string;
  endTime?: string;
  duration?: number;
  tokenUsed?: number;
  result?: string;
  error?: string;
}

// 统计数据
export interface Statistics {
  totalTasks: number;
  completedTasks: number;
  failedTasks: number;
  runningTasks: number;
  totalTokens: number;
  successRate: number;
}

// Token使用趋势
export interface TokenTrend {
  date: string;
  tokens: number;
}

// 任务分析数据
export interface TaskAnalysis {
  successCount: number;
  failedCount: number;
  durationDistribution: {
    range: string;
    count: number;
  }[];
}

// Tool Calling方法类型
export type ToolCallingMethod = 'auto' | 'function_call' | 'raw' | 'json_mode' | 'tools';

// Agent配置
export interface AgentConfig {
  agentType: string;
  maxSteps: number;
  useVision: boolean;
  maxActionsPerStep: number;
  toolCallInContent: boolean;
  maxInputTokens: number;
  toolCallingMethod: ToolCallingMethod;
}

// Browser配置
export interface BrowserConfig {
  headless: boolean;
  disableSecurity: boolean;
  windowWidth: number;
  windowHeight: number;
  saveRecordingPath?: string;
  saveTracePath?: string;
}

// LLM配置
export interface LLMConfig {
  provider: string;
  modelName: string;
  temperature: number;
  baseUrl?: string;
  apiKey?: string;
}

// LLM Planner配置
export interface LLMPlannerConfig {
  enabled: boolean;
  provider: string;
  modelName: string;
  temperature: number;
  baseUrl?: string;
  apiKey?: string;
}

// 完整LLM配置（包含主LLM和Planner）
export interface FullLLMConfig {
  main: LLMConfig;
  planner: LLMPlannerConfig;
}

// 分页参数
export interface PaginationParams {
  page: number;
  pageSize: number;
}

// 分页响应
export interface PaginatedResponse<T> {
  list: T[];
  total: number;
  page: number;
  pageSize: number;
}

// API响应
export interface ApiResponse<T = unknown> {
  code: number;
  message: string;
  data: T;
}
