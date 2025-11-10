import type { Meta, StoryObj } from "@storybook/react-vite";
import { FolderIcon, HomeIcon, SettingsIcon } from "lucide-react";

import {
  Breadcrumb,
  BreadcrumbEllipsis,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "./index";

const meta = {
  title: "UI/Breadcrumb",
  component: Breadcrumb,
  parameters: {
    layout: "padded",
    docs: {
      description: {
        component:
          "Breadcrumb reconstructs hierarchical navigation with shadcn spacing, typography, and focus tokens. Compose the primitives to keep long agent journeys understandable across light and dark themes.",
      },
    },
  },
  tags: ["autodocs"],
  argTypes: {
    className: {
      control: "text",
      description: "Utility classes applied to the `nav` wrapper.",
    },
    "aria-label": {
      control: "text",
      description:
        "Accessible label describing the breadcrumb trail for assistive tech.",
    },
  },
  args: {
    "aria-label": "Breadcrumb",
  },
} satisfies Meta<typeof Breadcrumb>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: args => (
    <div className="max-w-2xl">
      <Breadcrumb {...args}>
        <BreadcrumbList>
          <BreadcrumbItem>
            <BreadcrumbLink href="#dashboard">Dashboard</BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator />
          <BreadcrumbItem>
            <BreadcrumbLink href="#projects">Projects</BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator />
          <BreadcrumbItem>
            <BreadcrumbPage>Agent Workspace</BreadcrumbPage>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story:
          "Use the default breadcrumb to show users where they are inside multi-level flows such as project → workspace.",
      },
    },
  },
};

export const WithEllipsis: Story = {
  render: args => (
    <div className="max-w-2xl">
      <Breadcrumb {...args}>
        <BreadcrumbList>
          <BreadcrumbItem>
            <BreadcrumbLink href="#home">Home</BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator />
          <BreadcrumbItem>
            <BreadcrumbLink href="#library">Library</BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator />
          <BreadcrumbItem>
            <BreadcrumbEllipsis aria-label="Condensed breadcrumb items" />
          </BreadcrumbItem>
          <BreadcrumbSeparator />
          <BreadcrumbItem>
            <BreadcrumbLink href="#audits">Audit trails</BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator />
          <BreadcrumbItem>
            <BreadcrumbPage>Current review</BreadcrumbPage>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story:
          "Swap in the ellipsis primitive when there are more ancestors than you can comfortably show on smaller screens.",
      },
    },
  },
};

export const CustomSeparator: Story = {
  render: args => (
    <div className="max-w-2xl">
      <Breadcrumb {...args}>
        <BreadcrumbList>
          <BreadcrumbItem>
            <BreadcrumbLink href="#home">Home</BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator className="mx-0 font-semibold">
            /
          </BreadcrumbSeparator>
          <BreadcrumbItem>
            <BreadcrumbLink href="#settings">Settings</BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator className="mx-0 font-semibold">
            /
          </BreadcrumbSeparator>
          <BreadcrumbItem>
            <BreadcrumbPage>Notifications</BreadcrumbPage>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story:
          "BreadcrumbSeparator accepts custom children, making it easy to switch to slashes, dots, or branded glyphs without rewriting layout logic.",
      },
    },
  },
};

export const WithIcons: Story = {
  render: args => (
    <div className="max-w-2xl">
      <Breadcrumb {...args}>
        <BreadcrumbList>
          <BreadcrumbItem>
            <BreadcrumbLink href="#home">
              <HomeIcon aria-hidden="true" className="size-4" />
              Home
            </BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator />
          <BreadcrumbItem>
            <BreadcrumbLink href="#collections">
              <FolderIcon aria-hidden="true" className="size-4" />
              Collections
            </BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator />
          <BreadcrumbItem>
            <BreadcrumbPage>
              <SettingsIcon aria-hidden="true" className="size-4" />
              Feature flags
            </BreadcrumbPage>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story:
          "Inline icons can accompany any link or current page. They automatically inherit the breadcrumb tokens so hover and dark mode behavior stay consistent.",
      },
    },
  },
};

export const Responsive: Story = {
  render: args => (
    <div className="w-full">
      <Breadcrumb {...args}>
        <BreadcrumbList>
          <BreadcrumbItem>
            <BreadcrumbLink href="#home">
              <HomeIcon aria-hidden="true" className="size-4" />
              <span className="sr-only sm:not-sr-only sm:inline">Home</span>
            </BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator />
          <BreadcrumbItem className="hidden md:inline-flex">
            <BreadcrumbLink href="#projects">Projects</BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator className="hidden md:flex" />
          <BreadcrumbItem className="hidden md:inline-flex">
            <BreadcrumbLink href="#workspace">Workspace</BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator className="hidden md:flex" />
          <BreadcrumbItem className="hidden sm:inline-flex md:hidden">
            <BreadcrumbEllipsis aria-label="Hidden breadcrumb items" />
          </BreadcrumbItem>
          <BreadcrumbSeparator className="hidden sm:flex md:hidden" />
          <BreadcrumbItem>
            <BreadcrumbLink href="#tasks">Tasks</BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator />
          <BreadcrumbItem>
            <BreadcrumbPage>Task Details</BreadcrumbPage>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>
      <div className="mt-6 text-xs text-muted-foreground">
        <p className="font-medium">
          Resize viewport to see responsive behavior:
        </p>
        <ul className="mt-2 list-inside list-disc space-y-1">
          <li>
            <strong>Mobile (&lt;640px):</strong> Icon only → Tasks → Task
            Details
          </li>
          <li>
            <strong>Tablet (640-768px):</strong> Home → ... → Tasks → Task
            Details
          </li>
          <li>
            <strong>Desktop (&gt;768px):</strong> Full breadcrumb trail
          </li>
        </ul>
      </div>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story:
          "Responsive breadcrumbs adapt to different screen sizes by hiding intermediate items on smaller viewports. On mobile, show only essential start and end items. On tablets, use ellipsis for collapsed middle items. On desktop, display the full navigation path.",
      },
    },
  },
};

export const LongTextTruncation: Story = {
  render: args => (
    <div className="max-w-2xl">
      <Breadcrumb {...args}>
        <BreadcrumbList>
          <BreadcrumbItem>
            <BreadcrumbLink href="#home">Home</BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator />
          <BreadcrumbItem>
            <BreadcrumbLink href="#projects" className="max-w-40 truncate">
              Enterprise Cloud Infrastructure Projects
            </BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator />
          <BreadcrumbItem>
            <BreadcrumbLink href="#workspace" className="max-w-32 truncate">
              AI Model Training Workspace
            </BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator />
          <BreadcrumbItem>
            <BreadcrumbPage className="max-w-48 truncate">
              Deep Learning Neural Network Configuration Settings
            </BreadcrumbPage>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>
      <div className="mt-6 space-y-4">
        <div>
          <p className="text-sm font-medium text-foreground">
            Without truncation:
          </p>
          <Breadcrumb aria-label="Example without truncation">
            <BreadcrumbList>
              <BreadcrumbItem>
                <BreadcrumbLink href="#home">Home</BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator />
              <BreadcrumbItem>
                <BreadcrumbLink href="#projects">
                  Enterprise Cloud Infrastructure Projects
                </BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator />
              <BreadcrumbItem>
                <BreadcrumbPage>
                  Deep Learning Neural Network Configuration Settings
                </BreadcrumbPage>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
        </div>
        <div className="text-xs text-muted-foreground">
          <p className="font-medium">Best practices:</p>
          <ul className="mt-2 list-inside list-disc space-y-1">
            <li>
              Use <code className="rounded bg-muted px-1 py-0.5">truncate</code>{" "}
              utility with{" "}
              <code className="rounded bg-muted px-1 py-0.5">max-w-*</code>
            </li>
            <li>Apply different max widths based on item importance</li>
            <li>Keep current page (last item) more visible</li>
            <li>Consider using title attribute for full text on hover</li>
          </ul>
        </div>
      </div>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story:
          "Handle long breadcrumb labels gracefully with CSS truncation. Apply max-width constraints and the truncate utility to prevent layout overflow. Adjust max-width values per item based on its importance in the navigation hierarchy.",
      },
    },
  },
};
