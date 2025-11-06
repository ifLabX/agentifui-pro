import { createRef } from "react";
import { render } from "@testing-library/react";

import "@testing-library/jest-dom";

import { useTheme } from "next-themes";
import { Toaster as MockedSonnerToaster } from "sonner";

import { Toaster } from "./index";

jest.mock("next-themes", () => ({
  useTheme: jest.fn(),
}));

jest.mock("sonner", () => {
  const React = jest.requireActual<typeof import("react")>("react");
  const mock = jest.fn();
  const MockToaster = React.forwardRef((props, ref) => {
    mock(props, ref);
    return null;
  });
  MockToaster.displayName = "MockSonnerToaster";
  (MockToaster as unknown as { mock: jest.Mock }).mock = mock;
  return { Toaster: MockToaster };
});

const sonnerToasterMock = (
  MockedSonnerToaster as unknown as { mock: jest.Mock }
).mock;
const useThemeMock = useTheme as unknown as jest.Mock;

beforeEach(() => {
  jest.clearAllMocks();
  useThemeMock.mockReturnValue({ theme: "system" });
});

describe("Toaster", () => {
  test("passes active theme to Sonner", () => {
    useThemeMock.mockReturnValue({ theme: "dark" });

    render(<Toaster />);

    expect(sonnerToasterMock).toHaveBeenCalledTimes(1);
    const props = sonnerToasterMock.mock.calls[0][0] as {
      theme: string;
    };

    expect(props.theme).toBe("dark");
  });

  test("merges consumer className with design token classes", () => {
    render(<Toaster className="custom-toaster" />);

    const props = sonnerToasterMock.mock.calls[0][0] as {
      className: string;
    };

    expect(props.className).toContain("toaster");
    expect(props.className).toContain("group");
    expect(props.className).toContain("custom-toaster");
  });

  test("combines default and override toast class names", () => {
    render(
      <Toaster
        toastOptions={{
          classNames: {
            toast: "custom-toast",
            actionButton: "custom-action",
          },
        }}
      />
    );

    const props = sonnerToasterMock.mock.calls[0][0] as {
      toastOptions: {
        classNames: Record<string, string>;
      };
    };

    expect(props.toastOptions.classNames.toast).toContain(
      "group-[.toaster]:bg-background"
    );
    expect(props.toastOptions.classNames.toast).toContain("custom-toast");
    expect(props.toastOptions.classNames.actionButton).toContain(
      "group-[.toast]:bg-primary"
    );
    expect(props.toastOptions.classNames.actionButton).toContain(
      "custom-action"
    );
  });

  test("forwards refs to Sonner Toaster", () => {
    const ref = createRef<HTMLElement>();

    render(<Toaster ref={ref} />);

    expect(sonnerToasterMock).toHaveBeenCalledTimes(1);
    const forwardedRef = sonnerToasterMock.mock.calls[0][1];

    expect(forwardedRef).toBe(ref);
  });

  test("includes semantic design tokens for toast variants", () => {
    render(<Toaster />);

    const props = sonnerToasterMock.mock.calls[0][0] as {
      toastOptions: {
        classNames: Record<string, string>;
      };
    };
    const toastClasses = props.toastOptions.classNames.toast;

    expect(toastClasses).toContain(
      "data-[type=success]:group-[.toaster]:bg-status-success"
    );
    expect(toastClasses).toContain(
      "data-[type=info]:group-[.toaster]:bg-status-info"
    );
    expect(toastClasses).toContain(
      "data-[type=warning]:group-[.toaster]:bg-status-warning"
    );
    expect(toastClasses).toContain(
      "data-[type=error]:group-[.toaster]:bg-destructive"
    );
  });
});
