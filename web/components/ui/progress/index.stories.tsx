import type { Meta, StoryObj } from "@storybook/react-vite";

import { Progress } from "@/components/ui/progress";

const meta = {
  title: "UI/Progress",
  component: Progress,
  tags: ["autodocs"],
  parameters: {
    layout: "centered",
  },
} satisfies Meta<typeof Progress>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    value: 40,
  },
  render: args => (
    <div className="flex w-72 flex-col gap-2">
      <div className="flex items-center justify-between text-sm">
        <span>Uploading</span>
        <span className="text-muted-foreground">{args.value}%</span>
      </div>
      <Progress {...args} />
    </div>
  ),
};

export const Stacked: Story = {
  render: () => (
    <div className="flex w-80 flex-col gap-4">
      <div className="space-y-1">
        <div className="flex items-center justify-between text-sm">
          <span>Deployment</span>
          <span className="text-muted-foreground">72%</span>
        </div>
        <Progress value={72} />
      </div>
      <div className="space-y-1">
        <div className="flex items-center justify-between text-sm">
          <span>Tests</span>
          <span className="text-muted-foreground">55%</span>
        </div>
        <Progress value={55} className="bg-secondary/40" />
      </div>
      <div className="space-y-1">
        <div className="flex items-center justify-between text-sm">
          <span>Code coverage</span>
          <span className="text-muted-foreground">88%</span>
        </div>
        <Progress value={88} className="bg-muted/60" />
      </div>
    </div>
  ),
};
