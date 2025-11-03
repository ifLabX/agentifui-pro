import { createRef } from "react";
import { render, screen } from "@testing-library/react";

import "@testing-library/jest-dom";

import { Input } from "./index";

describe("Input", () => {
  it("renders with base classes and default type", () => {
    render(<Input placeholder="Full name" />);

    const input = screen.getByPlaceholderText("Full name");
    expect(input).toHaveAttribute("type", "text");
    expect(input).toHaveClass("flex", "h-9", "border", "bg-input-background");
    expect(input.className).toContain("placeholder:text-input-placeholder");
  });

  it("merges custom class names", () => {
    render(<Input placeholder="Email" className="custom-class" />);

    const input = screen.getByPlaceholderText("Email");
    expect(input).toHaveClass("custom-class");
  });

  it("includes disabled and invalid styling hooks", () => {
    render(<Input placeholder="Username" disabled aria-invalid="true" />);

    const input = screen.getByPlaceholderText("Username");
    expect(input.className).toContain("disabled:bg-input-disabled");
    expect(input.className).toContain(
      "aria-[invalid=true]:border-input-invalid"
    );
  });

  it("forwards refs to the underlying input element", () => {
    const ref = createRef<HTMLInputElement>();
    render(<Input ref={ref} placeholder="Ref target" />);

    expect(ref.current).toBeInstanceOf(HTMLInputElement);
  });
});
