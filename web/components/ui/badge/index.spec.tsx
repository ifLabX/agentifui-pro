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
    ["secondary", "bg-secondary"],
    ["destructive", "bg-destructive"],
    ["outline", "text-foreground"],
    ["success", "bg-emerald-100"],
    ["warning", "bg-amber-100"],
    ["info", "bg-blue-100"],
    ["purple", "bg-purple-100"],
  ] as const)(
    "renders correctly with variant '%s'",
    (variant, expectedClass) => {
      render(<Badge variant={variant}>{variant}</Badge>);
      const badge = screen.getByText(variant);
      expect(badge).toBeInTheDocument();
      expect(badge).toHaveClass(expectedClass);
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
    const ref = { current: null as HTMLDivElement | null };
    render(<Badge ref={ref}>Badge with ref</Badge>);
    expect(ref.current).toBeInstanceOf(HTMLDivElement);
    expect(ref.current).toHaveTextContent("Badge with ref");
  });
});
