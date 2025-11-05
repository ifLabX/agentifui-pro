import { createRef } from "react";
import { render, screen } from "@testing-library/react";

import "@testing-library/jest-dom";

import { Badge } from "./index";

describe("Badge", () => {
  test("renders with default variant", () => {
    render(<Badge>Default badge</Badge>);
    const badge = screen.getByText("Default badge");
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveClass("bg-primary", "text-primary-foreground");
  });

  test.each([
    ["secondary", ["bg-secondary", "text-secondary-foreground"]],
    ["destructive", ["bg-destructive", "text-destructive-foreground"]],
    ["outline", ["text-foreground", "border-border"]],
    ["success", ["bg-badge-success", "text-badge-success-foreground"]],
    ["warning", ["bg-badge-warning", "text-badge-warning-foreground"]],
    ["info", ["bg-badge-info", "text-badge-info-foreground"]],
    ["purple", ["bg-badge-purple", "text-badge-purple-foreground"]],
  ] as const)(
    "renders correctly with variant '%s'",
    (variant, expectedClasses) => {
      render(<Badge variant={variant}>{variant}</Badge>);
      const badge = screen.getByText(variant);
      expect(badge).toBeInTheDocument();
      expect(badge).toHaveClass(...expectedClasses);
    }
  );

  test("merges custom className correctly", () => {
    render(<Badge className="custom-class">Custom</Badge>);
    const badge = screen.getByText("Custom");
    expect(badge).toHaveClass("custom-class");
    expect(badge).toHaveClass("inline-flex");
  });

  test("passes through HTML attributes", () => {
    render(
      <Badge data-testid="test-badge" title="Test title">
        Badge
      </Badge>
    );
    const badge = screen.getByTestId("test-badge");
    expect(badge).toHaveAttribute("title", "Test title");
  });

  test("renders children correctly", () => {
    render(
      <Badge>
        <span>Icon</span> Text
      </Badge>
    );
    expect(screen.getByText("Icon")).toBeInTheDocument();
    expect(screen.getByText("Text")).toBeInTheDocument();
  });

  test("forwards ref correctly", () => {
    const ref = createRef<HTMLSpanElement>();
    render(<Badge ref={ref}>Badge with ref</Badge>);
    expect(ref.current).toBeInstanceOf(HTMLSpanElement);
    expect(ref.current).toHaveTextContent("Badge with ref");
  });
});
