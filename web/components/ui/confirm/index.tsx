"use client";

import * as React from "react";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

type ConfirmVariant = "default" | "destructive";

export interface ConfirmDialogProps {
  open: boolean;
  title: React.ReactNode;
  description?: React.ReactNode;
  confirmText?: React.ReactNode;
  cancelText?: React.ReactNode;
  onConfirm?: () => void;
  onCancel?: () => void;
  variant?: ConfirmVariant;
  isLoading?: boolean;
  disableCancel?: boolean;
  children?: React.ReactNode;
  icon?: React.ReactNode;
}

const variantButton: Record<ConfirmVariant, "default" | "destructive"> = {
  default: "default",
  destructive: "destructive",
};

const titleColor: Record<ConfirmVariant, string> = {
  default: "text-foreground",
  destructive: "text-destructive",
};

const iconWrapper: Record<ConfirmVariant, string> = {
  default: "bg-primary/10 text-primary",
  destructive: "bg-destructive/15 text-destructive",
};

export function ConfirmDialog({
  open,
  title,
  description,
  confirmText = "Confirm",
  cancelText = "Cancel",
  onConfirm,
  onCancel,
  variant = "default",
  isLoading = false,
  disableCancel = false,
  children,
  icon,
}: ConfirmDialogProps) {
  const fallbackIcon = icon ?? null;
  const handleOpenChange = (value: boolean) => {
    if (!value) {
      if (disableCancel || isLoading) {
        return;
      }
      onCancel?.();
    }
  };

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogContent
        showCloseButton={false}
        className="max-w-md space-y-4 border-border/70"
        onInteractOutside={event => {
          if (disableCancel || isLoading) {
            event.preventDefault();
          }
        }}
      >
        <DialogHeader className="space-y-3 text-left">
          {fallbackIcon ? (
            <span
              className={cn(
                "flex h-10 w-10 items-center justify-center rounded-full",
                iconWrapper[variant]
              )}
            >
              {fallbackIcon}
            </span>
          ) : null}
          <div className="space-y-2">
            <DialogTitle className={cn("text-left", titleColor[variant])}>
              {title}
            </DialogTitle>
            {description ? (
              <DialogDescription className="text-left text-sm text-muted-foreground">
                {description}
              </DialogDescription>
            ) : null}
          </div>
        </DialogHeader>

        {children ? (
          <div className="rounded-md border border-border/60 bg-muted/30 px-3 py-2 text-sm text-muted-foreground">
            {children}
          </div>
        ) : null}

        <DialogFooter className="sm:flex-row sm:justify-end">
          <Button
            variant={variant === "destructive" ? "outline" : "ghost"}
            onClick={() => onCancel?.()}
            disabled={isLoading || disableCancel}
          >
            {cancelText}
          </Button>
          <Button
            variant={variantButton[variant]}
            onClick={() => onConfirm?.()}
            disabled={isLoading}
          >
            {isLoading ? "Processing..." : confirmText}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
