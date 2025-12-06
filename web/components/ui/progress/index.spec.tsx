import { render, screen } from "@testing-library/react";

import "@testing-library/jest-dom";

import { Progress } from "./index";

describe("Progress", () => {
  test("renders progress indicator with calculated transform", () => {
    render(<Progress value={45} data-testid="progress" />);

    const indicator = screen
      .getByTestId("progress")
      .querySelector('[data-slot="progress-indicator"]');

    expect(indicator).toHaveStyle({ transform: "translateX(-55%)" });
    expect(indicator?.className).toContain("bg-primary");
  });

  test("defaults to zero progress when value is not provided", () => {
    render(<Progress data-testid="progress" />);

    const indicator = screen
      .getByTestId("progress")
      .querySelector('[data-slot="progress-indicator"]');

    expect(indicator).toHaveStyle({ transform: "translateX(-100%)" });
  });
});
