import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react-vite";
import { fn } from "storybook/test";

import { Button } from "@/components/ui/button/index";

import { AlertDialog } from "./index";

const meta = {
  title: "UI/Dialog Alert",
  component: AlertDialog,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  argTypes: {
    title: {
      control: "text",
      description: "Dialog title",
    },
    description: {
      control: "text",
      description: "Dialog description/message",
    },
    confirmText: {
      control: "text",
      description: "Text for confirm button",
    },
    cancelText: {
      control: "text",
      description: "Text for cancel button",
    },
    onConfirm: {
      description: "Callback when confirm is clicked",
    },
    showCloseButton: {
      control: "boolean",
      description: "Whether to show the close button",
    },
    isLoading: {
      control: "boolean",
      description: "Loading state",
    },
  },
  decorators: [
    Story => (
      <div className="p-4">
        <Story />
      </div>
    ),
  ],
} satisfies Meta<typeof AlertDialog>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: undefined as any, // eslint-disable-line @typescript-eslint/no-explicit-any
  render: () => {
    const Demo = () => {
      const [open, setOpen] = useState(false);

      return (
        <>
          <Button onClick={() => setOpen(true)}>Show Alert</Button>
          <AlertDialog
            open={open}
            onOpenChange={setOpen}
            title="Are you sure?"
            description="This action cannot be undone. This will permanently delete your data."
            onConfirm={fn()}
          />
        </>
      );
    };

    return <Demo />;
  },
};

export const WithCustomText: Story = {
  args: undefined as any, // eslint-disable-line @typescript-eslint/no-explicit-any
  render: () => {
    const Demo = () => {
      const [open, setOpen] = useState(false);

      return (
        <>
          <Button onClick={() => setOpen(true)}>Delete Account</Button>
          <AlertDialog
            open={open}
            onOpenChange={setOpen}
            title="Delete Account"
            description="Are you absolutely sure you want to delete your account? All your data will be permanently removed from our servers."
            confirmText="Yes, delete my account"
            cancelText="No, keep my account"
            onConfirm={fn()}
          />
        </>
      );
    };

    return <Demo />;
  },
};

export const WithConfirmCallback: Story = {
  args: undefined as any, // eslint-disable-line @typescript-eslint/no-explicit-any
  render: () => {
    const Demo = () => {
      const [open, setOpen] = useState(false);
      const [lastAction, setLastAction] = useState<string | null>(null);

      const handleConfirm = () => {
        setLastAction("Confirmed at " + new Date().toLocaleTimeString());
        fn()();
      };

      return (
        <div className="flex flex-col gap-4">
          <Button onClick={() => setOpen(true)}>Show Alert</Button>
          <AlertDialog
            open={open}
            onOpenChange={setOpen}
            title="Confirm Action"
            description="Click confirm to see the callback in action."
            onConfirm={handleConfirm}
          />
          {lastAction && (
            <div className="rounded-md border p-4 text-sm">
              <p className="font-medium">Last action:</p>
              <p className="text-muted-foreground">{lastAction}</p>
            </div>
          )}
        </div>
      );
    };

    return <Demo />;
  },
};

export const AsyncConfirm: Story = {
  args: undefined as any, // eslint-disable-line @typescript-eslint/no-explicit-any
  render: () => {
    const Demo = () => {
      const [open, setOpen] = useState(false);
      const [status, setStatus] = useState<string>("Idle");

      const handleConfirm = async () => {
        setStatus("Processing...");
        // Simulate async operation
        await new Promise(resolve => setTimeout(resolve, 2000));
        setStatus("Completed at " + new Date().toLocaleTimeString());
        fn()();
      };

      return (
        <div className="flex flex-col gap-4">
          <Button onClick={() => setOpen(true)}>Show Async Alert</Button>
          <AlertDialog
            open={open}
            onOpenChange={setOpen}
            title="Async Operation"
            description="This will trigger a 2-second async operation when confirmed."
            confirmText="Start Operation"
            onConfirm={handleConfirm}
          />
          <div className="rounded-md border p-4 text-sm">
            <p className="font-medium">Status:</p>
            <p className="text-muted-foreground">{status}</p>
          </div>
        </div>
      );
    };

    return <Demo />;
  },
};

export const WithoutCloseButton: Story = {
  args: undefined as any, // eslint-disable-line @typescript-eslint/no-explicit-any
  render: () => {
    const Demo = () => {
      const [open, setOpen] = useState(false);

      return (
        <>
          <Button onClick={() => setOpen(true)}>Show Alert</Button>
          <AlertDialog
            open={open}
            onOpenChange={setOpen}
            title="No Close Button"
            description="This alert dialog doesn't have a close button. You must use the footer buttons."
            showCloseButton={false}
            onConfirm={fn()}
          />
        </>
      );
    };

    return <Demo />;
  },
};

export const LoadingState: Story = {
  args: undefined as any, // eslint-disable-line @typescript-eslint/no-explicit-any
  render: () => {
    const Demo = () => {
      const [open, setOpen] = useState(false);

      return (
        <>
          <Button onClick={() => setOpen(true)}>Show Loading Alert</Button>
          <AlertDialog
            open={open}
            onOpenChange={setOpen}
            title="Loading State"
            description="This alert is in a loading state. The buttons are disabled."
            isLoading={true}
            onConfirm={fn()}
          />
        </>
      );
    };

    return <Demo />;
  },
};

export const WithTriggerChild: Story = {
  args: undefined as any, // eslint-disable-line @typescript-eslint/no-explicit-any
  render: () => {
    const Demo = () => {
      const [open, setOpen] = useState(false);

      return (
        <AlertDialog
          open={open}
          onOpenChange={setOpen}
          title="With Trigger"
          description="This alert uses a child as the trigger button."
          onConfirm={fn()}
        >
          <Button variant="destructive">Delete Item</Button>
        </AlertDialog>
      );
    };

    return <Demo />;
  },
};
