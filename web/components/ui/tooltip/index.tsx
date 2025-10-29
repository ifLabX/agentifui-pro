"use client";

import * as React from "react";
import * as TooltipPrimitive from "@radix-ui/react-tooltip";
import { HelpCircle } from "lucide-react";

import { cn } from "@/lib/utils";

import { tooltipManager } from "./tooltip-manager";

const TooltipProvider = TooltipPrimitive.Provider;

const TooltipRoot = TooltipPrimitive.Root;

const TooltipTrigger = TooltipPrimitive.Trigger;

const TooltipPortal = TooltipPrimitive.Portal;

const TooltipArrow = React.forwardRef<
  React.ElementRef<typeof TooltipPrimitive.Arrow>,
  React.ComponentPropsWithoutRef<typeof TooltipPrimitive.Arrow>
>(({ className, ...props }, ref) => (
  <TooltipPrimitive.Arrow
    ref={ref}
    className={cn("fill-popover", className)}
    {...props}
  />
));
TooltipArrow.displayName = TooltipPrimitive.Arrow.displayName;

const TooltipPrimitiveContent = React.forwardRef<
  React.ElementRef<typeof TooltipPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof TooltipPrimitive.Content>
>(({ className, sideOffset = 4, ...props }, ref) => (
  <TooltipPrimitive.Content
    ref={ref}
    sideOffset={sideOffset}
    className={cn(
      "z-50 overflow-hidden rounded-md bg-popover px-3 py-1.5 text-sm text-popover-foreground shadow-md",
      "animate-in fade-in-0 zoom-in-95",
      "data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95",
      "data-[side=bottom]:slide-in-from-top-2",
      "data-[side=left]:slide-in-from-right-2",
      "data-[side=right]:slide-in-from-left-2",
      "data-[side=top]:slide-in-from-bottom-2",
      className
    )}
    {...props}
  />
));
TooltipPrimitiveContent.displayName = TooltipPrimitive.Content.displayName;

export interface TooltipProps {
  children?: React.ReactNode;
  content: React.ReactNode;
  side?: "top" | "right" | "bottom" | "left";
  align?: "start" | "center" | "end";
  className?: string;
  contentClassName?: string;
  asChild?: boolean;
  open?: boolean;
  defaultOpen?: boolean;
  onOpenChange?: (open: boolean) => void;
  disabled?: boolean;
  delayDuration?: number;
  testId?: string;
}

function Tooltip({
  children,
  content,
  side = "top",
  align = "center",
  className,
  contentClassName,
  asChild = true,
  open: controlledOpen,
  defaultOpen,
  onOpenChange: controlledOnOpenChange,
  disabled = false,
  delayDuration,
  testId,
}: TooltipProps) {
  const [internalOpen, setInternalOpen] = React.useState(defaultOpen ?? false);
  const isControlled = controlledOpen !== undefined;
  const isOpen = isControlled ? controlledOpen : internalOpen;

  const setOpen = React.useCallback(
    (open: boolean) => {
      if (!isControlled) {
        setInternalOpen(open);
      }
      controlledOnOpenChange?.(open);
    },
    [isControlled, controlledOnOpenChange]
  );

  const close = React.useCallback(() => {
    setOpen(false);
  }, [setOpen]);

  const handleOpenChange = React.useCallback(
    (open: boolean) => {
      setOpen(open);
      if (open) {
        tooltipManager.register(close);
      } else {
        tooltipManager.clear(close);
      }
    },
    [close, setOpen]
  );

  React.useEffect(() => {
    return () => {
      tooltipManager.clear(close);
    };
  }, [close]);

  if (disabled) {
    return <>{children}</>;
  }

  const hasCustomTrigger = children !== undefined && children !== null;
  const triggerContent = hasCustomTrigger ? (
    children
  ) : (
    <button
      type="button"
      data-testid={testId}
      className={cn(
        "inline-flex h-4 w-4 items-center justify-center",
        "text-muted-foreground hover:text-foreground",
        "transition-colors",
        className
      )}
      aria-label="More information"
    >
      <HelpCircle className="h-4 w-4" />
    </button>
  );
  const triggerAsChild = hasCustomTrigger ? asChild : true;

  return (
    <TooltipRoot
      open={isOpen}
      onOpenChange={handleOpenChange}
      delayDuration={delayDuration}
    >
      <TooltipTrigger
        asChild={triggerAsChild}
        className={triggerAsChild ? undefined : className}
        data-testid={testId}
      >
        {triggerContent}
      </TooltipTrigger>
      <TooltipPortal>
        <TooltipPrimitiveContent
          side={side}
          align={align}
          className={cn("max-w-xs", contentClassName)}
        >
          {content}
        </TooltipPrimitiveContent>
      </TooltipPortal>
    </TooltipRoot>
  );
}

export {
  TooltipProvider,
  TooltipRoot,
  TooltipTrigger,
  TooltipPrimitiveContent,
  TooltipPortal,
  TooltipArrow,
};
export { Tooltip };
export { TooltipContent } from "./tooltip-content";
export type { TooltipContentProps } from "./tooltip-content";
export { TooltipWrapper } from "./tooltip-wrapper";
export { tooltipManager } from "./tooltip-manager";
