import type { Meta, StoryObj } from "@storybook/react-vite";

import { TypingDots } from "./index";

const meta: Meta<typeof TypingDots> = {
  title: "UI/TypingDots",
  component: TypingDots,
  tags: ["autodocs"],
  argTypes: {
    size: {
      control: "select",
      options: ["sm", "md", "lg"],
      description: "The size of the typing dots",
    },
    className: {
      control: "text",
      description: "Additional CSS classes",
    },
  },
};

export default meta;
type Story = StoryObj<typeof TypingDots>;

export const Small: Story = {
  args: {
    size: "sm",
  },
};

export const Medium: Story = {
  args: {
    size: "md",
  },
};

export const Large: Story = {
  args: {
    size: "lg",
  },
};

export const Playground: Story = {
  args: {
    size: "md",
  },
};

export const InContext: Story = {
  render: () => (
    <div className="space-y-6">
      <div className="flex items-center gap-3 p-4 bg-muted rounded-lg">
        <span className="text-sm">AI is typing</span>
        <TypingDots size="md" />
      </div>
      <div className="flex items-center gap-3 p-4 bg-card rounded-lg border">
        <span className="text-sm text-muted-foreground">Processing</span>
        <TypingDots size="sm" />
      </div>
      <div className="flex items-center gap-3 p-4 bg-primary text-primary-foreground rounded-lg">
        <span className="text-sm">Loading content</span>
        <TypingDots size="lg" />
      </div>
    </div>
  ),
};

export const AllSizes: Story = {
  render: () => (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <span className="w-24 text-sm text-muted-foreground">Small:</span>
        <TypingDots size="sm" />
      </div>
      <div className="flex items-center gap-4">
        <span className="w-24 text-sm text-muted-foreground">Medium:</span>
        <TypingDots size="md" />
      </div>
      <div className="flex items-center gap-4">
        <span className="w-24 text-sm text-muted-foreground">Large:</span>
        <TypingDots size="lg" />
      </div>
    </div>
  ),
};

export const CustomStyling: Story = {
  render: () => (
    <div className="space-y-6">
      <div className="p-4 bg-muted rounded-lg">
        <div className="flex items-center gap-3 mb-2">
          <span className="text-sm">Default:</span>
          <TypingDots />
        </div>
        <div className="flex items-center gap-3 mb-2">
          <span className="text-sm">With opacity:</span>
          <TypingDots className="opacity-50" />
        </div>
        <div className="flex items-center gap-3">
          <span className="text-sm">Scaled:</span>
          <TypingDots className="scale-150" />
        </div>
      </div>
    </div>
  ),
};
