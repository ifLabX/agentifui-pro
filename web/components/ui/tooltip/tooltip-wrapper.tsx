"use client";

import * as React from "react";

import { Tooltip, type TooltipProps } from "./index";

interface TooltipWrapperProps extends Omit<TooltipProps, "children"> {
  children: React.ReactNode;
}

/**
 * Tooltip wrapper component that handles client-side rendering
 * Prevents hydration mismatches by only rendering tooltip functionality on the client
 */
export function TooltipWrapper({
  children,
  ...tooltipProps
}: TooltipWrapperProps) {
  const [mounted, setMounted] = React.useState(false);

  React.useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return <>{children}</>;
  }

  return <Tooltip {...tooltipProps}>{children}</Tooltip>;
}
