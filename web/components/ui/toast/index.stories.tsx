import type { Meta, StoryObj } from "@storybook/react-vite";

import { Button } from "@/components/ui/button";

import { toast, Toaster } from "./index";

const meta = {
  title: "UI/Toast",
  component: Toaster,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
} satisfies Meta<typeof Toaster>;

export default meta;

type Story = StoryObj<typeof meta>;

const ToastPlayground = () => {
  const showDefault = () =>
    toast("Workflow saved", {
      description: "Your latest automation draft is ready to run.",
    });

  const showSuccess = () =>
    toast.success("Agents deployed", {
      description: "Three new agents picked up the triage queue.",
    });

  const showInfo = () =>
    toast.info("New integration", {
      description: "Salesforce sandbox connection is now live.",
    });

  const showWarning = () =>
    toast.warning("Limited capacity", {
      description: "Only two GPU workers remain available.",
    });

  const showError = () =>
    toast.error("Sync failed", {
      description: "Vector store credentials were revoked.",
    });

  const showAction = () =>
    toast("Event scheduled", {
      description: "Sunday, December 03, 2023 at 9:00 AM",
      action: {
        label: "Undo",
        onClick: () =>
          toast.success("Event restored", {
            description: "We reverted the change and notified your team.",
          }),
      },
      cancel: {
        label: "Dismiss",
        onClick: () => toast.dismiss(),
      },
    });

  return (
    <div className="flex flex-col items-center gap-4">
      <Toaster position="top-center" richColors closeButton />
      <div className="flex flex-wrap justify-center gap-3">
        <Button onClick={showDefault}>Show default</Button>
        <Button variant="secondary" onClick={showSuccess}>
          Show success
        </Button>
        <Button variant="outline" onClick={showInfo}>
          Show info
        </Button>
        <Button variant="ghost" onClick={showWarning}>
          Show warning
        </Button>
        <Button variant="destructive" onClick={showError}>
          Show error
        </Button>
        <Button variant="outline" onClick={showAction}>
          Show action toast
        </Button>
      </div>
    </div>
  );
};

export const Playground: Story = {
  render: () => <ToastPlayground />,
};

const ToastWithoutCloseButton = () => {
  const showToast = () =>
    toast("Focus mode enabled", {
      description: "You will stay in DND until 4:00 PM today.",
    });

  return (
    <div className="flex flex-col items-center gap-4">
      <Toaster position="top-center" closeButton={false} />
      <Button onClick={showToast}>Show toast without close button</Button>
    </div>
  );
};

export const WithoutCloseButton: Story = {
  render: () => <ToastWithoutCloseButton />,
};

const CustomSizeToast = () => {
  const showCustomToast = () =>
    toast("Quarterly review is ready", {
      description:
        "The detailed summary spans multiple metrics. Resize toast to see all highlights at once.",
    });

  return (
    <div className="flex flex-col items-center gap-4">
      <Toaster
        position="top-center"
        closeButton
        toastOptions={{
          classNames: {
            toast: "w-[420px] max-w-full px-6 py-5",
            description: "text-sm leading-relaxed",
          },
        }}
      />
      <Button variant="secondary" onClick={showCustomToast}>
        Show wide toast
      </Button>
    </div>
  );
};

export const CustomSizing: Story = {
  render: () => <CustomSizeToast />,
};
