import type { Meta, StoryObj } from "@storybook/react-vite";
import { CalendarDaysIcon, CheckIcon, SettingsIcon } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  ButtonGroup,
  ButtonGroupSeparator,
  ButtonGroupText,
} from "@/components/ui/button-group";

const meta = {
  title: "UI/Button Group",
  component: ButtonGroup,
  tags: ["autodocs"],
  parameters: {
    layout: "centered",
  },
  argTypes: {
    orientation: {
      control: "select",
      options: ["horizontal", "vertical"],
    },
  },
} satisfies Meta<typeof ButtonGroup>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Toolbar: Story = {
  args: {
    orientation: "horizontal",
  },
  render: args => (
    <ButtonGroup {...args}>
      <ButtonGroupText className="px-3">
        <CalendarDaysIcon className="size-4" />
        Sprint 12
      </ButtonGroupText>
      <Button variant="outline">Preview</Button>
      <Button>Publish</Button>
    </ButtonGroup>
  ),
};

export const WithSeparators: Story = {
  render: () => (
    <ButtonGroup orientation="horizontal">
      <Button variant="outline">List</Button>
      <ButtonGroupSeparator />
      <Button variant="outline">Board</Button>
      <ButtonGroupSeparator />
      <Button variant="outline">Calendar</Button>
    </ButtonGroup>
  ),
};

export const Vertical: Story = {
  render: () => (
    <ButtonGroup orientation="vertical">
      <ButtonGroupText asChild>
        <span className="justify-between">
          Deployment
          <SettingsIcon className="size-4" />
        </span>
      </ButtonGroupText>
      <Button variant="secondary" className="justify-start">
        <CheckIcon className="mr-2 size-4" />
        Promote to staging
      </Button>
      <Button variant="outline" className="justify-start">
        Roll back to previous
      </Button>
    </ButtonGroup>
  ),
};
