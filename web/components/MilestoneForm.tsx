'use client';

import React, { useState, useEffect } from 'react';
import { Milestone, MilestoneCreate, MilestoneUpdate } from '@/lib/types';
import { getTodayDateString } from '@/lib/utils';
import Modal from './Modal';
import { ModalFooter } from './Modal';
import Button from './Button';

/**
 * MilestoneForm component for creating and editing milestones.
 */
interface MilestoneFormProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (milestone: MilestoneCreate | MilestoneUpdate) => Promise<void>;
  milestone?: Milestone | null;
}

export default function MilestoneForm({
  isOpen,
  onClose,
  onSubmit,
  milestone,
}: MilestoneFormProps) {
  const [formData, setFormData] = useState<MilestoneCreate>({
    title: '',
    description: '',
    target_date: getTodayDateString(),
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  // Reset form when modal opens or milestone changes
  useEffect(() => {
    if (milestone) {
      setFormData({
        title: milestone.title,
        description: milestone.description,
        target_date: milestone.target_date,
      });
    } else {
      setFormData({
        title: '',
        description: '',
        target_date: getTodayDateString(),
      });
    }
    setErrors({});
  }, [milestone, isOpen]);

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.title.trim()) {
      newErrors.title = 'Título é obrigatório';
    }

    if (!formData.description.trim()) {
      newErrors.description = 'Descrição é obrigatória';
    }

    if (!formData.target_date) {
      newErrors.target_date = 'Data alvo é obrigatória';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) return;

    setIsSubmitting(true);
    try {
      await onSubmit(formData);
      onClose();
    } catch (error) {
      console.error('Error submitting milestone:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={milestone ? 'Editar Marco' : 'Adicionar Marco'}
      size="md"
    >
      <form onSubmit={handleSubmit}>
        <div className="space-y-4">
          {/* Title */}
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
              Título <span className="text-danger">*</span>
            </label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary ${
                errors.title ? 'border-danger' : 'border-gray-300'
              }`}
              placeholder="Ex: Defender tese de doutorado"
            />
            {errors.title && (
              <p className="mt-1 text-sm text-danger">{errors.title}</p>
            )}
          </div>

          {/* Description */}
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
              Descrição <span className="text-danger">*</span>
            </label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows={3}
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary ${
                errors.description ? 'border-danger' : 'border-gray-300'
              }`}
              placeholder="Descreva este marco"
            />
            {errors.description && (
              <p className="mt-1 text-sm text-danger">{errors.description}</p>
            )}
          </div>

          {/* Target Date */}
          <div>
            <label htmlFor="target_date" className="block text-sm font-medium text-gray-700 mb-1">
              Data Alvo <span className="text-danger">*</span>
            </label>
            <input
              type="date"
              id="target_date"
              name="target_date"
              value={formData.target_date}
              onChange={handleChange}
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary ${
                errors.target_date ? 'border-danger' : 'border-gray-300'
              }`}
            />
            {errors.target_date && (
              <p className="mt-1 text-sm text-danger">{errors.target_date}</p>
            )}
          </div>
        </div>

        <ModalFooter>
          <Button type="button" variant="secondary" onClick={onClose}>
            Cancelar
          </Button>
          <Button type="submit" isLoading={isSubmitting}>
            {milestone ? 'Salvar' : 'Criar'}
          </Button>
        </ModalFooter>
      </form>
    </Modal>
  );
}
