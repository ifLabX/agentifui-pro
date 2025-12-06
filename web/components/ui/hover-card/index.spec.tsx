import { render, screen } from "@testing-library/react";

import "@testing-library/jest-dom";

import { HoverCard, HoverCardContent, HoverCardTrigger } from "./index";

describe("HoverCard", () => {
  test("renders trigger and content with slot attributes", () => {
    render(
      <HoverCard open>
        <HoverCardTrigger data-testid="trigger">Trigger</HoverCardTrigger>
        <HoverCardContent data-testid="content">
          Card details
        </HoverCardContent>
      </HoverCard>
    );

    expect(screen.getByTestId("trigger")).toHaveAttribute(
      "data-slot",
      "hover-card-trigger"
    );

    const content = screen.getByTestId("content");
    expect(content).toHaveAttribute("data-slot", "hover-card-content");
    expect(content.className).toContain("rounded-md");
  });

  test("supports alignment and custom styling", () => {
    render(
      <HoverCard open>
        <HoverCardTrigger>Trigger</HoverCardTrigger>
        <HoverCardContent
          align="start"
          sideOffset={8}
          className="custom-card"
        >
          Insights
        </HoverCardContent>
      </HoverCard>
    );

    const content = screen.getByText("Insights");
    expect(content).toHaveClass("custom-card");
    expect(content.className).toContain("data-[state=open]:animate-in");
  });
});
