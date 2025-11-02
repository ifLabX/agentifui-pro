import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "./index";

describe("BaseDialog", () => {
  it("renders dialog trigger button", () => {
    render(
      <Dialog>
        <DialogTrigger>Open Dialog</DialogTrigger>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Test Dialog</DialogTitle>
          </DialogHeader>
        </DialogContent>
      </Dialog>
    );

    expect(screen.getByText("Open Dialog")).toBeInTheDocument();
  });

  it("opens dialog when trigger is clicked", async () => {
    const user = userEvent.setup();
    render(
      <Dialog>
        <DialogTrigger>Open Dialog</DialogTrigger>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Test Dialog</DialogTitle>
            <DialogDescription>This is a test description</DialogDescription>
          </DialogHeader>
        </DialogContent>
      </Dialog>
    );

    const trigger = screen.getByText("Open Dialog");
    await user.click(trigger);

    await waitFor(() => {
      expect(screen.getByText("Test Dialog")).toBeInTheDocument();
      expect(
        screen.getByText("This is a test description")
      ).toBeInTheDocument();
    });
  });

  it("closes dialog when close button is clicked", async () => {
    const user = userEvent.setup();
    render(
      <Dialog>
        <DialogTrigger>Open Dialog</DialogTrigger>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Test Dialog</DialogTitle>
          </DialogHeader>
        </DialogContent>
      </Dialog>
    );

    await user.click(screen.getByText("Open Dialog"));

    await waitFor(() => {
      expect(screen.getByText("Test Dialog")).toBeInTheDocument();
    });

    const closeButton = screen.getByLabelText("Close dialog");
    await user.click(closeButton);

    await waitFor(() => {
      expect(screen.queryByText("Test Dialog")).not.toBeInTheDocument();
    });
  });

  it("does not render close button when showCloseButton is false", async () => {
    const user = userEvent.setup();
    render(
      <Dialog>
        <DialogTrigger>Open Dialog</DialogTrigger>
        <DialogContent showCloseButton={false}>
          <DialogHeader>
            <DialogTitle>Test Dialog</DialogTitle>
          </DialogHeader>
        </DialogContent>
      </Dialog>
    );

    await user.click(screen.getByText("Open Dialog"));

    await waitFor(() => {
      expect(screen.getByText("Test Dialog")).toBeInTheDocument();
    });

    expect(screen.queryByLabelText("Close dialog")).not.toBeInTheDocument();
  });

  it("uses custom close button label", async () => {
    const user = userEvent.setup();
    render(
      <Dialog>
        <DialogTrigger>Open Dialog</DialogTrigger>
        <DialogContent closeButtonLabel="Dismiss">
          <DialogHeader>
            <DialogTitle>Test Dialog</DialogTitle>
          </DialogHeader>
        </DialogContent>
      </Dialog>
    );

    await user.click(screen.getByText("Open Dialog"));

    await waitFor(() => {
      expect(screen.getByLabelText("Dismiss")).toBeInTheDocument();
    });
  });

  it("renders dialog footer correctly", async () => {
    const user = userEvent.setup();
    render(
      <Dialog>
        <DialogTrigger>Open Dialog</DialogTrigger>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Test Dialog</DialogTitle>
          </DialogHeader>
          <DialogFooter>
            <button>Cancel</button>
            <button>Confirm</button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    );

    await user.click(screen.getByText("Open Dialog"));

    await waitFor(() => {
      expect(screen.getByText("Cancel")).toBeInTheDocument();
      expect(screen.getByText("Confirm")).toBeInTheDocument();
    });
  });

  it("handles controlled open state", async () => {
    const onOpenChange = jest.fn();
    const { rerender } = render(
      <Dialog open={false} onOpenChange={onOpenChange}>
        <DialogTrigger>Open Dialog</DialogTrigger>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Test Dialog</DialogTitle>
          </DialogHeader>
        </DialogContent>
      </Dialog>
    );

    expect(screen.queryByText("Test Dialog")).not.toBeInTheDocument();

    rerender(
      <Dialog open={true} onOpenChange={onOpenChange}>
        <DialogTrigger>Open Dialog</DialogTrigger>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Test Dialog</DialogTitle>
          </DialogHeader>
        </DialogContent>
      </Dialog>
    );

    await waitFor(() => {
      expect(screen.getByText("Test Dialog")).toBeInTheDocument();
    });
  });

  it("calls DialogClose callback when close trigger is used", async () => {
    const user = userEvent.setup();
    const handleClose = jest.fn();

    render(
      <Dialog>
        <DialogTrigger>Open Dialog</DialogTrigger>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Test Dialog</DialogTitle>
          </DialogHeader>
          <DialogClose asChild>
            <button onClick={handleClose}>Custom Close</button>
          </DialogClose>
        </DialogContent>
      </Dialog>
    );

    await user.click(screen.getByText("Open Dialog"));

    await waitFor(() => {
      expect(screen.getByText("Test Dialog")).toBeInTheDocument();
    });

    await user.click(screen.getByText("Custom Close"));

    expect(handleClose).toHaveBeenCalled();
  });
});
