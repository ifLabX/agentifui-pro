import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import "@testing-library/jest-dom";

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

describe("Dialog primitives", () => {
  test("renders dialog content when open", () => {
    render(
      <Dialog open>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Dialog title</DialogTitle>
            <DialogDescription>Dialog description</DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <button type="button">Close</button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    );

    expect(screen.getByText("Dialog title")).toBeInTheDocument();
    expect(screen.getByText("Dialog description")).toBeInTheDocument();
  });

  test("does not render close button when showCloseButton is false", () => {
    render(
      <Dialog open>
        <DialogContent showCloseButton={false}>
          <DialogHeader>
            <DialogTitle className="sr-only">Hidden title</DialogTitle>
            <DialogDescription className="sr-only">
              Hidden description
            </DialogDescription>
          </DialogHeader>
          <div>Body</div>
        </DialogContent>
      </Dialog>
    );

    expect(
      screen.queryByRole("button", { name: /close/i })
    ).not.toBeInTheDocument();
  });

  test("trigger toggles dialog visibility with overlay and custom close", async () => {
    const user = userEvent.setup();
    render(
      <Dialog>
        <DialogTrigger>Open dialog</DialogTrigger>
        <DialogContent showCloseButton={false}>
          <DialogHeader>
            <DialogTitle>Interactive dialog</DialogTitle>
            <DialogDescription>Helper text</DialogDescription>
          </DialogHeader>
          <div>Body</div>
          <DialogClose>Dismiss</DialogClose>
        </DialogContent>
      </Dialog>
    );

    await user.click(screen.getByText("Open dialog"));
    expect(screen.getByRole("dialog")).toBeInTheDocument();
    const overlay = document.querySelector("[data-slot='dialog-overlay']");
    expect(overlay).toHaveClass("fixed", "inset-0");

    await user.click(screen.getByText("Dismiss"));
    await waitFor(() =>
      expect(screen.queryByRole("dialog")).not.toBeInTheDocument()
    );
  });
});
