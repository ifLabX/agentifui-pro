import type { FC, PropsWithChildren, ReactNode } from "react";

import { cn } from "@/lib/utils";

export type TooltipContentProps = {
  title?: ReactNode;
  action?: ReactNode;
  className?: string;
} & PropsWithChildren;

export const ToolTipContent: FC<TooltipContentProps> = ({
  title,
  action,
  children,
  className,
}) => {
  return (
    <div className={cn("w-[180px]", className)}>
      {title && (
        <div className="mb-1.5 font-semibold text-foreground">{title}</div>
      )}
      <div className="mb-1.5 text-muted-foreground">{children}</div>
      {action && (
        <div className="cursor-pointer text-accent-foreground hover:underline">
          {action}
        </div>
      )}
    </div>
  );
};
