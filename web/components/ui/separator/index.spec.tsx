import { render, screen } from "@testing-library/react";

import "@testing-library/jest-dom";

import { Separator } from "./index";

describe("Separator", () => {
  test("renders a decorative horizontal separator by default", () => {
    render(<Separator data-testid="separator" />);

    const separator = screen.getByTestId("separator");
    expect(separator).toHaveAttribute("data-slot", "separator");
    expect(separator.className).toContain("data-[orientation=horizontal]:h-px");
    expect(separator.className).toContain("data-[orientation=horizontal]:w-full");
    expect(separator.getAttribute("role")).not.toBe("separator");
  });

  test("supports accessible vertical separators", () => {
    render(
      <Separator
        orientation="vertical"
        decorative={false}
        data-testid="vertical-separator"
      />
    );

    const separator = screen.getByTestId("vertical-separator");
    expect(separator).toHaveAttribute("role", "separator");
    expect(separator).toHaveAttribute("aria-orientation", "vertical");
    expect(separator.className).toContain("data-[orientation=vertical]:w-px");
  });

  test("merges custom class names", () => {
    render(<Separator className="custom-border" data-testid="custom" />);

    const separator = screen.getByTestId("custom");
    expect(separator).toHaveClass("custom-border");
  });
});
