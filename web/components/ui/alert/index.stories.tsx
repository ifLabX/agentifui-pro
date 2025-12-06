import type { Meta, StoryObj } from "@storybook/react-vite";
import { AlertCircleIcon, CheckIcon, InfoIcon } from "lucide-react";

import {
  Alert,
  AlertDescription,
  AlertTitle,
} from "@/components/ui/alert";

const meta = {
  title: "UI/Alert",
  component: Alert,
  tags: ["autodocs"],
  parameters: {
    layout: "centered",
  },
  argTypes: {
    variant: {
      control: "select",
      options: ["default", "destructive"],
    },
  },
} satisfies Meta<typeof Alert>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    variant: "default",
  },
  render: args => (
    <Alert {...args} className="w-[420px]">
      <AlertTitle>Heads up</AlertTitle>
      <AlertDescription>
        Use alerts to highlight contextual information without disrupting the
        primary task.
      </AlertDescription>
    </Alert>
  ),
};

export const WithIcon: Story = {
  render: args => (
    <Alert {...args} className="w-[420px]">
      <InfoIcon className="mt-1 text-blue-500" />
      <AlertTitle>New feature available</AlertTitle>
      <AlertDescription>
        Discover the redesigned workspace switcher in the top navigation bar.
      </AlertDescription>
    </Alert>
  ),
  args: {
    variant: "default",
  },
};

export const Destructive: Story = {
  render: args => (
    <Alert {...args} className="w-[420px]">
      <AlertCircleIcon className="mt-1 text-destructive" />
      <AlertTitle>Action required</AlertTitle>
      <AlertDescription>
        Billing failed for the last invoice. Update payment details to prevent
        service interruption.
      </AlertDescription>
    </Alert>
  ),
  args: {
    variant: "destructive",
  },
};

export const Checklist: Story = {
  render: () => (
    <div className="w-[480px] space-y-3">
      <Alert>
        <CheckIcon className="mt-1 text-emerald-500" />
        <AlertTitle>Environment configured</AlertTitle>
        <AlertDescription>
          Connection to production database is healthy and up to date.
        </AlertDescription>
      </Alert>
      <Alert>
        <InfoIcon className="mt-1 text-blue-500" />
        <AlertTitle>Deploy notice</AlertTitle>
        <AlertDescription>
          Deployments run nightly at 02:00 UTC with automatic rollbacks.
        </AlertDescription>
      </Alert>
    </div>
  ),
};
