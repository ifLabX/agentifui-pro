import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react-vite";
import { fn } from "storybook/test";

import { Button } from "../button";
import {
  Popover,
  PopoverBody,
  PopoverClose,
  PopoverContent,
  PopoverDivider,
  PopoverFooter,
  PopoverHeader,
  PopoverItem,
  PopoverTrigger,
} from "./index";

const meta = {
  title: "UI/Popover",
  component: Popover,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
} satisfies Meta<typeof Popover>;

export default meta;
type Story = Omit<StoryObj<typeof meta>, "args"> & {
  render: () => React.ReactElement;
};

export const Basic: Story = {
  render: () => (
    <Popover>
      <PopoverTrigger asChild>
        <Button>Open Popover</Button>
      </PopoverTrigger>
      <PopoverContent>
        <PopoverItem onClick={fn()}>Profile</PopoverItem>
        <PopoverItem onClick={fn()}>Settings</PopoverItem>
        <PopoverDivider />
        <PopoverItem onClick={fn()}>Logout</PopoverItem>
      </PopoverContent>
    </Popover>
  ),
};

export const Uncontrolled: Story = {
  render: () => (
    <Popover>
      <PopoverTrigger asChild>
        <Button>Uncontrolled Popover</Button>
      </PopoverTrigger>
      <PopoverContent>
        <PopoverHeader>Actions</PopoverHeader>
        <PopoverItem onClick={fn()}>Edit</PopoverItem>
        <PopoverItem onClick={fn()}>Duplicate</PopoverItem>
        <PopoverDivider />
        <PopoverItem danger onClick={fn()}>
          Delete
        </PopoverItem>
      </PopoverContent>
    </Popover>
  ),
};

export const Controlled: Story = {
  render: () => {
    const ControlledDemo = () => {
      const [open, setOpen] = useState(false);

      return (
        <div className="flex flex-col gap-4">
          <Popover open={open} onOpenChange={setOpen}>
            <PopoverTrigger asChild>
              <Button>Controlled Popover</Button>
            </PopoverTrigger>
            <PopoverContent>
              <PopoverHeader>Controlled Menu</PopoverHeader>
              <PopoverItem onClick={() => setOpen(false)}>
                Close from Item
              </PopoverItem>
              <PopoverItem onClick={fn()}>Keep Open</PopoverItem>
            </PopoverContent>
          </Popover>
          <div className="text-sm">Popover is {open ? "open" : "closed"}</div>
        </div>
      );
    };

    return <ControlledDemo />;
  },
};

export const WithHeaderBodyFooter: Story = {
  render: () => (
    <Popover>
      <PopoverTrigger asChild>
        <Button>Show Dialog</Button>
      </PopoverTrigger>
      <PopoverContent>
        <PopoverHeader>Confirm Action</PopoverHeader>
        <PopoverBody>
          Are you sure you want to proceed with this action?
        </PopoverBody>
        <PopoverFooter>
          <PopoverClose>
            <Button variant="outline" size="sm">
              Cancel
            </Button>
          </PopoverClose>
          <Button size="sm" onClick={fn()}>
            Confirm
          </Button>
        </PopoverFooter>
      </PopoverContent>
    </Popover>
  ),
};

export const WithIcons: Story = {
  render: () => (
    <Popover>
      <PopoverTrigger asChild>
        <Button>Options</Button>
      </PopoverTrigger>
      <PopoverContent>
        <PopoverItem
          icon={
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
              <circle cx="12" cy="7" r="4" />
            </svg>
          }
          onClick={fn()}
        >
          Profile
        </PopoverItem>
        <PopoverItem
          icon={
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z" />
              <circle cx="12" cy="12" r="3" />
            </svg>
          }
          onClick={fn()}
        >
          Settings
        </PopoverItem>
        <PopoverDivider />
        <PopoverItem
          danger
          icon={
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
              <polyline points="16 17 21 12 16 7" />
              <line x1="21" x2="9" y1="12" y2="12" />
            </svg>
          }
          onClick={fn()}
        >
          Logout
        </PopoverItem>
      </PopoverContent>
    </Popover>
  ),
};

export const WithDisabledItems: Story = {
  render: () => (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="outline">Menu</Button>
      </PopoverTrigger>
      <PopoverContent>
        <PopoverItem onClick={fn()}>Active Item</PopoverItem>
        <PopoverItem disabled>Disabled Item</PopoverItem>
        <PopoverItem onClick={fn()}>Another Active Item</PopoverItem>
      </PopoverContent>
    </Popover>
  ),
};

export const Modal: Story = {
  render: () => (
    <Popover modal>
      <PopoverTrigger asChild>
        <Button variant="outline">Modal Popover</Button>
      </PopoverTrigger>
      <PopoverContent>
        <PopoverHeader>Modal Dialog</PopoverHeader>
        <PopoverBody>
          This is a modal popover with backdrop and focus lock.
        </PopoverBody>
        <PopoverFooter>
          <PopoverClose>
            <Button variant="outline" size="sm">
              Close
            </Button>
          </PopoverClose>
        </PopoverFooter>
      </PopoverContent>
    </Popover>
  ),
};

export const CustomWidth: Story = {
  render: () => (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="outline">Wide Popover</Button>
      </PopoverTrigger>
      <PopoverContent className="w-80">
        <PopoverHeader>Custom Width</PopoverHeader>
        <PopoverBody>
          This popover has a custom width applied using the className prop. You
          can adjust the width to match your design requirements.
        </PopoverBody>
      </PopoverContent>
    </Popover>
  ),
};
