"use client";

import { useState } from "react";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";

import { Button } from "@/components/ui/button";

import {
  Popover,
  PopoverBody,
  PopoverClose,
  PopoverContent,
  PopoverItem,
  PopoverTrigger,
} from ".";

function UncontrolledPopoverExample() {
  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button data-testid="trigger">Open</Button>
      </PopoverTrigger>
      <PopoverContent data-testid="content">
        <PopoverBody>
          <PopoverItem data-testid="item">Action</PopoverItem>
        </PopoverBody>
      </PopoverContent>
    </Popover>
  );
}

function ControlledPopoverExample() {
  const [open, setOpen] = useState(false);

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button data-testid="controlled-trigger">
          {open ? "Close" : "Open"}
        </Button>
      </PopoverTrigger>
      <PopoverContent data-testid="controlled-content">
        <PopoverBody>
          <PopoverItem
            data-testid="controlled-item"
            onClick={() => {
              setOpen(false);
            }}
          >
            Controlled action
          </PopoverItem>
        </PopoverBody>
      </PopoverContent>
    </Popover>
  );
}

function AsChildHandlerExample({ onSelect }: { onSelect: () => void }) {
  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button data-testid="custom-trigger" onClick={onSelect}>
          Custom trigger
        </Button>
      </PopoverTrigger>
      <PopoverContent data-testid="custom-content">
        <PopoverBody>
          <PopoverItem data-testid="custom-item">Inner item</PopoverItem>
        </PopoverBody>
      </PopoverContent>
    </Popover>
  );
}

function DefaultTriggerExample() {
  return (
    <Popover>
      <PopoverTrigger data-testid="default-trigger">Toggle</PopoverTrigger>
      <PopoverContent data-testid="default-content">
        <PopoverBody>
          <PopoverItem>Inner item</PopoverItem>
        </PopoverBody>
      </PopoverContent>
    </Popover>
  );
}

function MatchWidthExample() {
  return (
    <Popover matchTriggerWidth>
      <PopoverTrigger asChild>
        <Button data-testid="width-trigger" style={{ width: "200px" }}>
          Match width
        </Button>
      </PopoverTrigger>
      <PopoverContent data-testid="width-content">
        <PopoverBody>
          <PopoverItem>Width item</PopoverItem>
        </PopoverBody>
      </PopoverContent>
    </Popover>
  );
}

function ModalPopoverExample() {
  return (
    <Popover modal>
      <PopoverTrigger asChild>
        <Button data-testid="modal-trigger">Open modal</Button>
      </PopoverTrigger>
      <PopoverContent data-testid="modal-content">
        <PopoverBody>
          <PopoverItem>Modal option</PopoverItem>
        </PopoverBody>
        <PopoverClose data-testid="modal-close">Cancel</PopoverClose>
      </PopoverContent>
    </Popover>
  );
}

describe("Popover", () => {
  it("toggles open/close in uncontrolled mode", () => {
    render(<UncontrolledPopoverExample />);
    const trigger = screen.getByTestId("trigger");

    expect(screen.queryByTestId("content")).not.toBeInTheDocument();

    fireEvent.click(trigger);
    expect(screen.getByTestId("content")).toBeInTheDocument();

    fireEvent.click(trigger);
    expect(screen.queryByTestId("content")).not.toBeInTheDocument();
  });

  it("respects controlled mode state", () => {
    render(<ControlledPopoverExample />);

    const trigger = screen.getByTestId("controlled-trigger");

    fireEvent.click(trigger);
    expect(screen.getByTestId("controlled-content")).toBeInTheDocument();

    fireEvent.click(screen.getByTestId("controlled-item"));
    expect(screen.queryByTestId("controlled-content")).not.toBeInTheDocument();
  });

  it("preserves custom handler when using asChild", () => {
    const handler = jest.fn();
    render(<AsChildHandlerExample onSelect={handler} />);

    const trigger = screen.getByTestId("custom-trigger");

    fireEvent.click(trigger);
    expect(handler).toHaveBeenCalledTimes(1);
    expect(screen.getByTestId("custom-content")).toBeInTheDocument();
  });

  it("handles default trigger without asChild", () => {
    render(<DefaultTriggerExample />);

    const trigger = screen.getByTestId("default-trigger");
    expect(trigger).toHaveAttribute("data-state", "closed");
    expect(screen.queryByTestId("default-content")).not.toBeInTheDocument();

    fireEvent.click(trigger);
    expect(trigger).toHaveAttribute("data-state", "open");
    expect(screen.getByTestId("default-content")).toBeInTheDocument();
  });

  it("matches trigger width when matchTriggerWidth is set", async () => {
    const originalGetBoundingClientRect =
      HTMLElement.prototype.getBoundingClientRect;
    HTMLElement.prototype.getBoundingClientRect = function () {
      if (
        this instanceof HTMLButtonElement &&
        this.dataset.testid === "width-trigger"
      ) {
        return {
          width: 200,
          height: 40,
          top: 0,
          left: 0,
          bottom: 40,
          right: 200,
          x: 0,
          y: 0,
          toJSON: () => {},
        } as DOMRect;
      }
      return originalGetBoundingClientRect.call(this);
    };

    try {
      render(<MatchWidthExample />);

      const trigger = screen.getByTestId("width-trigger");
      fireEvent.click(trigger);

      const content = screen.getByTestId("width-content");
      expect(content.firstElementChild).toBeInTheDocument();

      await waitFor(() => {
        expect(content).toHaveStyle({ width: "200px" });
      });
    } finally {
      HTMLElement.prototype.getBoundingClientRect =
        originalGetBoundingClientRect;
    }
  });

  it("renders overlay when modal is true and PopoverClose closes content", () => {
    render(<ModalPopoverExample />);

    const trigger = screen.getByTestId("modal-trigger");
    fireEvent.click(trigger);

    const overlay = document.querySelector(
      "[data-state='open'][class*='backdrop']"
    );
    expect(overlay).not.toBeNull();
    expect(screen.getByTestId("modal-content")).toBeInTheDocument();

    fireEvent.click(screen.getByTestId("modal-close"));
    expect(screen.queryByTestId("modal-content")).not.toBeInTheDocument();
  });
});
