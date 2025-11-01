"use client";

import * as React from "react";
import {
  FloatingFocusManager,
  FloatingOverlay,
  FloatingPortal,
  useMergeRefs,
} from "@floating-ui/react";

import { cn } from "@/lib/utils";

import {
  usePopover,
  type UsePopoverOptions,
  type UsePopoverReturn,
} from "./use-popover";

const PopoverContext = React.createContext<UsePopoverReturn | null>(null);

const usePopoverContext = () => {
  const context = React.useContext(PopoverContext);
  if (!context) {
    throw new Error("Popover components must be wrapped in <Popover />");
  }
  return context;
};

export interface PopoverProps extends UsePopoverOptions {
  children: React.ReactNode;
}

export function Popover({ children, ...options }: PopoverProps) {
  const popover = usePopover(options);
  return (
    <PopoverContext.Provider value={popover}>
      {children}
    </PopoverContext.Provider>
  );
}

export interface PopoverTriggerProps {
  children: React.ReactNode;
  asChild?: boolean;
}

export const PopoverTrigger = React.forwardRef<
  HTMLElement,
  PopoverTriggerProps & React.HTMLProps<HTMLElement>
>(({ children, asChild = false, ...props }, propRef) => {
  const context = usePopoverContext();
  type TriggerChild = React.ReactElement<Record<string, unknown>> & {
    ref?: React.Ref<HTMLElement>;
  };
  const child =
    asChild && React.isValidElement(children)
      ? (children as TriggerChild)
      : null;
  const childProps = (child?.props ?? {}) as Record<string, unknown>;
  const mergedRef = useMergeRefs<HTMLElement | null>([
    context.refs.setReference,
    propRef,
    child?.ref,
  ]);

  if (child) {
    const referenceProps = context.getReferenceProps({
      ref: mergedRef,
      ...childProps,
      ...props,
    }) as Record<string, unknown>;

    if (referenceProps.type == null && childProps.type == null) {
      referenceProps.type = "button";
    }

    return React.cloneElement(child, {
      ...referenceProps,
      "data-state": context.open ? "open" : "closed",
    });
  }

  return (
    <button
      ref={mergedRef as React.Ref<HTMLButtonElement>}
      type="button"
      data-state={context.open ? "open" : "closed"}
      {...context.getReferenceProps(props)}
    >
      {children}
    </button>
  );
});
PopoverTrigger.displayName = "PopoverTrigger";

export interface PopoverContentProps extends React.HTMLProps<HTMLDivElement> {
  container?: HTMLElement | null;
}

export const PopoverContent = React.forwardRef<
  HTMLDivElement,
  PopoverContentProps
>((props, propRef) => {
  const {
    style,
    className,
    children,
    container,
    "aria-labelledby": ariaLabelledByProp,
    "aria-describedby": ariaDescribedByProp,
    ...restProps
  } = props;
  const popover = usePopoverContext();
  const ref = useMergeRefs([popover.refs.setFloating, propRef]);
  const state = popover.open ? "open" : "closed";
  const portalRoot = container ?? popover.portalNode ?? undefined;

  if (!popover.open) return null;

  const ariaLabelledBy = ariaLabelledByProp ?? popover.labelId;
  const ariaDescribedBy = ariaDescribedByProp ?? popover.descriptionId;

  const floatingProps = popover.getFloatingProps({
    ...restProps,
    "aria-labelledby": ariaLabelledBy,
    "aria-describedby": ariaDescribedBy,
  }) as React.HTMLAttributes<HTMLDivElement>;

  const {
    className: floatingClassName,
    style: floatingInlineStyle,
    ...floatingRestProps
  } = floatingProps;
  const referenceHidden =
    popover.middlewareData?.hide?.referenceHidden ?? false;
  const combinedStyle: React.CSSProperties = {
    ...popover.floatingStyles,
    ...floatingInlineStyle,
    ...style,
  };

  if (referenceHidden) {
    combinedStyle.visibility = "hidden";
  }

  const content = (
    <div
      ref={ref}
      data-state={state}
      className={cn("z-50", floatingClassName)}
      style={combinedStyle}
      {...floatingRestProps}
    >
      <div
        data-state={state}
        className={cn(
          "pointer-events-auto min-w-[8rem] rounded-lg border bg-popover p-1 text-popover-foreground shadow-md outline-none",
          "transition-all duration-150 ease-out",
          "data-[state=open]:opacity-100 data-[state=open]:scale-100",
          "data-[state=closed]:pointer-events-none data-[state=closed]:opacity-0 data-[state=closed]:scale-95",
          className
        )}
      >
        {children}
      </div>
    </div>
  );

  return (
    <FloatingPortal root={portalRoot}>
      <FloatingFocusManager
        context={popover.context}
        modal={popover.modal}
        guards={popover.modal}
        initialFocus={popover.modal ? undefined : -1}
      >
        {popover.modal ? (
          <FloatingOverlay
            lockScroll
            className="grid place-items-center bg-background/60 p-4 backdrop-blur-sm"
            data-state={state}
          >
            {content}
          </FloatingOverlay>
        ) : (
          content
        )}
      </FloatingFocusManager>
    </FloatingPortal>
  );
});
PopoverContent.displayName = "PopoverContent";

export interface PopoverItemProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  icon?: React.ReactNode;
  danger?: boolean;
  closeOnSelect?: boolean;
}

export const PopoverItem = React.forwardRef<
  HTMLButtonElement,
  PopoverItemProps
>(
  (
    {
      className,
      children,
      icon,
      danger,
      disabled,
      onClick,
      closeOnSelect,
      ...props
    },
    ref
  ) => {
    const popover = usePopoverContext();
    const shouldClose = closeOnSelect ?? popover.closeOnSelect;

    const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
      if (disabled) return;
      onClick?.(event);
      if (!event.defaultPrevented && shouldClose) {
        popover.setOpen(false);
      }
    };

    return (
      <button
        ref={ref}
        type="button"
        disabled={disabled}
        data-popover-item
        className={cn(
          "relative flex w-full cursor-default select-none items-center gap-2 rounded-sm px-2 py-1.5 text-sm outline-none transition-colors",
          "focus:bg-accent focus:text-accent-foreground focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background",
          !disabled && "hover:bg-accent hover:text-accent-foreground",
          disabled && "pointer-events-none opacity-50",
          danger &&
            "text-destructive focus:bg-destructive/10 focus:text-destructive",
          className
        )}
        onClick={handleClick}
        {...props}
      >
        {icon && (
          <span className="flex h-4 w-4 items-center justify-center">
            {icon}
          </span>
        )}
        {children}
      </button>
    );
  }
);
PopoverItem.displayName = "PopoverItem";

export const PopoverDivider = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => {
  return (
    <div
      ref={ref}
      className={cn("-mx-1 my-1 h-px bg-border", className)}
      {...props}
    />
  );
});
PopoverDivider.displayName = "PopoverDivider";

export const PopoverHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, id, ...props }, ref) => {
  const { setLabelId } = usePopoverContext();
  const generatedId = React.useId();
  const headerId = id ?? generatedId;

  React.useEffect(() => {
    setLabelId(headerId);
    return () => setLabelId(undefined);
  }, [setLabelId, headerId]);

  return (
    <div
      ref={ref}
      id={headerId}
      className={cn("px-3 py-2 text-sm font-semibold", className)}
      {...props}
    />
  );
});
PopoverHeader.displayName = "PopoverHeader";

export const PopoverBody = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, id, ...props }, ref) => {
  const { setDescriptionId } = usePopoverContext();
  const generatedId = React.useId();
  const bodyId = id ?? generatedId;

  React.useEffect(() => {
    setDescriptionId(bodyId);
    return () => setDescriptionId(undefined);
  }, [setDescriptionId, bodyId]);

  return (
    <div ref={ref} id={bodyId} className={cn("p-3", className)} {...props} />
  );
});
PopoverBody.displayName = "PopoverBody";

export const PopoverFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => {
  return (
    <div
      ref={ref}
      className={cn("flex items-center gap-2 px-3 py-2", className)}
      {...props}
    />
  );
});
PopoverFooter.displayName = "PopoverFooter";

export const PopoverClose = React.forwardRef<
  HTMLButtonElement,
  React.ButtonHTMLAttributes<HTMLButtonElement>
>(({ className, onClick, children, ...props }, ref) => {
  const popover = usePopoverContext();

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    onClick?.(event);

    if (!event.defaultPrevented) {
      popover.setOpen(false);
    }
  };

  return (
    <button
      ref={ref}
      type="button"
      className={cn(
        "inline-flex items-center justify-center rounded-md px-3 py-1.5 text-sm font-medium transition",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background",
        className
      )}
      onClick={handleClick}
      {...props}
    >
      {children}
    </button>
  );
});
PopoverClose.displayName = "PopoverClose";
