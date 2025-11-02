import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { AlertDialog } from "./index";

describe("AlertDialog", () => {
  it("renders when open is true", async () => {
    render(
      <AlertDialog
        open={true}
        title="Test Alert"
        description="This is a test alert"
      />
    );

    await waitFor(() => {
      expect(screen.getByText("Test Alert")).toBeInTheDocument();
      expect(screen.getByText("This is a test alert")).toBeInTheDocument();
    });
  });

  it("does not render when open is false", () => {
    render(
      <AlertDialog
        open={false}
        title="Test Alert"
        description="This is a test alert"
      />
    );

    expect(screen.queryByText("Test Alert")).not.toBeInTheDocument();
  });

  it("renders default button text", async () => {
    render(
      <AlertDialog
        open={true}
        title="Test Alert"
        description="This is a test alert"
      />
    );

    await waitFor(() => {
      expect(screen.getByText("Confirm")).toBeInTheDocument();
      expect(screen.getByText("Cancel")).toBeInTheDocument();
    });
  });

  it("renders custom button text", async () => {
    render(
      <AlertDialog
        open={true}
        title="Test Alert"
        description="This is a test alert"
        confirmText="Yes, proceed"
        cancelText="No, go back"
      />
    );

    await waitFor(() => {
      expect(screen.getByText("Yes, proceed")).toBeInTheDocument();
      expect(screen.getByText("No, go back")).toBeInTheDocument();
    });
  });

  it("calls onOpenChange when cancel is clicked", async () => {
    const user = userEvent.setup();
    const handleOpenChange = jest.fn();

    render(
      <AlertDialog
        open={true}
        onOpenChange={handleOpenChange}
        title="Test Alert"
        description="This is a test alert"
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
      <AlertDialog
        open={true}
        onOpenChange={handleOpenChange}
        onConfirm={handleConfirm}
        title="Test Alert"
        description="This is a test alert"
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
      <AlertDialog
        open={true}
        onOpenChange={handleOpenChange}
        onConfirm={handleConfirm}
        title="Test Alert"
        description="This is a test alert"
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

  it("shows loading state when isLoading is true", async () => {
    render(
      <AlertDialog
        open={true}
        isLoading={true}
        title="Test Alert"
        description="This is a test alert"
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
      <AlertDialog
        open={true}
        showCloseButton={false}
        title="Test Alert"
        description="This is a test alert"
      />
    );

    await waitFor(() => {
      expect(screen.getByText("Test Alert")).toBeInTheDocument();
    });

    expect(screen.queryByLabelText("Close dialog")).not.toBeInTheDocument();
  });

  it("uses custom close button label", async () => {
    render(
      <AlertDialog
        open={true}
        closeButtonLabel="Dismiss alert"
        title="Test Alert"
        description="This is a test alert"
      />
    );

    await waitFor(() => {
      expect(screen.getByLabelText("Dismiss alert")).toBeInTheDocument();
    });
  });

  it("renders trigger child when provided", async () => {
    const user = userEvent.setup();
    const handleOpenChange = jest.fn();

    render(
      <AlertDialog
        open={false}
        onOpenChange={handleOpenChange}
        title="Test Alert"
        description="This is a test alert"
      >
        <button>Open Alert</button>
      </AlertDialog>
    );

    expect(screen.getByText("Open Alert")).toBeInTheDocument();

    await user.click(screen.getByText("Open Alert"));

    expect(handleOpenChange).toHaveBeenCalledWith(true);
  });
});
