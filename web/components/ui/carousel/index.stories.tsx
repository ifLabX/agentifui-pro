import type { Meta, StoryObj } from "@storybook/react-vite";

import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";

const meta = {
  title: "UI/Carousel",
  component: Carousel,
  tags: ["autodocs"],
  parameters: {
    layout: "centered",
  },
} satisfies Meta<typeof Carousel>;

export default meta;
type Story = StoryObj<typeof meta>;

const slides = [
  {
    title: "Analytics",
    description: "Track product usage and retention in real time.",
  },
  {
    title: "Automation",
    description: "Automate onboarding flows for new customers.",
  },
  {
    title: "Security",
    description: "Enforce MFA and device trust policies with ease.",
  },
  {
    title: "Reliability",
    description: "Multi-region redundancy keeps uptime above 99.9%.",
  },
  {
    title: "Support",
    description: "Reach the team 24/7 with guaranteed response times.",
  },
];

export const Default: Story = {
  render: () => (
    <div className="w-[380px]">
      <Carousel opts={{ align: "start" }}>
        <CarouselContent>
          {slides.map(item => (
            <CarouselItem key={item.title}>
              <div className="bg-card text-card-foreground rounded-xl border p-6 shadow-sm">
                <div className="text-sm text-muted-foreground">Feature</div>
                <h3 className="mt-2 text-lg font-semibold">{item.title}</h3>
                <p className="mt-1 text-sm text-muted-foreground">
                  {item.description}
                </p>
              </div>
            </CarouselItem>
          ))}
        </CarouselContent>
        <CarouselPrevious />
        <CarouselNext />
      </Carousel>
    </div>
  ),
};

export const Vertical: Story = {
  render: () => (
    <div className="h-[340px] w-[360px]">
      <Carousel orientation="vertical" opts={{ loop: true }}>
        <CarouselContent>
          {["Overview", "Incidents", "Deployments", "SLOs"].map(item => (
            <CarouselItem key={item}>
              <div className="bg-muted/30 text-foreground rounded-xl border p-4">
                <p className="text-sm font-medium">{item}</p>
                <p className="text-sm text-muted-foreground">
                  Scroll vertically to browse recent updates.
                </p>
              </div>
            </CarouselItem>
          ))}
        </CarouselContent>
        <CarouselPrevious />
        <CarouselNext />
      </Carousel>
    </div>
  ),
};
