/**
 * API client functions for communicating with the FastAPI backend.
 */

import {
  DashboardStats,
  Task,
  TaskCreate,
  TaskUpdate,
  Milestone,
  MilestoneCreate,
  MilestoneUpdate,
} from './types';

// Base URL for the API - defaults to localhost:8000
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Generic fetch wrapper that handles API requests and errors.
 */
async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
    throw new Error(error.detail || `HTTP error ${response.status}`);
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

// Dashboard API functions
export const dashboardApi = {
  /**
   * Fetch dashboard statistics including task counts and upcoming deadlines.
   */
  getStats: (): Promise<DashboardStats> => fetchApi<DashboardStats>('/dashboard'),
};

// Tasks API functions
export const tasksApi = {
  /**
   * List all tasks.
   */
  list: (): Promise<Task[]> => fetchApi<Task[]>('/tasks'),

  /**
   * Get a single task by ID.
   */
  get: (id: string): Promise<Task> => fetchApi<Task>(`/tasks/${id}`),

  /**
   * Create a new task.
   */
  create: (task: TaskCreate): Promise<Task> =>
    fetchApi<Task>('/tasks', {
      method: 'POST',
      body: JSON.stringify(task),
    }),

  /**
   * Update an existing task.
   */
  update: (id: string, task: TaskUpdate): Promise<Task> =>
    fetchApi<Task>(`/tasks/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(task),
    }),

  /**
   * Delete a task.
   */
  delete: (id: string): Promise<void> =>
    fetchApi<void>(`/tasks/${id}`, {
      method: 'DELETE',
    }),
};

// Milestones API functions
export const milestonesApi = {
  /**
   * List all milestones.
   */
  list: (): Promise<Milestone[]> => fetchApi<Milestone[]>('/milestones'),

  /**
   * Get a single milestone by ID.
   */
  get: (id: string): Promise<Milestone> => fetchApi<Milestone>(`/milestones/${id}`),

  /**
   * Create a new milestone.
   */
  create: (milestone: MilestoneCreate): Promise<Milestone> =>
    fetchApi<Milestone>('/milestones', {
      method: 'POST',
      body: JSON.stringify(milestone),
    }),

  /**
   * Update an existing milestone.
   */
  update: (id: string, milestone: MilestoneUpdate): Promise<Milestone> =>
    fetchApi<Milestone>(`/milestones/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(milestone),
    }),

  /**
   * Delete a milestone.
   */
  delete: (id: string): Promise<void> =>
    fetchApi<void>(`/milestones/${id}`, {
      method: 'DELETE',
    }),
};
