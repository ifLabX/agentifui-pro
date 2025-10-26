import type { ComponentProps } from "react";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { ChatInput } from ".";

const translations: Record<string, string> = {
  "chat.input.placeholder": "Type a message or paste an image...",
  "chat.dropzone.label": "Drop files to upload",
  "chat.attachments.upload-aria": "Upload files",
  "chat.attachments.add-aria": "Add attachment",
  "chat.attachments.remove-aria": "Remove attachment",
  "chat.attachments.file-size-zero": "0 B",
  "chat.attachments.units.bytes": "B",
  "chat.attachments.units.kilobytes": "KB",
  "chat.attachments.units.megabytes": "MB",
  "chat.attachments.units.gigabytes": "GB",
  "chat.submit.aria-label": "Send message",
};

jest.mock("next-intl", () => ({
  useTranslations: () => (key: string) => translations[key] ?? key,
}));

type ChatInputProps = ComponentProps<typeof ChatInput>;

const renderChatInput = (props: Partial<ChatInputProps> = {}) =>
  render(<ChatInput {...props} />);

describe("ChatInput", () => {
  it("renders default placeholder from translations", () => {
    renderChatInput();
    expect(
      screen.getByPlaceholderText(translations["chat.input.placeholder"])
    ).toBeInTheDocument();
  });

  it("submits message when pressing Enter", async () => {
    const user = userEvent.setup();
    const handleSubmit = jest.fn();
    renderChatInput({ onSubmit: handleSubmit });

    const textarea = screen.getByPlaceholderText(
      translations["chat.input.placeholder"]
    );
    await user.type(textarea, "Hello world{enter}");

    expect(handleSubmit).toHaveBeenCalledWith("Hello world", []);
  });

  it("handles adding and removing attachments", async () => {
    const user = userEvent.setup();
    renderChatInput();

    const fileInput = screen.getByLabelText(
      translations["chat.attachments.upload-aria"]
    );
    const file = new File(["test"], "example.txt", {
      type: "text/plain",
    });

    fireEvent.change(fileInput, { target: { files: [file] } });
    expect(await screen.findByText("example.txt")).toBeInTheDocument();

    const removeButton = screen.getByLabelText(
      translations["chat.attachments.remove-aria"]
    );
    await user.click(removeButton);

    await waitFor(() =>
      expect(screen.queryByText("example.txt")).not.toBeInTheDocument()
    );
  });
});
