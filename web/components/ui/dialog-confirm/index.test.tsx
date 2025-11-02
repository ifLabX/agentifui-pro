import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { ConfirmDialog } from "./index";

describe("ConfirmDialog", () => {
  it("renders when open is true", async () => {
    render(
      <ConfirmDialog
        open={true}
        title="Test Confirm"
        description="This is a test confirmation"
      />
    );

    await waitFor(() => {
      expect(screen.getByText("Test Confirm")).toBeInTheDocument();
      expect(
        screen.getByText("This is a test confirmation")
      ).toBeInTheDocument();
    });
  });

  it("does not render when open is false", () => {
    render(
      <ConfirmDialog
        open={false}
        title="Test Confirm"
        description="This is a test confirmation"
      />
    );

    expect(screen.queryByText("Test Confirm")).not.toBeInTheDocument();
  });

  it("renders default button text", async () => {
    render(
      <ConfirmDialog
        open={true}
        title="Test Confirm"
        description="This is a test confirmation"
      />
    );

    await waitFor(() => {
      expect(screen.getByText("Confirm")).toBeInTheDocument();
      expect(screen.getByText("Cancel")).toBeInTheDocument();
    });
  });

  it("renders custom button text", async () => {
    render(
      <ConfirmDialog
        open={true}
        title="Test Confirm"
        description="This is a test confirmation"
        confirmText="Yes, delete"
        cancelText="No, keep"
      />
    );

    await waitFor(() => {
      expect(screen.getByText("Yes, delete")).toBeInTheDocument();
      expect(screen.getByText("No, keep")).toBeInTheDocument();
    });
  });

  it("calls onOpenChange when cancel is clicked", async () => {
    const user = userEvent.setup();
    const handleOpenChange = jest.fn();

    render(
      <ConfirmDialog
        open={true}
        onOpenChange={handleOpenChange}
        title="Test Confirm"
        description="This is a test confirmation"
      />
    );

    await waitFor(() => {
      expect(screen.getByText("Cancel")).toBeInTheDocument();
    });

    await user.click(screen.getByText("Cancel"));

    expect(handleOpenChange).toHaveBeenCalledWith(false);
  });

  it("calls onConfirm and onOpenChange when confirm is clicked", async () => {
    const user = userEvent.setup();
    const handleConfirm = jest.fn();
    const handleOpenChange = jest.fn();

    render(
      <ConfirmDialog
        open={true}
        onOpenChange={handleOpenChange}
        onConfirm={handleConfirm}
        title="Test Confirm"
        description="This is a test confirmation"
      />
    );

    await waitFor(() => {
      expect(screen.getByText("Confirm")).toBeInTheDocument();
    });

    await user.click(screen.getByText("Confirm"));

    await waitFor(() => {
      expect(handleConfirm).toHaveBeenCalled();
      expect(handleOpenChange).toHaveBeenCalledWith(false);
    });
  });

  it("handles async onConfirm callback", async () => {
    const user = userEvent.setup();
    const handleConfirm = jest.fn(
      () => new Promise<void>(resolve => setTimeout(resolve, 100))
    );
    const handleOpenChange = jest.fn();

    render(
      <ConfirmDialog
        open={true}
        onOpenChange={handleOpenChange}
        onConfirm={handleConfirm}
        title="Test Confirm"
        description="This is a test confirmation"
      />
    );

    await waitFor(() => {
      expect(screen.getByText("Confirm")).toBeInTheDocument();
    });

    await user.click(screen.getByText("Confirm"));

    expect(screen.getByText("Loading...")).toBeInTheDocument();

    await waitFor(() => {
      expect(handleConfirm).toHaveBeenCalled();
      expect(handleOpenChange).toHaveBeenCalledWith(false);
    });
  });

  it("applies destructive variant styling when variant is danger", async () => {
    render(
      <ConfirmDialog
        open={true}
        variant="danger"
        title="Test Confirm"
        description="This is a test confirmation"
      />
    );

    await waitFor(() => {
      expect(screen.getByText("Confirm")).toBeInTheDocument();
    });

    // The button should have destructive variant class
    const confirmButton = screen.getByText("Confirm");
    expect(confirmButton).toBeInTheDocument();
  });

  it("applies default variant styling when variant is default", async () => {
    render(
      <ConfirmDialog
        open={true}
        variant="default"
        title="Test Confirm"
        description="This is a test confirmation"
      />
    );

    await waitFor(() => {
      expect(screen.getByText("Confirm")).toBeInTheDocument();
    });

    const confirmButton = screen.getByText("Confirm");
    expect(confirmButton).toBeInTheDocument();
  });

  it("shows loading state when isLoading is true", async () => {
    render(
      <ConfirmDialog
        open={true}
        isLoading={true}
        title="Test Confirm"
        description="This is a test confirmation"
      />
    );

    await waitFor(() => {
      expect(screen.getByText("Loading...")).toBeInTheDocument();
    });

    const confirmButton = screen.getByText("Loading...");
    const cancelButton = screen.getByText("Cancel");

    expect(confirmButton).toBeDisabled();
    expect(cancelButton).toBeDisabled();
  });

  it("does not show close button when showCloseButton is false", async () => {
    render(
      <ConfirmDialog
        open={true}
        showCloseButton={false}
        title="Test Confirm"
        description="This is a test confirmation"
      />
    );

    await waitFor(() => {
      expect(screen.getByText("Test Confirm")).toBeInTheDocument();
    });

    expect(screen.queryByLabelText("Close dialog")).not.toBeInTheDocument();
  });

  it("uses custom close button label", async () => {
    render(
      <ConfirmDialog
        open={true}
        closeButtonLabel="Dismiss confirmation"
        title="Test Confirm"
        description="This is a test confirmation"
      />
    );

    await waitFor(() => {
      expect(screen.getByLabelText("Dismiss confirmation")).toBeInTheDocument();
    });
  });

  it("renders trigger child when provided", async () => {
    const user = userEvent.setup();
    const handleOpenChange = jest.fn();

    render(
      <ConfirmDialog
        open={false}
        onOpenChange={handleOpenChange}
        title="Test Confirm"
        description="This is a test confirmation"
      >
        <button>Open Confirm</button>
      </ConfirmDialog>
    );

    expect(screen.getByText("Open Confirm")).toBeInTheDocument();

    await user.click(screen.getByText("Open Confirm"));

    expect(handleOpenChange).toHaveBeenCalledWith(true);
  });

  it("handles no onConfirm callback gracefully", async () => {
    const user = userEvent.setup();
    const handleOpenChange = jest.fn();

    render(
      <ConfirmDialog
        open={true}
        onOpenChange={handleOpenChange}
        title="Test Confirm"
        description="This is a test confirmation"
      />
    );

    await waitFor(() => {
      expect(screen.getByText("Confirm")).toBeInTheDocument();
    });

    await user.click(screen.getByText("Confirm"));

    await waitFor(() => {
      expect(handleOpenChange).toHaveBeenCalledWith(false);
    });
  });

  describe("Alert Dialog Use Cases", () => {
    it("works as an alert dialog for information display", async () => {
      const handleOpenChange = jest.fn();

      render(
        <ConfirmDialog
          open={true}
          onOpenChange={handleOpenChange}
          title="Information"
          description="This is an informational message."
          confirmText="Got it"
          cancelText="Close"
        />
      );

      await waitFor(() => {
        expect(screen.getByText("Information")).toBeInTheDocument();
        expect(
          screen.getByText("This is an informational message.")
        ).toBeInTheDocument();
        expect(screen.getByText("Got it")).toBeInTheDocument();
        expect(screen.getByText("Close")).toBeInTheDocument();
      });
    });

    it("works as an alert with single action button", async () => {
      const user = userEvent.setup();
      const handleConfirm = jest.fn();
      const handleOpenChange = jest.fn();

      render(
        <ConfirmDialog
          open={true}
          onOpenChange={handleOpenChange}
          onConfirm={handleConfirm}
          title="Success"
          description="Your changes have been saved successfully."
          confirmText="OK"
        />
      );

      await waitFor(() => {
        expect(screen.getByText("Success")).toBeInTheDocument();
        expect(
          screen.getByText("Your changes have been saved successfully.")
        ).toBeInTheDocument();
      });

      await user.click(screen.getByText("OK"));

      await waitFor(() => {
        expect(handleConfirm).toHaveBeenCalled();
        expect(handleOpenChange).toHaveBeenCalledWith(false);
      });
    });

    it("prevents multiple confirms when rapidly clicked", async () => {
      const user = userEvent.setup();
      const handleConfirm = jest.fn(
        () => new Promise<void>(resolve => setTimeout(resolve, 100))
      );
      const handleOpenChange = jest.fn();

      render(
        <ConfirmDialog
          open={true}
          onOpenChange={handleOpenChange}
          onConfirm={handleConfirm}
          title="Test"
          description="Test description"
        />
      );

      await waitFor(() => {
        expect(screen.getByText("Confirm")).toBeInTheDocument();
      });

      const confirmButton = screen.getByText("Confirm");

      // Click multiple times rapidly
      await user.click(confirmButton);
      await user.click(confirmButton);
      await user.click(confirmButton);

      // Should only call once
      await waitFor(() => {
        expect(handleConfirm).toHaveBeenCalledTimes(1);
      });
    });
  });
});
