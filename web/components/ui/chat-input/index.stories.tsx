import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react-vite";
import { fn } from "storybook/test";

import { ChatInput } from "./index";

const meta = {
  title: "UI/ChatInput",
  component: ChatInput,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  argTypes: {
    onSubmit: {
      description: "Callback when message is submitted",
    },
    placeholder: {
      control: "text",
      description: "Placeholder text for the input",
    },
    disabled: {
      control: "boolean",
      description: "Whether the input is disabled",
    },
  },
  args: {
    onSubmit: fn(),
  },
  decorators: [
    Story => (
      <div className="w-full max-w-3xl p-4">
        <Story />
      </div>
    ),
  ],
} satisfies Meta<typeof ChatInput>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {},
};

export const WithCustomPlaceholder: Story = {
  args: {
    placeholder: "Ask me anything...",
  },
};

export const Disabled: Story = {
  args: {
    disabled: true,
  },
};

export const WithMessage: Story = {
  render: () => {
    const WithMessageDemo = () => {
      // Demo component to show input behavior
      return (
        <div className="flex flex-col gap-4">
          <ChatInput onSubmit={fn()} />
          <div className="text-sm text-muted-foreground">
            Note: This story shows the empty state. Type to see the input
            expand.
          </div>
        </div>
      );
    };

    return <WithMessageDemo />;
  },
};

export const WithSubmitHandler: Story = {
  render: () => {
    const SubmitHandlerDemo = () => {
      const [lastSubmitted, setLastSubmitted] = useState<{
        message: string;
        attachmentCount: number;
      } | null>(null);

      const handleSubmit = (
        message: string,
        attachments: Array<{ id: string; name: string }>
      ) => {
        setLastSubmitted({
          message,
          attachmentCount: attachments.length,
        });
        fn()(message, attachments);
      };

      return (
        <div className="flex flex-col gap-4">
          <ChatInput onSubmit={handleSubmit} />
          {lastSubmitted && (
            <div className="rounded-md border p-4 space-y-2">
              <p className="text-sm font-medium">Last submitted:</p>
              <p className="text-sm">Message: {lastSubmitted.message}</p>
              <p className="text-sm">
                Attachments: {lastSubmitted.attachmentCount}
              </p>
            </div>
          )}
        </div>
      );
    };

    return <SubmitHandlerDemo />;
  },
};

export const FileUploadDemo: Story = {
  render: () => (
    <div className="flex flex-col gap-4">
      <ChatInput onSubmit={fn()} />
      <div className="rounded-md border p-4 space-y-2 text-sm">
        <p className="font-medium">Features to test:</p>
        <ul className="list-disc list-inside space-y-1 text-muted-foreground">
          <li>Click the paperclip icon to select files</li>
          <li>Drag and drop files onto the input area</li>
          <li>Paste images from clipboard (Ctrl/Cmd + V)</li>
          <li>Remove attachments by clicking the X button</li>
          <li>Image files show thumbnails</li>
        </ul>
      </div>
    </div>
  ),
};

export const DisabledWithContent: Story = {
  render: () => {
    const DisabledDemo = () => {
      const [isDisabled, setIsDisabled] = useState(false);

      return (
        <div className="flex flex-col gap-4">
          <ChatInput disabled={isDisabled} onSubmit={fn()} />
          <div className="flex items-center gap-2">
            <label className="text-sm flex items-center gap-2">
              <input
                type="checkbox"
                checked={isDisabled}
                onChange={e => setIsDisabled(e.target.checked)}
                className="rounded"
              />
              Disabled
            </label>
          </div>
        </div>
      );
    };

    return <DisabledDemo />;
  },
};

export const MultilineText: Story = {
  render: () => (
    <div className="flex flex-col gap-4">
      <ChatInput onSubmit={fn()} />
      <div className="rounded-md border p-4 space-y-2 text-sm">
        <p className="font-medium">Multiline behavior:</p>
        <ul className="list-disc list-inside space-y-1 text-muted-foreground">
          <li>Press Enter to submit</li>
          <li>Press Shift + Enter for new line</li>
          <li>Textarea auto-expands up to max height (180px)</li>
          <li>Then becomes scrollable</li>
        </ul>
      </div>
    </div>
  ),
};

export const DragAndDropDemo: Story = {
  render: () => (
    <div className="flex flex-col gap-4">
      <ChatInput onSubmit={fn()} />
      <div className="rounded-md border p-4 space-y-2 text-sm">
        <p className="font-medium">Drag and drop instructions:</p>
        <p className="text-muted-foreground">
          Drag files from your file system and drop them onto the input area to
          attach them. A visual indicator will appear when dragging files over
          the component.
        </p>
      </div>
    </div>
  ),
};
