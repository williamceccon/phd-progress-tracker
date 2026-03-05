/**
 * Unit tests for Modal component.
 */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Modal from '@/components/Modal';

describe('Modal', () => {
  const mockOnClose = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    // Clean up any open modals
    document.body.style.overflow = 'unset';
  });

  it('does not render when closed', () => {
    render(
      <Modal isOpen={false} onClose={mockOnClose} title="Test Modal">
        <p>Modal content</p>
      </Modal>
    );

    expect(screen.queryByText('Test Modal')).not.toBeInTheDocument();
    expect(screen.queryByText('Modal content')).not.toBeInTheDocument();
  });

  it('renders when open', () => {
    render(
      <Modal isOpen={true} onClose={mockOnClose} title="Test Modal">
        <p>Modal content</p>
      </Modal>
    );

    expect(screen.getByText('Test Modal')).toBeInTheDocument();
    expect(screen.getByText('Modal content')).toBeInTheDocument();
  });

  it('closes on ESC key press', async () => {
    render(
      <Modal isOpen={true} onClose={mockOnClose} title="Test Modal">
        <p>Modal content</p>
      </Modal>
    );

    // Press ESC key
    fireEvent.keyDown(document, { key: 'Escape' });

    await waitFor(() => {
      expect(mockOnClose).toHaveBeenCalled();
    });
  });

  it('closes on backdrop click', async () => {
    render(
      <Modal isOpen={true} onClose={mockOnClose} title="Test Modal">
        <p>Modal content</p>
      </Modal>
    );

    // Click on the backdrop (not on the modal content)
    const backdrop = document.querySelector('.bg-black');
    if (backdrop) {
      fireEvent.click(backdrop);
    }

    await waitFor(() => {
      expect(mockOnClose).toHaveBeenCalled();
    });
  });

  it('does not close when clicking inside modal content', async () => {
    render(
      <Modal isOpen={true} onClose={mockOnClose} title="Test Modal">
        <p>Modal content</p>
      </Modal>
    );

    // Click on the modal content
    const modalContent = screen.getByText('Modal content');
    fireEvent.click(modalContent);

    // onClose should not be called
    expect(mockOnClose).not.toHaveBeenCalled();
  });

  it('renders children correctly', () => {
    render(
      <Modal isOpen={true} onClose={mockOnClose} title="Test Modal">
        <div data-testid="child-component">Child Content</div>
      </Modal>
    );

    expect(screen.getByTestId('child-component')).toBeInTheDocument();
    expect(screen.getByText('Child Content')).toBeInTheDocument();
  });

  it('renders with different sizes', () => {
    const { rerender } = render(
      <Modal isOpen={true} onClose={mockOnClose} title="Small Modal" size="sm">
        <p>Small content</p>
      </Modal>
    );

    // Small size
    let modal = document.querySelector('.max-w-md');
    expect(modal).toBeInTheDocument();

    // Medium size
    rerender(
      <Modal isOpen={true} onClose={mockOnClose} title="Medium Modal" size="md">
        <p>Medium content</p>
      </Modal>
    );
    modal = document.querySelector('.max-w-lg');
    expect(modal).toBeInTheDocument();

    // Large size
    rerender(
      <Modal isOpen={true} onClose={mockOnClose} title="Large Modal" size="lg">
        <p>Large content</p>
      </Modal>
    );
    modal = document.querySelector('.max-w-2xl');
    expect(modal).toBeInTheDocument();
  });

  it('closes on X button click', async () => {
    render(
      <Modal isOpen={true} onClose={mockOnClose} title="Test Modal">
        <p>Modal content</p>
      </Modal>
    );

    // Click the close button
    const closeButton = screen.getByRole('button');
    fireEvent.click(closeButton);

    await waitFor(() => {
      expect(mockOnClose).toHaveBeenCalled();
    });
  });

  it('sets body overflow to hidden when open', () => {
    render(
      <Modal isOpen={true} onClose={mockOnClose} title="Test Modal">
        <p>Modal content</p>
      </Modal>
    );

    expect(document.body.style.overflow).toBe('hidden');
  });

  it('resets body overflow when closed', () => {
    const { unmount } = render(
      <Modal isOpen={true} onClose={mockOnClose} title="Test Modal">
        <p>Modal content</p>
      </Modal>
    );

    unmount();
    expect(document.body.style.overflow).toBe('unset');
  });
});
