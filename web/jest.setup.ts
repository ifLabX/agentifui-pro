import "@testing-library/jest-dom";

import { cleanup } from "@testing-library/react";

if (typeof URL.createObjectURL !== "function") {
  Object.defineProperty(URL, "createObjectURL", {
    configurable: true,
    writable: true,
    value: jest.fn(() => "blob:mock-preview"),
  });
}

afterEach(() => {
  cleanup();
});
