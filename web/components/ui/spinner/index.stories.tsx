import type { Meta, StoryObj } from "@storybook/react";

import { Spinner } from "./index";

const meta = {
  title: "UI/Spinner",
  component: Spinner,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  argTypes: {
    variant: {
      control: "select",
      options: ["default", "loader"],
      description: "The icon variant of the spinner",
    },
    size: {
      control: "select",
      options: ["sm", "md", "lg", "xl"],
      description: "The size of the spinner",
    },
    "aria-label": {
      control: "text",
      description: "Accessible label for screen readers",
    },
  },
} satisfies Meta<typeof Spinner>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    variant: "default",
    size: "md",
  },
};

export const Loader: Story = {
  args: {
    variant: "loader",
    size: "md",
  },
};

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

export const ExtraLarge: Story = {
  args: {
    size: "xl",
  },
};

export const CustomAriaLabel: Story = {
  args: {
    "aria-label": "Processing your request",
  },
};

export const AllSizes: Story = {
  render: () => (
    <div className="flex items-center gap-4">
      <div className="flex flex-col items-center gap-2">
        <Spinner size="sm" />
        <span className="text-xs">Small</span>
      </div>
      <div className="flex flex-col items-center gap-2">
        <Spinner size="md" />
        <span className="text-xs">Medium</span>
      </div>
      <div className="flex flex-col items-center gap-2">
        <Spinner size="lg" />
        <span className="text-xs">Large</span>
      </div>
      <div className="flex flex-col items-center gap-2">
        <Spinner size="xl" />
        <span className="text-xs">Extra Large</span>
      </div>
    </div>
  ),
};

export const AllVariants: Story = {
  render: () => (
    <div className="flex items-center gap-8">
      <div className="flex flex-col items-center gap-2">
        <Spinner variant="default" size="lg" />
        <span className="text-xs">Default</span>
      </div>
      <div className="flex flex-col items-center gap-2">
        <Spinner variant="loader" size="lg" />
        <span className="text-xs">Loader</span>
      </div>
    </div>
  ),
};

export const WithText: Story = {
  render: () => (
    <div className="flex items-center gap-2">
      <Spinner size="sm" />
      <span>Loading...</span>
    </div>
  ),
};
