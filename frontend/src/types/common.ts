/**
 * Common Types - 通用类型定义
 */

// =============================================================================
// Menu Types
// =============================================================================

export interface MenuItem {
  name: string;
  icon: string;
  link: string;
}

export interface MenuGroup {
  name: string;
  icon?: string;
  children: MenuItem[];
}

// =============================================================================
// Task Types
// =============================================================================

export type TaskStatus = 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';

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

export interface TaskStatistics {
  totalTasks: number;
  completedTasks: number;
  failedTasks: number;
  runningTasks: number;
  totalTokens: number;
  successRate: number;
}

export interface TokenTrend {
  date: string;
  tokens: number;
}

export interface DurationDistribution {
  range: string;
  count: number;
}

export interface TaskAnalysis {
  successCount: number;
  failedCount: number;
  durationDistribution: DurationDistribution[];
}

// =============================================================================
// Agent Types
// =============================================================================

export interface AgentConfig {
  agentType: string;
  maxSteps: number;
  useVision: boolean;
  maxActionsPerStep: number;
  toolCallInContent: boolean;
  maxInputTokens: number;
  toolCallingMethod: string;
  overrideSystemPrompt?: string;
  extendSystemPrompt?: string;
}

export interface BrowserConfig {
  headless: boolean;
  disableSecurity: boolean;
  windowWidth: number;
  windowHeight: number;
  saveRecordingPath?: string;
  saveTracePath?: string;
  useOwnBrowser: boolean;
  keepBrowserOpen: boolean;
  browserBinaryPath?: string;
  browserUserDataDir?: string;
  cdpUrl?: string;
  wssUrl?: string;
}

export interface LLMConfig {
  provider: string;
  modelName: string;
  temperature: number;
  baseUrl?: string;
  apiKey?: string;
  plannerEnabled?: boolean;
  plannerProvider?: string;
  plannerModelName?: string;
  plannerTemperature?: number;
  plannerBaseUrl?: string;
  plannerApiKey?: string;
}

// =============================================================================
// Execution Types
// =============================================================================

export interface ExecutionMetrics {
  status: string;
  currentStep: number;
  maxSteps: number;
  totalDuration: number;
  avgStepDuration: number;
  promptTokens: number;
  completionTokens: number;
  totalTokens: number;
  systemRetries: number;
  businessRetries: number;
  totalRetries: number;
}

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp?: string;
}

export interface AgentRunState {
  taskId: string;
  task: string;
  status: string;
  currentStep: number;
  maxSteps: number;
  totalDuration: number;
  avgStepDuration: number;
  promptTokens: number;
  completionTokens: number;
  totalTokens: number;
  systemRetries: number;
  businessRetries: number;
  totalRetries: number;
  screenshot?: string;
  chatHistory: ChatMessage[];
}

// =============================================================================
// API Response Types
// =============================================================================

export interface ApiResponse<T = unknown> {
  code: number;
  message: string;
  data?: T;
}

export interface PaginatedData<T> {
  list: T[];
  total: number;
  page: number;
  pageSize: number;
}

// =============================================================================
// Config Template Types
// =============================================================================

export interface ConfigTemplate {
  id: string;
  name: string;
  description?: string;
  agentConfig: AgentConfig;
  browserConfig: BrowserConfig;
  llmConfig: LLMConfig;
  createdAt: string;
  updatedAt: string;
}

// =============================================================================
// User Types
// =============================================================================

export interface UserInfo {
  username: string;
  nickname: string;
  avatar?: string;
}

// =============================================================================
// ZKH MCP Types
// =============================================================================

export interface ZKHMCPTool {
  name: string;
  description: string;
  enabled: boolean;
}

export interface ZKHConfig {
  enabled: boolean;
  tools: ZKHMCPTool[];
  customSelectors?: Record<string, string>;
}
