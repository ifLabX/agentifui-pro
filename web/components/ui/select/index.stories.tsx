import { useState, type ComponentProps, type ReactNode } from "react";
import type { Meta, StoryObj } from "@storybook/react-vite";
import {
  CalendarClock,
  Command,
  Layers,
  Monitor,
  MoonStar,
  Palette,
  ShieldCheck,
  Sparkles,
  Sun,
  Workflow,
} from "lucide-react";

import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectSeparator,
  SelectTrigger,
  SelectValue,
} from "./index";

type SelectTriggerProps = ComponentProps<typeof SelectTrigger>;
type SelectRootProps = ComponentProps<typeof Select>;

type Option = {
  value: string;
  label: string;
  description?: string;
  leadingIcon?: ReactNode;
  indicator?: ReactNode;
  hideIndicator?: boolean;
  group?: string;
};

const productivityOptions: Option[] = [
  {
    value: "raycast",
    label: "Raycast",
    description: "Spotlight replacement with rich extensions.",
    leadingIcon: <Command className="size-4" />,
  },
  {
    value: "linear",
    label: "Linear",
    description: "Opinionated issue tracking for product teams.",
    leadingIcon: <Workflow className="size-4" />,
  },
  {
    value: "notion",
    label: "Notion",
    description: "Docs, databases, and tasks under one workspace.",
    leadingIcon: <Layers className="size-4" />,
  },
  {
    value: "height",
    label: "Height",
    description: "Collaborative project planning for async teams.",
    leadingIcon: <Sparkles className="size-4" />,
  },
];

const themeOptions: Option[] = [
  {
    value: "system",
    label: "Match system",
    description: "Follow the appearance defined by the OS.",
    leadingIcon: <Monitor className="size-4" />,
  },
  {
    value: "light",
    label: "Light mode",
    description: "Optimized contrast for daytime reading.",
    leadingIcon: <Sun className="size-4" />,
  },
  {
    value: "dark",
    label: "Dark mode",
    description: "Dim palette to reduce glare at night.",
    leadingIcon: <MoonStar className="size-4" />,
  },
];

const statusOptions: Option[] = [
  {
    value: "draft",
    label: "Draft",
    description: "Still iterating and not ready for review.",
    leadingIcon: <Palette className="size-4" />,
    indicator: <Palette className="h-4 w-4" />,
  },
  {
    value: "scheduled",
    label: "Scheduled",
    description: "Has a launch date in the calendar.",
    leadingIcon: <CalendarClock className="size-4" />,
    indicator: <CalendarClock className="h-4 w-4" />,
  },
  {
    value: "published",
    label: "Published",
    description: "Live for customers to experience.",
    leadingIcon: <ShieldCheck className="size-4" />,
    indicator: <ShieldCheck className="h-4 w-4" />,
  },
];

const languageOptions: Option[] = [
  { value: "en", label: "English (US)", group: "Recommended" },
  { value: "en-GB", label: "English (UK)", group: "Recommended" },
  { value: "zh-CN", label: "Chinese (Simplified)", group: "Recommended" },
  { value: "es", label: "Spanish", group: "More languages" },
  { value: "de", label: "German", group: "More languages" },
  { value: "fr", label: "French", group: "More languages" },
  { value: "pt-BR", label: "Portuguese (Brazil)", group: "More languages" },
  { value: "ja", label: "Japanese", group: "More languages" },
];

const timeZoneOptions: Option[] = [
  { value: "UTC-8", label: "Pacific Time (UTC−08:00)" },
  { value: "UTC-7", label: "Mountain Time (UTC−07:00)" },
  { value: "UTC-6", label: "Central Time (UTC−06:00)" },
  { value: "UTC-5", label: "Eastern Time (UTC−05:00)" },
  { value: "UTC", label: "Coordinated Universal Time (UTC)" },
  { value: "UTC+1", label: "Central European Time (UTC+01:00)" },
  { value: "UTC+3", label: "Arabia Standard Time (UTC+03:00)" },
  { value: "UTC+5:30", label: "India Standard Time (UTC+05:30)" },
  { value: "UTC+8", label: "China Standard Time (UTC+08:00)" },
  { value: "UTC+9", label: "Japan Standard Time (UTC+09:00)" },
  { value: "UTC+10", label: "Australian Eastern Time (UTC+10:00)" },
  { value: "UTC+12", label: "New Zealand Time (UTC+12:00)" },
];

interface SelectFieldProps {
  options: Option[];
  placeholder?: string;
  defaultValue?: string;
  contentClassName?: string;
  selectProps?: Omit<SelectRootProps, "children">;
  triggerProps?: ComponentProps<typeof SelectTrigger>;
  contentProps?: Omit<ComponentProps<typeof SelectContent>, "children" | "ref">;
}

const UNGROUPED_KEY = "__ungrouped";

function SelectField({
  options,
  placeholder,
  defaultValue,
  contentClassName,
  selectProps,
  triggerProps,
  contentProps,
}: SelectFieldProps) {
  const groupedOptions = options.reduce<Map<string, Option[]>>(
    (acc, option) => {
      const key = option.group ?? UNGROUPED_KEY;
      if (!acc.has(key)) {
        acc.set(key, []);
      }
      acc.get(key)!.push(option);
      return acc;
    },
    new Map()
  );

  const groups = Array.from(groupedOptions.entries());

  return (
    <Select defaultValue={defaultValue} {...selectProps}>
      <SelectTrigger {...triggerProps}>
        <SelectValue placeholder={placeholder} />
      </SelectTrigger>
      <SelectContent className={contentClassName} {...contentProps}>
        {groups.map(([groupName, groupOptions], groupIndex) => (
          <SelectGroup key={`${groupName}-${groupIndex}`}>
            {groupName !== UNGROUPED_KEY ? (
              <SelectLabel>{groupName}</SelectLabel>
            ) : null}
            {groupOptions.map(option => (
              <SelectItem
                key={option.value}
                value={option.value}
                leadingIcon={option.leadingIcon}
                description={option.description}
                indicator={option.indicator}
                hideIndicator={option.hideIndicator}
                textValue={option.label}
              >
                {option.label}
              </SelectItem>
            ))}
            {groupIndex < groups.length - 1 ? <SelectSeparator /> : null}
          </SelectGroup>
        ))}
      </SelectContent>
    </Select>
  );
}

const meta: Meta<SelectTriggerProps> = {
  title: "UI/Select",
  component: SelectTrigger,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  argTypes: {
    disabled: {
      control: "boolean",
      description: "When true, the trigger cannot be interacted with.",
    },
    className: {
      control: "text",
      description: "Utility classes applied to the trigger.",
    },
  },
  args: {
    className: "w-[260px]",
  },
};

export default meta;

type Story = StoryObj<SelectTriggerProps>;

export const Playground: Story = {
  render: args => (
    <SelectField
      triggerProps={args}
      options={productivityOptions}
      placeholder="Pick a productivity tool"
      defaultValue="linear"
    />
  ),
};

export const WithIconsAndDescriptions: Story = {
  render: () => (
    <SelectField
      triggerProps={{ className: "w-[260px]" }}
      options={themeOptions}
      placeholder="Choose appearance"
      defaultValue="system"
    />
  ),
};

export const GroupedOptions: Story = {
  render: () => (
    <SelectField
      triggerProps={{ className: "w-[300px]" }}
      options={languageOptions}
      placeholder="Choose a language"
      defaultValue="en"
    />
  ),
};

export const WithoutIndicators: Story = {
  render: () => (
    <SelectField
      triggerProps={{ className: "w-[240px]" }}
      options={productivityOptions.map(option => ({
        ...option,
        hideIndicator: true,
      }))}
      placeholder="Quick actions"
    />
  ),
};

export const CustomIndicator: Story = {
  render: () => (
    <SelectField
      triggerProps={{ className: "w-[260px]" }}
      options={statusOptions}
      placeholder="Workflow status"
      defaultValue="draft"
    />
  ),
};

export const NoScrollIndicators: Story = {
  render: () => (
    <SelectField
      triggerProps={{ className: "w-[280px]" }}
      options={timeZoneOptions}
      placeholder="Set your time zone"
      contentClassName="w-[280px] max-h-48"
      contentProps={{ hideScrollIndicators: true }}
    />
  ),
};

export const WithScrollIndicators: Story = {
  render: () => (
    <SelectField
      triggerProps={{ className: "w-[280px]" }}
      options={[
        ...timeZoneOptions,
        { value: "UTC+13", label: "Tokelau Time (UTC+13:00)" },
        { value: "UTC+14", label: "Line Islands Time (UTC+14:00)" },
      ]}
      placeholder="Browse time zones"
      contentClassName="w-[280px] max-h-48"
    />
  ),
};

export const Controlled: Story = {
  render: args => {
    const [value, setValue] = useState("published");

    return (
      <div className="space-y-3">
        <SelectField
          triggerProps={args}
          options={statusOptions}
          placeholder="Workflow status"
          selectProps={{ value, onValueChange: setValue }}
        />
        <p className="text-sm text-muted-foreground">
          Current status: <span className="font-medium">{value}</span>
        </p>
      </div>
    );
  },
};
