import type { Meta, StoryObj } from "@storybook/react-vite";

import { Input } from "./index";

const meta = {
  title: "UI/Input",
  component: Input,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  argTypes: {
    type: {
      control: "select",
      options: ["text", "email", "password", "search", "url", "tel"],
      description: "HTML input type attribute",
    },
    disabled: {
      control: "boolean",
      description: "Disables user interaction",
    },
    placeholder: {
      control: "text",
      description: "Placeholder text shown when the input is empty",
    },
    "aria-invalid": {
      control: "boolean",
      description:
        "Marks the field as invalid for assistive technologies and styling",
    },
  },
  args: {
    type: "text",
    placeholder: "Enter text",
  },
} satisfies Meta<typeof Input>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    placeholder: "Enter your email",
    type: "email",
  },
};

export const Password: Story = {
  args: {
    placeholder: "Enter your password",
    type: "password",
  },
};

export const Disabled: Story = {
  args: {
    placeholder: "Input disabled",
    disabled: true,
  },
};

export const Invalid: Story = {
  args: {
    placeholder: "Enter your email",
    type: "email",
    "aria-invalid": true,
  },
  render: args => (
    <div className="flex w-72 flex-col gap-2">
      <label
        className="text-sm font-medium text-input-foreground"
        htmlFor="input-invalid"
      >
        Email
      </label>
      <Input id="input-invalid" {...args} />
      <p className="text-xs text-input-invalid-ring">
        Please provide a valid email address.
      </p>
    </div>
  ),
};

export const WithLabelAndHelper: Story = {
  render: args => (
    <div className="flex w-72 flex-col gap-2">
      <label
        className="text-sm font-medium text-input-foreground"
        htmlFor="input-helper"
      >
        Full name
      </label>
      <Input id="input-helper" aria-describedby="input-helper-text" {...args} />
      <p className="text-xs text-muted-foreground" id="input-helper-text">
        Use the name that appears on legal documents.
      </p>
    </div>
  ),
  args: {
    placeholder: "Jane Doe",
  },
};
