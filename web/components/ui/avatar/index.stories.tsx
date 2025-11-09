import type { Meta, StoryObj } from "@storybook/react-vite";

import { Avatar, AvatarFallback, AvatarImage } from "./index";

const meta = {
  title: "UI/Avatar",
  component: Avatar,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  argTypes: {
    className: {
      control: "text",
      description: "Utility classes applied to the avatar root element.",
    },
  },
} satisfies Meta<typeof Avatar>;

export default meta;
type Story = StoryObj<typeof meta>;

const SAMPLE_IMAGE =
  "https://images.unsplash.com/photo-1544723795-3fb6469f5b39?auto=format&fit=facearea&facepad=3&w=256&h=256&q=80";
const SAMPLE_IMAGE_ALT = "Product designer portrait";
const imageWithSeed = (seed: string) =>
  `${SAMPLE_IMAGE}&seed=${encodeURIComponent(seed)}`;

export const Default: Story = {
  render: args => (
    <Avatar {...args}>
      <AvatarImage src={SAMPLE_IMAGE} alt={SAMPLE_IMAGE_ALT} />
      <AvatarFallback aria-label="Default initials">JD</AvatarFallback>
    </Avatar>
  ),
};

export const WithFallback: Story = {
  render: () => (
    <div className="flex items-center gap-6">
      <Avatar>
        <AvatarImage
          src="https://invalid-url.example.com/avatar.png"
          alt="Broken avatar example"
        />
        <AvatarFallback aria-label="Connection error">CE</AvatarFallback>
      </Avatar>
      <Avatar>
        <AvatarFallback aria-label="No photo available">NA</AvatarFallback>
      </Avatar>
    </div>
  ),
};

export const CustomSizes: Story = {
  render: () => (
    <div className="flex items-end gap-6">
      <div className="space-y-2 text-center text-sm">
        <Avatar className="h-8 w-8 text-xs">
          <AvatarImage src={SAMPLE_IMAGE} alt={SAMPLE_IMAGE_ALT} />
          <AvatarFallback>JR</AvatarFallback>
        </Avatar>
        <span className="text-muted-foreground">Small (32px)</span>
      </div>
      <div className="space-y-2 text-center text-sm">
        <Avatar className="h-12 w-12 text-base">
          <AvatarImage src={SAMPLE_IMAGE} alt={SAMPLE_IMAGE_ALT} />
          <AvatarFallback>JR</AvatarFallback>
        </Avatar>
        <span className="text-muted-foreground">Medium (48px)</span>
      </div>
      <div className="space-y-2 text-center text-sm">
        <Avatar className="h-16 w-16 border-2 border-primary text-lg">
          <AvatarImage src={SAMPLE_IMAGE} alt={SAMPLE_IMAGE_ALT} />
          <AvatarFallback>JR</AvatarFallback>
        </Avatar>
        <span className="text-muted-foreground">Large (64px)</span>
      </div>
    </div>
  ),
};

export const AvatarGroup: Story = {
  render: () => (
    <div className="flex items-center">
      {["AL", "BW", "CE", "DJ"].map(initials => (
        <Avatar
          key={initials}
          className="relative -ml-3 first:ml-0 border-2 border-background"
        >
          <AvatarImage
            src={imageWithSeed(initials)}
            alt={`Team member ${initials}`}
          />
          <AvatarFallback>{initials}</AvatarFallback>
        </Avatar>
      ))}
    </div>
  ),
};

export const WithStatusIndicator: Story = {
  render: () => (
    <div className="flex items-center gap-6">
      {[
        { label: "Online", indicator: "bg-emerald-500" },
        { label: "Away", indicator: "bg-amber-500" },
        { label: "Offline", indicator: "bg-muted-foreground" },
      ].map(({ label, indicator }) => (
        <div key={label} className="flex flex-col items-center gap-2">
          <div className="relative">
            <Avatar className="h-12 w-12">
              <AvatarImage src={imageWithSeed(label)} alt={`${label} user`} />
              <AvatarFallback>{label.slice(0, 2)}</AvatarFallback>
            </Avatar>
            <span
              className={`absolute bottom-0 right-0 block size-3 rounded-full border-2 border-background ${indicator}`}
              aria-label={label}
            />
          </div>
          <span className="text-xs text-muted-foreground">{label}</span>
        </div>
      ))}
    </div>
  ),
};
