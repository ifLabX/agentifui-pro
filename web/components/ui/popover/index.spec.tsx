import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import "@testing-library/jest-dom";

import { Popover, PopoverContent, PopoverTrigger } from "./index";

describe("Popover", () => {
  describe("Rendering", () => {
    test("renders popover content when open", () => {
      render(
        <Popover open>
          <PopoverTrigger>Open</PopoverTrigger>
          <PopoverContent>Popover content</PopoverContent>
        </Popover>
      );

      expect(screen.getByText("Popover content")).toBeInTheDocument();
    });

    test("does not render content when closed", () => {
      render(
        <Popover open={false}>
          <PopoverTrigger>Open</PopoverTrigger>
          <PopoverContent>Popover content</PopoverContent>
        </Popover>
      );

      expect(screen.queryByText("Popover content")).not.toBeInTheDocument();
    });
  });

  describe("Interaction", () => {
    test("trigger toggles popover visibility", async () => {
      const user = userEvent.setup();
      render(
        <Popover>
          <PopoverTrigger>Open popover</PopoverTrigger>
          <PopoverContent>Popover content</PopoverContent>
        </Popover>
      );

      expect(screen.queryByText("Popover content")).not.toBeInTheDocument();

      await user.click(screen.getByText("Open popover"));
      expect(screen.getByText("Popover content")).toBeInTheDocument();

      await user.click(screen.getByText("Open popover"));
      await waitFor(() =>
        expect(screen.queryByText("Popover content")).not.toBeInTheDocument()
      );
    });

    test("closes when clicking outside", async () => {
      const user = userEvent.setup();
      render(
        <div>
          <Popover>
            <PopoverTrigger>Open popover</PopoverTrigger>
            <PopoverContent>Popover content</PopoverContent>
          </Popover>
          <button>Outside button</button>
        </div>
      );

      await user.click(screen.getByText("Open popover"));
      expect(screen.getByText("Popover content")).toBeInTheDocument();

      await user.click(screen.getByText("Outside button"));
      await waitFor(() =>
        expect(screen.queryByText("Popover content")).not.toBeInTheDocument()
      );
    });
  });

  describe("Controlled state", () => {
    test("respects controlled open state", async () => {
      const onOpenChange = jest.fn();
      const user = userEvent.setup();

      render(
        <Popover open={false} onOpenChange={onOpenChange}>
          <PopoverTrigger>Open popover</PopoverTrigger>
          <PopoverContent>Popover content</PopoverContent>
        </Popover>
      );

      await user.click(screen.getByText("Open popover"));
      expect(onOpenChange).toHaveBeenCalledWith(true);
    });
  });

  describe("Styling", () => {
    test("applies custom className to content", () => {
      render(
        <Popover open>
          <PopoverTrigger>Open</PopoverTrigger>
          <PopoverContent className="custom-class">Content</PopoverContent>
        </Popover>
      );

      const content = screen.getByText("Content");
      expect(content).toHaveClass("custom-class");
    });

    test("renders with default styling classes", () => {
      render(
        <Popover open>
          <PopoverTrigger>Open</PopoverTrigger>
          <PopoverContent>Content</PopoverContent>
        </Popover>
      );

      const content = screen.getByText("Content");
      expect(content).toHaveClass("z-50", "rounded-md", "border", "shadow-md");
    });
  });
});
