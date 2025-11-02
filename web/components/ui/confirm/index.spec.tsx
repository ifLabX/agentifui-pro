import { fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import "@testing-library/jest-dom";

import { ConfirmDialog } from "./index";

describe("ConfirmDialog", () => {
  const baseProps = {
    open: true,
    title: "Confirm action",
    description: "Are you sure?",
    onConfirm: jest.fn(),
    onCancel: jest.fn(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("renders destructive variant with icon and extra content", () => {
    render(
      <ConfirmDialog
        {...baseProps}
        variant="destructive"
        icon={<span data-testid="icon">!</span>}
        confirmText="Delete"
      >
        <p>Additional context</p>
      </ConfirmDialog>
    );

    expect(screen.getByText("Confirm action")).toHaveClass("text-destructive");
    expect(screen.getByText("Additional context")).toBeInTheDocument();
    expect(screen.getByTestId("icon").parentElement).toHaveClass(
      "bg-destructive/15",
      "text-destructive"
    );
  });

  test("invokes onConfirm when confirm button is clicked", () => {
    render(<ConfirmDialog {...baseProps} confirmText="Continue" />);

    fireEvent.click(screen.getByRole("button", { name: "Continue" }));
    expect(baseProps.onConfirm).toHaveBeenCalledTimes(1);
    expect(baseProps.onCancel).not.toHaveBeenCalled();
  });

  test("calls onCancel when dialog requests close", async () => {
    const user = userEvent.setup();
    render(<ConfirmDialog {...baseProps} />);

    await user.keyboard("{Escape}");

    expect(baseProps.onCancel).toHaveBeenCalledTimes(1);
  });

  test("disables cancel path when disableCancel is true", async () => {
    const user = userEvent.setup();
    render(<ConfirmDialog {...baseProps} disableCancel cancelText="Go back" />);

    const cancelButton = screen.getByRole("button", { name: "Go back" });
    expect(cancelButton).toBeDisabled();
    fireEvent.click(cancelButton);
    expect(baseProps.onCancel).not.toHaveBeenCalled();

    await user.keyboard("{Escape}");
    expect(baseProps.onCancel).not.toHaveBeenCalled();
  });

  test("prevents closing while loading", async () => {
    const user = userEvent.setup();
    render(<ConfirmDialog {...baseProps} isLoading />);

    const confirmButton = screen.getByRole("button", { name: "Processing..." });
    expect(confirmButton).toBeDisabled();

    await user.keyboard("{Escape}");
    expect(baseProps.onCancel).not.toHaveBeenCalled();
  });
});
