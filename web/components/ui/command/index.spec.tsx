import { render, screen } from "@testing-library/react";

import "@testing-library/jest-dom";

import { DialogDescription, DialogTitle } from "../dialog";
import {
  Command,
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
  CommandShortcut,
} from "./index";

describe("Command", () => {
  test("merges custom class with defaults", () => {
    const { container } = render(
      <Command className="custom-class" loop>
        <CommandInput placeholder="Search…" />
        <CommandList>
          <CommandItem>Option</CommandItem>
        </CommandList>
      </Command>
    );

    const root = container.querySelector("[cmdk-root]");
    expect(root).toBeInTheDocument();
    expect(root).toHaveClass("custom-class");
    expect(root?.className).toContain("flex");
  });

  test("renders dialog variant with command props and close button", () => {
    render(
      <CommandDialog
        open
        showCloseButton
        commandProps={{ className: "inner-command", loop: true }}
      >
        <DialogTitle>Palette</DialogTitle>
        <DialogDescription className="sr-only">
          Dialog description for accessibility
        </DialogDescription>
        <CommandInput placeholder="Filter options" />
        <CommandList>
          <CommandGroup heading="Group">
            <CommandItem value="first">
              First
              <CommandShortcut>⌘F</CommandShortcut>
            </CommandItem>
          </CommandGroup>
          <CommandSeparator />
        </CommandList>
      </CommandDialog>
    );

    const root = document.querySelector("[cmdk-root]");
    expect(root).toHaveClass("inner-command");
    expect(screen.getByRole("button", { name: /close/i })).toBeInTheDocument();
    expect(screen.getByText("⌘F")).toHaveClass(
      "ml-auto",
      "text-xs",
      "tracking-widest"
    );
  });

  test("shows empty state when no command items match", () => {
    const { container } = render(
      <Command>
        <CommandList>
          <CommandEmpty>No items</CommandEmpty>
        </CommandList>
      </Command>
    );

    const emptyState = container.querySelector("[cmdk-empty]");
    expect(emptyState).toHaveTextContent("No items");
  });
});
