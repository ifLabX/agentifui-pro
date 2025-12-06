import type { Meta, StoryObj } from "@storybook/react-vite";

import { Textarea } from "@/components/ui/textarea";

const meta = {
  title: "UI/Textarea",
  component: Textarea,
  tags: ["autodocs"],
  parameters: {
    layout: "centered",
  },
  argTypes: {
    disabled: {
      control: "boolean",
    },
    placeholder: {
      control: "text",
    },
  },
} satisfies Meta<typeof Textarea>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    placeholder: "Share more details",
  },
  render: args => <Textarea {...args} className="w-96" rows={4} />,
};

export const WithLabelAndHelper: Story = {
  render: () => (
    <div className="flex w-[420px] flex-col gap-2">
      <label className="text-sm font-medium" htmlFor="feedback">
        Feedback
      </label>
      <Textarea
        id="feedback"
        placeholder="What went well? What could be improved?"
        aria-describedby="feedback-helper"
        rows={4}
      />
      <p className="text-xs text-muted-foreground" id="feedback-helper">
        Share specific examples so the team can take action.
      </p>
    </div>
  ),
};

export const Disabled: Story = {
  args: {
    disabled: true,
    placeholder: "Textarea is disabled",
  },
  render: args => <Textarea {...args} className="w-96" rows={3} />,
};
