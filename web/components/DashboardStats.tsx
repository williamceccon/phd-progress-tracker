'use client';

import React from 'react';
import { DashboardStats as DashboardStatsType } from '@/lib/types';
import { formatDate, getRelativeTime } from '@/lib/utils';
import Card, { CardHeader, CardTitle, CardContent } from './Card';
import StatusBadge from './StatusBadge';

/**
 * DashboardStats component for displaying task statistics.
 */
interface DashboardStatsProps {
  stats: DashboardStatsType | null;
  isLoading?: boolean;
}

export default function DashboardStats({ stats, isLoading = false }: DashboardStatsProps) {
  if (isLoading) {
    return (
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[1, 2, 3, 4].map((i) => (
          <Card key={i}>
            <div className="animate-pulse">
              <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
              <div className="h-8 bg-gray-200 rounded w-3/4"></div>
            </div>
          </Card>
        ))}
      </div>
    );
  }

  if (!stats) {
    return null;
  }

  const statCards = [
    {
      label: 'Total de Tarefas',
      value: stats.total_tasks,
      color: 'text-primary',
      bgColor: 'bg-blue-50',
    },
    {
      label: 'Concluídas',
      value: stats.completed_tasks,
      color: 'text-success',
      bgColor: 'bg-green-50',
      percentage: stats.total_tasks > 0 
        ? Math.round((stats.completed_tasks / stats.total_tasks) * 100) 
        : 0,
    },
    {
      label: 'Pendentes',
      value: stats.pending_tasks,
      color: 'text-warning',
      bgColor: 'bg-amber-50',
    },
    {
      label: 'Atrasadas',
      value: stats.overdue_tasks,
      color: stats.overdue_tasks > 0 ? 'text-danger' : 'text-gray-500',
      bgColor: stats.overdue_tasks > 0 ? 'bg-red-50' : 'bg-gray-50',
    },
  ];

  return (
    <div className="space-y-8">
      {/* Stats Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((stat) => (
          <Card key={stat.label}>
            <div className={`${stat.bgColor} rounded-lg p-4`}>
              <p className="text-sm font-medium text-gray-600">{stat.label}</p>
              <p className={`text-3xl font-bold mt-1 ${stat.color}`}>
                {stat.value}
              </p>
              {stat.percentage !== undefined && (
                <p className="text-xs text-gray-500 mt-1">
                  {stat.percentage}% do total
                </p>
              )}
            </div>
          </Card>
        ))}
      </div>

      {/* Upcoming Deadlines */}
      <Card>
        <CardHeader>
          <CardTitle>Prazos Próximos (Próximos 7 Dias)</CardTitle>
        </CardHeader>
        <CardContent>
          {stats.upcoming_deadlines.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <svg
                className="mx-auto h-10 w-10 text-gray-400 mb-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                />
              </svg>
              <p>Nenhum prazo nos próximos 7 dias</p>
            </div>
          ) : (
            <div className="space-y-3">
              {stats.upcoming_deadlines.map((task) => (
                <div
                  key={task.id}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {task.title}
                    </p>
                    <p className="text-xs text-gray-500">
                      {formatDate(task.deadline)} • {getRelativeTime(task.deadline)}
                    </p>
                  </div>
                  <div className="flex items-center gap-2 ml-4">
                    <StatusBadge variant="priority" value={task.priority} />
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
