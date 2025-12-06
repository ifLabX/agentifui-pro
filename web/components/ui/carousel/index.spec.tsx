import { act, fireEvent, render, screen } from "@testing-library/react";

import "@testing-library/jest-dom";
import useEmblaCarousel from "embla-carousel-react";

import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "./index";

jest.mock("embla-carousel-react", () => ({
  __esModule: true,
  default: jest.fn(),
}));

const mockCarouselRef = jest.fn();
const listeners: Record<string, (api: unknown) => void> = {};
const mockApi = {
  canScrollPrev: jest.fn(),
  canScrollNext: jest.fn(),
  scrollPrev: jest.fn(),
  scrollNext: jest.fn(),
  on: jest.fn(),
  off: jest.fn(),
};
const useEmblaCarouselMock = useEmblaCarousel as unknown as jest.Mock;

beforeEach(() => {
  jest.clearAllMocks();
  Object.keys(listeners).forEach(key => delete listeners[key]);

  mockApi.canScrollPrev.mockReturnValue(false);
  mockApi.canScrollNext.mockReturnValue(true);
  mockApi.on.mockImplementation(
    (event: string, handler: (api: unknown) => void) => {
      listeners[event] = handler;
    }
  );

  useEmblaCarouselMock.mockReturnValue([mockCarouselRef, mockApi]);
});

describe("Carousel", () => {
  test("sets navigation state from Embla API and exposes it to controls", () => {
    const setApi = jest.fn();

    render(
      <Carousel setApi={setApi}>
        <CarouselContent>
          <CarouselItem>Slide 1</CarouselItem>
          <CarouselItem>Slide 2</CarouselItem>
        </CarouselContent>
        <CarouselPrevious />
        <CarouselNext />
      </Carousel>
    );

    expect(setApi).toHaveBeenCalledWith(mockApi);

    const prev = screen.getByRole("button", { name: /previous slide/i });
    const next = screen.getByRole("button", { name: /next slide/i });

    expect(prev).toBeDisabled();
    expect(next).not.toBeDisabled();

    mockApi.canScrollPrev.mockReturnValue(true);
    mockApi.canScrollNext.mockReturnValue(false);

    act(() => {
      listeners.select?.(mockApi);
    });

    expect(prev).not.toBeDisabled();
    expect(next).toBeDisabled();
  });

  test("responds to keyboard navigation via arrow keys", () => {
    render(
      <Carousel>
        <CarouselContent>
          <CarouselItem>Slide</CarouselItem>
        </CarouselContent>
        <CarouselPrevious />
        <CarouselNext />
      </Carousel>
    );

    const region = document.querySelector('[data-slot="carousel"]');

    fireEvent.keyDown(region as HTMLElement, { key: "ArrowLeft" });
    fireEvent.keyDown(region as HTMLElement, { key: "ArrowRight" });

    expect(mockApi.scrollPrev).toHaveBeenCalled();
    expect(mockApi.scrollNext).toHaveBeenCalled();
  });

  test("applies vertical orientation spacing to content and items", () => {
    render(
      <Carousel orientation="vertical">
        <CarouselContent data-testid="content">
          <CarouselItem data-testid="item">Card</CarouselItem>
        </CarouselContent>
      </Carousel>
    );

    const content = screen.getByTestId("content");
    const item = screen.getByTestId("item");

    expect(content.className).toContain("flex-col");
    expect(content.className).toContain("-mt-4");
    expect(item.className).toContain("pt-4");
  });
});
