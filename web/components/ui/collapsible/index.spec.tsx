import { fireEvent, render, screen } from "@testing-library/react";

import "@testing-library/jest-dom";

import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "./index";

describe("Collapsible", () => {
  test("toggles open state when the trigger is clicked", () => {
    const handleOpenChange = jest.fn();

    render(
      <Collapsible onOpenChange={handleOpenChange}>
        <CollapsibleTrigger>Toggle</CollapsibleTrigger>
        <CollapsibleContent>Hidden content</CollapsibleContent>
      </Collapsible>
    );

    const trigger = screen.getByRole("button", { name: /toggle/i });

    fireEvent.click(trigger);
    expect(handleOpenChange).toHaveBeenCalledWith(true);

    fireEvent.click(trigger);
    expect(handleOpenChange).toHaveBeenCalledWith(false);
  });

  test("exposes slot attributes for trigger and content", () => {
    render(
      <Collapsible open>
        <CollapsibleTrigger data-testid="trigger">Trigger</CollapsibleTrigger>
        <CollapsibleContent data-testid="content">
          Panel content
        </CollapsibleContent>
      </Collapsible>
    );

    expect(screen.getByTestId("trigger")).toHaveAttribute(
      "data-slot",
      "collapsible-trigger"
    );

    const content = screen.getByTestId("content");
    expect(content).toHaveAttribute("data-slot", "collapsible-content");
    expect(content.getAttribute("data-state")).toBe("open");
  });
});
