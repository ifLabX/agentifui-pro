import type { ComponentProps } from "react";

import { cn } from "@/lib/utils";

function Kbd({ className, children, ...props }: ComponentProps<"kbd">) {
  const isShortText = typeof children === "string" && children.length <= 2;
  const widthClass = isShortText ? "w-5" : "min-w-[26px] px-1";

  return (
    <kbd
      data-slot="kbd"
      className={cn(
        "pointer-events-none inline-flex h-5 select-none items-center justify-center gap-1 rounded font-mono text-[10px] font-medium leading-none",
        widthClass,
        "border border-kbd-border bg-kbd-bg text-kbd-text shadow-sm backdrop-blur-sm",
        "[[data-slot=tooltip-content]_&]:border-white/10 [[data-slot=tooltip-content]_&]:bg-black/10 [[data-slot=tooltip-content]_&]:text-white/70 [[data-slot=tooltip-content]_&]:backdrop-blur-none dark:[[data-slot=tooltip-content]_&]:border-white/10 dark:[[data-slot=tooltip-content]_&]:bg-black/10 dark:[[data-slot=tooltip-content]_&]:text-white/70",
        "[&_svg:not([class*='size-'])]:size-3",
        className
      )}
      {...props}
    >
      {children}
    </kbd>
  );
}

function KbdGroup({ className, ...props }: ComponentProps<"div">) {
  return (
    <div
      data-slot="kbd-group"
      className={cn("inline-flex items-center gap-1", className)}
      {...props}
    />
  );
}

export { Kbd, KbdGroup };
