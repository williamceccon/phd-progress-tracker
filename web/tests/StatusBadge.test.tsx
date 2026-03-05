/**
 * Unit tests for StatusBadge component.
 */
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import StatusBadge from '@/components/StatusBadge';

describe('StatusBadge', () => {
  describe('Status variants', () => {
    it('renders A Fazer status with gray styling', () => {
      render(<StatusBadge variant="status" value="A Fazer" />);
      
      const badge = screen.getByText('A Fazer');
      expect(badge).toHaveClass('bg-gray-100', 'text-gray-700');
    });

    it('renders Em Progresso status with amber styling', () => {
      render(<StatusBadge variant="status" value="Em Progresso" />);
      
      const badge = screen.getByText('Em Progresso');
      expect(badge).toHaveClass('bg-amber-100', 'text-amber-700');
    });

    it('renders Concluída status with green styling', () => {
      render(<StatusBadge variant="status" value="Concluída" />);
      
      const badge = screen.getByText('Concluída');
      expect(badge).toHaveClass('bg-green-100', 'text-green-700');
    });

    it('renders Bloqueada status with red styling', () => {
      render(<StatusBadge variant="status" value="Bloqueada" />);
      
      const badge = screen.getByText('Bloqueada');
      expect(badge).toHaveClass('bg-red-100', 'text-red-700');
    });
  });

  describe('Priority variants', () => {
    it('renders Baixa priority with light gray styling', () => {
      render(<StatusBadge variant="priority" value="Baixa" />);
      
      const badge = screen.getByText('Baixa');
      expect(badge).toHaveClass('bg-gray-100', 'text-gray-600');
    });

    it('renders Média priority with blue styling', () => {
      render(<StatusBadge variant="priority" value="Média" />);
      
      const badge = screen.getByText('Média');
      expect(badge).toHaveClass('bg-blue-100', 'text-blue-700');
    });

    it('renders Alta priority with orange styling', () => {
      render(<StatusBadge variant="priority" value="Alta" />);
      
      const badge = screen.getByText('Alta');
      expect(badge).toHaveClass('bg-orange-100', 'text-orange-700');
    });

    it('renders Crítica priority with red styling', () => {
      render(<StatusBadge variant="priority" value="Crítica" />);
      
      const badge = screen.getByText('Crítica');
      expect(badge).toHaveClass('bg-red-100', 'text-red-700');
    });
  });

  describe('Category variant', () => {
    it('renders category with purple styling', () => {
      render(<StatusBadge variant="category" value="RSL" />);
      
      const badge = screen.getByText('RSL');
      expect(badge).toHaveClass('bg-purple-100', 'text-purple-700');
    });

    it('renders unknown category with default styling', () => {
      render(<StatusBadge variant="category" value="Unknown" />);
      
      const badge = screen.getByText('Unknown');
      expect(badge).toHaveClass('bg-purple-100', 'text-purple-700');
    });
  });

  it('renders with correct base classes', () => {
    render(<StatusBadge variant="status" value="A Fazer" />);
    
    const badge = screen.getByText('A Fazer');
    expect(badge).toHaveClass('inline-flex', 'items-center', 'px-2.5', 'py-0.5', 'rounded-full', 'text-xs', 'font-medium');
  });

  it('renders unknown status with default styling', () => {
    render(<StatusBadge variant="status" value="Unknown Status" />);
    
    const badge = screen.getByText('Unknown Status');
    expect(badge).toHaveClass('bg-gray-100', 'text-gray-700');
  });
});
