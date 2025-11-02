import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react-vite";

import { Button } from "@/components/ui/button/index";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "./index";

const meta = {
  title: "UI/Dialog",
  component: Dialog,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  decorators: [
    Story => (
      <div className="p-4">
        <Story />
      </div>
    ),
  ],
} satisfies Meta<typeof Dialog>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {},
  render: () => (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline">Open Dialog</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Dialog Title</DialogTitle>
          <DialogDescription>
            This is a description of what the dialog is about.
          </DialogDescription>
        </DialogHeader>
        <div className="py-4">
          <p className="text-sm text-dialog-text-secondary">
            Dialog content goes here.
          </p>
        </div>
        <DialogFooter>
          <Button variant="outline">Cancel</Button>
          <Button>Confirm</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  ),
};

export const WithoutCloseButton: Story = {
  args: {},
  render: () => (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline">Open Dialog (No Close Button)</Button>
      </DialogTrigger>
      <DialogContent showCloseButton={false}>
        <DialogHeader>
          <DialogTitle>Dialog Without Close Button</DialogTitle>
          <DialogDescription>
            This dialog doesn&apos;t have a close button in the top right.
          </DialogDescription>
        </DialogHeader>
        <div className="py-4">
          <p className="text-sm text-dialog-text-secondary">
            You must use the footer buttons to close this dialog.
          </p>
        </div>
        <DialogFooter>
          <Button variant="outline">Close</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  ),
};

export const CustomCloseLabel: Story = {
  args: {},
  render: () => (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline">Open Dialog (Custom Close Label)</Button>
      </DialogTrigger>
      <DialogContent closeButtonLabel="Dismiss dialog">
        <DialogHeader>
          <DialogTitle>Custom Accessibility Label</DialogTitle>
          <DialogDescription>
            The close button has a custom aria-label for accessibility.
          </DialogDescription>
        </DialogHeader>
        <div className="py-4">
          <p className="text-sm text-dialog-text-secondary">
            Hover over the close button and inspect it to see the custom label.
          </p>
        </div>
      </DialogContent>
    </Dialog>
  ),
};

export const ControlledState: Story = {
  args: {},
  render: () => {
    const ControlledDemo = () => {
      const [open, setOpen] = useState(false);

      return (
        <div className="flex flex-col gap-4">
          <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild>
              <Button variant="outline">Open Controlled Dialog</Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Controlled Dialog</DialogTitle>
                <DialogDescription>
                  This dialog&apos;s open state is controlled externally.
                </DialogDescription>
              </DialogHeader>
              <div className="py-4">
                <p className="text-sm text-dialog-text-secondary">
                  You can open and close this dialog programmatically.
                </p>
              </div>
              <DialogFooter>
                <Button variant="outline" onClick={() => setOpen(false)}>
                  Close
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
          <div className="rounded-md border p-4 text-sm">
            <p className="font-medium mb-2">External Controls:</p>
            <div className="flex gap-2">
              <Button size="sm" onClick={() => setOpen(true)}>
                Open Dialog
              </Button>
              <Button
                size="sm"
                variant="outline"
                onClick={() => setOpen(false)}
              >
                Close Dialog
              </Button>
            </div>
            <p className="mt-2 text-muted-foreground">
              Current state: {open ? "Open" : "Closed"}
            </p>
          </div>
        </div>
      );
    };

    return <ControlledDemo />;
  },
};

export const LongContent: Story = {
  args: {},
  render: () => (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline">Open Dialog with Long Content</Button>
      </DialogTrigger>
      <DialogContent className="max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Dialog with Scrollable Content</DialogTitle>
          <DialogDescription>
            This dialog contains long content that requires scrolling.
          </DialogDescription>
        </DialogHeader>
        <div className="py-4 space-y-4">
          {Array.from({ length: 20 }).map((_, i) => (
            <p key={i} className="text-sm text-dialog-text-secondary">
              Paragraph {i + 1}: Lorem ipsum dolor sit amet, consectetur
              adipiscing elit. Sed do eiusmod tempor incididunt ut labore et
              dolore magna aliqua.
            </p>
          ))}
        </div>
        <DialogFooter>
          <Button variant="outline">Cancel</Button>
          <Button>Confirm</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  ),
};

export const NestedDialogs: Story = {
  args: {},
  render: () => (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline">Open First Dialog</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>First Dialog</DialogTitle>
          <DialogDescription>
            You can open another dialog from within this one.
          </DialogDescription>
        </DialogHeader>
        <div className="py-4">
          <Dialog>
            <DialogTrigger asChild>
              <Button variant="outline">Open Second Dialog</Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Second Dialog</DialogTitle>
                <DialogDescription>
                  This is a nested dialog. Close this to return to the first
                  dialog.
                </DialogDescription>
              </DialogHeader>
              <DialogFooter>
                <Button>Got it</Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </div>
        <DialogFooter>
          <Button>Close</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  ),
};
