"use client";

import type React from "react";
import { useState } from "react";
import { useTranslations } from "next-intl";

import { Button } from "@/components/ui/button/index";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "../dialog/index";

type ConfirmVariant = "default" | "danger";

interface ConfirmDialogProps {
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  title: string;
  description: string;
  confirmText?: string;
  cancelText?: string;
  onConfirm?: () => void | Promise<void>;
  variant?: ConfirmVariant;
  showCloseButton?: boolean;
  closeButtonLabel?: string;
  isLoading?: boolean;
  children?: React.ReactNode;
}

export function ConfirmDialog({
  open,
  onOpenChange,
  title,
  description,
  confirmText,
  cancelText,
  onConfirm,
  variant = "default",
  showCloseButton = true,
  closeButtonLabel,
  isLoading = false,
  children,
}: ConfirmDialogProps) {
  const t = useTranslations("common");
  const [isConfirming, setIsConfirming] = useState(false);

  const defaultConfirmText = t("actions.confirm");
  const defaultCancelText = t("actions.cancel");
  const loadingText = t("actions.loading");

  const handleConfirm = async () => {
    if (isLoading || isConfirming) {
      return;
    }

    if (onConfirm) {
      setIsConfirming(true);
    }

    try {
      await onConfirm?.();
    } finally {
      if (onConfirm) {
        setIsConfirming(false);
      }
      onOpenChange?.(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      {children && <DialogTrigger asChild>{children}</DialogTrigger>}
      <DialogContent
        className="sm:max-w-md"
        showCloseButton={showCloseButton}
        closeButtonLabel={closeButtonLabel}
      >
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
        </DialogHeader>
        <DialogDescription className="text-left">
          {description}
        </DialogDescription>
        <DialogFooter>
          <Button
            variant="outline"
            onClick={() => onOpenChange?.(false)}
            disabled={isLoading || isConfirming}
          >
            {cancelText ?? defaultCancelText}
          </Button>
          <Button
            variant={variant === "danger" ? "destructive" : "default"}
            onClick={handleConfirm}
            disabled={isLoading || isConfirming}
          >
            {isLoading || isConfirming
              ? loadingText
              : (confirmText ?? defaultConfirmText)}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
