import { useMemo, useState } from "react";
import type { Meta, StoryObj } from "@storybook/react-vite";

import { Button } from "@/components/ui/button";

import {
  Command,
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
  CommandShortcut,
} from "./index";

type CommandAction = {
  value: string;
  label: string;
  shortcut?: string;
  group: string;
  keywords?: string[];
};

const actions: CommandAction[] = [
  {
    value: "new-chat",
    label: "Start new chat",
    shortcut: "⌘ + N",
    group: "Workspace",
    keywords: ["conversation", "chat"],
  },
  {
    value: "invite",
    label: "Invite teammate",
    shortcut: "⌘ + I",
    group: "Workspace",
    keywords: ["member", "collaborator"],
  },
  {
    value: "settings",
    label: "Open settings",
    shortcut: "⌘ + ,",
    group: "Workspace",
    keywords: ["preferences"],
  },
  {
    value: "docs",
    label: "View documentation",
    shortcut: "⌘ + ?",
    group: "Resources",
    keywords: ["help", "guide", "documentation"],
  },
  {
    value: "shortcuts",
    label: "Keyboard shortcuts",
    shortcut: "Shift + ?",
    group: "Resources",
    keywords: ["keys", "shortcuts"],
  },
  {
    value: "profile",
    label: "Edit profile",
    shortcut: "⌘ + P",
    group: "Account",
    keywords: ["user", "profile"],
  },
  {
    value: "logout",
    label: "Sign out",
    group: "Account",
    keywords: ["sign out", "exit"],
  },
];

const filterActions = (query: string) => {
  if (!query.trim()) {
    return actions;
  }
  const normalized = query.toLowerCase();
  return actions.filter(action => {
    return (
      action.label.toLowerCase().includes(normalized) ||
      action.value.toLowerCase().includes(normalized) ||
      action.keywords?.some(keyword =>
        keyword.toLowerCase().includes(normalized)
      )
    );
  });
};

const CommandPalette = () => {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");

  const filtered = useMemo(() => filterActions(query), [query]);
  const grouped = useMemo(() => {
    return filtered.reduce<Record<string, CommandAction[]>>((acc, action) => {
      if (!acc[action.group]) {
        acc[action.group] = [];
      }
      acc[action.group].push(action);
      return acc;
    }, {});
  }, [filtered]);

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium">Command palette demo</p>
          <p className="text-sm text-muted-foreground">
            Click open or press{" "}
            <kbd className="rounded border border-border bg-muted px-1 py-0.5 text-xs uppercase">
              ⌘K
            </kbd>
          </p>
        </div>
        <Button onClick={() => setOpen(true)}>Open palette</Button>
      </div>

      <CommandDialog
        open={open}
        onOpenChange={setOpen}
        commandProps={{ loop: true, vimBindings: true }}
      >
        <CommandInput
          placeholder="Search actions..."
          value={query}
          onValueChange={setQuery}
        />
        <CommandList>
          <CommandEmpty>No commands found.</CommandEmpty>
          {Object.entries(grouped).map(([group, items]) => (
            <CommandGroup key={group} heading={group}>
              {items.map(item => (
                <CommandItem
                  key={item.value}
                  value={item.value}
                  onSelect={() => {
                    setOpen(false);
                    setQuery("");
                  }}
                >
                  <span>{item.label}</span>
                  {item.shortcut ? (
                    <CommandShortcut>{item.shortcut}</CommandShortcut>
                  ) : null}
                </CommandItem>
              ))}
            </CommandGroup>
          ))}
          <CommandSeparator />
          <CommandGroup heading="Tips">
            <CommandItem disabled>Use arrow keys to navigate</CommandItem>
            <CommandItem disabled>Press Enter to run command</CommandItem>
          </CommandGroup>
        </CommandList>
      </CommandDialog>
    </div>
  );
};

const meta: Meta<typeof CommandPalette> = {
  title: "UI/Command",
  component: CommandPalette,
  tags: ["autodocs"],
};

export default meta;

type Story = StoryObj<typeof CommandPalette>;

export const Default: Story = {
  render: () => <CommandPalette />,
};

export const EmptyState: Story = {
  render: () => {
    const Template = () => {
      const [open, setOpen] = useState(false);
      return (
        <div className="space-y-3">
          <Button onClick={() => setOpen(true)}>Open empty palette</Button>
          <CommandDialog
            open={open}
            onOpenChange={setOpen}
            commandProps={{ loop: true }}
          >
            <CommandInput
              placeholder="Search..."
              value="zzzzz"
              onValueChange={() => {}}
            />
            <CommandList>
              <CommandEmpty>Nothing matched your search.</CommandEmpty>
            </CommandList>
          </CommandDialog>
        </div>
      );
    };
    return (
      <div className="space-y-4">
        <p className="text-sm text-muted-foreground">
          This scenario shows the empty state messaging.
        </p>
        <Template />
      </div>
    );
  },
};

export const WithDisabledItems: Story = {
  render: () => {
    const Demo = () => {
      const [open, setOpen] = useState(false);

      return (
        <div className="space-y-3">
          <Button onClick={() => setOpen(true)}>
            Open keyboard-only palette
          </Button>
          <CommandDialog
            open={open}
            onOpenChange={setOpen}
            commandProps={{ disablePointerSelection: true }}
          >
            <CommandInput placeholder="Search shortcuts..." />
            <CommandList>
              <CommandGroup heading="Shortcuts">
                <CommandItem onSelect={() => setOpen(false)}>
                  Cycle theme
                  <CommandShortcut>⌘ + T</CommandShortcut>
                </CommandItem>
                <CommandItem data-disabled>Delete workspace</CommandItem>
                <CommandItem onSelect={() => setOpen(false)}>
                  Toggle sidebar
                  <CommandShortcut>⌘ + B</CommandShortcut>
                </CommandItem>
              </CommandGroup>
            </CommandList>
          </CommandDialog>
        </div>
      );
    };

    return <Demo />;
  },
};

export const Standalone: Story = {
  render: () => (
    <Command className="max-w-lg rounded-xl border border-border" loop>
      <CommandInput placeholder="Type a command..." />
      <CommandList>
        <CommandEmpty>No commands found.</CommandEmpty>
        <CommandGroup heading="Suggestions">
          <CommandItem>Create project</CommandItem>
          <CommandItem>Open analytics</CommandItem>
          <CommandItem>Invite member</CommandItem>
        </CommandGroup>
      </CommandList>
    </Command>
  ),
};
