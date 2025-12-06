import { render } from "@testing-library/react";

import "@testing-library/jest-dom";

import { ScrollArea, ScrollBar } from "./index";

describe("ScrollArea", () => {
  test("renders viewport and scrollbar slots", () => {
    render(
      <ScrollArea type="always" className="h-16 w-24">
        <div style={{ height: "160px" }}>Scrollable content</div>
      </ScrollArea>
    );

    const root = document.querySelector('[data-slot="scroll-area"]');
    const viewport = document.querySelector(
      '[data-slot="scroll-area-viewport"]'
    );
    const scrollbar = document.querySelector(
      '[data-slot="scroll-area-scrollbar"]'
    );

    expect(root).toBeInTheDocument();
    expect(viewport?.className).toContain("rounded-[inherit]");
    expect(scrollbar).toHaveAttribute("data-orientation", "vertical");
  });

  test("supports horizontal scrollbars with orientation styling", () => {
    render(
      <ScrollArea type="always" className="h-24 w-24">
        <div style={{ width: "240px" }}>Long content</div>
        <ScrollBar orientation="horizontal" data-testid="horizontal-bar" />
      </ScrollArea>
    );

    const scrollbar = document.querySelector(
      '[data-testid="horizontal-bar"]'
    );
    expect(scrollbar).toHaveAttribute("data-slot", "scroll-area-scrollbar");
    expect(scrollbar).toHaveAttribute("data-orientation", "horizontal");
    expect(scrollbar?.className).toContain("flex-col");
  });
});
