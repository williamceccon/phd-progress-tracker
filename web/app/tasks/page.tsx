'use client';

import { useState, useEffect } from 'react';
import { Task, TaskCreate, TaskUpdate, TaskStatus } from '@/lib/types';
import { tasksApi } from '@/lib/api';
import TaskList from '@/components/TaskList';
import TaskForm from '@/components/TaskForm';
import Button from '@/components/Button';

/**
 * Tasks management page with CRUD functionality.
 */
export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);

  const fetchTasks = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await tasksApi.list();
      setTasks(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar tarefas');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const handleCreateTask = async (taskData: TaskCreate | TaskUpdate) => {
    try {
      await tasksApi.create(taskData as TaskCreate);
      await fetchTasks();
    } catch (err) {
      throw err;
    }
  };

  const handleEditTask = async (taskData: TaskCreate | TaskUpdate) => {
    if (!editingTask) return;
    try {
      await tasksApi.update(editingTask.id, taskData as TaskUpdate);
      await fetchTasks();
      setEditingTask(null);
    } catch (err) {
      throw err;
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    setDeleteConfirm(taskId);
  };

  const confirmDelete = async () => {
    if (!deleteConfirm) return;
    try {
      await tasksApi.delete(deleteConfirm);
      await fetchTasks();
      setDeleteConfirm(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao excluir tarefa');
      setDeleteConfirm(null);
    }
  };

  const handleToggleStatus = async (task: Task) => {
    const newStatus: TaskStatus = task.status === 'Concluída' ? 'A Fazer' : 'Concluída';
    try {
      await tasksApi.update(task.id, { status: newStatus });
      await fetchTasks();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao atualizar status');
    }
  };

  const openEditForm = (task: Task) => {
    setEditingTask(task);
    setIsFormOpen(true);
  };

  const closeForm = () => {
    setIsFormOpen(false);
    setEditingTask(null);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Page Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Tarefas</h1>
          <p className="mt-1 text-sm text-gray-500">
            Gerencie suas tarefas de doutorado
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
          Adicionar Tarefa
        </Button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-center justify-between">
            <p className="text-sm text-danger">{error}</p>
            <Button variant="secondary" size="sm" onClick={fetchTasks}>
              Tentar novamente
            </Button>
          </div>
        </div>
      )}

      {/* Task List */}
      <TaskList
        tasks={tasks}
        onEdit={openEditForm}
        onDelete={handleDeleteTask}
        onToggleStatus={handleToggleStatus}
        isLoading={isLoading}
      />

      {/* Task Form Modal */}
      <TaskForm
        isOpen={isFormOpen}
        onClose={closeForm}
        onSubmit={editingTask ? handleEditTask : handleCreateTask}
        task={editingTask}
      />

      {/* Delete Confirmation Modal */}
      {deleteConfirm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Confirmar exclusão
            </h3>
            <p className="text-sm text-gray-600 mb-6">
              Tem certeza que deseja excluir esta tarefa? Esta ação não pode ser
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
