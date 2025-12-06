import { fireEvent, render, screen } from "@testing-library/react";

import "@testing-library/jest-dom";

import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupInput,
  InputGroupTextarea,
  InputGroupText,
} from "./index";

describe("InputGroup", () => {
  test("focuses the input when clicking on an addon", () => {
    render(
      <InputGroup>
        <InputGroupAddon data-testid="addon">
          <InputGroupText>+1</InputGroupText>
        </InputGroupAddon>
        <InputGroupInput placeholder="Phone" />
      </InputGroup>
    );

    const input = screen.getByPlaceholderText("Phone");
    expect(document.activeElement).not.toBe(input);

    fireEvent.click(screen.getByTestId("addon"));
    expect(document.activeElement).toBe(input);
  });

  test("does not steal focus when clicking an interactive child", () => {
    render(
      <InputGroup>
        <InputGroupAddon>
          <InputGroupButton data-testid="inner-button" size="icon-sm">
            ↵
          </InputGroupButton>
        </InputGroupAddon>
        <InputGroupInput placeholder="Search" />
      </InputGroup>
    );

    const innerButton = screen.getByTestId("inner-button");
    fireEvent.click(innerButton);

    expect(screen.getByPlaceholderText("Search")).not.toHaveFocus();
  });

  test("supports textarea controls and block alignment", () => {
    render(
      <InputGroup>
        <InputGroupAddon data-testid="block-addon" align="block-start">
          Label
        </InputGroupAddon>
        <InputGroupTextarea aria-label="Description" />
      </InputGroup>
    );

    const addon = screen.getByTestId("block-addon");
    expect(addon).toHaveAttribute("data-align", "block-start");
    expect(addon.className).toContain("w-full");

    const textarea = screen.getByLabelText("Description");
    expect(textarea).toHaveAttribute("data-slot", "input-group-control");
    expect(textarea.className).toContain("resize-none");
  });

  test("applies size token to embedded buttons", () => {
    render(
      <InputGroupButton data-testid="group-button" size="icon-xs">
        Run
      </InputGroupButton>
    );

    const button = screen.getByTestId("group-button");
    expect(button).toHaveAttribute("data-size", "icon-xs");
    expect(button.className).toContain("rounded-");
  });
});
