import { render, screen } from "@testing-library/react";

import "@testing-library/jest-dom";

import Divider from "./index";

describe("Divider", () => {
  it("renders a decorative horizontal divider by default", () => {
    render(<Divider data-testid="divider" />);
    const divider = screen.getByTestId("divider");

    expect(divider).toHaveAttribute("data-orientation", "horizontal");
    expect(divider).not.toHaveAttribute("aria-labelledby");
    expect(divider.className).toContain("w-full");
  });

  it("creates an accessible labelled divider with aria linkage", () => {
    const { container } = render(<Divider label="Overview" />);

    const labelElement = screen.getByText("Overview");
    const separators = container.querySelectorAll('[role="separator"]');

    expect(separators).toHaveLength(1);

    const accessibleSeparator = separators[0];
    const labelledById = accessibleSeparator.getAttribute("aria-labelledby");

    expect(labelledById).toEqual(labelElement.id);
    expect(accessibleSeparator).not.toHaveAttribute("aria-hidden", "true");

    const decorativeSegments = container.querySelectorAll(
      '[aria-hidden="true"]'
    );
    expect(decorativeSegments.length).toBeGreaterThanOrEqual(2);
  });

  it("keeps labelled content-length separators visible without flex fill", () => {
    const { container } = render(<Divider label="Overview" length="content" />);

    const decorativeSegments = container.querySelectorAll(
      '[aria-hidden="true"]'
    );
    expect(decorativeSegments).toHaveLength(2);
    decorativeSegments.forEach(segment => {
      expect(segment).toHaveClass("min-w-8");
      expect(segment).not.toHaveClass("flex-1");
    });
  });

  it("supports vertical layout with inset padding and content length", () => {
    render(
      <Divider
        orientation="vertical"
        length="content"
        inset="md"
        label="Details"
        labelPosition="start"
      />
    );

    const labelElement = screen.getByText("Details");
    const wrapper = labelElement.parentElement;

    expect(wrapper).toHaveClass("flex-col");
    expect(wrapper).toHaveClass("py-6");
    expect(wrapper).toHaveClass("h-fit");

    const decorativeSegments = wrapper?.querySelectorAll(
      '[aria-hidden="true"]'
    );
    expect(decorativeSegments?.length).toBe(1);
    if (decorativeSegments?.[0]) {
      expect(decorativeSegments[0]).toHaveClass("min-h-8");
      expect(decorativeSegments[0]).not.toHaveClass("flex-1");
    }
  });

  it("forwards separator props to the accessible root when labelled", () => {
    const { container } = render(
      <Divider
        label="Overview"
        aria-describedby="details"
        data-testid="divider"
      />
    );

    const wrapper = screen.getByTestId("divider");
    expect(wrapper).toBeTruthy();
    expect(wrapper).not.toHaveAttribute("aria-describedby");

    const accessibleSeparator = container.querySelector('[role="separator"]');
    expect(accessibleSeparator).toHaveAttribute("aria-describedby", "details");

    expect(accessibleSeparator).not.toHaveAttribute("data-testid");
    expect(wrapper).toContainElement(accessibleSeparator);
  });
});
