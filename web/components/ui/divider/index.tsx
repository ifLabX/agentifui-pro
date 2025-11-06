import * as React from "react";
import * as SeparatorPrimitive from "@radix-ui/react-separator";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";

const orientationStyles: Record<"horizontal" | "vertical", string> = {
  horizontal: "h-[var(--divider-default-thickness)]",
  vertical: "w-[var(--divider-default-thickness)]",
};

const dividerVariants = cva(
  "shrink-0 bg-[var(--divider-default-color)] transition-colors",
  {
    variants: {
      orientation: {
        horizontal: "",
        vertical: "",
      },
      weight: {
        subtle: "bg-[var(--divider-muted-color)]",
        default: "",
        emphasized: "bg-[var(--divider-emphasized-color)]",
      },
      inset: {
        none: "",
        sm: "",
        md: "",
        lg: "",
      },
      length: {
        full: "",
        content: "",
      },
    },
    compoundVariants: [
      {
        orientation: "horizontal",
        weight: "emphasized",
        class: "h-[var(--divider-emphasized-thickness)]",
      },
      {
        orientation: "vertical",
        weight: "emphasized",
        class: "w-[var(--divider-emphasized-thickness)]",
      },
      {
        orientation: "horizontal",
        inset: "sm",
        class: "mx-4",
      },
      {
        orientation: "horizontal",
        inset: "md",
        class: "mx-6",
      },
      {
        orientation: "horizontal",
        inset: "lg",
        class: "mx-8",
      },
      {
        orientation: "vertical",
        inset: "sm",
        length: "content",
        class: "my-4",
      },
      {
        orientation: "vertical",
        inset: "md",
        length: "content",
        class: "my-6",
      },
      {
        orientation: "vertical",
        inset: "lg",
        length: "content",
        class: "my-8",
      },
      {
        orientation: "horizontal",
        length: "full",
        class: "w-full",
      },
      {
        orientation: "vertical",
        length: "full",
        class: "h-full",
      },
    ],
    defaultVariants: {
      orientation: "horizontal",
      weight: "default",
      inset: "none",
      length: "full",
    },
  }
);

export type DividerVariants = VariantProps<typeof dividerVariants>;

const horizontalInsetPadding: Record<
  NonNullable<DividerVariants["inset"]>,
  string
> = {
  none: "",
  sm: "px-4",
  md: "px-6",
  lg: "px-8",
};

const verticalInsetPadding: Record<
  NonNullable<DividerVariants["inset"]>,
  string
> = {
  none: "",
  sm: "py-4",
  md: "py-6",
  lg: "py-8",
};

const horizontalLengthClasses: Record<
  NonNullable<DividerVariants["length"]>,
  string
> = {
  full: "w-full",
  content: "w-fit",
};

const verticalLengthClasses: Record<
  NonNullable<DividerVariants["length"]>,
  string
> = {
  full: "h-full",
  content: "h-fit",
};

const labelBaseClass =
  "text-xs font-medium uppercase tracking-wide text-muted-foreground";

export interface DividerProps
  extends Omit<
      React.ComponentPropsWithoutRef<typeof SeparatorPrimitive.Root>,
      "orientation"
    >,
    DividerVariants {
  orientation?: "horizontal" | "vertical";
  label?: string;
  labelPosition?: "start" | "center" | "end";
  lineClassName?: string;
}

export const Divider = React.forwardRef<
  React.ElementRef<typeof SeparatorPrimitive.Root>,
  DividerProps
>(
  (
    {
      className,
      lineClassName,
      orientation = "horizontal",
      weight,
      inset,
      length,
      decorative = true,
      label,
      labelPosition = "center",
      ...restProps
    },
    ref
  ) => {
    const labelId = React.useId();
    const hasLabel = Boolean(label);
    const finalDecorative = hasLabel ? false : decorative;

    if (!hasLabel) {
      return (
        <SeparatorPrimitive.Root
          ref={ref}
          decorative={finalDecorative}
          orientation={orientation}
          className={cn(
            orientationStyles[orientation],
            dividerVariants({ orientation, weight, inset, length }),
            lineClassName,
            className
          )}
          {...restProps}
        />
      );
    }

    const normalizedInset = inset ?? "none";
    const normalizedLength = length ?? "full";
    const wrapperInsetClass =
      orientation === "horizontal"
        ? horizontalInsetPadding[normalizedInset]
        : normalizedLength === "content"
          ? verticalInsetPadding[normalizedInset]
          : undefined;
    const wrapperLengthClass =
      orientation === "horizontal"
        ? horizontalLengthClasses[normalizedLength]
        : verticalLengthClasses[normalizedLength];
    const lineShouldGrow = normalizedLength !== "content";
    const contentLengthFallbackClass =
      normalizedLength === "content"
        ? orientation === "horizontal"
          ? "min-w-8"
          : "min-h-8"
        : undefined;
    const sharedLineClass = cn(
      orientationStyles[orientation],
      dividerVariants({
        orientation,
        weight,
        inset: "none",
        length: normalizedLength,
      }),
      contentLengthFallbackClass,
      lineShouldGrow ? "flex-1" : undefined,
      lineClassName
    );

    const accessibleSeparator = (
      <SeparatorPrimitive.Root
        ref={ref}
        decorative={false}
        orientation={orientation}
        aria-labelledby={labelId}
        className="sr-only"
      />
    );

    if (orientation === "horizontal") {
      const horizontalJustifyClass =
        labelPosition === "start"
          ? "justify-start"
          : labelPosition === "end"
            ? "justify-end"
            : "justify-center";

      return (
        <div
          className={cn(
            "flex items-center gap-3",
            wrapperInsetClass,
            wrapperLengthClass,
            horizontalJustifyClass,
            className
          )}
          {...restProps}
        >
          {labelPosition !== "start" ? (
            <SeparatorPrimitive.Root
              aria-hidden
              decorative
              orientation="horizontal"
              className={sharedLineClass}
            />
          ) : null}
          <span id={labelId} className={labelBaseClass}>
            {label}
          </span>
          {labelPosition !== "end" ? (
            <SeparatorPrimitive.Root
              aria-hidden
              decorative
              orientation="horizontal"
              className={sharedLineClass}
            />
          ) : null}
          {accessibleSeparator}
        </div>
      );
    }

    const verticalJustifyClass =
      labelPosition === "start"
        ? "justify-start"
        : labelPosition === "end"
          ? "justify-end"
          : "justify-center";

    return (
      <div
        className={cn(
          "flex items-center gap-3",
          "flex-col",
          verticalJustifyClass,
          wrapperInsetClass,
          wrapperLengthClass,
          className
        )}
        {...restProps}
      >
        {labelPosition !== "start" ? (
          <SeparatorPrimitive.Root
            aria-hidden
            decorative
            orientation="vertical"
            className={sharedLineClass}
          />
        ) : null}
        <span id={labelId} className={labelBaseClass}>
          {label}
        </span>
        {labelPosition !== "end" ? (
          <SeparatorPrimitive.Root
            aria-hidden
            decorative
            orientation="vertical"
            className={sharedLineClass}
          />
        ) : null}
        {accessibleSeparator}
      </div>
    );
  }
);

Divider.displayName = "Divider";

export default Divider;
