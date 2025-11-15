import { useMemo, useState, type ReactNode } from "react";
import type { Meta, StoryObj } from "@storybook/react-vite";
import { addDays, format, startOfDay } from "date-fns";
import { ar } from "date-fns/locale";
import type { DateRange } from "react-day-picker";

import { cn } from "@/lib/utils";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import { Calendar } from "./index";

const meta = {
  title: "UI/Calendar",
  component: Calendar,
  tags: ["autodocs"],
  parameters: {
    layout: "padded",
    docs: {
      description: {
        component:
          "Calendar builds on react-day-picker and ships global design tokens (background, accent, primary, border) so that date selection feels consistent in cards, popovers, and dashboards.",
      },
    },
  },
  args: {
    captionLayout: "label",
    buttonVariant: "ghost",
    showOutsideDays: true,
  },
  argTypes: {
    captionLayout: {
      control: "select",
      options: ["label", "dropdown", "dropdown-months", "dropdown-years"],
    },
    buttonVariant: {
      control: "select",
      options: ["ghost", "outline", "secondary", "default"],
    },
    showOutsideDays: {
      control: "boolean",
    },
  },
} satisfies Meta<typeof Calendar>;

export default meta;

type Story = StoryObj<typeof meta>;

const Showcase = ({ children }: { children: ReactNode }) => (
  <div className="mx-auto flex w-full max-w-5xl flex-col gap-6">{children}</div>
);

const MetricGrid = ({ children }: { children: ReactNode }) => (
  <div className="grid gap-3 text-sm text-muted-foreground sm:grid-cols-2">
    {children}
  </div>
);

interface MetricTileProps {
  label: string;
  value: string;
  secondary?: string;
  accent?: boolean;
}

const MetricTile = ({ label, value, secondary, accent }: MetricTileProps) => (
  <div
    className={cn(
      "rounded-2xl border border-border bg-background/80 p-4 shadow-sm",
      accent && "border-primary/40 bg-primary/5 text-foreground"
    )}
  >
    <p className="text-xs uppercase tracking-wide text-muted-foreground">
      {label}
    </p>
    <p className="mt-1 text-base font-semibold text-foreground">{value}</p>
    {secondary ? (
      <p className="mt-1 text-xs text-muted-foreground">{secondary}</p>
    ) : null}
  </div>
);

const StorySection = ({
  title,
  description,
  children,
}: {
  title: string;
  description: string;
  children: ReactNode;
}) => (
  <Card>
    <CardHeader>
      <CardTitle>{title}</CardTitle>
      <CardDescription>{description}</CardDescription>
    </CardHeader>
    <CardContent className="pt-0">{children}</CardContent>
  </Card>
);

export const Playground: Story = {
  render: args => {
    const [selectedDate, setSelectedDate] = useState<Date | undefined>(
      startOfDay(new Date())
    );

    const nextRetro = selectedDate ? addDays(selectedDate, 7) : undefined;

    return (
      <Showcase>
        <StorySection
          title="Sprint planning surface"
          description="Pair the calendar with summary metrics so PMs can pick sprint anchors without leaving the modal shell."
        >
          <div className="grid gap-6 lg:grid-cols-[minmax(0,360px)_1fr]">
            <div className="space-y-4 rounded-2xl border border-card-border/80 bg-background/60 p-4">
              <p className="text-sm font-medium text-foreground">
                Summary metrics
              </p>
              <MetricGrid>
                <MetricTile
                  label="Selected day"
                  value={
                    selectedDate
                      ? format(selectedDate, "eee, MMM d")
                      : "Pick a day"
                  }
                  secondary="Sets the stand-up anchor"
                  accent
                />
                <MetricTile
                  label="Week"
                  value={
                    selectedDate ? `Week ${format(selectedDate, "I")}` : "TBD"
                  }
                  secondary="Align tasks to ISO week"
                />
                <MetricTile
                  label="Next retro"
                  value={
                    nextRetro
                      ? format(nextRetro, "eee, MMM d")
                      : "Auto once selected"
                  }
                  secondary="One week after sprint start"
                />
                <MetricTile
                  label="Remaining capacity"
                  value={selectedDate ? "82 hrs" : "Awaiting date"}
                  secondary="Based on assigned points"
                />
              </MetricGrid>
            </div>
            <div className="space-y-4 rounded-2xl border border-card-border bg-card/70 p-4">
              <Calendar
                {...args}
                mode="single"
                selected={selectedDate}
                onSelect={(value?: Date) => {
                  setSelectedDate(value);
                }}
              />
              <p className="text-sm text-muted-foreground">
                Every interactive element inherits `bg-card`,
                `border-card-border` and `text-foreground`, so the picker feels
                integrated with the rest of the dashboard surface.
              </p>
            </div>
          </div>
        </StorySection>
      </Showcase>
    );
  },
  parameters: {
    docs: {
      description: {
        story:
          "The playground keeps the calendar controlled so selecting a date updates localized summaries without breaking the tokenized shell.",
      },
    },
  },
};

export const RangeSelection: Story = {
  args: {
    buttonVariant: "outline",
    showOutsideDays: false,
    captionLayout: "dropdown",
    numberOfMonths: 2,
    fixedWeeks: true,
    fromYear: new Date().getFullYear() - 1,
    toYear: new Date().getFullYear() + 2,
  },
  render: args => {
    const today = useMemo(() => startOfDay(new Date()), []);
    const [range, setRange] = useState<DateRange | undefined>({
      from: today,
      to: addDays(today, 4),
    });

    return (
      <Showcase>
        <StorySection
          title="Retreat range picker"
          description="Align multi-day events to your global border + background tokens, even when exposing dropdown captions."
        >
          <div className="grid gap-8 lg:grid-cols-[minmax(0,360px)_1fr]">
            <div className="space-y-5 rounded-2xl border border-border bg-background/70 p-5">
              <MetricGrid>
                <MetricTile
                  label="Check-in"
                  value={
                    range?.from
                      ? format(range.from, "PPP")
                      : "Choose a start date"
                  }
                  secondary="Earliest arrival"
                />
                <MetricTile
                  label="Check-out"
                  value={
                    range?.to ? format(range.to, "PPP") : "Choose an end date"
                  }
                  secondary="Latest departure"
                />
                <MetricTile
                  label="Duration"
                  value={
                    range?.from && range?.to
                      ? `${Math.max(
                          1,
                          Math.ceil(
                            (range.to.getTime() - range.from.getTime()) /
                              (1000 * 60 * 60 * 24)
                          )
                        )} nights`
                      : "Waiting for both dates"
                  }
                  secondary="Auto-updates as the range expands"
                  accent
                />
                <MetricTile
                  label="Blocked days"
                  value="No conflicts"
                  secondary="Weekends allowed"
                />
              </MetricGrid>
              <div className="rounded-2xl border border-card-border/60 bg-card/60 p-4 text-sm text-muted-foreground">
                <p className="font-medium text-foreground">Why fixed weeks?</p>
                <p className="mt-2">
                  Fixed weeks keep the component height consistent, so the modal
                  never jumps even when ranged dates fall at the end of the
                  month.
                </p>
              </div>
            </div>
            <div className="rounded-2xl border border-card-border bg-card/80 p-4">
              <Calendar
                {...args}
                mode="range"
                selected={range}
                onSelect={(value?: DateRange) => {
                  setRange(value);
                }}
                disabled={{ before: today }}
              />
            </div>
          </div>
        </StorySection>
      </Showcase>
    );
  },
  parameters: {
    docs: {
      description: {
        story:
          "Pair two months with the outlined navigation buttons when you need parity with panel borders. Fixed weeks keep the layout height predictable for modals.",
      },
    },
  },
};

export const LocalizedRtl: Story = {
  args: {
    captionLayout: "dropdown-years",
    buttonVariant: "secondary",
    showOutsideDays: true,
    fromYear: 2020,
    toYear: 2030,
  },
  render: args => {
    const [preferredDate, setPreferredDate] = useState<Date | undefined>(
      startOfDay(new Date())
    );

    return (
      <Showcase>
        <StorySection
          title="RTL + localized captions"
          description="Mirror navigation and swap locales while keeping token spacing and borders intact."
        >
          <div className="grid gap-6 lg:grid-cols-[minmax(0,320px)_1fr]">
            <div className="space-y-4 rounded-2xl border border-border bg-background/70 p-4">
              <p className="text-sm font-medium text-foreground">
                Arabic launch details
              </p>
              <MetricTile
                label="Target date"
                value={
                  preferredDate
                    ? format(preferredDate, "PPP", { locale: ar })
                    : "اختر تاريخاً"
                }
                secondary="Mirrors dropdown captions"
                accent
              />
              <MetricTile
                label="Locale"
                value="ar-EG"
                secondary="Date-fns locale prop"
              />
              <MetricTile
                label="Direction"
                value="dir=rtl"
                secondary="Applies to the wrapper"
              />
              <p className="text-sm text-muted-foreground">
                Wrap the calendar in an RTL container to automatically flip day
                grids and icon chevrons. Tokens continue to read from globals.
              </p>
            </div>
            <div
              dir="rtl"
              className="rounded-2xl border border-card-border bg-card/80 p-4"
            >
              <Calendar
                {...args}
                locale={ar}
                mode="single"
                selected={preferredDate}
                onSelect={(value?: Date) => {
                  setPreferredDate(value);
                }}
              />
            </div>
          </div>
        </StorySection>
      </Showcase>
    );
  },
  parameters: {
    docs: {
      description: {
        story:
          'Use the same component for localized dashboards by passing the Date-Fns locale and wrapping the slot with `dir="rtl"`.',
      },
    },
  },
};
