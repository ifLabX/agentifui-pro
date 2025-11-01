"use client";

import type React from "react";
import { useState } from "react";

import { Button } from "@/components/ui/button";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "./base-dialog";

interface AlertDialogProps {
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  title: string;
  description: string;
  confirmText?: string;
  cancelText?: string;
  onConfirm?: () => void | Promise<void>;
  showCloseButton?: boolean;
  closeButtonLabel?: string;
  isLoading?: boolean;
  children?: React.ReactNode;
}

export function AlertDialog({
  open,
  onOpenChange,
  title,
  description,
  confirmText = "Confirm",
  cancelText = "Cancel",
  onConfirm,
  showCloseButton = true,
  closeButtonLabel,
  isLoading = false,
  children,
}: AlertDialogProps) {
  const [isConfirming, setIsConfirming] = useState(false);

  const handleConfirm = async () => {
    if (onConfirm) {
      setIsConfirming(true);
      try {
        await onConfirm();
      } finally {
        setIsConfirming(false);
        onOpenChange?.(false);
      }
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
            {cancelText}
          </Button>
          <Button onClick={handleConfirm} disabled={isLoading || isConfirming}>
            {isLoading || isConfirming ? "Loading..." : confirmText}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
