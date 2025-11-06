import commonEn from "@/messages/en-US/common.json";
import type { Meta, StoryObj } from "@storybook/react-vite";

import Divider from "./index";

const meta = {
  title: "UI/Divider",
  component: Divider,
  parameters: {
    layout: "padded",
    docs: {
      description: {
        component:
          "The Divider separates related content blocks while following design tokens for spacing, contrast, and accessibility. Use it to break long panels into readable sections without introducing ad-hoc borders.",
      },
    },
  },
  tags: ["autodocs"],
  argTypes: {
    orientation: {
      control: "inline-radio",
      options: ["horizontal", "vertical"],
    },
    weight: {
      control: "inline-radio",
      options: ["subtle", "default", "emphasized"],
    },
    inset: {
      control: "select",
      options: ["none", "sm", "md", "lg"],
    },
    length: {
      control: "inline-radio",
      options: ["full", "content"],
    },
    label: {
      control: "text",
    },
    labelPosition: {
      control: "inline-radio",
      options: ["start", "center", "end"],
    },
    decorative: {
      control: "boolean",
    },
  },
  args: {
    orientation: "horizontal",
    weight: "default",
    inset: "none",
    length: "full",
    label: "",
    labelPosition: "center",
    decorative: true,
  },
} satisfies Meta<typeof Divider>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Playground: Story = {
  render: args => (
    <div className="mx-auto flex w-full max-w-xl flex-col gap-4 rounded-xl border border-card-border bg-card p-6 text-sm text-muted-foreground">
      <div className="space-y-1">
        <p className="text-sm font-medium text-foreground">
          Prompt instructions
        </p>
        <p>
          Use dividers to break dense agent transcripts or settings panels into
          logical segments.
        </p>
      </div>
      <Divider {...args} />
      <div className="space-y-1">
        <p className="text-sm font-medium text-foreground">
          Output configuration
        </p>
        <p>
          Divider spacing respects inset variants while adapting to light and
          dark themes automatically.
        </p>
      </div>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story:
          "Start with the horizontal divider and consider an inset when adjacent content needs breathing room from the container edge.",
      },
    },
  },
};

export const VerticalDivider: Story = {
  args: {
    orientation: "vertical",
    length: "full",
  },
  render: args => (
    <div className="flex h-40 w-full max-w-xl items-center justify-center gap-6 rounded-xl border border-card-border bg-card p-6">
      <span className="text-sm text-muted-foreground">Timeline</span>
      <Divider {...args} />
      <span className="text-sm text-muted-foreground">Activity</span>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story:
          'Vertical dividers work best inside flexible layouts. Pair them with `length="content"` when the surrounding modules are short to avoid dead space.',
      },
    },
  },
};

export const Weights: Story = {
  render: () => (
    <div className="mx-auto flex w-full max-w-xl flex-col gap-6 text-sm text-muted-foreground">
      <div className="space-y-2">
        <p className="text-sm font-medium text-foreground">Subtle</p>
        <Divider weight="subtle" />
      </div>
      <div className="space-y-2">
        <p className="text-sm font-medium text-foreground">Default</p>
        <Divider weight="default" />
      </div>
      <div className="space-y-2">
        <p className="text-sm font-medium text-foreground">Emphasized</p>
        <Divider weight="emphasized" />
      </div>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story:
          "Reserve the emphasized weight for section breaks inside dense dashboards. Use the subtle weight when creating lightweight groupings such as metadata lists.",
      },
    },
  },
};

export const LabeledDividers: Story = {
  render: () => (
    <div className="mx-auto flex w-full max-w-xl flex-col gap-6 text-sm text-muted-foreground">
      <Divider
        label={commonEn.layout["divider-overview"]}
        labelPosition="center"
      />
      <Divider
        label={commonEn.layout["divider-details"]}
        labelPosition="start"
      />
      <Divider
        label={commonEn.layout["divider-insights"]}
        labelPosition="end"
      />
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story:
          "Labels automatically switch the separator into an announced role. Keep copy short and pass localized strings (e.g. `t('common.layout.divider-overview')`) so assistive tech and designers receive consistent guidance.",
      },
    },
  },
};

export const Insets: Story = {
  render: () => (
    <div className="mx-auto flex w-full max-w-xl flex-col gap-6">
      <div className="space-y-2">
        <p className="text-sm font-medium text-foreground">Inset none</p>
        <Divider inset="none" />
      </div>
      <div className="space-y-2">
        <p className="text-sm font-medium text-foreground">Inset sm</p>
        <Divider inset="sm" />
      </div>
      <div className="space-y-2">
        <p className="text-sm font-medium text-foreground">Inset md</p>
        <Divider inset="md" />
      </div>
      <div className="space-y-2">
        <p className="text-sm font-medium text-foreground">Inset lg</p>
        <Divider inset="lg" />
      </div>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story:
          "Inset spacing keeps the divider aligned with surrounding content gutters. Choose the smallest inset that clears adjacent controls to prevent uneven whitespace.",
      },
    },
  },
};

export const VerticalLabeled: Story = {
  render: () => (
    <div className="mx-auto flex h-48 w-full max-w-xl items-center justify-center rounded-xl border border-card-border bg-card p-6">
      <Divider
        orientation="vertical"
        length="full"
        label={commonEn.layout["divider-overview"]}
        labelPosition="center"
      />
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story:
          "Combine labels with vertical layouts when you need to annotate multi-column flows. The label follows locale direction, and assistive tech announces the orientation for you.",
      },
    },
  },
};
