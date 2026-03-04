'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { DashboardStats as DashboardStatsType } from '@/lib/types';
import { dashboardApi } from '@/lib/api';
import DashboardStats from '@/components/DashboardStats';
import Button from '@/components/Button';
import Card, { CardHeader, CardTitle, CardContent } from '@/components/Card';
import { Milestone } from '@/lib/types';
import { milestonesApi } from '@/lib/api';
import { formatDate, getRelativeTime } from '@/lib/utils';

/**
 * Dashboard page showing statistics and upcoming milestones.
 */
export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStatsType | null>(null);
  const [milestones, setMilestones] = useState<Milestone[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const [statsData, milestonesData] = await Promise.all([
        dashboardApi.getStats(),
        milestonesApi.list(),
      ]);
      setStats(statsData);
      setMilestones(milestonesData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar dados');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // Get current date formatted
  const today = new Date().toLocaleDateString('pt-BR', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Hero Section */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Bem-vindo ao seu PhD Progress Tracker
        </h1>
        <p className="mt-2 text-gray-600 capitalize">{today}</p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-center justify-between">
            <p className="text-sm text-danger">{error}</p>
            <Button variant="secondary" size="sm" onClick={fetchData}>
              Tentar novamente
            </Button>
          </div>
        </div>
      )}

      {/* Dashboard Stats */}
      <DashboardStats stats={stats} isLoading={isLoading} />

      {/* Upcoming Milestones */}
      <div className="mt-8">
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Próximos Marcos</CardTitle>
              <Link href="/milestones">
                <Button variant="ghost" size="sm">
                  Ver todos
                </Button>
              </Link>
            </div>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="space-y-3">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="animate-pulse">
                    <div className="h-4 bg-gray-200 rounded w-1/2"></div>
                  </div>
                ))}
              </div>
            ) : milestones.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <p>Nenhum marco definido ainda.</p>
                <Link href="/milestones">
                  <Button variant="primary" size="sm" className="mt-2">
                    Criar primeiro marco
                  </Button>
                </Link>
              </div>
            ) : (
              <div className="space-y-3">
                {milestones
                  .filter((m) => !m.is_achieved)
                  .slice(0, 5)
                  .map((milestone) => (
                    <div
                      key={milestone.id}
                      className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                    >
                      <div>
                        <p className="text-sm font-medium text-gray-900">
                          {milestone.title}
                        </p>
                        <p className="text-xs text-gray-500">
                          {formatDate(milestone.target_date)} •{' '}
                          {getRelativeTime(milestone.target_date)}
                        </p>
                      </div>
                      <span
                        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          milestone.is_achieved
                            ? 'bg-green-100 text-green-700'
                            : 'bg-purple-100 text-purple-700'
                        }`}
                      >
                        {milestone.is_achieved ? 'Concluído' : 'Em progresso'}
                      </span>
                    </div>
                  ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-4">
        <Link href="/tasks">
          <Card hover className="cursor-pointer">
            <div className="flex items-center">
              <div className="p-3 bg-blue-100 rounded-lg">
                <svg
                  className="w-6 h-6 text-primary"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
                  />
                </svg>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-medium text-gray-900">
                  Gerenciar Tarefas
                </h3>
                <p className="text-sm text-gray-500">
                  Adicione, edite ou conclua tarefas
                </p>
              </div>
            </div>
          </Card>
        </Link>

        <Link href="/milestones">
          <Card hover className="cursor-pointer">
            <div className="flex items-center">
              <div className="p-3 bg-purple-100 rounded-lg">
                <svg
                  className="w-6 h-6 text-purple-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"
                  />
                </svg>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-medium text-gray-900">
                  Gerenciar Marcos
                </h3>
                <p className="text-sm text-gray-500">
                  Defina e acompanhe seus marcos
                </p>
              </div>
            </div>
          </Card>
        </Link>
      </div>
    </div>
  );
}
