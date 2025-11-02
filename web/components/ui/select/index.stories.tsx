import { useState, type ReactNode } from "react";
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

type SelectTriggerProps = React.ComponentProps<typeof SelectTrigger>;
type SelectRootProps = React.ComponentProps<typeof Select>;

type Option = {
  value: string;
  label: string;
  description?: string;
  icon?: ReactNode;
  group?: string;
};

const productivityOptions: Option[] = [
  {
    value: "raycast",
    label: "Raycast",
    description: "Spotlight replacement with rich extensions.",
    icon: <Command className="size-4" />,
  },
  {
    value: "linear",
    label: "Linear",
    description: "Opinionated issue tracking for product teams.",
    icon: <Workflow className="size-4" />,
  },
  {
    value: "notion",
    label: "Notion",
    description: "Docs, databases, and tasks under one workspace.",
    icon: <Layers className="size-4" />,
  },
  {
    value: "height",
    label: "Height",
    description: "Collaborative project planning for async teams.",
    icon: <Sparkles className="size-4" />,
  },
];

const themeOptions: Option[] = [
  {
    value: "system",
    label: "Match system",
    description: "Follow the appearance defined by the OS.",
    icon: <Monitor className="size-4" />,
  },
  {
    value: "light",
    label: "Light mode",
    description: "Optimized contrast for daytime reading.",
    icon: <Sun className="size-4" />,
  },
  {
    value: "dark",
    label: "Dark mode",
    description: "Dim palette to reduce glare at night.",
    icon: <MoonStar className="size-4" />,
  },
];

const statusOptions: Option[] = [
  {
    value: "draft",
    label: "Draft",
    description: "Still iterating and not ready for review.",
    icon: <Palette className="size-4" />,
  },
  {
    value: "scheduled",
    label: "Scheduled",
    description: "Has a launch date in the calendar.",
    icon: <CalendarClock className="size-4" />,
  },
  {
    value: "published",
    label: "Published",
    description: "Live for customers to experience.",
    icon: <ShieldCheck className="size-4" />,
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

interface SelectFieldProps extends SelectTriggerProps {
  options: Option[];
  placeholder?: string;
  defaultValue?: string;
  contentClassName?: string;
  selectProps?: Omit<SelectRootProps, "children">;
}

const UNGROUPED_KEY = "__ungrouped";

function SelectField({
  options,
  placeholder,
  defaultValue,
  contentClassName,
  selectProps,
  ...triggerProps
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
      <SelectContent className={contentClassName}>
        {groups.map(([groupName, groupOptions], groupIndex) => (
          <SelectGroup key={`${groupName}-${groupIndex}`}>
            {groupName !== UNGROUPED_KEY && (
              <SelectLabel>{groupName}</SelectLabel>
            )}
            {groupOptions.map(option => (
              <SelectItem
                key={option.value}
                value={option.value}
                icon={option.icon}
                description={option.description}
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
  tags: ["autodocs"],
  argTypes: {
    variant: {
      control: "inline-radio",
      options: ["default", "outline", "subtle"],
      description: "Visual style of the trigger surface.",
    },
    size: {
      control: "inline-radio",
      options: ["sm", "md", "lg"],
      description: "Adjusts the trigger height and font size.",
    },
    state: {
      control: "inline-radio",
      options: ["default", "error"],
      description: "Highlights validation state for the field.",
    },
    disabled: {
      control: "boolean",
      description: "When true, the trigger cannot be interacted with.",
    },
    className: {
      control: "text",
      description: "Width or layout classes applied to the trigger.",
    },
  },
  args: {
    variant: "default",
    size: "md",
    state: "default",
    className: "w-[260px]",
  },
};

export default meta;

type Story = StoryObj<SelectTriggerProps>;

export const Playground: Story = {
  render: args => (
    <SelectField
      {...args}
      options={productivityOptions}
      placeholder="Pick a productivity tool"
      defaultValue="linear"
    />
  ),
};

export const SurfaceVariants: Story = {
  render: () => (
    <div className="grid gap-4 md:grid-cols-2">
      <SelectField
        variant="default"
        size="md"
        className="w-full"
        options={productivityOptions}
        placeholder="Default surface"
        defaultValue="raycast"
      />
      <SelectField
        variant="outline"
        size="sm"
        className="w-full"
        options={themeOptions}
        placeholder="Outline surface"
        defaultValue="system"
      />
      <SelectField
        variant="subtle"
        size="lg"
        className="md:col-span-2 w-full"
        options={statusOptions}
        placeholder="Muted surface"
        defaultValue="published"
      />
    </div>
  ),
};

export const GroupedOptions: Story = {
  render: () => (
    <SelectField
      variant="outline"
      className="w-[300px]"
      options={languageOptions}
      placeholder="Choose a language"
      defaultValue="en"
    />
  ),
};

export const ScrollableContent: Story = {
  render: () => (
    <SelectField
      variant="default"
      className="w-[280px]"
      options={timeZoneOptions}
      placeholder="Set your time zone"
      contentClassName="max-h-60 w-[280px]"
      defaultValue="UTC"
    />
  ),
};

export const Controlled: Story = {
  render: args => {
    const [value, setValue] = useState("published");

    return (
      <div className="space-y-3">
        <SelectField
          {...args}
          options={statusOptions}
          placeholder="Workflow status"
          selectProps={{
            value,
            onValueChange: setValue,
          }}
        />
        <p className="text-sm text-muted-foreground">
          Current status: <span className="font-medium">{value}</span>
        </p>
      </div>
    );
  },
};
