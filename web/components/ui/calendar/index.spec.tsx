import { render, screen, waitFor } from "@testing-library/react";

import "@testing-library/jest-dom";

import { DayPicker as MockedDayPicker } from "react-day-picker";

import { Calendar, CalendarDayButton } from "./index";

jest.mock("react-day-picker", () => {
  const React = jest.requireActual<typeof import("react")>("react");
  const mock = jest.fn();

  const MockDayPicker = React.forwardRef<
    HTMLDivElement,
    Record<string, unknown>
  >((props, ref) => {
    mock(props);
    return null;
  });
  MockDayPicker.displayName = "MockDayPicker";

  (MockDayPicker as unknown as { mock: jest.Mock }).mock = mock;

  const DayButton = React.forwardRef<
    HTMLButtonElement,
    React.ButtonHTMLAttributes<HTMLButtonElement>
  >((props, ref) => (
    <button ref={ref} {...props}>
      {props.children}
    </button>
  ));
  DayButton.displayName = "MockDayButton";

  const defaultClassNames = {
    root: "rdp-root",
    months: "rdp-months",
    month: "rdp-month",
    nav: "rdp-nav",
    button_previous: "rdp-prev",
    button_next: "rdp-next",
    month_caption: "rdp-caption",
    dropdowns: "rdp-dropdowns",
    dropdown_root: "rdp-dropdown-root",
    dropdown: "rdp-dropdown",
    caption_label: "rdp-caption-label",
    weekdays: "rdp-weekdays",
    weekday: "rdp-weekday",
    week: "rdp-week",
    week_number_header: "rdp-week-number-header",
    week_number: "rdp-week-number",
    day: "rdp-day",
    range_start: "rdp-range-start",
    range_middle: "rdp-range-middle",
    range_end: "rdp-range-end",
    today: "rdp-today",
    outside: "rdp-outside",
    disabled: "rdp-disabled",
    hidden: "rdp-hidden",
  };

  return {
    DayPicker: MockDayPicker,
    DayButton,
    getDefaultClassNames: () => ({ ...defaultClassNames }),
  };
});

const dayPickerMock = (MockedDayPicker as unknown as { mock: jest.Mock }).mock;

describe("Calendar", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("applies global design token classes to structural slots", () => {
    render(<Calendar />);

    expect(dayPickerMock).toHaveBeenCalledTimes(1);
    const props = dayPickerMock.mock.calls[0][0] as {
      className: string;
      classNames: Record<string, string>;
    };

    expect(props.className).toContain("bg-card");
    expect(props.className).toContain("group/calendar");
    expect(props.classNames.today).toContain("text-primary");
    expect(props.classNames.range_start).toContain("bg-primary");
    expect(props.classNames.day).toContain("rdp-day");
  });

  test("merges consumer className overrides and custom slots", () => {
    const CustomWeekNumber = () => null;

    render(
      <Calendar
        className="custom-shell"
        classNames={{ day: "custom-day" }}
        components={{ WeekNumber: CustomWeekNumber }}
      />
    );

    const props = dayPickerMock.mock.calls[0][0] as {
      className: string;
      classNames: Record<string, string>;
      components: Record<string, unknown>;
    };

    expect(props.className).toContain("custom-shell");
    expect(props.classNames.day).toContain("custom-day");
    expect(props.components.WeekNumber).toBe(CustomWeekNumber);
    expect(props.components.DayButton).toBe(CalendarDayButton);
  });

  test("respects formatter overrides and button variants", () => {
    const formatMonthDropdown = jest.fn().mockReturnValue("Mon");

    render(
      <Calendar
        captionLayout="dropdown"
        buttonVariant="outline"
        formatters={{ formatMonthDropdown }}
      />
    );

    const props = dayPickerMock.mock.calls[0][0] as {
      captionLayout?: string;
      formatters?: { formatMonthDropdown?: (date: Date) => string };
      classNames: Record<string, string>;
    };

    expect(props.captionLayout).toBe("dropdown");
    expect(props.formatters?.formatMonthDropdown).toBe(formatMonthDropdown);
    expect(props.classNames.button_next).toContain("border-input");
    expect(props.classNames.button_next).toContain("bg-background");
  });

  test("forwards DayPicker props like range mode and outside days", () => {
    render(
      <Calendar showOutsideDays={false} mode="range" numberOfMonths={2} />
    );

    const props = dayPickerMock.mock.calls[0][0] as {
      showOutsideDays: boolean;
      mode?: string;
      numberOfMonths?: number;
    };

    expect(props.showOutsideDays).toBe(false);
    expect(props.mode).toBe("range");
    expect(props.numberOfMonths).toBe(2);
  });

  test("exposes token-aware root slot for custom wrappers", () => {
    render(<Calendar />);

    const props = dayPickerMock.mock.calls[0][0] as {
      components: {
        Root: React.ComponentType<{
          className?: string;
          rootRef?: React.Ref<HTMLDivElement>;
        }>;
      };
    };

    const RootComponent = props.components.Root;
    const { getByTestId } = render(
      <RootComponent
        rootRef={() => undefined}
        className="token-shell"
        data-testid="calendar-root"
      />
    );

    const root = getByTestId("calendar-root");
    expect(root).toHaveAttribute("data-slot", "calendar");
    expect(root).toHaveClass("token-shell");
  });
});

describe("CalendarDayButton", () => {
  test("applies token classes and datasets for single selections", () => {
    const day = { date: new Date(2024, 5, 15) };

    render(
      <CalendarDayButton
        day={day as never}
        modifiers={
          {
            selected: true,
            range_start: false,
            range_end: false,
            range_middle: false,
          } as never
        }
      >
        <span>15</span>
      </CalendarDayButton>
    );

    const button = screen.getByRole("button");
    expect(button).toHaveAttribute("data-day", day.date.toLocaleDateString());
    expect(button).toHaveAttribute("data-selected-single", "true");
    expect(button).toHaveClass("rdp-day");
    expect(button.className).toContain(
      "data-[selected-single=true]:bg-primary"
    );
    expect(button.className).toContain(
      "data-[selected-single=true]:text-primary-foreground"
    );
  });

  test("focuses itself when the focused modifier is present", async () => {
    render(
      <CalendarDayButton
        day={{ date: new Date(2024, 5, 16) } as never}
        modifiers={
          {
            focused: true,
            selected: false,
            range_start: true,
            range_end: true,
            range_middle: false,
          } as never
        }
      >
        <span>16</span>
      </CalendarDayButton>
    );

    const button = screen.getByRole("button");
    await waitFor(() => expect(button).toHaveFocus());
    expect(button).toHaveAttribute("data-range-start", "true");
    expect(button).toHaveAttribute("data-range-end", "true");
    expect(button.className).toContain(
      "group-data-[focused=true]/day:ring-ring/40"
    );
  });
});
