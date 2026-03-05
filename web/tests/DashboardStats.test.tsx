/**
 * Unit tests for DashboardStats component.
 */
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import DashboardStats from '@/components/DashboardStats';
import { DashboardStats as DashboardStatsType } from '@/lib/types';

describe('DashboardStats', () => {
  const mockStats: DashboardStatsType = {
    total_tasks: 10,
    completed_tasks: 6,
    pending_tasks: 3,
    overdue_tasks: 1,
    upcoming_deadlines: [
      {
        id: '1',
        title: 'Task 1',
        description: 'Description 1',
        deadline: '2026-03-10',
        status: 'A Fazer' as const,
        priority: 'Alta' as const,
        category: 'Geral',
        created_at: '2026-01-01T10:00:00',
        completed_at: null,
      },
    ],
  };

  it('shows loading skeleton when isLoading is true', () => {
    render(<DashboardStats stats={null} isLoading={true} />);

    // Check for skeleton elements (by looking for animate-pulse class)
    const skeletonElements = document.querySelectorAll('.animate-pulse');
    expect(skeletonElements.length).toBeGreaterThan(0);
  });

  it('returns null when stats is null and not loading', () => {
    const { container } = render(<DashboardStats stats={null} isLoading={false} />);
    
    // Component should return null (no rendered content)
    expect(container.firstChild).toBeNull();
  });

  it('displays stats correctly', () => {
    render(<DashboardStats stats={mockStats} isLoading={false} />);

    // Check stat cards are rendered with correct values
    expect(screen.getByText('Total de Tarefas')).toBeInTheDocument();
    expect(screen.getByText('10')).toBeInTheDocument();
    
    expect(screen.getByText('Concluídas')).toBeInTheDocument();
    expect(screen.getByText('6')).toBeInTheDocument();
    
    expect(screen.getByText('Pendentes')).toBeInTheDocument();
    expect(screen.getByText('3')).toBeInTheDocument();
    
    expect(screen.getByText('Atrasadas')).toBeInTheDocument();
    expect(screen.getByText('1')).toBeInTheDocument();
  });

  it('shows percentage for completed tasks when total > 0', () => {
    render(<DashboardStats stats={mockStats} isLoading={false} />);

    // 6 completed out of 10 = 60%
    expect(screen.getByText('60% do total')).toBeInTheDocument();
  });

  it('shows 0% when total is 0', () => {
    const emptyStats: DashboardStatsType = {
      total_tasks: 0,
      completed_tasks: 0,
      pending_tasks: 0,
      overdue_tasks: 0,
      upcoming_deadlines: [],
    };

    render(<DashboardStats stats={emptyStats} isLoading={false} />);

    // Should show 0% text
    expect(screen.getByText('0% do total')).toBeInTheDocument();
  });

  it('renders upcoming deadlines when available', () => {
    render(<DashboardStats stats={mockStats} isLoading={false} />);

    // Check upcoming deadlines section
    expect(screen.getByText('Prazos Próximos (Próximos 7 Dias)')).toBeInTheDocument();
    expect(screen.getByText('Task 1')).toBeInTheDocument();
  });

  it('shows empty state when no upcoming deadlines', () => {
    const statsWithoutDeadlines: DashboardStatsType = {
      total_tasks: 5,
      completed_tasks: 2,
      pending_tasks: 3,
      overdue_tasks: 0,
      upcoming_deadlines: [],
    };

    render(<DashboardStats stats={statsWithoutDeadlines} isLoading={false} />);

    // Check empty state message
    expect(screen.getByText('Nenhum prazo nos próximos 7 dias')).toBeInTheDocument();
  });
});
