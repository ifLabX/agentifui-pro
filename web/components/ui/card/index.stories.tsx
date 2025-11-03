import type { Meta, StoryObj } from "@storybook/react-vite";

import { Button } from "@/components/ui/button";

import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "./index";

const meta = {
  title: "UI/Card",
  component: Card,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  argTypes: {
    children: {
      control: false,
      description:
        "Card content. Compose with Card subcomponents for structure.",
    },
  },
} satisfies Meta<typeof Card>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <Card className="w-[350px]">
      <CardHeader>
        <CardTitle>Notifications</CardTitle>
        <CardDescription>
          Manage the channels where you receive updates.
        </CardDescription>
        <CardAction>
          <Button variant="outline" size="sm">
            Add channel
          </Button>
        </CardAction>
      </CardHeader>
      <CardContent className="grid gap-4">
        <div className="flex items-center justify-between">
          <div className="space-y-1">
            <p className="text-sm font-medium leading-none">Email</p>
            <p className="text-sm text-muted-foreground">
              Stay on top of account activity.
            </p>
          </div>
          <Button variant="outline" size="sm">
            Configure
          </Button>
        </div>
        <div className="flex items-center justify-between">
          <div className="space-y-1">
            <p className="text-sm font-medium leading-none">Push</p>
            <p className="text-sm text-muted-foreground">
              Receive updates on your devices.
            </p>
          </div>
          <Button variant="outline" size="sm">
            Configure
          </Button>
        </div>
      </CardContent>
      <CardFooter className="flex justify-end">
        <Button>Save changes</Button>
      </CardFooter>
    </Card>
  ),
};

export const WithMedia: Story = {
  render: () => (
    <Card className="w-[400px]">
      <CardHeader>
        <CardTitle>Design review</CardTitle>
        <CardDescription>Thursday, 9:00 AM · Zoom</CardDescription>
        <CardAction className="gap-3">
          <Button variant="outline" size="sm">
            Share
          </Button>
          <Button size="sm">Join</Button>
        </CardAction>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="h-32 rounded-lg bg-muted" />
        <div className="grid gap-1 text-sm text-muted-foreground">
          <span>Host: Alex Kim</span>
          <span>Agenda: Discuss component tokens and layout.</span>
        </div>
      </CardContent>
      <CardFooter className="flex justify-between">
        <Button variant="outline">Reschedule</Button>
        <Button>Join meeting</Button>
      </CardFooter>
    </Card>
  ),
};

export const SignIn: Story = {
  render: () => (
    <Card className="w-[360px]">
      <CardHeader className="flex-row items-start justify-between gap-4 space-y-0">
        <div className="space-y-1.5">
          <CardTitle>Login to your account</CardTitle>
          <CardDescription>
            Enter your email below to login to your account.
          </CardDescription>
        </div>
        <CardAction className="self-start text-sm font-medium text-primary">
          <button type="button" className="hover:underline whitespace-nowrap">
            Sign Up
          </button>
        </CardAction>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2 text-sm">
          <label className="font-medium text-foreground" htmlFor="email">
            Email
          </label>
          <input
            id="email"
            className="h-10 w-full rounded-md border border-input bg-background px-3 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            placeholder="m@example.com"
          />
        </div>
        <div className="space-y-2 text-sm">
          <div className="flex items-center justify-between font-medium">
            <label className="text-foreground" htmlFor="password">
              Password
            </label>
            <button
              type="button"
              className="text-sm text-muted-foreground hover:text-foreground"
            >
              Forgot your password?
            </button>
          </div>
          <input
            id="password"
            type="password"
            className="h-10 w-full rounded-md border border-input bg-background px-3 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          />
        </div>
      </CardContent>
      <CardFooter className="flex flex-col gap-3">
        <Button className="w-full">Login</Button>
        <Button variant="outline" className="w-full">
          Login with Google
        </Button>
      </CardFooter>
    </Card>
  ),
};
