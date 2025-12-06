import { render, screen } from "@testing-library/react";

import "@testing-library/jest-dom";

import {
  ButtonGroup,
  ButtonGroupSeparator,
  ButtonGroupText,
} from "./index";

describe("ButtonGroup", () => {
  test("renders a horizontal grouped control with role semantics", () => {
    render(
      <ButtonGroup
        orientation="horizontal"
        data-testid="button-group"
        className="custom-group"
      >
        <button type="button">Create</button>
        <button type="button">Edit</button>
      </ButtonGroup>
    );

    const group = screen.getByTestId("button-group");
    expect(group).toHaveAttribute("role", "group");
    expect(group).toHaveAttribute("data-slot", "button-group");
    expect(group).toHaveAttribute("data-orientation", "horizontal");
    expect(group.className).toContain("flex");
    expect(group).toHaveClass("custom-group");
  });

  test("supports vertical orientation for stacked actions", () => {
    render(
      <ButtonGroup orientation="vertical">
        <button type="button">Top</button>
        <button type="button">Bottom</button>
      </ButtonGroup>
    );

    const group = screen.getByRole("group");
    expect(group).toHaveAttribute("data-orientation", "vertical");
    expect(group.className).toContain("flex-col");
  });

  test("forwards typography styles to child nodes when rendered asChild", () => {
    render(
      <ButtonGroupText asChild>
        <span data-testid="label">Schedule</span>
      </ButtonGroupText>
    );

    const label = screen.getByTestId("label");
    expect(label.className).toContain("bg-muted");
    expect(label.className).toContain("rounded-md");
  });

  test("renders separators that inherit orientation styles", () => {
    render(
      <ButtonGroup orientation="horizontal">
        <button type="button">One</button>
        <ButtonGroupSeparator data-testid="separator" />
        <button type="button">Two</button>
      </ButtonGroup>
    );

    const separator = screen.getByTestId("separator");
    expect(separator).toHaveAttribute("data-slot", "button-group-separator");
    expect(separator.className).toContain("self-stretch");
  });
});
