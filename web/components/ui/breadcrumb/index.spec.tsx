import { render, screen } from "@testing-library/react";

import "@testing-library/jest-dom";

import {
  Breadcrumb,
  BreadcrumbEllipsis,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "./index";

describe("Breadcrumb", () => {
  test("renders with default aria-label and nested structure", () => {
    render(
      <Breadcrumb>
        <BreadcrumbList>
          <BreadcrumbItem>
            <BreadcrumbLink href="/">Home</BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator />
          <BreadcrumbItem>
            <BreadcrumbPage>Dashboard</BreadcrumbPage>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>
    );

    const nav = screen.getByRole("navigation");
    expect(nav).toHaveAttribute("aria-label", "Breadcrumb");
    expect(screen.getByText("Home")).toBeInTheDocument();
    expect(screen.getByText("Dashboard")).toHaveAttribute(
      "aria-current",
      "page"
    );
  });

  test("BreadcrumbList and BreadcrumbItem merge custom class names", () => {
    const { container } = render(
      <Breadcrumb>
        <BreadcrumbList className="custom-list">
          <BreadcrumbItem className="custom-item">
            <BreadcrumbPage>Only page</BreadcrumbPage>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>
    );

    const list = container.querySelector("ol");
    expect(list).toHaveClass("custom-list");
    expect(list?.className).toContain("flex");

    const item = container.querySelector("li");
    expect(item).toHaveClass("custom-item");
    expect(item?.className).toContain("inline-flex");
  });

  test("BreadcrumbLink supports rendering via Slot when asChild is true", () => {
    render(
      <Breadcrumb>
        <BreadcrumbList>
          <BreadcrumbItem>
            <BreadcrumbLink asChild className="custom-link">
              <button type="button">Trigger</button>
            </BreadcrumbLink>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>
    );

    const button = screen.getByRole("button", { name: "Trigger" });
    expect(button).toHaveClass("custom-link");
    expect(button).toHaveClass("inline-flex");
  });

  test("BreadcrumbSeparator renders fallback icon and allows custom children", () => {
    const { rerender, container } = render(<BreadcrumbSeparator />);
    expect(container.querySelector("svg")).toBeInTheDocument();

    rerender(<BreadcrumbSeparator>•</BreadcrumbSeparator>);
    expect(container).toHaveTextContent("•");
  });

  test("BreadcrumbEllipsis exposes assistive text for screen readers", () => {
    render(<BreadcrumbEllipsis />);

    const srOnly = screen.getByText("More breadcrumb items");
    expect(srOnly).toHaveClass("sr-only");
  });
});
