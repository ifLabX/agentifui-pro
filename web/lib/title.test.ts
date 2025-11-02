import { formatTitle } from "./title";

describe("formatTitle", () => {
  it("joins title and brand with separator", () => {
    expect(formatTitle({ title: "Dashboard", brand: "AgentifUI" })).toBe(
      "Dashboard - AgentifUI"
    );
  });

  it("returns brand when title is missing", () => {
    expect(formatTitle({ brand: "AgentifUI" })).toBe("AgentifUI");
  });

  it("returns title when brand is missing", () => {
    expect(formatTitle({ title: "Dashboard" })).toBe("Dashboard");
  });

  it("appends suffix when provided", () => {
    expect(
      formatTitle({
        title: "Dashboard",
        brand: "AgentifUI",
        suffix: "[Beta]",
      })
    ).toBe("Dashboard - AgentifUI [Beta]");
  });

  it("handles custom separator", () => {
    expect(
      formatTitle({
        title: "Datasets",
        brand: "AgentifUI",
        separator: " · ",
      })
    ).toBe("Datasets · AgentifUI");
  });

  it("trims extraneous whitespace", () => {
    expect(
      formatTitle({
        title: "  Dashboard ",
        brand: " AgentifUI ",
        suffix: " [Internal] ",
      })
    ).toBe("Dashboard - AgentifUI [Internal]");
  });

  it("returns empty string when nothing provided", () => {
    expect(formatTitle({})).toBe("");
  });
});
