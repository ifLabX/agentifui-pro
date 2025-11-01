"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import {
  autoUpdate,
  flip,
  hide,
  offset,
  shift,
  size,
  useClick,
  useDismiss,
  useFloating,
  useInteractions,
  useRole,
  type Placement,
  type Strategy,
} from "@floating-ui/react";

export interface UsePopoverOptions {
  initialOpen?: boolean;
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  placement?: Placement;
  modal?: boolean;
  offset?: number;
  closeOnSelect?: boolean;
  strategy?: Strategy;
  matchTriggerWidth?: boolean;
  hideWhenReferenceHidden?: boolean;
}

export function usePopover({
  initialOpen = false,
  open: controlledOpen,
  onOpenChange: setControlledOpen,
  placement = "bottom",
  modal = false,
  offset: offsetValue = 8,
  closeOnSelect = true,
  strategy = "fixed",
  matchTriggerWidth = false,
  hideWhenReferenceHidden = true,
}: UsePopoverOptions = {}) {
  const [uncontrolledOpen, setUncontrolledOpen] = useState(initialOpen);
  const [currentLabelId, setCurrentLabelId] = useState<string | undefined>();
  const [currentDescriptionId, setCurrentDescriptionId] = useState<
    string | undefined
  >();
  const [portalNode, setPortalNode] = useState<HTMLElement | null>(null);

  const open = controlledOpen ?? uncontrolledOpen;
  const setOpen = useCallback(
    (nextOpen: boolean) => {
      setControlledOpen?.(nextOpen);

      if (controlledOpen == null) {
        setUncontrolledOpen(nextOpen);
      }
    },
    [setControlledOpen, controlledOpen]
  );

  useEffect(() => {
    if (typeof window === "undefined") return;
    const doc = window.document;
    const portalId = "ui-popover-root";
    let root = doc.getElementById(portalId) as HTMLElement | null;

    if (!root) {
      root = doc.createElement("div");
      root.id = portalId;
      root.style.display = "contents";
      doc.body.appendChild(root);
    }

    setPortalNode(root);
  }, []);

  const middleware = [
    offset(offsetValue),
    flip({
      crossAxis: placement.includes("-"),
      fallbackAxisSideDirection: "end",
      padding: 5,
    }),
    shift({ padding: 5 }),
  ];

  if (matchTriggerWidth) {
    middleware.push(
      size({
        apply({ rects, elements }) {
          elements.floating.style.width = `${rects.reference.width}px`;
        },
      })
    );
  }

  if (hideWhenReferenceHidden) {
    middleware.push(
      hide({
        strategy: "referenceHidden",
      })
    );
  }

  const data = useFloating({
    placement,
    open,
    onOpenChange: setOpen,
    strategy,
    whileElementsMounted: autoUpdate,
    middleware,
  });

  const context = data.context;

  const click = useClick(context);
  const dismiss = useDismiss(context);
  const role = useRole(context);

  const interactions = useInteractions([click, dismiss, role]);

  return useMemo(
    () => ({
      open,
      setOpen,
      ...interactions,
      ...data,
      modal,
      labelId: currentLabelId,
      descriptionId: currentDescriptionId,
      setLabelId: setCurrentLabelId,
      setDescriptionId: setCurrentDescriptionId,
      closeOnSelect,
      strategy,
      portalNode,
      matchTriggerWidth,
      hideWhenReferenceHidden,
    }),
    [
      open,
      setOpen,
      interactions,
      data,
      modal,
      currentLabelId,
      currentDescriptionId,
      closeOnSelect,
      strategy,
      portalNode,
      matchTriggerWidth,
      hideWhenReferenceHidden,
    ]
  );
}

export type UsePopoverReturn = ReturnType<typeof usePopover>;
