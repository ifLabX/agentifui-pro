import type { Meta, StoryObj } from "@storybook/react-vite";
import { AlertCircleIcon, CheckIcon, InfoIcon, XIcon } from "lucide-react";
import { fn } from "storybook/test";

import { Badge } from "./index";

const meta = {
  title: "UI/Badge",
  component: Badge,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  argTypes: {
    variant: {
      control: "select",
      options: [
        "default",
        "secondary",
        "destructive",
        "outline",
        "success",
        "warning",
        "info",
        "purple",
      ],
    },
  },
} satisfies Meta<typeof Badge>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    children: "Badge",
    variant: "default",
  },
};

export const AllVariants: Story = {
  render: () => (
    <div className="flex flex-wrap items-center gap-3">
      <Badge variant="default">Default</Badge>
      <Badge variant="secondary">Secondary</Badge>
      <Badge variant="destructive">Destructive</Badge>
      <Badge variant="outline">Outline</Badge>
      <Badge variant="success">Success</Badge>
      <Badge variant="warning">Warning</Badge>
      <Badge variant="info">Info</Badge>
      <Badge variant="purple">Purple</Badge>
    </div>
  ),
};

export const WithIcons: Story = {
  render: () => (
    <div className="flex flex-wrap items-center gap-3">
      <Badge variant="success">
        <CheckIcon className="mr-1 h-3 w-3" />
        Completed
      </Badge>
      <Badge variant="destructive">
        <XIcon className="mr-1 h-3 w-3" />
        Failed
      </Badge>
      <Badge variant="warning">
        <AlertCircleIcon className="mr-1 h-3 w-3" />
        Warning
      </Badge>
      <Badge variant="info">
        <InfoIcon className="mr-1 h-3 w-3" />
        Information
      </Badge>
    </div>
  ),
};

export const StatusBadges: Story = {
  render: () => (
    <div className="flex flex-wrap items-center gap-3">
      <Badge variant="success">Active</Badge>
      <Badge variant="warning">Pending</Badge>
      <Badge variant="destructive">Inactive</Badge>
      <Badge variant="info">Draft</Badge>
      <Badge variant="purple">Beta</Badge>
    </div>
  ),
};

export const WithCounts: Story = {
  render: () => (
    <div className="flex flex-wrap items-center gap-3">
      <Badge variant="default">New 12</Badge>
      <Badge variant="secondary">Messages 5</Badge>
      <Badge variant="info">Updates 3</Badge>
      <Badge variant="destructive">Errors 2</Badge>
    </div>
  ),
};

export const CustomSizes: Story = {
  render: () => (
    <div className="flex flex-wrap items-center gap-3">
      <Badge className="px-1.5 py-0 text-[10px]">Tiny</Badge>
      <Badge className="px-2 py-0.5 text-xs">Small</Badge>
      <Badge className="px-3 py-1 text-sm">Medium</Badge>
      <Badge className="px-4 py-1.5 text-base">Large</Badge>
    </div>
  ),
};

export const Interactive: Story = {
  render: () => (
    <div className="flex flex-wrap items-center gap-3">
      <Badge
        variant="default"
        className="cursor-pointer hover:opacity-80"
        onClick={fn()}
      >
        Clickable badge
      </Badge>
      <Badge
        variant="secondary"
        className="cursor-pointer hover:opacity-80"
        onClick={fn()}
      >
        Filter: Active
        <XIcon className="ml-1 h-3 w-3" />
      </Badge>
      <Badge
        variant="outline"
        className="cursor-pointer hover:opacity-80"
        onClick={fn()}
      >
        Tag: React
        <XIcon className="ml-1 h-3 w-3" />
      </Badge>
    </div>
  ),
};

export const InContext: Story = {
  render: () => (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <h3 className="text-base font-semibold">Project Status</h3>
        <Badge variant="success">On Track</Badge>
      </div>
      <div className="flex items-center gap-2">
        <span className="text-sm text-muted-foreground">Version:</span>
        <Badge variant="outline">v2.1.0</Badge>
        <Badge variant="purple">Beta</Badge>
      </div>
      <div className="flex items-center gap-2">
        <span className="text-sm text-muted-foreground">Environment:</span>
        <Badge variant="info">Development</Badge>
      </div>
      <div className="flex items-center gap-2">
        <span className="text-sm text-muted-foreground">Notifications:</span>
        <Badge variant="destructive">3 Errors</Badge>
        <Badge variant="warning">5 Warnings</Badge>
      </div>
    </div>
  ),
};
