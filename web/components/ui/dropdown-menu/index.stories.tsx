import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react";
import { fn } from "@storybook/test";

import { Button } from "../button";
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuTrigger,
} from "./index";

const meta = {
  title: "UI/DropdownMenu",
  component: DropdownMenu,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
} satisfies Meta<typeof DropdownMenu>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Basic: Story = {
  render: () => (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline">Open Menu</Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent>
        <DropdownMenuItem onClick={fn()}>Profile</DropdownMenuItem>
        <DropdownMenuItem onClick={fn()}>Settings</DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={fn()}>Logout</DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  ),
};

export const WithLabelsAndShortcuts: Story = {
  render: () => (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline">Actions</Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-56">
        <DropdownMenuLabel>My Account</DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuGroup>
          <DropdownMenuItem onClick={fn()}>
            Profile
            <DropdownMenuShortcut>⇧⌘P</DropdownMenuShortcut>
          </DropdownMenuItem>
          <DropdownMenuItem onClick={fn()}>
            Billing
            <DropdownMenuShortcut>⌘B</DropdownMenuShortcut>
          </DropdownMenuItem>
          <DropdownMenuItem onClick={fn()}>
            Settings
            <DropdownMenuShortcut>⌘S</DropdownMenuShortcut>
          </DropdownMenuItem>
        </DropdownMenuGroup>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={fn()}>
          Logout
          <DropdownMenuShortcut>⇧⌘Q</DropdownMenuShortcut>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  ),
};

export const WithCheckboxItems: Story = {
  render: () => {
    const CheckboxDemo = () => {
      const [showStatusBar, setShowStatusBar] = useState(true);
      const [showActivityBar, setShowActivityBar] = useState(false);
      const [showPanel, setShowPanel] = useState(false);

      return (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline">View Options</Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="w-56">
            <DropdownMenuLabel>Appearance</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuCheckboxItem
              checked={showStatusBar}
              onCheckedChange={setShowStatusBar}
            >
              Status Bar
            </DropdownMenuCheckboxItem>
            <DropdownMenuCheckboxItem
              checked={showActivityBar}
              onCheckedChange={setShowActivityBar}
            >
              Activity Bar
            </DropdownMenuCheckboxItem>
            <DropdownMenuCheckboxItem
              checked={showPanel}
              onCheckedChange={setShowPanel}
            >
              Panel
            </DropdownMenuCheckboxItem>
          </DropdownMenuContent>
        </DropdownMenu>
      );
    };

    return <CheckboxDemo />;
  },
};

export const WithRadioGroup: Story = {
  render: () => {
    const RadioDemo = () => {
      const [position, setPosition] = useState("bottom");

      return (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline">Panel Position</Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="w-56">
            <DropdownMenuLabel>Position</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuRadioGroup
              value={position}
              onValueChange={setPosition}
            >
              <DropdownMenuRadioItem value="top">Top</DropdownMenuRadioItem>
              <DropdownMenuRadioItem value="bottom">
                Bottom
              </DropdownMenuRadioItem>
              <DropdownMenuRadioItem value="right">Right</DropdownMenuRadioItem>
            </DropdownMenuRadioGroup>
          </DropdownMenuContent>
        </DropdownMenu>
      );
    };

    return <RadioDemo />;
  },
};

export const WithSubmenu: Story = {
  render: () => (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline">Advanced Menu</Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-56">
        <DropdownMenuItem onClick={fn()}>New Tab</DropdownMenuItem>
        <DropdownMenuItem onClick={fn()}>New Window</DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuSub>
          <DropdownMenuSubTrigger>Share</DropdownMenuSubTrigger>
          <DropdownMenuSubContent>
            <DropdownMenuItem onClick={fn()}>Email</DropdownMenuItem>
            <DropdownMenuItem onClick={fn()}>Message</DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={fn()}>Copy Link</DropdownMenuItem>
          </DropdownMenuSubContent>
        </DropdownMenuSub>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={fn()}>Print</DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  ),
};

export const WithDisabledItems: Story = {
  render: () => (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline">Options</Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-56">
        <DropdownMenuItem onClick={fn()}>Enabled Item</DropdownMenuItem>
        <DropdownMenuItem disabled>Disabled Item</DropdownMenuItem>
        <DropdownMenuItem onClick={fn()}>Another Enabled Item</DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  ),
};
