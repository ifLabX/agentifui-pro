"use client";

import { forwardRef, useMemo } from "react";
import deepmerge from "deepmerge";
import { useTheme } from "next-themes";
import { Toaster as Sonner } from "sonner";

import { cn } from "@/lib/utils";

type ToasterProps = React.ComponentProps<typeof Sonner>;

type ToastClassNames = NonNullable<
  NonNullable<ToasterProps["toastOptions"]>["classNames"]
>;

const defaultToastClassNames: ToastClassNames = {
  toast: cn(
    "group toast group-[.toaster]:border group-[.toaster]:border-border",
    "group-[.toaster]:bg-background group-[.toaster]:text-foreground group-[.toaster]:shadow-lg",
    "data-[type=success]:group-[.toaster]:bg-status-success data-[type=success]:group-[.toaster]:text-status-success-foreground data-[type=success]:group-[.toaster]:border-transparent",
    "data-[type=info]:group-[.toaster]:bg-status-info data-[type=info]:group-[.toaster]:text-status-info-foreground data-[type=info]:group-[.toaster]:border-transparent",
    "data-[type=warning]:group-[.toaster]:bg-status-warning data-[type=warning]:group-[.toaster]:text-status-warning-foreground data-[type=warning]:group-[.toaster]:border-transparent",
    "data-[type=error]:group-[.toaster]:bg-destructive data-[type=error]:group-[.toaster]:text-destructive-foreground data-[type=error]:group-[.toaster]:border-transparent",
    "data-[type=loading]:group-[.toaster]:bg-muted data-[type=loading]:group-[.toaster]:text-muted-foreground data-[type=loading]:group-[.toaster]:border-transparent"
  ),
  description: "group-[.toast]:text-muted-foreground",
  actionButton:
    "group-[.toast]:bg-primary group-[.toast]:text-primary-foreground group-[.toast]:hover:bg-primary/90",
  cancelButton:
    "group-[.toast]:bg-muted group-[.toast]:text-muted-foreground group-[.toast]:hover:bg-muted/80",
};

const defaultToastOptions: NonNullable<ToasterProps["toastOptions"]> = {
  classNames: defaultToastClassNames,
};

const cloneDefaultToastOptions = (): NonNullable<
  ToasterProps["toastOptions"]
> => ({
  ...defaultToastOptions,
  classNames: { ...defaultToastClassNames },
});

const mergeToastOptions = (
  overrides?: ToasterProps["toastOptions"]
): NonNullable<ToasterProps["toastOptions"]> => {
  const base = cloneDefaultToastOptions();

  if (!overrides) {
    return base;
  }

  const merged = deepmerge(base, overrides, {
    arrayMerge: (_target, sourceArray) => sourceArray,
  });

  if (overrides.classNames) {
    const classNames = Object.keys({
      ...defaultToastClassNames,
      ...overrides.classNames,
    }).reduce((acc, key) => {
      const typedKey = key as keyof ToastClassNames;

      acc[typedKey] = cn(
        defaultToastClassNames[typedKey],
        overrides.classNames?.[typedKey]
      );
      return acc;
    }, {} as Partial<ToastClassNames>);

    merged.classNames = {
      ...merged.classNames,
      ...classNames,
    } as ToastClassNames;
  }

  return merged;
};

const Toaster = forwardRef<HTMLElement, ToasterProps>(
  ({ className, toastOptions, ...props }, ref) => {
    const { theme = "system" } = useTheme();

    const mergedToastOptions = useMemo(
      () => mergeToastOptions(toastOptions),
      [toastOptions]
    );

    return (
      <Sonner
        ref={ref}
        theme={theme as ToasterProps["theme"]}
        className={cn("toaster group", className)}
        toastOptions={mergedToastOptions}
        {...props}
      />
    );
  }
);

Toaster.displayName = "Toaster";

export { Toaster };
export { toast } from "sonner";
