import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { Loader2Icon, LoaderIcon } from "lucide-react";

import { cn } from "@/lib/utils";

const spinnerVariants = cva("animate-spin", {
  variants: {
    size: {
      sm: "size-3",
      md: "size-4",
      lg: "size-6",
      xl: "size-8",
    },
  },
  defaultVariants: {
    size: "md",
  },
});

interface SpinnerProps
  extends React.ComponentPropsWithoutRef<"svg">,
  VariantProps<typeof spinnerVariants> {
  variant?: "default" | "loader";
}

const Spinner = React.forwardRef<SVGSVGElement, SpinnerProps>(
  ({ className, variant = "default", size, ...props }, ref) => {
    const Icon = variant === "loader" ? LoaderIcon : Loader2Icon;
    const { "aria-label": ariaLabel = "Loading", role: _role, ...rest } = props;

    return (
      <Icon
        ref={ref}
        role="status"
        aria-label={ariaLabel}
        className={cn(spinnerVariants({ size, className }))}
        {...rest}
      />
    );
  }
);
Spinner.displayName = "Spinner";

export { Spinner, spinnerVariants };
export type { SpinnerProps };
