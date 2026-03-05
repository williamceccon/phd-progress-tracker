/**
 * Unit tests for MilestoneForm component.
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import MilestoneForm from '@/components/MilestoneForm';

describe('MilestoneForm', () => {
  const mockOnSubmit = vi.fn().mockResolvedValue(undefined);
  const mockOnClose = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders form fields when open', () => {
    render(
      <MilestoneForm
        isOpen={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
      />
    );

    expect(screen.getByLabelText(/título/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/descrição/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/data alvo/i)).toBeInTheDocument();
  });

  it('shows validation errors when submitting empty form', async () => {
    const user = userEvent.setup();
    
    render(
      <MilestoneForm
        isOpen={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
      />
    );

    // Clear the target date field which has a default value
    const targetDateInput = screen.getByLabelText(/data alvo/i);
    await user.clear(targetDateInput);

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
      <MilestoneForm
        isOpen={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
      />
    );

    // Fill in the form
    const titleInput = screen.getByLabelText(/título/i);
    const descInput = screen.getByLabelText(/descrição/i);
    
    await user.type(titleInput, 'Test Milestone');
    await user.type(descInput, 'Test Milestone Description');

    // Submit the form
    const submitButton = screen.getByRole('button', { name: /criar/i });
    await user.click(submitButton);

    // Check onSubmit was called with correct data
    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith(
        expect.objectContaining({
          title: 'Test Milestone',
          description: 'Test Milestone Description',
        })
      );
    });

    // Check modal closes
    expect(mockOnClose).toHaveBeenCalled();
  });

  it('populates form with existing milestone data in edit mode', () => {
    const existingMilestone = {
      id: '1',
      title: 'Existing Milestone',
      description: 'Existing Milestone Description',
      target_date: '2026-06-15',
      is_achieved: false,
    };

    render(
      <MilestoneForm
        isOpen={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
        milestone={existingMilestone}
      />
    );

    // Check form is pre-filled with existing data
    expect(screen.getByLabelText(/título/i)).toHaveValue('Existing Milestone');
    expect(screen.getByLabelText(/descrição/i)).toHaveValue('Existing Milestone Description');
    expect(screen.getByLabelText(/data alvo/i)).toHaveValue('2026-06-15');
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
      <MilestoneForm
        isOpen={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
      />
    );

    // Fill in the form
    const titleInput = screen.getByLabelText(/título/i);
    const descInput = screen.getByLabelText(/descrição/i);
    
    await user.type(titleInput, 'Test Milestone');
    await user.type(descInput, 'Test Milestone Description');

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
