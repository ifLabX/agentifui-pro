import type { Meta, StoryObj } from "@storybook/react-vite";
import { AtSignIcon, LinkIcon, SearchIcon } from "lucide-react";

import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupInput,
  InputGroupText,
  InputGroupTextarea,
} from "@/components/ui/input-group";

const meta = {
  title: "UI/Input Group",
  component: InputGroup,
  tags: ["autodocs"],
  parameters: {
    layout: "centered",
  },
} satisfies Meta<typeof InputGroup>;

export default meta;
type Story = StoryObj<typeof meta>;

export const InlineAddons: Story = {
  render: () => (
    <div className="w-[420px] space-y-3">
      <InputGroup>
        <InputGroupAddon>
          <InputGroupText>
            <AtSignIcon className="size-4" />
          </InputGroupText>
        </InputGroupAddon>
        <InputGroupInput placeholder="team" />
        <InputGroupAddon align="inline-end">
          <InputGroupText>.company.com</InputGroupText>
        </InputGroupAddon>
      </InputGroup>
      <InputGroup>
        <InputGroupAddon>
          <InputGroupText>https://</InputGroupText>
        </InputGroupAddon>
        <InputGroupInput placeholder="workspace.domain" />
        <InputGroupAddon align="inline-end">
          <InputGroupButton size="icon-sm">
            <LinkIcon className="size-4" />
          </InputGroupButton>
        </InputGroupAddon>
      </InputGroup>
    </div>
  ),
};

export const WithActions: Story = {
  render: () => (
    <InputGroup>
      <InputGroupAddon>
        <InputGroupButton size="icon-sm">
          <SearchIcon className="size-4" />
        </InputGroupButton>
      </InputGroupAddon>
      <InputGroupInput placeholder="Search projects" />
      <InputGroupAddon align="inline-end">
        <InputGroupButton size="sm" variant="secondary">
          Filter
        </InputGroupButton>
      </InputGroupAddon>
    </InputGroup>
  ),
};

export const WithTextarea: Story = {
  render: () => (
    <InputGroup className="min-h-24 items-start">
      <InputGroupAddon align="block-start" className="border-b">
        <InputGroupText>Notes</InputGroupText>
      </InputGroupAddon>
      <InputGroupTextarea
        placeholder="Add context for this request"
        rows={4}
      />
      <InputGroupAddon align="block-end" className="border-t">
        <InputGroupText>Max 500 characters</InputGroupText>
      </InputGroupAddon>
    </InputGroup>
  ),
};
