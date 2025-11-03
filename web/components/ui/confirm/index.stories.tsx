import { useEffect, useState, type ReactNode } from "react";
import type { Meta, StoryObj } from "@storybook/react-vite";

import { Button } from "@/components/ui/button";

import { ConfirmDialog, type ConfirmDialogProps } from "./index";

const meta = {
  title: "UI/ConfirmDialog",
  component: ConfirmDialog,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  argTypes: {
    variant: {
      control: "inline-radio",
      options: ["default", "destructive"],
    },
    isLoading: {
      control: "boolean",
    },
    disableCancel: {
      control: "boolean",
    },
  },
} satisfies Meta<typeof ConfirmDialog>;

export default meta;

type Story = StoryObj<typeof meta>;

type TriggerRenderer = (controls: { onOpen: () => void }) => ReactNode;

function ManagedDialog(trigger: TriggerRenderer, props: ConfirmDialogProps) {
  const { open: controlledOpen, onCancel, onConfirm, ...restProps } = props;
  const [open, setOpen] = useState(controlledOpen ?? false);

  useEffect(() => {
    if (typeof controlledOpen === "boolean") {
      setOpen(controlledOpen);
    }
  }, [controlledOpen]);

  return (
    <div className="space-y-3">
      {trigger({ onOpen: () => setOpen(true) })}
      <ConfirmDialog
        {...restProps}
        open={open}
        onCancel={() => {
          onCancel?.();
          setOpen(false);
        }}
        onConfirm={() => {
          onConfirm?.();
          setOpen(false);
        }}
      />
    </div>
  );
}

export const Playground: Story = {
  args: {
    open: false,
    title: "Reset workspace preferences?",
    description:
      "This action restores notification, theme, and experimental flags to their defaults. Existing chats remain untouched.",
    confirmText: "Reset settings",
    cancelText: "Keep current",
  },
  render: args =>
    ManagedDialog(
      ({ onOpen }) => <Button onClick={onOpen}>Reset preferences</Button>,
      { ...args }
    ),
};

export const Destructive: Story = {
  args: {
    open: false,
    title: "Delete this conversation?",
    description:
      "All collaborators lose access to the thread and history. This action cannot be undone.",
    confirmText: "Delete conversation",
    cancelText: "Cancel",
    variant: "destructive",
    children: (
      <p>
        Messages created on <strong>March 24</strong> will be permanently
        removed.
      </p>
    ),
  },
  render: args =>
    ManagedDialog(
      ({ onOpen }) => (
        <Button variant="destructive" onClick={onOpen}>
          Delete conversation
        </Button>
      ),
      { ...args }
    ),
};

export const CancelDisabled: Story = {
  args: {
    open: false,
    title: "Require explicit acknowledgment?",
    description:
      "Users must confirm before leaving. Outside clicks and ESC are disabled to prevent accidental closure.",
    confirmText: "I understand",
    cancelText: "Cancel",
    disableCancel: true,
  },
  render: args =>
    ManagedDialog(
      ({ onOpen }) => (
        <Button variant="secondary" onClick={onOpen}>
          Review warning
        </Button>
      ),
      { ...args }
    ),
};

export const WithAdditionalContext: Story = {
  args: {
    open: false,
    title: "Pause nightly summaries?",
    description: "Notifications stop until the automation is reactivated.",
    confirmText: "Pause",
    cancelText: "Keep running",
    children: (
      <ul className="list-disc space-y-1 pl-4">
        <li>Existing summaries stay in the archive.</li>
        <li>Resume any time from Settings → Automations.</li>
      </ul>
    ),
  },
  render: args =>
    ManagedDialog(
      ({ onOpen }) => (
        <Button variant="secondary" onClick={onOpen}>
          Pause automation
        </Button>
      ),
      { ...args }
    ),
};

export const LoadingState: Story = {
  args: {
    open: false,
    title: "Transfer workspace ownership?",
    description:
      "We’ll notify the new owner by email. You retain editor permissions.",
    confirmText: "Transfer",
    cancelText: "Cancel",
  },
  render: args => {
    const [open, setOpen] = useState(false);
    const [loading, setLoading] = useState(false);

    return (
      <div className="space-y-3">
        <Button onClick={() => setOpen(true)}>Transfer ownership</Button>
        <ConfirmDialog
          {...args}
          open={open}
          isLoading={loading}
          disableCancel={loading}
          onCancel={() => {
            args.onCancel?.();
            setLoading(false);
            setOpen(false);
          }}
          onConfirm={() => {
            args.onConfirm?.();
            setLoading(true);
            setTimeout(() => {
              setLoading(false);
              setOpen(false);
            }, 1500);
          }}
        />
      </div>
    );
  },
};
