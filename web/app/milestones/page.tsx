'use client';

import { useState, useEffect } from 'react';
import { Milestone, MilestoneCreate, MilestoneUpdate } from '@/lib/types';
import { milestonesApi } from '@/lib/api';
import MilestoneList from '@/components/MilestoneList';
import MilestoneForm from '@/components/MilestoneForm';
import Button from '@/components/Button';

/**
 * Milestones management page with CRUD functionality.
 */
export default function MilestonesPage() {
  const [milestones, setMilestones] = useState<Milestone[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingMilestone, setEditingMilestone] = useState<Milestone | null>(null);
  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);

  const fetchMilestones = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await milestonesApi.list();
      setMilestones(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar marcos');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchMilestones();
  }, []);

  const handleCreateMilestone = async (milestoneData: MilestoneCreate | MilestoneUpdate) => {
    try {
      await milestonesApi.create(milestoneData as MilestoneCreate);
      await fetchMilestones();
    } catch (err) {
      throw err;
    }
  };

  const handleEditMilestone = async (milestoneData: MilestoneCreate | MilestoneUpdate) => {
    if (!editingMilestone) return;
    try {
      await milestonesApi.update(editingMilestone.id, milestoneData as MilestoneUpdate);
      await fetchMilestones();
      setEditingMilestone(null);
    } catch (err) {
      throw err;
    }
  };

  const handleDeleteMilestone = async (milestoneId: string) => {
    setDeleteConfirm(milestoneId);
  };

  const confirmDelete = async () => {
    if (!deleteConfirm) return;
    try {
      await milestonesApi.delete(deleteConfirm);
      await fetchMilestones();
      setDeleteConfirm(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao excluir marco');
      setDeleteConfirm(null);
    }
  };

  const handleToggleAchieved = async (milestone: Milestone) => {
    try {
      await milestonesApi.update(milestone.id, { is_achieved: !milestone.is_achieved });
      await fetchMilestones();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao atualizar marco');
    }
  };

  const openEditForm = (milestone: Milestone) => {
    setEditingMilestone(milestone);
    setIsFormOpen(true);
  };

  const closeForm = () => {
    setIsFormOpen(false);
    setEditingMilestone(null);
  };

  // Calculate achievement stats
  const achievedCount = milestones.filter((m) => m.is_achieved).length;
  const totalCount = milestones.length;
  const achievementPercentage = totalCount > 0 ? Math.round((achievedCount / totalCount) * 100) : 0;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Page Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Marcos</h1>
          <p className="mt-1 text-sm text-gray-500">
            Defina e acompanhe os marcos do seu doutorado
          </p>
        </div>
        <Button onClick={() => setIsFormOpen(true)}>
          <svg
            className="w-5 h-5 mr-2"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 4v16m8-8H4"
            />
          </svg>
          Adicionar Marco
        </Button>
      </div>

      {/* Stats Summary */}
      {milestones.length > 0 && (
        <div className="mb-6 p-4 bg-white rounded-lg border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Progresso Geral</p>
              <p className="text-2xl font-bold text-gray-900">
                {achievedCount} de {totalCount} marcos concluídos
              </p>
            </div>
            <div className="flex items-center">
              <div className="w-32 h-3 bg-gray-200 rounded-full overflow-hidden mr-3">
                <div
                  className="h-full bg-success rounded-full transition-all duration-300"
                  style={{ width: `${achievementPercentage}%` }}
                />
              </div>
              <span className="text-sm font-medium text-gray-700">
                {achievementPercentage}%
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-center justify-between">
            <p className="text-sm text-danger">{error}</p>
            <Button variant="secondary" size="sm" onClick={fetchMilestones}>
              Tentar novamente
            </Button>
          </div>
        </div>
      )}

      {/* Milestone List */}
      <MilestoneList
        milestones={milestones}
        onEdit={openEditForm}
        onDelete={handleDeleteMilestone}
        onToggleAchieved={handleToggleAchieved}
        isLoading={isLoading}
      />

      {/* Milestone Form Modal */}
      <MilestoneForm
        isOpen={isFormOpen}
        onClose={closeForm}
        onSubmit={editingMilestone ? handleEditMilestone : handleCreateMilestone}
        milestone={editingMilestone}
      />

      {/* Delete Confirmation Modal */}
      {deleteConfirm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Confirmar exclusão
            </h3>
            <p className="text-sm text-gray-600 mb-6">
              Tem certeza que deseja excluir este marco? Esta ação não pode ser
              desfeita.
            </p>
            <div className="flex justify-end gap-3">
              <Button variant="secondary" onClick={() => setDeleteConfirm(null)}>
                Cancelar
              </Button>
              <Button variant="danger" onClick={confirmDelete}>
                Excluir
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
