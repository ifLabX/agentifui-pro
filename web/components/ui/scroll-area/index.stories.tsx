import type { Meta, StoryObj } from "@storybook/react-vite";

import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";

const meta = {
  title: "UI/Scroll Area",
  component: ScrollArea,
  tags: ["autodocs"],
  parameters: {
    layout: "centered",
  },
} satisfies Meta<typeof ScrollArea>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <ScrollArea className="h-48 w-72 rounded-md border">
      <div className="space-y-2 p-4">
        {Array.from({ length: 20 }).map((_, index) => (
          <p key={index} className="text-sm text-muted-foreground">
            Activity item {index + 1}
          </p>
        ))}
      </div>
    </ScrollArea>
  ),
};

export const Horizontal: Story = {
  render: () => (
    <ScrollArea className="w-[420px] rounded-md border">
      <div className="flex min-w-[720px] gap-3 p-4">
        {Array.from({ length: 10 }).map((_, index) => (
          <div
            key={index}
            className="bg-muted text-foreground w-40 rounded-lg border p-4"
          >
            <p className="text-sm font-semibold">Card {index + 1}</p>
            <p className="text-xs text-muted-foreground">
              Horizontal scrolling example.
            </p>
          </div>
        ))}
      </div>
      <ScrollBar orientation="horizontal" />
    </ScrollArea>
  ),
};
