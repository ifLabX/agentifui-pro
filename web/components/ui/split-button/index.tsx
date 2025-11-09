import * as React from "react";
import { ChevronDown } from "lucide-react";

import { cn } from "@/lib/utils";

export type SplitButtonAction = Omit<
  React.ButtonHTMLAttributes<HTMLButtonElement>,
  "children"
> & {
  label?: React.ReactNode;
  icon?: React.ReactNode;
};

export interface SplitButtonProps
  extends Omit<React.HTMLAttributes<HTMLDivElement>, "children"> {
  primaryAction: SplitButtonAction;
  secondaryAction?: SplitButtonAction;
  size?: "sm" | "default" | "lg";
  fullWidth?: boolean;
  disabled?: boolean;
}

const DEFAULT_SECONDARY_ARIA_LABEL = "Show additional actions";

const defaultSecondaryAction: SplitButtonAction = {
  icon: <ChevronDown aria-hidden="true" className="split-button__chevron" />,
  "aria-label": DEFAULT_SECONDARY_ARIA_LABEL,
  type: "button",
};

const SplitButton = React.forwardRef<HTMLDivElement, SplitButtonProps>(
  (
    {
      className,
      primaryAction,
      secondaryAction,
      size = "default",
      fullWidth = false,
      disabled = false,
      ...rest
    },
    ref
  ) => {
    const {
      label: primaryLabel,
      icon: primaryIcon,
      className: primaryClassName,
      type: primaryType = "button",
      disabled: primaryDisabledExplicit,
      ...primaryRest
    } = primaryAction;

    const resolvedSecondary = secondaryAction ?? defaultSecondaryAction;
    const {
      label: secondaryLabel,
      icon: secondaryIcon,
      className: secondaryClassName,
      type: secondaryType = "button",
      disabled: secondaryDisabledExplicit,
      ["aria-label"]: secondaryAriaLabelProp,
      ...secondaryRest
    } = resolvedSecondary;

    const shouldUseFallbackChevron = !secondaryIcon && !secondaryLabel;
    const secondaryAriaLabel =
      secondaryAriaLabelProp ??
      (shouldUseFallbackChevron ? DEFAULT_SECONDARY_ARIA_LABEL : undefined);

    const isPrimaryDisabled = disabled || Boolean(primaryDisabledExplicit);
    const isSecondaryDisabled = disabled || Boolean(secondaryDisabledExplicit);

    return (
      <div
        ref={ref}
        className={cn(
          "split-button",
          fullWidth && "split-button--block",
          className
        )}
        data-size={size}
        {...rest}
      >
        <button
          type={primaryType}
          className={cn(
            "split-button__segment split-button__segment--primary",
            primaryClassName
          )}
          disabled={isPrimaryDisabled}
          {...primaryRest}
        >
          {primaryIcon ? (
            <span className="split-button__icon" aria-hidden="true">
              {primaryIcon}
            </span>
          ) : null}
          {primaryLabel ? (
            <span className="split-button__label">{primaryLabel}</span>
          ) : null}
        </button>
        <button
          type={secondaryType}
          className={cn(
            "split-button__segment split-button__segment--secondary",
            secondaryClassName
          )}
          disabled={isSecondaryDisabled}
          aria-label={secondaryAriaLabel}
          {...secondaryRest}
        >
          {secondaryIcon ? (
            <span className="split-button__icon" aria-hidden="true">
              {secondaryIcon}
            </span>
          ) : null}
          {secondaryLabel ? (
            <span className="split-button__label">{secondaryLabel}</span>
          ) : null}
          {shouldUseFallbackChevron ? (
            <span className="split-button__icon" aria-hidden="true">
              <ChevronDown className="split-button__chevron" />
            </span>
          ) : null}
        </button>
      </div>
    );
  }
);
SplitButton.displayName = "SplitButton";

export { SplitButton, DEFAULT_SECONDARY_ARIA_LABEL };
