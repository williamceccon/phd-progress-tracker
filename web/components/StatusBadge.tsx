'use client';

import React from 'react';
import { TaskStatus, TaskPriority } from '@/lib/types';

/**
 * StatusBadge component for displaying task status and priority.
 */
interface StatusBadgeProps {
  variant: 'status' | 'priority' | 'category';
  value: TaskStatus | TaskPriority | string;
}

export default function StatusBadge({ variant, value }: StatusBadgeProps) {
  const getColorClasses = () => {
    if (variant === 'status') {
      switch (value) {
        case 'A Fazer':
          return 'bg-gray-100 text-gray-700';
        case 'Em Progresso':
          return 'bg-amber-100 text-amber-700';
        case 'Concluída':
          return 'bg-green-100 text-green-700';
        case 'Bloqueada':
          return 'bg-red-100 text-red-700';
        default:
          return 'bg-gray-100 text-gray-700';
      }
    }

    if (variant === 'priority') {
      switch (value) {
        case 'Baixa':
          return 'bg-gray-100 text-gray-600';
        case 'Média':
          return 'bg-blue-100 text-blue-700';
        case 'Alta':
          return 'bg-orange-100 text-orange-700';
        case 'Crítica':
          return 'bg-red-100 text-red-700';
        default:
          return 'bg-gray-100 text-gray-600';
      }
    }

    // Category variant
    return 'bg-purple-100 text-purple-700';
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getColorClasses()}`}
    >
      {value}
    </span>
  );
}
