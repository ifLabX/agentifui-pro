import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react-vite";

import { Button } from "@/components/ui/button";

import { Popover, PopoverContent, PopoverTrigger } from "./index";

const meta = {
  title: "UI/Popover",
  component: Popover,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
} satisfies Meta<typeof Popover>;

export default meta;

type Story = StoryObj<typeof meta>;

const DefaultPopoverDemo = () => {
  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="outline">Open popover</Button>
      </PopoverTrigger>
      <PopoverContent>
        <div className="space-y-2">
          <h4 className="font-medium leading-none">Dimensions</h4>
          <p className="text-sm text-muted-foreground">
            Set the dimensions for the layer.
          </p>
        </div>
      </PopoverContent>
    </Popover>
  );
};

export const Default: Story = {
  render: () => <DefaultPopoverDemo />,
};

const PositionDemo = ({
  side,
}: {
  side: "top" | "right" | "bottom" | "left";
}) => {
  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="outline">{side}</Button>
      </PopoverTrigger>
      <PopoverContent side={side}>
        <p className="text-sm">Popover positioned on {side}</p>
      </PopoverContent>
    </Popover>
  );
};

export const Top: Story = {
  render: () => <PositionDemo side="top" />,
};

export const Right: Story = {
  render: () => <PositionDemo side="right" />,
};

export const Bottom: Story = {
  render: () => <PositionDemo side="bottom" />,
};

export const Left: Story = {
  render: () => <PositionDemo side="left" />,
};

const ControlledDemo = () => {
  const [open, setOpen] = useState(false);

  return (
    <div className="flex flex-col items-center gap-4">
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button variant="outline">Controlled popover</Button>
        </PopoverTrigger>
        <PopoverContent>
          <p className="text-sm">This is a controlled popover</p>
        </PopoverContent>
      </Popover>
      <div className="flex gap-2">
        <Button size="sm" onClick={() => setOpen(true)}>
          Open
        </Button>
        <Button size="sm" variant="outline" onClick={() => setOpen(false)}>
          Close
        </Button>
      </div>
      <div className="text-sm text-muted-foreground">
        Popover is {open ? "open" : "closed"}
      </div>
    </div>
  );
};

export const Controlled: Story = {
  render: () => <ControlledDemo />,
};

const AlignmentDemo = () => {
  return (
    <div className="flex flex-col gap-4">
      <Popover>
        <PopoverTrigger asChild>
          <Button variant="outline">Start alignment</Button>
        </PopoverTrigger>
        <PopoverContent align="start">
          <p className="text-sm">Aligned to start</p>
        </PopoverContent>
      </Popover>
      <Popover>
        <PopoverTrigger asChild>
          <Button variant="outline">Center alignment</Button>
        </PopoverTrigger>
        <PopoverContent align="center">
          <p className="text-sm">Aligned to center</p>
        </PopoverContent>
      </Popover>
      <Popover>
        <PopoverTrigger asChild>
          <Button variant="outline">End alignment</Button>
        </PopoverTrigger>
        <PopoverContent align="end">
          <p className="text-sm">Aligned to end</p>
        </PopoverContent>
      </Popover>
    </div>
  );
};

export const Alignments: Story = {
  render: () => <AlignmentDemo />,
};

const WithFormDemo = () => {
  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="outline">Update dimensions</Button>
      </PopoverTrigger>
      <PopoverContent className="w-80">
        <div className="grid gap-4">
          <div className="space-y-2">
            <h4 className="font-medium leading-none">Dimensions</h4>
            <p className="text-sm text-muted-foreground">
              Set the dimensions for the layer.
            </p>
          </div>
          <div className="grid gap-2">
            <div className="grid grid-cols-3 items-center gap-4">
              <label htmlFor="width" className="text-sm">
                Width
              </label>
              <input
                id="width"
                defaultValue="100%"
                className="col-span-2 h-8 rounded-md border px-2 text-sm"
              />
            </div>
            <div className="grid grid-cols-3 items-center gap-4">
              <label htmlFor="height" className="text-sm">
                Height
              </label>
              <input
                id="height"
                defaultValue="25px"
                className="col-span-2 h-8 rounded-md border px-2 text-sm"
              />
            </div>
          </div>
        </div>
      </PopoverContent>
    </Popover>
  );
};

export const WithForm: Story = {
  render: () => <WithFormDemo />,
};

const CustomWidthDemo = () => {
  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="outline">Wide popover</Button>
      </PopoverTrigger>
      <PopoverContent className="w-96">
        <div className="space-y-2">
          <h4 className="font-medium leading-none">Wide content</h4>
          <p className="text-sm text-muted-foreground">
            This popover has a custom width of 24rem (384px). You can customize
            the width by adding a className to PopoverContent.
          </p>
        </div>
      </PopoverContent>
    </Popover>
  );
};

export const CustomWidth: Story = {
  render: () => <CustomWidthDemo />,
};
