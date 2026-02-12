/**
 * API请求工具
 */
import axios from 'axios';
import type { ApiResponse } from '@/types/common';

const request = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

export default request;

// 统计数据API
export const fetchStatistics = () => {
  return request.get<unknown, ApiResponse>('/statistics');
};

// Token趋势API
export const fetchTokenTrend = (days: number = 7) => {
  return request.get<unknown, ApiResponse>('/statistics/token-trend', {
    params: { days },
  });
};

// 任务分析API
export const fetchTaskAnalysis = () => {
  return request.get<unknown, ApiResponse>('/statistics/task-analysis');
};

// 任务列表API
export const fetchTasks = (params: { page: number; pageSize: number }) => {
  return request.get<unknown, ApiResponse>('/tasks', { params });
};

// Agent配置API
export const fetchAgentConfig = () => {
  return request.get<unknown, ApiResponse>('/config/agent');
};

export const updateAgentConfig = (data: Record<string, unknown>) => {
  return request.post<unknown, ApiResponse>('/config/agent', data);
};

// Browser配置API
export const fetchBrowserConfig = () => {
  return request.get<unknown, ApiResponse>('/config/browser');
};

export const updateBrowserConfig = (data: Record<string, unknown>) => {
  return request.post<unknown, ApiResponse>('/config/browser', data);
};

// LLM配置API
export const fetchLLMConfig = () => {
  return request.get<unknown, ApiResponse>('/config/llm');
};

export const updateLLMConfig = (data: Record<string, unknown>) => {
  return request.post<unknown, ApiResponse>('/config/llm', data);
};
