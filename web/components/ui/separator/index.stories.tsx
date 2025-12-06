import type { Meta, StoryObj } from "@storybook/react-vite";

import { Separator } from "@/components/ui/separator";

const meta = {
  title: "UI/Separator",
  component: Separator,
  tags: ["autodocs"],
  parameters: {
    layout: "centered",
  },
  argTypes: {
    orientation: {
      control: "select",
      options: ["horizontal", "vertical"],
    },
    decorative: {
      control: "boolean",
    },
  },
} satisfies Meta<typeof Separator>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Horizontal: Story = {
  render: args => (
    <div className="w-96 space-y-2">
      <div className="flex items-center justify-between text-sm">
        <span>Overview</span>
        <span className="text-muted-foreground">12 updates</span>
      </div>
      <Separator {...args} />
      <p className="text-sm text-muted-foreground">
        Use separators to divide groups of related content such as lists or
        metadata blocks.
      </p>
    </div>
  ),
  args: {
    orientation: "horizontal",
    decorative: true,
  },
};

export const Vertical: Story = {
  render: () => (
    <div className="flex items-center gap-4">
      <div className="space-y-1">
        <p className="text-sm font-semibold">New</p>
        <p className="text-xs text-muted-foreground">Added today</p>
      </div>
      <Separator orientation="vertical" decorative={false} className="h-12" />
      <div className="space-y-1">
        <p className="text-sm font-semibold">Resolved</p>
        <p className="text-xs text-muted-foreground">Cleared by owners</p>
      </div>
    </div>
  ),
};
