import * as React from "react";

import { cn } from "@/lib/utils";

export type InputProps = React.InputHTMLAttributes<HTMLInputElement>;

const baseInputClasses = [
  "flex h-9 w-full rounded-lg border border-input bg-input-background px-3 py-1",
  "text-base text-input-foreground shadow-[var(--input-shadow)] transition-[box-shadow,color] duration-200 ring-offset-background",
  "file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-input-foreground",
  "placeholder:text-input-placeholder",
  "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-input-ring focus-visible:ring-offset-2 focus-visible:shadow-[var(--input-shadow-focus)]",
  "disabled:cursor-not-allowed disabled:border-input disabled:bg-input-disabled disabled:text-input-disabled-foreground disabled:placeholder:text-input-disabled-foreground disabled:opacity-50",
  "aria-[invalid=true]:border-input-invalid aria-[invalid=true]:focus-visible:ring-input-invalid-ring",
  "md:text-sm",
] as const;

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type = "text", ...props }, ref) => (
    <input
      type={type}
      className={cn(baseInputClasses, className)}
      ref={ref}
      {...props}
    />
  )
);

Input.displayName = "Input";

export { Input };
