import type { Meta, StoryObj } from "@storybook/react-vite";

import { Button } from "@/components/ui/button";
import { Tooltip, TooltipProvider } from "@/components/ui/tooltip";

import { Kbd, KbdGroup } from "./index";

const meta = {
  title: "UI/Kbd",
  component: Kbd,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  argTypes: {
    children: {
      control: "text",
    },
    size: {
      control: { type: "select" },
      options: ["default", "sm"],
    },
  },
} satisfies Meta<typeof Kbd>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Playground: Story = {
  args: {
    children: "Ctrl",
    size: "default",
  },
};

export const ShortcutCombo: Story = {
  render: () => (
    <KbdGroup>
      <Kbd>⌘</Kbd>
      <Kbd>K</Kbd>
    </KbdGroup>
  ),
};

export const WithButton: Story = {
  render: () => (
    <Button variant="outline" className="justify-between w-64">
      <span>Search...</span>
      <KbdGroup>
        <Kbd>⌘</Kbd>
        <Kbd>K</Kbd>
      </KbdGroup>
    </Button>
  ),
};

export const CompactVariants: Story = {
  render: () => (
    <div className="flex flex-col gap-3">
      <KbdGroup className="gap-0.5">
        <Kbd size="sm">⌘</Kbd>
        <Kbd size="sm">K</Kbd>
      </KbdGroup>

      <Button variant="outline" className="justify-between w-48">
        <span>Search...</span>
        <KbdGroup className="gap-0.5">
          <Kbd size="sm">⌘</Kbd>
          <Kbd size="sm">F</Kbd>
        </KbdGroup>
      </Button>
    </div>
  ),
};

export const ButtonWithHover: Story = {
  render: () => (
    <div className="flex flex-col gap-2">
      <Button variant="ghost" className="group justify-between w-64">
        <span>Copy</span>
        <KbdGroup
          aria-hidden
          className="opacity-0 transition-opacity duration-150 group-hover:opacity-100"
        >
          <Kbd>⌘</Kbd>
          <Kbd>C</Kbd>
        </KbdGroup>
      </Button>
      <Button variant="ghost" className="group justify-between w-64">
        <span>Paste</span>
        <KbdGroup
          aria-hidden
          className="opacity-0 transition-opacity duration-150 group-hover:opacity-100"
        >
          <Kbd>⌘</Kbd>
          <Kbd>V</Kbd>
        </KbdGroup>
      </Button>
      <Button variant="ghost" className="group justify-between w-64">
        <span>Cut</span>
        <KbdGroup
          aria-hidden
          className="opacity-0 transition-opacity duration-150 group-hover:opacity-100"
        >
          <Kbd>⌘</Kbd>
          <Kbd>X</Kbd>
        </KbdGroup>
      </Button>
    </div>
  ),
};

export const WithTooltip: Story = {
  render: () => (
    <TooltipProvider>
      <Tooltip
        content={
          <div className="flex items-center gap-2">
            <span className="text-xs leading-tight">Open command palette</span>
            <KbdGroup className="gap-1">
              <Kbd size="sm">⌘</Kbd>
              <Kbd size="sm">K</Kbd>
            </KbdGroup>
          </div>
        }
        contentClassName="text-muted-foreground"
      >
        <Button variant="outline">Search</Button>
      </Tooltip>
    </TooltipProvider>
  ),
};

export const SingleKeys: Story = {
  render: () => (
    <div className="flex gap-2">
      <Kbd>⌘</Kbd>
      <Kbd>⇧</Kbd>
      <Kbd>⌥</Kbd>
      <Kbd>⌃</Kbd>
      <Kbd>A</Kbd>
      <Kbd>Z</Kbd>
      <Kbd>↵</Kbd>
      <Kbd>⌫</Kbd>
    </div>
  ),
};

export const TextKeys: Story = {
  render: () => (
    <div className="flex gap-2 flex-wrap">
      <Kbd>Ctrl</Kbd>
      <Kbd>Shift</Kbd>
      <Kbd>Enter</Kbd>
      <Kbd>Escape</Kbd>
      <Kbd>Tab</Kbd>
      <Kbd>Space</Kbd>
    </div>
  ),
};
