import { render, screen } from "@testing-library/react";

import "@testing-library/jest-dom";

import { Textarea } from "./index";

describe("Textarea", () => {
  test("renders with textarea slot and base styling", () => {
    render(<Textarea placeholder="Write here" data-testid="textarea" />);

    const textarea = screen.getByTestId("textarea");
    expect(textarea).toHaveAttribute("data-slot", "textarea");
    expect(textarea.className).toContain("rounded-md");
    expect(textarea.className).toContain("min-h-16");
  });

  test("applies aria-invalid attribute for error state", () => {
    render(<Textarea aria-invalid placeholder="Email" />);

    const textarea = screen.getByPlaceholderText("Email");
    expect(textarea).toHaveAttribute("aria-invalid", "true");
    expect(textarea.className).toContain("aria-invalid:border-destructive");
  });

  test("merges consumer provided class names", () => {
    render(
      <Textarea placeholder="Notes" className="custom-textarea" rows={5} />
    );

    expect(screen.getByPlaceholderText("Notes")).toHaveClass("custom-textarea");
  });
});
