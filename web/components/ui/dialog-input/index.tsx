"use client";

import React, { useEffect, useState } from "react";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button/index";
import { Input } from "@/components/ui/input";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "../dialog/index";

interface InputDialogProps {
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  title: string;
  description?: string;
  label: string;
  placeholder?: string;
  defaultValue?: string;
  confirmText?: string;
  cancelText?: string;
  onConfirm?: (value: string) => void | Promise<void>;
  isLoading?: boolean;
  showCloseButton?: boolean;
  closeButtonLabel?: string;
  maxLength?: number;
  children?: React.ReactNode;
}

export function InputDialog({
  open,
  onOpenChange,
  title,
  description,
  label,
  placeholder,
  defaultValue = "",
  confirmText = "Save changes",
  cancelText = "Cancel",
  onConfirm,
  isLoading = false,
  showCloseButton = true,
  closeButtonLabel,
  maxLength = 100,
  children,
}: InputDialogProps) {
  const [inputValue, setInputValue] = useState(defaultValue);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const inputRef = React.useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (open) {
      setInputValue(defaultValue);
      setTimeout(() => {
        inputRef.current?.focus();
        inputRef.current?.select();
      }, 150);
    }
  }, [open, defaultValue]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const trimmedValue = inputValue.trim();
    if (trimmedValue && !isSubmitting && !isLoading) {
      setIsSubmitting(true);
      try {
        await onConfirm?.(trimmedValue);
      } finally {
        setIsSubmitting(false);
        onOpenChange?.(false);
      }
    }
  };

  const isInputValid = inputValue.trim().length > 0;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      {children && <DialogTrigger asChild>{children}</DialogTrigger>}
      <DialogContent
        className="sm:max-w-md"
        showCloseButton={showCloseButton}
        closeButtonLabel={closeButtonLabel}
      >
        <form onSubmit={handleSubmit}>
          <DialogHeader>
            <DialogTitle>{title}</DialogTitle>
            {description && (
              <DialogDescription>{description}</DialogDescription>
            )}
          </DialogHeader>

          <div className="py-4">
            <label
              htmlFor="dialog-input"
              className="mb-2 block text-sm font-medium text-dialog-text"
            >
              {label}
            </label>
            <Input
              id="dialog-input"
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={e => setInputValue(e.target.value)}
              placeholder={placeholder}
              maxLength={maxLength}
              disabled={isLoading || isSubmitting}
              className={cn(
                "border border-dialog-input-border bg-dialog-input-bg text-dialog-input-text placeholder-dialog-input-placeholder",
                "focus:border-dialog-text focus:ring-2 focus:ring-dialog-text/20"
              )}
            />
          </div>

          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange?.(false)}
              disabled={isLoading || isSubmitting}
            >
              {cancelText}
            </Button>
            <Button
              type="submit"
              disabled={isLoading || isSubmitting || !isInputValid}
            >
              {isLoading || isSubmitting ? "Loading..." : confirmText}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
