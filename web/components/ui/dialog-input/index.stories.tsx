import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react-vite";
import { fn } from "storybook/test";

import { Button } from "@/components/ui/button/index";

import { InputDialog } from "./index";

const meta = {
  title: "UI/Dialog Input",
  component: InputDialog,
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
      description: "Dialog description",
    },
    label: {
      control: "text",
      description: "Label for the input field",
    },
    placeholder: {
      control: "text",
      description: "Placeholder text for the input",
    },
    defaultValue: {
      control: "text",
      description: "Default value for the input",
    },
    confirmText: {
      control: "text",
      description: "Text for confirm button",
    },
    cancelText: {
      control: "text",
      description: "Text for cancel button",
    },
    maxLength: {
      control: "number",
      description: "Maximum length for input",
    },
    onConfirm: {
      description: "Callback when confirm is clicked with input value",
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
} satisfies Meta<typeof InputDialog>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: undefined as any, // eslint-disable-line @typescript-eslint/no-explicit-any
  render: () => {
    const Demo = () => {
      const [open, setOpen] = useState(false);

      return (
        <>
          <Button onClick={() => setOpen(true)}>Edit Name</Button>
          <InputDialog
            open={open}
            onOpenChange={setOpen}
            title="Edit name"
            label="Name"
            placeholder="Enter your name"
            onConfirm={fn()}
          />
        </>
      );
    };

    return <Demo />;
  },
};

export const WithDescription: Story = {
  args: undefined as any, // eslint-disable-line @typescript-eslint/no-explicit-any
  render: () => {
    const Demo = () => {
      const [open, setOpen] = useState(false);

      return (
        <>
          <Button onClick={() => setOpen(true)}>Rename Project</Button>
          <InputDialog
            open={open}
            onOpenChange={setOpen}
            title="Rename project"
            description="Enter a new name for your project. This will be visible to all team members."
            label="Project name"
            placeholder="My Awesome Project"
            confirmText="Rename"
            onConfirm={fn()}
          />
        </>
      );
    };

    return <Demo />;
  },
};

export const WithDefaultValue: Story = {
  args: undefined as any, // eslint-disable-line @typescript-eslint/no-explicit-any
  render: () => {
    const Demo = () => {
      const [open, setOpen] = useState(false);

      return (
        <>
          <Button onClick={() => setOpen(true)}>Edit Username</Button>
          <InputDialog
            open={open}
            onOpenChange={setOpen}
            title="Edit username"
            label="Username"
            placeholder="Enter username"
            defaultValue="john_doe_123"
            confirmText="Update"
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
          <Button onClick={() => setOpen(true)}>Add Tag</Button>
          <InputDialog
            open={open}
            onOpenChange={setOpen}
            title="Add new tag"
            description="Tags help organize your content."
            label="Tag name"
            placeholder="e.g., Important, Urgent, Review"
            confirmText="Add tag"
            cancelText="Discard"
            onConfirm={fn()}
          />
        </>
      );
    };

    return <Demo />;
  },
};

export const WithMaxLength: Story = {
  args: undefined as any, // eslint-disable-line @typescript-eslint/no-explicit-any
  render: () => {
    const Demo = () => {
      const [open, setOpen] = useState(false);

      return (
        <>
          <Button onClick={() => setOpen(true)}>Set Bio</Button>
          <InputDialog
            open={open}
            onOpenChange={setOpen}
            title="Edit bio"
            description="Your bio is limited to 50 characters."
            label="Bio"
            placeholder="Tell us about yourself"
            maxLength={50}
            confirmText="Save bio"
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
      const [savedValue, setSavedValue] = useState<string | null>(null);

      const handleConfirm = (value: string) => {
        setSavedValue(value);
        fn()(value);
      };

      return (
        <div className="flex flex-col gap-4">
          <Button onClick={() => setOpen(true)}>Edit Title</Button>
          <InputDialog
            open={open}
            onOpenChange={setOpen}
            title="Edit title"
            label="Title"
            placeholder="Enter title"
            defaultValue={savedValue || ""}
            onConfirm={handleConfirm}
          />
          {savedValue && (
            <div className="rounded-md border p-4 text-sm">
              <p className="font-medium">Saved value:</p>
              <p className="text-muted-foreground">{savedValue}</p>
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
      const [savedValue, setSavedValue] = useState<string>("");

      const handleConfirm = async (value: string) => {
        setStatus("Saving...");
        // Simulate async operation
        await new Promise(resolve => setTimeout(resolve, 2000));
        setSavedValue(value);
        setStatus("Saved at " + new Date().toLocaleTimeString());
        fn()(value);
      };

      return (
        <div className="flex flex-col gap-4">
          <Button onClick={() => setOpen(true)}>Edit Description</Button>
          <InputDialog
            open={open}
            onOpenChange={setOpen}
            title="Edit description"
            description="This will trigger a 2-second save operation."
            label="Description"
            placeholder="Enter description"
            defaultValue={savedValue}
            confirmText="Save"
            onConfirm={handleConfirm}
          />
          <div className="rounded-md border p-4 text-sm space-y-2">
            <div>
              <p className="font-medium">Status:</p>
              <p className="text-muted-foreground">{status}</p>
            </div>
            {savedValue && (
              <div>
                <p className="font-medium">Current value:</p>
                <p className="text-muted-foreground">{savedValue}</p>
              </div>
            )}
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
          <Button onClick={() => setOpen(true)}>Edit Item</Button>
          <InputDialog
            open={open}
            onOpenChange={setOpen}
            title="Edit item"
            label="Item name"
            placeholder="Enter item name"
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
          <InputDialog
            open={open}
            onOpenChange={setOpen}
            title="Loading State"
            label="Value"
            placeholder="Enter value"
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
        <InputDialog
          open={open}
          onOpenChange={setOpen}
          title="Quick edit"
          label="Name"
          placeholder="Enter name"
          onConfirm={fn()}
        >
          <Button variant="outline">Edit Name</Button>
        </InputDialog>
      );
    };

    return <Demo />;
  },
};

export const AutoFocusAndSelect: Story = {
  args: undefined as any, // eslint-disable-line @typescript-eslint/no-explicit-any
  render: () => {
    const Demo = () => {
      const [open, setOpen] = useState(false);

      return (
        <div className="flex flex-col gap-4">
          <Button onClick={() => setOpen(true)}>Edit Email</Button>
          <InputDialog
            open={open}
            onOpenChange={setOpen}
            title="Edit email address"
            description="The input will be automatically focused and selected when the dialog opens."
            label="Email"
            placeholder="email@example.com"
            defaultValue="user@example.com"
            onConfirm={fn()}
          />
          <div className="rounded-md border p-4 text-sm">
            <p className="font-medium">Features:</p>
            <ul className="list-disc list-inside space-y-1 text-muted-foreground">
              <li>Input is automatically focused when dialog opens</li>
              <li>Text is automatically selected for easy replacement</li>
              <li>Submit disabled when input is empty</li>
              <li>Press Enter to submit the form</li>
            </ul>
          </div>
        </div>
      );
    };

    return <Demo />;
  },
};

export const ValidationExample: Story = {
  args: undefined as any, // eslint-disable-line @typescript-eslint/no-explicit-any
  render: () => {
    const Demo = () => {
      const [open, setOpen] = useState(false);

      return (
        <div className="flex flex-col gap-4">
          <Button onClick={() => setOpen(true)}>Try Empty Submission</Button>
          <InputDialog
            open={open}
            onOpenChange={setOpen}
            title="Input validation"
            description="Try submitting with an empty or whitespace-only value."
            label="Required field"
            placeholder="This field is required"
            onConfirm={fn()}
          />
          <div className="rounded-md border p-4 text-sm">
            <p className="font-medium">Validation rules:</p>
            <ul className="list-disc list-inside space-y-1 text-muted-foreground">
              <li>Input is trimmed before validation</li>
              <li>Empty or whitespace-only values are not allowed</li>
              <li>Submit button is disabled when input is invalid</li>
            </ul>
          </div>
        </div>
      );
    };

    return <Demo />;
  },
};
