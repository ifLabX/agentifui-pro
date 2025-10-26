"use client";

import type React from "react";
import { useEffect, useRef, useState } from "react";
import { ArrowUp, FileText, ImageIcon, Paperclip, X } from "lucide-react";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

interface Attachment {
  id: string;
  name: string;
  size: number;
  type: string;
  file: File;
  preview?: string;
}

interface ChatInputProps {
  onSubmit?: (message: string, attachments: Attachment[]) => void;
  placeholder?: string;
  disabled?: boolean;
  className?: string;
}

export function ChatInput({
  onSubmit,
  placeholder = "Type a message or paste an image...",
  disabled = false,
  className,
}: ChatInputProps) {
  const [message, setMessage] = useState("");
  const [attachments, setAttachments] = useState<Attachment[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const hasContent = message.trim().length > 0 || attachments.length > 0;

  // Auto-resize textarea
  useEffect(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    textarea.style.height = "0";
    const scrollHeight = textarea.scrollHeight;
    const newHeight = Math.min(scrollHeight, 180);
    textarea.style.height = `${newHeight}px`;
  }, [message]);

  useEffect(() => {
    return () => {
      attachments.forEach(attachment => {
        if (attachment.preview) {
          URL.revokeObjectURL(attachment.preview);
        }
      });
    };
  }, [attachments]);

  const handleSubmit = () => {
    if (!hasContent || disabled) return;

    onSubmit?.(message, attachments);
    setMessage("");
    setAttachments([]);

    // Reset textarea height
    if (textareaRef.current) {
      textareaRef.current.style.height = "48px";
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const processFiles = (files: File[]) => {
    const newAttachments: Attachment[] = files.map(file => {
      const attachment: Attachment = {
        id: Math.random().toString(36).substring(7),
        name: file.name,
        size: file.size,
        type: file.type,
        file: file,
      };

      // Generate preview URLs for images
      if (file.type.startsWith("image/")) {
        attachment.preview = URL.createObjectURL(file);
      }

      return attachment;
    });

    setAttachments(prev => [...prev, ...newAttachments]);
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    processFiles(files);

    // Reset file input
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handlePaste = (e: React.ClipboardEvent<HTMLTextAreaElement>) => {
    const items = Array.from(e.clipboardData.items);
    const files: File[] = [];

    items.forEach(item => {
      if (item.kind === "file") {
        const file = item.getAsFile();
        if (file) {
          files.push(file);
        }
      }
    });

    if (files.length > 0) {
      e.preventDefault();
      processFiles(files);
    }
  };

  const handleDragEnter = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();

    // Only reset the drag state when the container loses hover
    if (e.currentTarget === containerRef.current) {
      setIsDragging(false);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      processFiles(files);
    }
  };

  const removeAttachment = (id: string) => {
    setAttachments(prev => {
      const attachment = prev.find(att => att.id === id);
      if (attachment?.preview) {
        URL.revokeObjectURL(attachment.preview);
      }
      return prev.filter(att => att.id !== id);
    });
  };

  const formatBytes = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i)) + " " + sizes[i];
  };

  const getFileIcon = (type: string) => {
    if (type.startsWith("image/")) {
      return <ImageIcon className="h-4 w-4" />;
    }
    return <FileText className="h-4 w-4" />;
  };

  return (
    <div className={cn("w-full max-w-3xl mx-auto", className)}>
      <div
        ref={containerRef}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        className={cn(
          "flex flex-col rounded-2xl relative",
          "bg-chat-input-bg border border-chat-input-border",
          "shadow-[var(--chat-shadow)]",
          "transition-all duration-200",
          isDragging && "border-chat-submit-bg border-2 bg-chat-button-hover-bg"
        )}
      >
        {isDragging && (
          <div className="absolute inset-0 z-10 flex items-center justify-center rounded-2xl bg-chat-input-bg/95 backdrop-blur-sm">
            <div className="flex flex-col items-center gap-2">
              <Paperclip className="h-8 w-8 text-chat-submit-bg" />
              <p className="font-serif text-sm font-medium text-chat-input-text">
                Drop files to upload
              </p>
            </div>
          </div>
        )}

        {/* Attachment Preview Bar */}
        {attachments.length > 0 && (
          <div
            className={cn(
              "px-3 pt-3 pb-2",
              "border-b border-chat-input-border",
              "transition-all duration-300 ease-in-out"
            )}
          >
            <div className="flex flex-wrap gap-2">
              {attachments.map(attachment => (
                <div
                  key={attachment.id}
                  className={cn(
                    "relative flex items-center gap-2 rounded-md py-1 pr-1 pl-2",
                    "max-w-[180px]",
                    "bg-chat-attachment-bg border border-chat-attachment-border"
                  )}
                >
                  {attachment.preview ? (
                    <img
                      src={attachment.preview || "/placeholder.svg"}
                      alt={attachment.name}
                      className="h-8 w-8 rounded object-cover flex-shrink-0"
                    />
                  ) : (
                    <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded bg-chat-button-bg text-chat-button-text">
                      {getFileIcon(attachment.type)}
                    </div>
                  )}

                  <div className="min-w-0 flex-grow">
                    <p className="truncate font-serif text-sm font-medium text-chat-attachment-text">
                      {attachment.name}
                    </p>
                    <p className="font-serif text-xs text-chat-attachment-text-secondary">
                      {formatBytes(attachment.size)}
                    </p>
                  </div>

                  <button
                    type="button"
                    onClick={() => removeAttachment(attachment.id)}
                    className={cn(
                      "flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full",
                      "bg-chat-attachment-remove-bg hover:bg-chat-attachment-remove-hover-bg",
                      "transition-colors"
                    )}
                    aria-label="Remove attachment"
                  >
                    <X className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Text Input Area */}
        <div className="px-4 pt-4 pb-1">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={e => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            onPaste={handlePaste}
            placeholder={placeholder}
            disabled={disabled}
            rows={1}
            className={cn(
              "w-full resize-none border-0 bg-transparent",
              "focus:ring-0 focus:outline-none",
              "min-h-[48px] overflow-y-auto",
              "font-serif text-chat-input-text placeholder:text-chat-input-placeholder"
            )}
            style={{ maxHeight: "180px" }}
          />
        </div>

        {/* Button Area */}
        <div className="flex items-center justify-between px-2 py-2">
          <div className="flex items-center gap-2">
            {/* Attachment Button */}
            <input
              ref={fileInputRef}
              type="file"
              multiple
              onChange={handleFileSelect}
              className="hidden"
              aria-label="Upload files"
            />
            <Button
              type="button"
              size="sm"
              variant="ghost"
              onClick={() => fileInputRef.current?.click()}
              disabled={disabled}
              className={cn(
                "flex h-8 w-8 items-center justify-center rounded-lg",
                "bg-chat-button-bg border border-chat-button-border",
                "text-chat-button-text hover:bg-chat-button-hover-bg"
              )}
              aria-label="Add attachment"
            >
              <Paperclip className="h-4 w-4" />
            </Button>
          </div>

          {/* Submit Button */}
          <Button
            type="button"
            size="sm"
            onClick={handleSubmit}
            disabled={!hasContent || disabled}
            className={cn(
              "flex h-8 w-8 items-center justify-center rounded-full",
              "shadow-sm transition-colors",
              hasContent && !disabled
                ? "bg-chat-submit-bg text-chat-submit-text hover:bg-chat-submit-hover-bg"
                : "bg-chat-submit-disabled-bg text-chat-submit-disabled-text cursor-not-allowed"
            )}
            aria-label="Send message"
          >
            <ArrowUp className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}
