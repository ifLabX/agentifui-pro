import type { Meta, StoryObj } from "@storybook/react-vite";
import { ArrowUpRightIcon, CheckIcon } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";

const meta = {
  title: "UI/Hover Card",
  component: HoverCard,
  tags: ["autodocs"],
  parameters: {
    layout: "centered",
  },
} satisfies Meta<typeof HoverCard>;

export default meta;
type Story = StoryObj<typeof meta>;

export const ProfilePreview: Story = {
  render: () => (
    <HoverCard openDelay={150}>
      <HoverCardTrigger className="inline-flex items-center gap-2 rounded-full border px-3 py-1 text-sm font-medium shadow-sm">
        <span className="size-6 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500" />
        @design-lead
      </HoverCardTrigger>
      <HoverCardContent className="space-y-3">
        <div className="flex items-center gap-3">
          <span className="size-12 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 shadow-sm" />
          <div>
            <p className="text-sm font-semibold leading-tight">
              Taylor Kim
            </p>
            <p className="text-xs text-muted-foreground">
              Design Lead · San Francisco
            </p>
          </div>
        </div>
        <p className="text-sm text-muted-foreground">
          Shipping a new design system for the workspace experience. Open for
          feedback on tokens and motion guidelines.
        </p>
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <CheckIcon className="size-3.5 text-emerald-500" />
          Available for pairing this week
        </div>
      </HoverCardContent>
    </HoverCard>
  ),
};

export const WithCTA: Story = {
  render: () => (
    <HoverCard openDelay={100}>
      <HoverCardTrigger asChild>
        <Button variant="outline" size="sm">
          View roadmap
        </Button>
      </HoverCardTrigger>
      <HoverCardContent className="space-y-3">
        <div>
          <p className="text-sm font-semibold">Q2 Highlights</p>
          <p className="text-sm text-muted-foreground">
            Major bets and milestones planned for the quarter.
          </p>
        </div>
        <ul className="list-disc space-y-1 pl-4 text-sm text-muted-foreground">
          <li>Multi-tenant billing rollout</li>
          <li>Improved changelog and release feeds</li>
          <li>Faster onboarding with saved templates</li>
        </ul>
        <Button size="sm" className="w-full">
          Explore roadmap
          <ArrowUpRightIcon className="ml-2 size-4" />
        </Button>
      </HoverCardContent>
    </HoverCard>
  ),
};
