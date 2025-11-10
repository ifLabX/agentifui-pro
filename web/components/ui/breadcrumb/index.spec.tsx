import * as React from "react";
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

const FrameworkLink = React.forwardRef<
  HTMLAnchorElement,
  React.ComponentPropsWithoutRef<"a">
>(({ children, ...props }, ref) => (
  <a ref={ref} {...props}>
    {children}
  </a>
));
FrameworkLink.displayName = "FrameworkLink";

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
    render(
      <Breadcrumb>
        <BreadcrumbList className="custom-list">
          <BreadcrumbItem className="custom-item">
            <BreadcrumbPage>Only page</BreadcrumbPage>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>
    );

    const list = screen.getByRole("list");
    expect(list).toHaveClass("custom-list");
    expect(list).toHaveClass("flex");

    const item = screen.getByRole("listitem");
    expect(item).toHaveClass("custom-item");
    expect(item).toHaveClass("inline-flex");
  });

  test("BreadcrumbLink composes framework links via Slot when asChild is true", () => {
    render(
      <Breadcrumb>
        <BreadcrumbList>
          <BreadcrumbItem>
            <BreadcrumbLink asChild className="custom-link">
              <FrameworkLink href="/settings">Settings</FrameworkLink>
            </BreadcrumbLink>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>
    );

    const link = screen.getByRole("link", { name: "Settings" });
    expect(link).toHaveAttribute("href", "/settings");
    expect(link).toHaveClass("custom-link");
    expect(link).toHaveClass("inline-flex");
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
