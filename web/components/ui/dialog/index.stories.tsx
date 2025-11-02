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

const meta = {
  title: "UI/Dialog",
  component: Dialog,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
} satisfies Meta<typeof Dialog>;

export default meta;

type Story = StoryObj<typeof meta>;

const DefaultDialogDemo = () => {
  const [open, setOpen] = useState(false);

  return (
    <div className="space-y-3">
      <Button onClick={() => setOpen(true)}>Enable sync</Button>
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Enable multi-device sync</DialogTitle>
            <DialogDescription>
              Sync chat history and workspace preferences across every signed-in
              device. We’ll email you when the first sync completes.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-3 text-sm text-muted-foreground">
            <p>
              Syncing keeps your drafts and history aligned across desktop and
              mobile apps. You can disable it at any time from settings.
            </p>
          </div>
          <DialogFooter>
            <Button variant="ghost" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button onClick={() => setOpen(false)}>Enable sync</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export const Default: Story = {
  render: () => <DefaultDialogDemo />,
};

const ForcedActionDialog = () => {
  const [open, setOpen] = useState(false);

  return (
    <div className="space-y-3">
      <Button variant="outline" onClick={() => setOpen(true)}>
        Force update
      </Button>
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent showCloseButton={false}>
          <DialogHeader>
            <DialogTitle>Updating workspace</DialogTitle>
            <DialogDescription>
              This update introduces new permissions. You need to confirm before
              continuing.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="secondary" onClick={() => setOpen(false)}>
              Review later
            </Button>
            <Button onClick={() => setOpen(false)}>Apply update</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export const WithoutCloseButton: Story = {
  render: () => <ForcedActionDialog />,
};

const ScrollableDialog = () => {
  const [open, setOpen] = useState(false);

  return (
    <div className="space-y-3">
      <Button onClick={() => setOpen(true)}>View release notes</Button>
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
                improved voice input, analytics dashboards, and refreshed
                workspace permissions. Visit settings for the full breakdown.
              </p>
            ))}
          </div>
          <DialogFooter>
            <Button variant="ghost" onClick={() => setOpen(false)}>
              Dismiss
            </Button>
            <Button onClick={() => setOpen(false)}>Install update</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export const LongContent: Story = {
  render: () => <ScrollableDialog />,
};

const CustomActionsDialog = () => {
  const [open, setOpen] = useState(false);

  return (
    <div className="space-y-3">
      <Button variant="secondary" onClick={() => setOpen(true)}>
        Export transcript
      </Button>
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Export conversation transcript</DialogTitle>
            <DialogDescription>
              Choose the format and destination. Transcript includes attachments
              and system messages.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 text-sm text-muted-foreground">
            <p>Select export format:</p>
            <div className="flex gap-2">
              <Button variant="outline">Markdown</Button>
              <Button variant="outline">PDF</Button>
              <Button variant="outline">JSON</Button>
            </div>
          </div>
          <DialogFooter className="sm:flex-row sm:justify-between">
            <Button variant="ghost" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <div className="flex gap-2">
              <Button variant="outline">Send via email</Button>
              <Button onClick={() => setOpen(false)}>Download</Button>
            </div>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export const CustomActions: Story = {
  render: () => <CustomActionsDialog />,
};
