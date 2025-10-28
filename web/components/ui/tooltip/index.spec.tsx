import React from "react";
import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import "@testing-library/jest-dom";

import type { TooltipProviderProps } from "@radix-ui/react-tooltip";

import { Tooltip, TooltipProvider } from "./index";

afterEach(cleanup);

beforeAll(() => {
  if (!window.PointerEvent) {
    class PointerEventPolyfill extends MouseEvent {
      constructor(type: string, params?: PointerEventInit) {
        super(type, params);
      }
    }
    // @ts-expect-error JSDOM pointer event polyfill
    window.PointerEvent = PointerEventPolyfill;
    // @ts-expect-error Node global pointer event polyfill
    global.PointerEvent = PointerEventPolyfill;
  }
});

const renderWithProvider = (
  ui: React.ReactElement,
  providerProps?: Omit<TooltipProviderProps, "children">
) => {
  return render(
    <TooltipProvider
      delayDuration={100}
      skipDelayDuration={300}
      {...providerProps}
    >
      {ui}
    </TooltipProvider>
  );
};

describe("Tooltip", () => {
  describe("Rendering", () => {
    test("should render default tooltip with question icon", () => {
      const { container } = renderWithProvider(
        <Tooltip content="Tooltip content" testId="test-tooltip" />
      );
      const trigger = container.querySelector('[data-testid="test-tooltip"]');
      expect(trigger).not.toBeNull();
      expect(trigger?.querySelector("svg")).not.toBeNull();
    });

    test("should render with custom children", () => {
      const { getByText } = renderWithProvider(
        <Tooltip content="Tooltip content">
          <button>Hover me</button>
        </Tooltip>
      );
      expect(getByText("Hover me")).toBeInTheDocument();
    });
  });

  describe("Disabled state", () => {
    test("should not show tooltip when disabled", async () => {
      const { container } = renderWithProvider(
        <Tooltip content="Tooltip content" disabled testId="test-tooltip">
          <button>Trigger</button>
        </Tooltip>
      );
      const trigger = container.querySelector("button");
      act(() => {
        fireEvent.pointerEnter(trigger!);
      });
      await waitFor(() => {
        expect(screen.queryByText("Tooltip content")).not.toBeInTheDocument();
      });
    });
  });

  describe("Hover behavior", () => {
    test("should open on hover", async () => {
      const { container } = renderWithProvider(
        <Tooltip content="Tooltip content" testId="test-tooltip">
          <button>Trigger</button>
        </Tooltip>
      );
      const trigger = container.querySelector("button");
      const user = userEvent.setup();
      await user.hover(trigger!);
      await waitFor(() => {
        expect(screen.getAllByText("Tooltip content").length).toBeGreaterThan(
          0
        );
      });
    });

    test("respects delayDuration before showing tooltip", async () => {
      jest.useFakeTimers();
      const user = userEvent.setup({ advanceTimers: jest.advanceTimersByTime });
      try {
        const { container } = renderWithProvider(
          <Tooltip content="Tooltip content" delayDuration={500}>
            <button>Trigger</button>
          </Tooltip>,
          { delayDuration: 100 }
        );
        const trigger = container.querySelector("button");

        await user.hover(trigger!);

        act(() => {
          jest.advanceTimersByTime(300);
        });
        expect(screen.queryByText("Tooltip content")).not.toBeInTheDocument();

        act(() => {
          jest.advanceTimersByTime(200);
        });
        await waitFor(() => {
          expect(screen.getAllByText("Tooltip content").length).toBeGreaterThan(
            0
          );
        });
      } finally {
        jest.useRealTimers();
      }
    });
  });

  describe("Styling and positioning", () => {
    test("should apply custom contentClassName", async () => {
      const { container } = renderWithProvider(
        <Tooltip
          content="Tooltip content"
          contentClassName="custom-popup"
          testId="test-tooltip"
        >
          <button>Trigger</button>
        </Tooltip>
      );
      const trigger = container.querySelector("button");
      const user = userEvent.setup();
      await user.hover(trigger!);
      await waitFor(() => {
        const content = screen.getByRole("tooltip", {
          hidden: true,
        }).parentElement;
        expect(content).not.toBeNull();
        expect(content).toHaveClass("custom-popup");
      });
    });

    test("should support different positions", async () => {
      const positions = ["top", "right", "bottom", "left"] as const;
      for (const side of positions) {
        const { container, unmount } = renderWithProvider(
          <Tooltip
            content={`${side} tooltip`}
            side={side}
            testId="test-tooltip"
          >
            <button>Trigger</button>
          </Tooltip>
        );
        const trigger = container.querySelector("button");
        const user = userEvent.setup();
        await user.hover(trigger!);
        await waitFor(() => {
          expect(screen.getAllByText(`${side} tooltip`).length).toBeGreaterThan(
            0
          );
        });
        unmount();
      }
    });
  });

  describe("Test ID support", () => {
    test("should apply testId to trigger element", () => {
      const { container } = renderWithProvider(
        <Tooltip content="Tooltip content" testId="custom-test-id">
          <button>Trigger</button>
        </Tooltip>
      );
      const trigger = container.querySelector('[data-testid="custom-test-id"]');
      expect(trigger).toBeInTheDocument();
    });

    test("should apply testId to default icon", () => {
      const { container } = renderWithProvider(
        <Tooltip content="Tooltip content" testId="icon-test-id" />
      );
      const trigger = container.querySelector('[data-testid="icon-test-id"]');
      expect(trigger).toBeInTheDocument();
      expect(trigger?.tagName).toBe("BUTTON");
    });
  });
});
