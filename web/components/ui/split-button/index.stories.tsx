import type { CSSProperties } from "react";
import type { Meta, StoryObj } from "@storybook/react-vite";
import { Layers, MoreHorizontal, Play } from "lucide-react";

import { SplitButton } from ".";

const meta = {
  title: "UI/SplitButton",
  component: SplitButton,
  parameters: {
    layout: "centered",
    docs: {
      description: {
        component:
          "SplitButton keeps two related actions inside one visual control. It relies on the `--split-button-*` design tokens so the surface matches the global theme, and the center divider is simulated rather than a hard border so the control still reads as a single button.",
      },
    },
  },
  tags: ["autodocs"],
  argTypes: {
    size: {
      control: "select",
      options: ["sm", "default", "lg"],
    },
    fullWidth: {
      control: "boolean",
    },
    disabled: {
      control: "boolean",
    },
    primaryAction: {
      control: "object",
      description:
        "Configuration for the leading action (label, icon, handlers).",
      table: {
        type: { summary: "SplitButtonAction" },
        defaultValue: { summary: "{ label: string }" },
      },
    },
    secondaryAction: {
      control: "object",
      description:
        "Optional trailing action, defaults to a chevron menu trigger.",
      table: {
        type: { summary: "SplitButtonAction" },
        defaultValue: { summary: "{ icon?: ReactNode }" },
      },
    },
  },
  args: {
    size: "default",
    fullWidth: false,
    disabled: false,
    primaryAction: {
      label: "Deploy",
    },
    secondaryAction: {
      label: "More",
    },
  },
} satisfies Meta<typeof SplitButton>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: args => <SplitButton {...args} />,
  parameters: {
    docs: {
      source: {
        code: `<SplitButton
  primaryAction={{ label: "Deploy" }}
  secondaryAction={{ label: "More" }}
/>`,
      },
    },
  },
};

export const WithIcons: Story = {
  render: () => (
    <SplitButton
      primaryAction={{ label: "Run checks", icon: <Play className="size-4" /> }}
      secondaryAction={{
        icon: <MoreHorizontal className="size-4" />,
        "aria-label": "Show menu",
      }}
    />
  ),
  parameters: {
    docs: {
      source: {
        code: `<SplitButton
  primaryAction={{ label: "Run checks", icon: <Play /> }}
  secondaryAction={{ icon: <MoreHorizontal />, aria-label: "Show menu" }}
/>`,
      },
    },
  },
};

export const Small: Story = {
  args: {
    size: "sm",
    primaryAction: {
      label: "Sync",
    },
  },
};

export const Large: Story = {
  args: {
    size: "lg",
    primaryAction: {
      label: "Launch",
    },
    secondaryAction: {
      label: "Actions",
    },
  },
};

export const WithoutSecondaryProp: Story = {
  args: {
    secondaryAction: undefined,
  },
};

export const FullWidth: Story = {
  args: {
    fullWidth: true,
    primaryAction: {
      label: "Publish",
    },
  },
};

export const Disabled: Story = {
  args: {
    disabled: true,
  },
};

const monoSurfaceStyle = {
  "--split-button-primary-bg": "var(--split-button-bg)",
  "--split-button-secondary-bg": "var(--split-button-bg)",
  "--split-button-primary-soft-stop": "var(--split-button-bg)",
  "--split-button-secondary-soft-stop": "var(--split-button-bg)",
} as CSSProperties;

export const MonoSurface: Story = {
  render: () => (
    <SplitButton
      primaryAction={{ label: "Approve" }}
      secondaryAction={{ label: "Details" }}
      style={monoSurfaceStyle}
    />
  ),
  parameters: {
    docs: {
      description: {
        story:
          "Overrides the component tokens so both halves share the same surface colour while still rendering the center seam.",
      },
    },
  },
};

export const LayeredSurface: Story = {
  render: () => (
    <SplitButton
      primaryAction={{ label: "Accent", icon: <Layers className="size-4" /> }}
      secondaryAction={{ "aria-label": "Open menu" }}
      fullWidth
      size="lg"
    />
  ),
  parameters: {
    docs: {
      description: {
        story:
          "Large surface example showing how the gradient subtly differentiates sides without feeling like two buttons.",
      },
    },
  },
};

export const Sizes: Story = {
  render: () => (
    <div className="flex w-full max-w-xl flex-col gap-3">
      <SplitButton
        size="sm"
        primaryAction={{ label: "Tiny" }}
        secondaryAction={{ label: "Menu" }}
      />
      <SplitButton
        size="default"
        primaryAction={{ label: "Default" }}
        secondaryAction={undefined}
      />
      <SplitButton
        size="lg"
        primaryAction={{ label: "Large" }}
        secondaryAction={{ label: "More" }}
        style={monoSurfaceStyle}
      />
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story:
          "Showcases all supported sizes, including a mono-surface large variant to highlight the centered split.",
      },
    },
  },
};
