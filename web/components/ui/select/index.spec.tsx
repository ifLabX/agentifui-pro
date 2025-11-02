import { render, screen } from "@testing-library/react";

import "@testing-library/jest-dom";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./index";

describe("Select", () => {
  test("renders trigger with placeholder text", () => {
    render(
      <Select>
        <SelectTrigger data-testid="select-trigger">
          <SelectValue placeholder="Choose tool" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="linear">Linear</SelectItem>
        </SelectContent>
      </Select>
    );

    expect(screen.getByTestId("select-trigger")).toHaveTextContent(
      "Choose tool"
    );
  });

  test("merges custom class on content and hides scroll indicators", () => {
    render(
      <Select open onOpenChange={() => {}}>
        <SelectTrigger>
          <SelectValue placeholder="Pick option" />
        </SelectTrigger>
        <SelectContent
          className="custom-content"
          hideScrollIndicators
          position="popper"
        >
          <SelectItem value="one">One</SelectItem>
        </SelectContent>
      </Select>
    );

    const content = screen.getByRole("listbox");
    expect(content).toHaveClass("custom-content");
    expect(content.className).toContain("translate");
  });

  test("renders item with custom indicator, leading icon and description", () => {
    render(
      <Select open value="two" onValueChange={() => {}} onOpenChange={() => {}}>
        <SelectTrigger>
          <SelectValue placeholder="Pick option" />
        </SelectTrigger>
        <SelectContent hideScrollIndicators>
          <SelectItem
            value="two"
            leadingIcon={<span data-testid="lead">★</span>}
            description="Secondary line"
            indicator={<span data-testid="indicator">✓</span>}
          >
            Option Two
          </SelectItem>
        </SelectContent>
      </Select>
    );

    expect(
      screen.getByRole("option", { name: "Option Two" })
    ).toBeInTheDocument();
    expect(screen.getByTestId("lead")).toBeInTheDocument();
    expect(screen.getByText("Secondary line")).toHaveClass(
      "text-xs",
      "text-muted-foreground"
    );
    expect(screen.getByTestId("indicator")).toBeInTheDocument();
  });
});
