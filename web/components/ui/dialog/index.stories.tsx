import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react-vite";

import { Button } from "@/components/ui/button";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "./index";

const DialogDemo = () => {
  const [open, setOpen] = useState(false);

  return (
    <>
      <Button onClick={() => setOpen(true)}>Open dialog</Button>
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Enable multi-device sync</DialogTitle>
            <DialogDescription>
              Sync chat history and workspace preferences across every signed-in
              device. The process usually completes in less than a minute.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-3 text-sm text-muted-foreground">
            <p>
              Your data is securely encrypted and never leaves our
              infrastructure without your consent.
            </p>
            <p>Would you like to proceed?</p>
          </div>
          <DialogFooter>
            <Button variant="ghost" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button onClick={() => setOpen(false)}>Confirm</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
};

const WithoutCloseButtonDemo = () => {
  const [open, setOpen] = useState(false);

  return (
    <>
      <Button onClick={() => setOpen(true)}>Open forced dialog</Button>
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent showCloseButton={false}>
          <DialogHeader>
            <DialogTitle>Updating workspace</DialogTitle>
            <DialogDescription>
              This dialog intentionally hides the close button for forced
              actions.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="secondary" onClick={() => setOpen(false)}>
              Keep draft
            </Button>
            <Button onClick={() => setOpen(false)}>Continue</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
};

const meta: Meta<typeof DialogDemo> = {
  title: "UI/Dialog",
  component: DialogDemo,
  tags: ["autodocs"],
};

export default meta;

type Story = StoryObj<typeof DialogDemo>;

export const Default: Story = {
  render: () => <DialogDemo />,
};

export const WithoutCloseButton: Story = {
  render: () => <WithoutCloseButtonDemo />,
};

const LongContentDemo = () => {
  const [open, setOpen] = useState(false);

  return (
    <>
      <Button onClick={() => setOpen(true)}>Open release notes</Button>
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Release notes</DialogTitle>
            <DialogDescription>
              Scrollable content stays within the dialog bounds.
            </DialogDescription>
          </DialogHeader>
          <div
            className="space-y-4 overflow-y-auto text-sm text-muted-foreground"
            style={{ maxHeight: "16rem" }}
          >
            {[...Array(6)].map((_, index) => (
              <p key={index}>
                Version 3.{index + 1}.0 introduces advanced prompt history,
                improved voice input, and updates to enterprise controls. Review
                the settings page for the full breakdown.
              </p>
            ))}
          </div>
          <DialogFooter>
            <Button variant="ghost" onClick={() => setOpen(false)}>
              Later
            </Button>
            <Button onClick={() => setOpen(false)}>Install update</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
};

export const LongContent: Story = {
  render: () => <LongContentDemo />,
};
