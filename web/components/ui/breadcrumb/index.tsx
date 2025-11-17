import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { ChevronRight, MoreHorizontal } from "lucide-react";

import { cn } from "@/lib/utils";

const Breadcrumb = React.forwardRef<
  React.ElementRef<"nav">,
  React.ComponentPropsWithoutRef<"nav">
>(({ className, "aria-label": ariaLabel = "Breadcrumb", ...props }, ref) => (
  <nav
    ref={ref}
    aria-label={ariaLabel}
    className={cn("w-full", className)}
    {...props}
  />
));
Breadcrumb.displayName = "Breadcrumb";

const BreadcrumbList = React.forwardRef<
  React.ElementRef<"ol">,
  React.ComponentPropsWithoutRef<"ol">
>(({ className, ...props }, ref) => (
  <ol
    ref={ref}
    className={cn(
      "flex min-h-[var(--breadcrumb-min-height)] flex-wrap list-none items-center gap-[var(--breadcrumb-gap)] text-sm text-[var(--breadcrumb-foreground)]",
      className
    )}
    {...props}
  />
));
BreadcrumbList.displayName = "BreadcrumbList";

const BreadcrumbItem = React.forwardRef<
  React.ElementRef<"li">,
  React.ComponentPropsWithoutRef<"li">
>(({ className, ...props }, ref) => (
  <li
    ref={ref}
    className={cn(
      "inline-flex items-center gap-[var(--breadcrumb-item-gap)] text-sm",
      className
    )}
    {...props}
  />
));
BreadcrumbItem.displayName = "BreadcrumbItem";

export interface BreadcrumbLinkProps
  extends React.AnchorHTMLAttributes<HTMLAnchorElement> {
  asChild?: boolean;
}

const BreadcrumbLink = React.forwardRef<HTMLAnchorElement, BreadcrumbLinkProps>(
  ({ className, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "a";
    return (
      <Comp
        ref={ref}
        className={cn(
          "inline-flex h-[var(--breadcrumb-min-height)] items-center gap-2 rounded-[var(--breadcrumb-radius)] px-[var(--breadcrumb-link-padding-x)] py-[var(--breadcrumb-link-padding-y)] text-sm text-[var(--breadcrumb-foreground)] transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background hover:text-[var(--breadcrumb-hover-foreground)]",
          className
        )}
        {...props}
      />
    );
  }
);
BreadcrumbLink.displayName = "BreadcrumbLink";

const BreadcrumbPage = React.forwardRef<
  React.ElementRef<"span">,
  React.ComponentPropsWithoutRef<"span">
>(({ className, "aria-current": ariaCurrent = "page", ...props }, ref) => (
  <span
    ref={ref}
    aria-current={ariaCurrent}
    className={cn(
      "inline-flex h-[var(--breadcrumb-min-height)] items-center gap-2 rounded-[var(--breadcrumb-radius)] px-[var(--breadcrumb-link-padding-x)] py-[var(--breadcrumb-link-padding-y)] text-sm font-medium text-[var(--breadcrumb-current-foreground)]",
      className
    )}
    {...props}
  />
));
BreadcrumbPage.displayName = "BreadcrumbPage";

const BreadcrumbSeparator = React.forwardRef<
  React.ElementRef<"li">,
  React.ComponentPropsWithoutRef<"li">
>(({ children, className, ...props }, ref) => (
  <li
    ref={ref}
    role="presentation"
    aria-hidden="true"
    className={cn(
      "flex items-center text-[var(--breadcrumb-separator-color)] [&>svg]:size-3.5",
      className
    )}
    {...props}
  >
    {children ?? <ChevronRight aria-hidden="true" />}
  </li>
));
BreadcrumbSeparator.displayName = "BreadcrumbSeparator";

const BreadcrumbEllipsis = React.forwardRef<
  React.ElementRef<"span">,
  React.ComponentPropsWithoutRef<"span">
>(({ className, ...props }, ref) => (
  <span
    ref={ref}
    className={cn(
      "inline-flex h-[var(--breadcrumb-min-height)] w-[var(--breadcrumb-min-height)] items-center justify-center rounded-[var(--breadcrumb-radius)] text-[var(--breadcrumb-ellipsis-foreground)]",
      className
    )}
    {...props}
  >
    <MoreHorizontal aria-hidden="true" className="size-4" />
    <span className="sr-only">More breadcrumb items</span>
  </span>
));
BreadcrumbEllipsis.displayName = "BreadcrumbEllipsis";

export {
  Breadcrumb,
  BreadcrumbEllipsis,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
};
