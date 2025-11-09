import { fireEvent, render, screen } from "@testing-library/react";

import {
  DEFAULT_SECONDARY_ARIA_LABEL,
  SplitButton,
  type SplitButtonAction,
} from ".";

const primary = (overrides: Partial<SplitButtonAction> = {}) => ({
  label: "Primary",
  onClick: jest.fn(),
  ...overrides,
});

const secondary = (overrides: Partial<SplitButtonAction> = {}) => ({
  label: "More",
  onClick: jest.fn(),
  ...overrides,
});

describe("SplitButton", () => {
  it("renders primary and secondary labels", () => {
    render(
      <SplitButton primaryAction={primary()} secondaryAction={secondary()} />
    );

    expect(screen.getByRole("button", { name: "Primary" })).toBeEnabled();
    expect(screen.getByRole("button", { name: "More" })).toBeEnabled();
  });

  it("calls provided handlers when segments are clicked", () => {
    const onPrimary = jest.fn();
    const onSecondary = jest.fn();

    render(
      <SplitButton
        primaryAction={{ label: "Save", onClick: onPrimary }}
        secondaryAction={{ label: "Options", onClick: onSecondary }}
      />
    );

    fireEvent.click(screen.getByRole("button", { name: "Save" }));
    fireEvent.click(screen.getByRole("button", { name: "Options" }));

    expect(onPrimary).toHaveBeenCalledTimes(1);
    expect(onSecondary).toHaveBeenCalledTimes(1);
  });

  it("disables both segments when disabled prop is set", () => {
    render(
      <SplitButton
        primaryAction={{ label: "Submit" }}
        secondaryAction={{ label: "Schedule" }}
        disabled
      />
    );

    expect(screen.getByRole("button", { name: "Submit" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "Schedule" })).toBeDisabled();
  });

  it("renders default secondary action when none is provided", () => {
    render(<SplitButton primaryAction={{ label: "Deploy" }} />);

    expect(
      screen.getByLabelText(DEFAULT_SECONDARY_ARIA_LABEL)
    ).toBeInTheDocument();
  });

  it("expands to full width when requested", () => {
    const { container } = render(
      <SplitButton
        primaryAction={{ label: "Run" }}
        secondaryAction={{ label: "More" }}
        fullWidth
      />
    );

    expect(container.firstChild).toHaveClass("split-button--block");
  });
});
