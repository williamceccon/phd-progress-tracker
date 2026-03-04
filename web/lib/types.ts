/**
 * TypeScript type definitions matching the backend API.
 * Values are in Portuguese to match the backend enum values.
 */

// Task status enum - Portuguese values from backend
export type TaskStatus = 'A Fazer' | 'Em Progresso' | 'Concluída' | 'Bloqueada';

// Task priority enum - Portuguese values from backend
export type TaskPriority = 'Baixa' | 'Média' | 'Alta' | 'Crítica';

// Task category options
export type TaskCategory = 'Geral' | 'Coleta de Dados' | 'Análise' | 'Escrita' | 'Revisão';

// Task interface matching backend TaskResponse
export interface Task {
  id: string;
  title: string;
  description: string;
  deadline: string; // ISO date: "2024-12-31"
  status: TaskStatus;
  priority: TaskPriority;
  category: string;
  created_at: string; // ISO datetime: "2024-01-15T10:30:00"
  completed_at: string | null;
}

// Task creation payload
export interface TaskCreate {
  title: string;
  description: string;
  deadline: string;
  category?: string;
  priority?: TaskPriority;
}

// Task update payload
export interface TaskUpdate {
  title?: string;
  description?: string;
  deadline?: string;
  status?: TaskStatus;
  priority?: TaskPriority;
  category?: string;
}

// Milestone interface matching backend MilestoneResponse
export interface Milestone {
  id: string;
  title: string;
  description: string;
  target_date: string; // ISO date: "2024-12-31"
  is_achieved: boolean;
}

// Milestone creation payload
export interface MilestoneCreate {
  title: string;
  description: string;
  target_date: string;
}

// Milestone update payload
export interface MilestoneUpdate {
  title?: string;
  description?: string;
  target_date?: string;
  is_achieved?: boolean;
}

// Dashboard statistics response
export interface DashboardStats {
  total_tasks: number;
  completed_tasks: number;
  pending_tasks: number;
  overdue_tasks: number;
  upcoming_deadlines: Task[];
}

// API error response
export interface ApiError {
  detail: string;
}

// Task category options for dropdowns
export const TASK_CATEGORIES: TaskCategory[] = [
  'Geral',
  'Coleta de Dados',
  'Análise',
  'Escrita',
  'Revisão',
];

// Task priority options for dropdowns
export const TASK_PRIORITIES: TaskPriority[] = [
  'Baixa',
  'Média',
  'Alta',
  'Crítica',
];

// Task status options for dropdowns
export const TASK_STATUSES: TaskStatus[] = [
  'A Fazer',
  'Em Progresso',
  'Concluída',
  'Bloqueada',
];
