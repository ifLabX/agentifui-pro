import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { Button } from "../button";
import { Tooltip, TooltipProvider, TooltipWrapper } from "./index";

const meta = {
  title: "UI/Tooltip",
  component: Tooltip,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  decorators: [
    Story => (
      <TooltipProvider delayDuration={200}>
        <div className="p-20">
          <Story />
        </div>
      </TooltipProvider>
    ),
  ],
  argTypes: {
    side: {
      control: "select",
      options: ["top", "right", "bottom", "left"],
      description: "The preferred side of the trigger to render against",
    },
    align: {
      control: "select",
      options: ["start", "center", "end"],
      description: "The preferred alignment against the trigger",
    },
    disabled: {
      control: "boolean",
      description: "Whether the tooltip is disabled",
    },
    delayDuration: {
      control: "number",
      description:
        "The duration from when the mouse enters until the tooltip opens (ms)",
    },
  },
} satisfies Meta<typeof Tooltip>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    content: "This is a helpful tooltip",
  },
};

export const WithCustomTrigger: Story = {
  args: {
    content: "Tooltip content here",
    children: <Button variant="outline">Hover me</Button>,
  },
};

export const Top: Story = {
  args: {
    content: "Tooltip positioned on top",
    side: "top",
    children: <Button variant="outline">Top</Button>,
  },
};

export const Right: Story = {
  args: {
    content: "Tooltip positioned on right",
    side: "right",
    children: <Button variant="outline">Right</Button>,
  },
};

export const Bottom: Story = {
  args: {
    content: "Tooltip positioned on bottom",
    side: "bottom",
    children: <Button variant="outline">Bottom</Button>,
  },
};

export const Left: Story = {
  args: {
    content: "Tooltip positioned on left",
    side: "left",
    children: <Button variant="outline">Left</Button>,
  },
};

export const LongContent: Story = {
  args: {
    content:
      "This is a longer tooltip with more detailed information that helps explain the feature or functionality in greater detail.",
    children: <Button variant="outline">Long content</Button>,
  },
};

export const Disabled: Story = {
  args: {
    content: "You should not see this",
    disabled: true,
    children: <Button variant="outline">Disabled tooltip</Button>,
  },
};

export const Controlled: Story = {
  render: () => {
    const ControlledDemo = () => {
      const [open, setOpen] = useState(false);

      return (
        <div className="flex flex-col items-center gap-4">
          <Tooltip
            content="This is a controlled tooltip"
            open={open}
            onOpenChange={setOpen}
          >
            <Button variant="outline">Controlled Tooltip</Button>
          </Tooltip>
          <div className="flex gap-2">
            <Button size="sm" onClick={() => setOpen(true)}>
              Open
            </Button>
            <Button size="sm" variant="outline" onClick={() => setOpen(false)}>
              Close
            </Button>
          </div>
          <div className="text-sm">Tooltip is {open ? "open" : "closed"}</div>
        </div>
      );
    };

    return <ControlledDemo />;
  },
};

export const MultipleTooltips: Story = {
  render: () => (
    <div className="flex gap-4">
      <Tooltip content="First tooltip">
        <Button variant="outline">One</Button>
      </Tooltip>
      <Tooltip content="Second tooltip">
        <Button variant="outline">Two</Button>
      </Tooltip>
      <Tooltip content="Third tooltip">
        <Button variant="outline">Three</Button>
      </Tooltip>
    </div>
  ),
};

export const WithTooltipManager: Story = {
  render: () => (
    <div className="flex gap-4">
      <Tooltip content="Only one tooltip can be open at a time due to tooltip manager">
        <Button variant="outline">Hover 1</Button>
      </Tooltip>
      <Tooltip content="Try hovering between these buttons quickly">
        <Button variant="outline">Hover 2</Button>
      </Tooltip>
      <Tooltip content="The manager ensures only one tooltip shows">
        <Button variant="outline">Hover 3</Button>
      </Tooltip>
    </div>
  ),
};

export const DifferentAlignments: Story = {
  render: () => (
    <div className="flex flex-col gap-4">
      <Tooltip content="Aligned to start" align="start" side="bottom">
        <Button variant="outline">Start Alignment</Button>
      </Tooltip>
      <Tooltip content="Aligned to center" align="center" side="bottom">
        <Button variant="outline">Center Alignment</Button>
      </Tooltip>
      <Tooltip content="Aligned to end" align="end" side="bottom">
        <Button variant="outline">End Alignment</Button>
      </Tooltip>
    </div>
  ),
};

export const WithTooltipWrapper: Story = {
  render: () => (
    <TooltipWrapper content="This uses TooltipWrapper for SSR safety">
      <Button variant="outline">Wrapped Tooltip</Button>
    </TooltipWrapper>
  ),
};

export const QuickDelay: Story = {
  args: {
    content: "Quick to appear (100ms delay)",
    delayDuration: 100,
    children: <Button variant="outline">Quick delay</Button>,
  },
};

export const LongDelay: Story = {
  args: {
    content: "Takes longer to appear (1000ms delay)",
    delayDuration: 1000,
    children: <Button variant="outline">Long delay</Button>,
  },
};

export const InlineText: Story = {
  render: () => (
    <p className="text-sm">
      This is some text with an{" "}
      <Tooltip content="Additional information appears here">
        <span className="underline decoration-dotted cursor-help">
          inline tooltip
        </span>
      </Tooltip>{" "}
      that provides extra context.
    </p>
  ),
};
