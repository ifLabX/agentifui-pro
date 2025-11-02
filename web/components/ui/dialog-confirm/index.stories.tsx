import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react-vite";
import { fn } from "storybook/test";

import { Button } from "@/components/ui/button/index";

import { ConfirmDialog } from "./index";

const meta = {
  title: "UI/Dialog Confirm",
  component: ConfirmDialog,
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
    variant: {
      control: "select",
      options: ["default", "danger"],
      description: "Visual variant for the confirm button",
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
} satisfies Meta<typeof ConfirmDialog>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: undefined as any, // eslint-disable-line @typescript-eslint/no-explicit-any
  render: () => {
    const Demo = () => {
      const [open, setOpen] = useState(false);

      return (
        <>
          <Button onClick={() => setOpen(true)}>Show Confirm Dialog</Button>
          <ConfirmDialog
            open={open}
            onOpenChange={setOpen}
            title="Confirm Action"
            description="Please confirm that you want to proceed with this action."
            onConfirm={fn()}
          />
        </>
      );
    };

    return <Demo />;
  },
};

export const DangerVariant: Story = {
  args: undefined as any, // eslint-disable-line @typescript-eslint/no-explicit-any
  render: () => {
    const Demo = () => {
      const [open, setOpen] = useState(false);

      return (
        <>
          <Button variant="destructive" onClick={() => setOpen(true)}>
            Delete Item
          </Button>
          <ConfirmDialog
            open={open}
            onOpenChange={setOpen}
            variant="danger"
            title="Delete Item"
            description="This will permanently delete this item. This action cannot be undone."
            confirmText="Delete"
            cancelText="Keep"
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
          <Button onClick={() => setOpen(true)}>Publish Changes</Button>
          <ConfirmDialog
            open={open}
            onOpenChange={setOpen}
            title="Publish Changes"
            description="Your changes will be published and visible to all users. Do you want to continue?"
            confirmText="Yes, publish"
            cancelText="No, go back"
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
          <Button onClick={() => setOpen(true)}>Show Confirm Dialog</Button>
          <ConfirmDialog
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
          <Button onClick={() => setOpen(true)}>Start Async Operation</Button>
          <ConfirmDialog
            open={open}
            onOpenChange={setOpen}
            title="Async Operation"
            description="This will trigger a 2-second async operation when confirmed."
            confirmText="Start"
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

export const DangerWithAsyncConfirm: Story = {
  args: undefined as any, // eslint-disable-line @typescript-eslint/no-explicit-any
  render: () => {
    const Demo = () => {
      const [open, setOpen] = useState(false);
      const [status, setStatus] = useState<string>("Idle");

      const handleConfirm = async () => {
        setStatus("Deleting...");
        await new Promise(resolve => setTimeout(resolve, 1500));
        setStatus("Deleted at " + new Date().toLocaleTimeString());
        fn()();
      };

      return (
        <div className="flex flex-col gap-4">
          <Button variant="destructive" onClick={() => setOpen(true)}>
            Delete Account
          </Button>
          <ConfirmDialog
            open={open}
            onOpenChange={setOpen}
            variant="danger"
            title="Delete Account"
            description="This will permanently delete your account and all associated data. This operation may take a few seconds."
            confirmText="Delete Forever"
            cancelText="Cancel"
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
          <Button onClick={() => setOpen(true)}>Show Dialog</Button>
          <ConfirmDialog
            open={open}
            onOpenChange={setOpen}
            title="No Close Button"
            description="This confirm dialog doesn't have a close button. You must use the footer buttons."
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
          <Button onClick={() => setOpen(true)}>Show Loading Dialog</Button>
          <ConfirmDialog
            open={open}
            onOpenChange={setOpen}
            title="Loading State"
            description="This dialog is in a loading state. The buttons are disabled."
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
        <ConfirmDialog
          open={open}
          onOpenChange={setOpen}
          variant="danger"
          title="Remove User"
          description="This will remove the user from the team. They will need to be re-invited."
          confirmText="Remove"
          onConfirm={fn()}
        >
          <Button variant="destructive">Remove User</Button>
        </ConfirmDialog>
      );
    };

    return <Demo />;
  },
};

export const ComparisonDefaultVsDanger: Story = {
  args: undefined as any, // eslint-disable-line @typescript-eslint/no-explicit-any
  render: () => {
    const Demo = () => {
      const [openDefault, setOpenDefault] = useState(false);
      const [openDanger, setOpenDanger] = useState(false);

      return (
        <div className="flex gap-4">
          <>
            <Button onClick={() => setOpenDefault(true)}>
              Default Variant
            </Button>
            <ConfirmDialog
              open={openDefault}
              onOpenChange={setOpenDefault}
              variant="default"
              title="Default Variant"
              description="This uses the default button styling."
              onConfirm={fn()}
            />
          </>
          <>
            <Button variant="destructive" onClick={() => setOpenDanger(true)}>
              Danger Variant
            </Button>
            <ConfirmDialog
              open={openDanger}
              onOpenChange={setOpenDanger}
              variant="danger"
              title="Danger Variant"
              description="This uses the destructive/danger button styling."
              onConfirm={fn()}
            />
          </>
        </div>
      );
    };

    return <Demo />;
  },
};

export const AsAlertDialog: Story = {
  args: undefined as any, // eslint-disable-line @typescript-eslint/no-explicit-any
  render: () => {
    const Demo = () => {
      const [open, setOpen] = useState(false);

      return (
        <>
          <Button onClick={() => setOpen(true)}>Show Information</Button>
          <ConfirmDialog
            open={open}
            onOpenChange={setOpen}
            title="Information"
            description="This is an informational message. ConfirmDialog can be used as an alert dialog for notifications and information display."
            confirmText="Got it"
            cancelText="Close"
            onConfirm={fn()}
          />
        </>
      );
    };

    return <Demo />;
  },
};

export const AsSuccessAlert: Story = {
  args: undefined as any, // eslint-disable-line @typescript-eslint/no-explicit-any
  render: () => {
    const Demo = () => {
      const [open, setOpen] = useState(false);

      return (
        <>
          <Button onClick={() => setOpen(true)}>Show Success</Button>
          <ConfirmDialog
            open={open}
            onOpenChange={setOpen}
            title="Success"
            description="Your changes have been saved successfully."
            confirmText="OK"
            onConfirm={fn()}
          />
        </>
      );
    };

    return <Demo />;
  },
};
