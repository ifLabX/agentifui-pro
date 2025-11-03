import type { ComponentProps } from "react";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";

const kbdVariants = cva(
  "pointer-events-none inline-flex select-none items-center justify-center gap-1 rounded font-mono font-medium leading-none border border-kbd-border bg-kbd-bg text-kbd-text shadow-sm backdrop-blur-sm [[data-slot=tooltip-content]_&]:backdrop-blur-none dark:[[data-slot=tooltip-content]_&]:border-white/10 dark:[[data-slot=tooltip-content]_&]:bg-black/10 dark:[[data-slot=tooltip-content]_&]:text-white/70 [&_svg:not([class*='size-'])]:size-3",
  {
    variants: {
      size: {
        default: "h-5 min-w-[26px] px-1 text-[10px]",
        sm: "h-4 min-w-[20px] px-1 text-[9px]",
      },
    },
    defaultVariants: {
      size: "default",
    },
  }
);

type KbdProps = ComponentProps<"kbd"> & VariantProps<typeof kbdVariants>;

function Kbd({ className, children, size, ...props }: KbdProps) {
  const isShortText = typeof children === "string" && children.length <= 2;
  const shortWidthClass = size === "sm" ? "w-4" : "w-5";

  return (
    <kbd
      data-slot="kbd"
      className={cn(
        kbdVariants({ size }),
        isShortText && [shortWidthClass, "min-w-0 px-0"],
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

export { Kbd, KbdGroup, kbdVariants };
