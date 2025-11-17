import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

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

  test("supports keyboard navigation through links", async () => {
    const user = userEvent.setup();
    render(
      <Breadcrumb>
        <BreadcrumbList>
          <BreadcrumbItem>
            <BreadcrumbLink href="/home">Home</BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator />
          <BreadcrumbItem>
            <BreadcrumbLink href="/projects">Projects</BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator />
          <BreadcrumbItem>
            <BreadcrumbPage>Current</BreadcrumbPage>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>
    );

    const homeLink = screen.getByRole("link", { name: "Home" });
    const projectsLink = screen.getByRole("link", { name: "Projects" });

    await user.tab();
    expect(homeLink).toHaveFocus();

    await user.tab();
    expect(projectsLink).toHaveFocus();
  });

  test("maintains proper semantic HTML structure", () => {
    render(
      <Breadcrumb>
        <BreadcrumbList>
          <BreadcrumbItem>
            <BreadcrumbLink href="/">Home</BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator />
          <BreadcrumbItem>
            <BreadcrumbPage>Current</BreadcrumbPage>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>
    );

    const nav = screen.getByRole("navigation");
    expect(nav).toHaveAttribute("aria-label", "Breadcrumb");

    const list = screen.getByRole("list");
    expect(list.tagName).toBe("OL");
    expect(nav.contains(list)).toBe(true);

    const listItems = screen.getAllByRole("listitem");
    expect(listItems.length).toBeGreaterThan(0);
    expect(listItems[0].parentElement).toBe(list);
  });

  test("forwards refs correctly to underlying DOM elements", () => {
    const breadcrumbRef = React.createRef<HTMLElement>();
    const listRef = React.createRef<HTMLOListElement>();
    const itemRef = React.createRef<HTMLLIElement>();
    const linkRef = React.createRef<HTMLAnchorElement>();
    const pageRef = React.createRef<HTMLSpanElement>();
    const separatorRef = React.createRef<HTMLLIElement>();
    const ellipsisRef = React.createRef<HTMLSpanElement>();

    render(
      <Breadcrumb ref={breadcrumbRef}>
        <BreadcrumbList ref={listRef}>
          <BreadcrumbItem ref={itemRef}>
            <BreadcrumbLink ref={linkRef} href="/test">
              Link
            </BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator ref={separatorRef} />
          <BreadcrumbItem>
            <BreadcrumbPage ref={pageRef}>Current</BreadcrumbPage>
          </BreadcrumbItem>
          <BreadcrumbItem>
            <BreadcrumbEllipsis ref={ellipsisRef} />
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>
    );

    expect(breadcrumbRef.current).toBeInstanceOf(HTMLElement);
    expect(breadcrumbRef.current?.tagName).toBe("NAV");
    expect(listRef.current).toBeInstanceOf(HTMLOListElement);
    expect(itemRef.current).toBeInstanceOf(HTMLLIElement);
    expect(linkRef.current).toBeInstanceOf(HTMLAnchorElement);
    expect(pageRef.current).toBeInstanceOf(HTMLSpanElement);
    expect(separatorRef.current).toBeInstanceOf(HTMLLIElement);
    expect(ellipsisRef.current).toBeInstanceOf(HTMLSpanElement);
  });

  test("accepts and applies custom aria-label", () => {
    render(
      <Breadcrumb aria-label="Project navigation">
        <BreadcrumbList>
          <BreadcrumbItem>
            <BreadcrumbPage>Home</BreadcrumbPage>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>
    );

    const nav = screen.getByRole("navigation");
    expect(nav).toHaveAttribute("aria-label", "Project navigation");
  });

  test("BreadcrumbPage accepts custom aria-current values", () => {
    render(
      <Breadcrumb>
        <BreadcrumbList>
          <BreadcrumbItem>
            <BreadcrumbPage aria-current="step">Step 1</BreadcrumbPage>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>
    );

    expect(screen.getByText("Step 1")).toHaveAttribute("aria-current", "step");
  });
});
