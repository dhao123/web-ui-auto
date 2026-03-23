/**
 * API - 后端接口封装
 */
import type { 
  ApiResponse, 
  TaskStatistics, 
  TokenTrend, 
  TaskAnalysis, 
  PaginatedData, 
  Task,
  AgentRunState,
  AgentConfig,
  BrowserConfig,
  LLMConfig,
} from '@/types/common';

const BASE_URL = '/api';

// 通用请求封装
async function request<T>(url: string, options?: RequestInit): Promise<ApiResponse<T>> {
  const response = await fetch(`${BASE_URL}${url}`, {
    headers: {
      'Content-Type': 'application/json',
    },
    ...options,
  });
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return response.json();
}

// =============================================================================
// Statistics API
// =============================================================================

export const api = {
  // 获取统计数据
  getStatistics(): Promise<ApiResponse<TaskStatistics>> {
    return request('/statistics');
  },

  // 获取Token趋势
  getTokenTrend(days: number = 7): Promise<ApiResponse<{ trends: TokenTrend[] }>> {
    return request(`/statistics/token-trend?days=${days}`);
  },

  // 获取任务分析
  getTaskAnalysis(): Promise<ApiResponse<TaskAnalysis>> {
    return request('/statistics/task-analysis');
  },

  // =============================================================================
  // Task API
  // =============================================================================

  // 获取任务列表
  getTasks(params: { page: number; pageSize: number }): Promise<ApiResponse<PaginatedData<Task>>> {
    return request(`/tasks?page=${params.page}&pageSize=${params.pageSize}`);
  },

  // 获取任务详情
  getTask(taskId: string): Promise<ApiResponse<Task>> {
    return request(`/tasks/${taskId}`);
  },

  // 停止任务
  stopTask(taskId: string): Promise<ApiResponse<void>> {
    return request(`/tasks/${taskId}/stop`, { method: 'POST' });
  },

  // =============================================================================
  // Agent Run API
  // =============================================================================

  // 开始Agent任务
  startAgentRun(task: string): Promise<ApiResponse<{ taskId: string }>> {
    return request('/agent/run', {
      method: 'POST',
      body: JSON.stringify({ task }),
    });
  },

  // 获取Agent运行状态
  getAgentRunStatus(taskId: string): Promise<ApiResponse<AgentRunState>> {
    return request(`/agent/run/${taskId}/status`);
  },

  // 停止Agent运行
  stopAgentRun(taskId: string): Promise<ApiResponse<void>> {
    return request(`/agent/run/${taskId}/stop`, { method: 'POST' });
  },

  // 暂停Agent运行
  pauseAgentRun(taskId: string): Promise<ApiResponse<void>> {
    return request(`/agent/run/${taskId}/pause`, { method: 'POST' });
  },

  // 恢复Agent运行
  resumeAgentRun(taskId: string): Promise<ApiResponse<void>> {
    return request(`/agent/run/${taskId}/resume`, { method: 'POST' });
  },

  // =============================================================================
  // Config API
  // =============================================================================

  // 获取Agent配置
  getAgentConfig(): Promise<ApiResponse<AgentConfig>> {
    return request('/config/agent');
  },

  // 更新Agent配置
  updateAgentConfig(config: AgentConfig): Promise<ApiResponse<void>> {
    return request('/config/agent', {
      method: 'POST',
      body: JSON.stringify(config),
    });
  },

  // 获取Browser配置
  getBrowserConfig(): Promise<ApiResponse<BrowserConfig>> {
    return request('/config/browser');
  },

  // 更新Browser配置
  updateBrowserConfig(config: BrowserConfig): Promise<ApiResponse<void>> {
    return request('/config/browser', {
      method: 'POST',
      body: JSON.stringify(config),
    });
  },

  // 获取LLM配置
  getLLMConfig(): Promise<ApiResponse<LLMConfig>> {
    return request('/config/llm');
  },

  // 更新LLM配置
  updateLLMConfig(config: LLMConfig): Promise<ApiResponse<void>> {
    return request('/config/llm', {
      method: 'POST',
      body: JSON.stringify(config),
    });
  },
};
