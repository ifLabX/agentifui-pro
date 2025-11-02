import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { InputDialog } from "./index";

describe("InputDialog", () => {
  it("renders when open is true", async () => {
    render(
      <InputDialog
        open={true}
        title="Test Input"
        label="Name"
        placeholder="Enter name"
      />
    );

    await waitFor(() => {
      expect(screen.getByText("Test Input")).toBeInTheDocument();
      expect(screen.getByText("Name")).toBeInTheDocument();
      expect(screen.getByPlaceholderText("Enter name")).toBeInTheDocument();
    });
  });

  it("does not render when open is false", () => {
    render(
      <InputDialog
        open={false}
        title="Test Input"
        label="Name"
        placeholder="Enter name"
      />
    );

    expect(screen.queryByText("Test Input")).not.toBeInTheDocument();
  });

  it("renders description when provided", async () => {
    render(
      <InputDialog
        open={true}
        title="Test Input"
        description="This is a test description"
        label="Name"
        placeholder="Enter name"
      />
    );

    await waitFor(() => {
      expect(
        screen.getByText("This is a test description")
      ).toBeInTheDocument();
    });
  });

  it("renders default button text", async () => {
    render(
      <InputDialog
        open={true}
        title="Test Input"
        label="Name"
        placeholder="Enter name"
      />
    );

    await waitFor(() => {
      expect(screen.getByText("Save changes")).toBeInTheDocument();
      expect(screen.getByText("Cancel")).toBeInTheDocument();
    });
  });

  it("renders custom button text", async () => {
    render(
      <InputDialog
        open={true}
        title="Test Input"
        label="Name"
        placeholder="Enter name"
        confirmText="Submit"
        cancelText="Discard"
      />
    );

    await waitFor(() => {
      expect(screen.getByText("Submit")).toBeInTheDocument();
      expect(screen.getByText("Discard")).toBeInTheDocument();
    });
  });

  it("sets default value in input", async () => {
    render(
      <InputDialog
        open={true}
        title="Test Input"
        label="Name"
        defaultValue="John Doe"
        placeholder="Enter name"
      />
    );

    await waitFor(() => {
      const input = screen.getByDisplayValue("John Doe");
      expect(input).toBeInTheDocument();
    });
  });

  it("calls onOpenChange when cancel is clicked", async () => {
    const user = userEvent.setup();
    const handleOpenChange = jest.fn();

    render(
      <InputDialog
        open={true}
        onOpenChange={handleOpenChange}
        title="Test Input"
        label="Name"
        placeholder="Enter name"
      />
    );

    await waitFor(() => {
      expect(screen.getByText("Cancel")).toBeInTheDocument();
    });

    await user.click(screen.getByText("Cancel"));

    expect(handleOpenChange).toHaveBeenCalledWith(false);
  });

  it("calls onConfirm with trimmed value when form is submitted", async () => {
    const user = userEvent.setup();
    const handleConfirm = jest.fn();
    const handleOpenChange = jest.fn();

    render(
      <InputDialog
        open={true}
        onOpenChange={handleOpenChange}
        onConfirm={handleConfirm}
        title="Test Input"
        label="Name"
        placeholder="Enter name"
      />
    );

    await waitFor(() => {
      expect(screen.getByPlaceholderText("Enter name")).toBeInTheDocument();
    });

    const input = screen.getByPlaceholderText("Enter name");
    await user.type(input, "  Test Value  ");
    await user.click(screen.getByText("Save changes"));

    await waitFor(() => {
      expect(handleConfirm).toHaveBeenCalledWith("Test Value");
      expect(handleOpenChange).toHaveBeenCalledWith(false);
    });
  });

  it("submits form when Enter is pressed", async () => {
    const user = userEvent.setup();
    const handleConfirm = jest.fn();

    render(
      <InputDialog
        open={true}
        onConfirm={handleConfirm}
        title="Test Input"
        label="Name"
        placeholder="Enter name"
      />
    );

    await waitFor(() => {
      expect(screen.getByPlaceholderText("Enter name")).toBeInTheDocument();
    });

    const input = screen.getByPlaceholderText("Enter name");
    await user.type(input, "Test Value{enter}");

    await waitFor(() => {
      expect(handleConfirm).toHaveBeenCalledWith("Test Value");
    });
  });

  it("does not submit when input is empty", async () => {
    const user = userEvent.setup();
    const handleConfirm = jest.fn();

    render(
      <InputDialog
        open={true}
        onConfirm={handleConfirm}
        title="Test Input"
        label="Name"
        placeholder="Enter name"
      />
    );

    await waitFor(() => {
      expect(screen.getByText("Save changes")).toBeInTheDocument();
    });

    const submitButton = screen.getByText("Save changes");
    expect(submitButton).toBeDisabled();

    await user.click(submitButton);

    expect(handleConfirm).not.toHaveBeenCalled();
  });

  it("does not submit when input is only whitespace", async () => {
    const user = userEvent.setup();
    const handleConfirm = jest.fn();

    render(
      <InputDialog
        open={true}
        onConfirm={handleConfirm}
        title="Test Input"
        label="Name"
        placeholder="Enter name"
      />
    );

    await waitFor(() => {
      expect(screen.getByPlaceholderText("Enter name")).toBeInTheDocument();
    });

    const input = screen.getByPlaceholderText("Enter name");
    await user.type(input, "   ");

    const submitButton = screen.getByText("Save changes");
    expect(submitButton).toBeDisabled();
  });

  it("handles async onConfirm callback", async () => {
    const user = userEvent.setup();
    const handleConfirm = jest.fn(
      () => new Promise<void>(resolve => setTimeout(resolve, 100))
    );
    const handleOpenChange = jest.fn();

    render(
      <InputDialog
        open={true}
        onOpenChange={handleOpenChange}
        onConfirm={handleConfirm}
        title="Test Input"
        label="Name"
        placeholder="Enter name"
      />
    );

    await waitFor(() => {
      expect(screen.getByPlaceholderText("Enter name")).toBeInTheDocument();
    });

    const input = screen.getByPlaceholderText("Enter name");
    await user.type(input, "Test Value");
    await user.click(screen.getByText("Save changes"));

    expect(screen.getByText("Loading...")).toBeInTheDocument();

    await waitFor(() => {
      expect(handleConfirm).toHaveBeenCalledWith("Test Value");
      expect(handleOpenChange).toHaveBeenCalledWith(false);
    });
  });

  it("respects maxLength prop", async () => {
    const user = userEvent.setup();

    render(
      <InputDialog
        open={true}
        title="Test Input"
        label="Name"
        placeholder="Enter name"
        maxLength={10}
      />
    );

    await waitFor(() => {
      expect(screen.getByPlaceholderText("Enter name")).toBeInTheDocument();
    });

    const input = screen.getByPlaceholderText("Enter name") as HTMLInputElement;
    await user.type(input, "12345678901234567890");

    // Input should only contain 10 characters
    expect(input.value.length).toBeLessThanOrEqual(10);
  });

  it("shows loading state when isLoading is true", async () => {
    render(
      <InputDialog
        open={true}
        isLoading={true}
        title="Test Input"
        label="Name"
        placeholder="Enter name"
      />
    );

    await waitFor(() => {
      expect(screen.getByText("Loading...")).toBeInTheDocument();
    });

    const input = screen.getByPlaceholderText("Enter name");
    const submitButton = screen.getByText("Loading...");
    const cancelButton = screen.getByText("Cancel");

    expect(input).toBeDisabled();
    expect(submitButton).toBeDisabled();
    expect(cancelButton).toBeDisabled();
  });

  it("does not show close button when showCloseButton is false", async () => {
    render(
      <InputDialog
        open={true}
        showCloseButton={false}
        title="Test Input"
        label="Name"
        placeholder="Enter name"
      />
    );

    await waitFor(() => {
      expect(screen.getByText("Test Input")).toBeInTheDocument();
    });

    expect(screen.queryByLabelText("Close dialog")).not.toBeInTheDocument();
  });

  it("uses custom close button label", async () => {
    render(
      <InputDialog
        open={true}
        closeButtonLabel="Dismiss input dialog"
        title="Test Input"
        label="Name"
        placeholder="Enter name"
      />
    );

    await waitFor(() => {
      expect(screen.getByLabelText("Dismiss input dialog")).toBeInTheDocument();
    });
  });

  it("renders trigger child when provided", async () => {
    const user = userEvent.setup();
    const handleOpenChange = jest.fn();

    render(
      <InputDialog
        open={false}
        onOpenChange={handleOpenChange}
        title="Test Input"
        label="Name"
        placeholder="Enter name"
      >
        <button>Open Input</button>
      </InputDialog>
    );

    expect(screen.getByText("Open Input")).toBeInTheDocument();

    await user.click(screen.getByText("Open Input"));

    expect(handleOpenChange).toHaveBeenCalledWith(true);
  });

  it("resets input value when dialog reopens", async () => {
    const { rerender } = render(
      <InputDialog
        open={true}
        title="Test Input"
        label="Name"
        placeholder="Enter name"
        defaultValue="Initial"
      />
    );

    await waitFor(() => {
      expect(screen.getByDisplayValue("Initial")).toBeInTheDocument();
    });

    rerender(
      <InputDialog
        open={false}
        title="Test Input"
        label="Name"
        placeholder="Enter name"
        defaultValue="Initial"
      />
    );

    rerender(
      <InputDialog
        open={true}
        title="Test Input"
        label="Name"
        placeholder="Enter name"
        defaultValue="Updated"
      />
    );

    await waitFor(() => {
      expect(screen.getByDisplayValue("Updated")).toBeInTheDocument();
    });
  });
});
