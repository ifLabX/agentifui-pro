import { render, screen } from "@testing-library/react";

import "@testing-library/jest-dom";

import { Alert, AlertDescription, AlertTitle } from "./index";

describe("Alert", () => {
  test("renders an accessible alert with title and description slots", () => {
    render(
      <Alert className="custom-alert">
        <AlertTitle>Heads up!</AlertTitle>
        <AlertDescription>Use caution when proceeding.</AlertDescription>
      </Alert>
    );

    const alert = screen.getByRole("alert");
    expect(alert).toHaveAttribute("data-slot", "alert");
    expect(alert).toHaveClass("custom-alert");
    expect(alert.className).toContain("rounded-lg");

    expect(screen.getByText("Heads up!")).toHaveAttribute(
      "data-slot",
      "alert-title"
    );
    expect(screen.getByText("Use caution when proceeding.")).toHaveAttribute(
      "data-slot",
      "alert-description"
    );
  });

  test("applies the destructive variant styling", () => {
    render(
      <Alert variant="destructive">
        <AlertTitle>System issue</AlertTitle>
        <AlertDescription>Something went wrong.</AlertDescription>
      </Alert>
    );

    const alert = screen.getByRole("alert");
    expect(alert.className).toContain("text-destructive");
    expect(alert.className).toContain("bg-card");
  });

  test("keeps title and description aligned to the content column", () => {
    render(
      <Alert>
        <AlertTitle>Title</AlertTitle>
        <AlertDescription>Details</AlertDescription>
      </Alert>
    );

    const title = screen.getByText("Title");
    const description = screen.getByText("Details");

    expect(title.className).toContain("col-start-2");
    expect(description.className).toContain("col-start-2");
    expect(description.className).toContain("text-muted-foreground");
  });
});
