/**
 * Unit tests for TaskForm component.
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import TaskForm from '@/components/TaskForm';

describe('TaskForm', () => {
  const mockOnSubmit = vi.fn().mockResolvedValue(undefined);
  const mockOnClose = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders form fields when open', async () => {
    render(
      <TaskForm
        isOpen={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
      />
    );

    expect(screen.getByLabelText(/título/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/descrição/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/data limite/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/categoria/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/prioridade/i)).toBeInTheDocument();
  });

  it('shows validation errors when submitting empty form', async () => {
    const user = userEvent.setup();
    
    render(
      <TaskForm
        isOpen={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
      />
    );

    // Clear the deadline field which has a default value
    const deadlineInput = screen.getByLabelText(/data limite/i);
    await user.clear(deadlineInput);

    // Click the submit button
    const submitButton = screen.getByRole('button', { name: /criar/i });
    await user.click(submitButton);

    // Check for validation error messages
    await waitFor(() => {
      expect(screen.getByText(/título é obrigatório/i)).toBeInTheDocument();
      expect(screen.getByText(/descrição é obrigatória/i)).toBeInTheDocument();
    });

    // onSubmit should not be called
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it('calls onSubmit with valid data', async () => {
    const user = userEvent.setup();
    
    render(
      <TaskForm
        isOpen={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
      />
    );

    // Fill in the form
    const titleInput = screen.getByLabelText(/título/i);
    const descInput = screen.getByLabelText(/descrição/i);
    
    await user.type(titleInput, 'Test Task');
    await user.type(descInput, 'Test Description');

    // Submit the form
    const submitButton = screen.getByRole('button', { name: /criar/i });
    await user.click(submitButton);

    // Check onSubmit was called with correct data
    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith(
        expect.objectContaining({
          title: 'Test Task',
          description: 'Test Description',
        })
      );
    });

    // Check modal closes
    expect(mockOnClose).toHaveBeenCalled();
  });

  it('populates form with existing task data in edit mode', () => {
    const existingTask = {
      id: '1',
      title: 'Existing Task',
      description: 'Existing Description',
      deadline: '2026-03-15',
      status: 'A Fazer' as const,
      priority: 'Alta' as const,
      category: 'Escrita',
      created_at: '2026-01-01T10:00:00',
      completed_at: null,
    };

    render(
      <TaskForm
        isOpen={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
        task={existingTask}
      />
    );

    // Check form is pre-filled with existing data
    expect(screen.getByLabelText(/título/i)).toHaveValue('Existing Task');
    expect(screen.getByLabelText(/descrição/i)).toHaveValue('Existing Description');
    expect(screen.getByLabelText(/data limite/i)).toHaveValue('2026-03-15');
  });

  it('shows loading state when submitting', async () => {
    // Create a promise that we can control
    let resolveSubmit: () => void;
    const submitPromise = new Promise<void>((resolve) => {
      resolveSubmit = resolve;
    });
    
    mockOnSubmit.mockReturnValue(submitPromise);
    
    const user = userEvent.setup();
    
    render(
      <TaskForm
        isOpen={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
      />
    );

    // Fill in the form
    const titleInput = screen.getByLabelText(/título/i);
    const descInput = screen.getByLabelText(/descrição/i);
    
    await user.type(titleInput, 'Test Task');
    await user.type(descInput, 'Test Description');

    // Submit the form
    const submitButton = screen.getByRole('button', { name: /criar/i });
    await user.click(submitButton);

    // Check button shows loading state
    expect(submitButton).toBeDisabled();

    // Resolve the promise
    resolveSubmit!();
    
    await waitFor(() => {
      expect(submitButton).not.toBeDisabled();
    });
  });
});
