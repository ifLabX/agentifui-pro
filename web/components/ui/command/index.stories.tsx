"use client";

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
  group: "Workspace" | "Resources" | "Account";
  keywords?: string[];
};

const actions: CommandAction[] = [
  {
    value: "new-chat",
    label: "Start new chat",
    shortcut: "⌘ + N",
    group: "Workspace",
    keywords: ["conversation", "thread"],
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
    keywords: ["help", "guide"],
  },
  {
    value: "shortcuts",
    label: "Keyboard shortcuts",
    shortcut: "Shift + ?",
    group: "Resources",
    keywords: ["tips"],
  },
  {
    value: "profile",
    label: "Edit profile",
    shortcut: "⌘ + P",
    group: "Account",
    keywords: ["user"],
  },
  {
    value: "logout",
    label: "Sign out",
    group: "Account",
    keywords: ["exit"],
  },
];

const meta = {
  title: "UI/Command",
  component: CommandDialog,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
} satisfies Meta<typeof CommandDialog>;

export default meta;

export type Story = StoryObj<typeof meta>;

const groupActions = (query: string) => {
  if (!query.trim()) return actions;
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

function CommandPaletteStory() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");

  const filtered = useMemo(() => groupActions(query), [query]);
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
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm font-medium">Command palette demo</p>
          <p className="text-sm text-muted-foreground">
            Try typing keywords or use arrow keys to explore actions.
          </p>
        </div>
        <Button onClick={() => setOpen(true)}>Open palette</Button>
      </div>

      <CommandDialog
        open={open}
        onOpenChange={value => {
          if (!value) {
            setOpen(false);
          }
        }}
        commandProps={{ loop: true, vimBindings: true }}
      >
        <CommandInput
          placeholder="Search actions..."
          value={query}
          onValueChange={setQuery}
        />
        <CommandList>
          <CommandEmpty>No commands matched “{query || "…"}”.</CommandEmpty>
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
            <CommandItem disabled>Press Enter to run the command</CommandItem>
          </CommandGroup>
        </CommandList>
      </CommandDialog>
    </div>
  );
}

function KeyboardOnlyStory() {
  const [open, setOpen] = useState(false);

  return (
    <div className="space-y-3">
      <Button onClick={() => setOpen(true)}>Keyboard-only palette</Button>
      <CommandDialog
        open={open}
        onOpenChange={setOpen}
        commandProps={{ disablePointerSelection: true }}
      >
        <CommandInput placeholder="Only keyboard input works here" />
        <CommandList>
          <CommandGroup heading="Shortcuts">
            <CommandItem onSelect={() => setOpen(false)}>
              Toggle theme
              <CommandShortcut>⌘ + T</CommandShortcut>
            </CommandItem>
            <CommandItem disabled>Delete workspace (disabled)</CommandItem>
            <CommandItem onSelect={() => setOpen(false)}>
              Toggle sidebar
              <CommandShortcut>⌘ + B</CommandShortcut>
            </CommandItem>
          </CommandGroup>
        </CommandList>
      </CommandDialog>
    </div>
  );
}

function EmptyStateStory() {
  const [open, setOpen] = useState(false);

  return (
    <div className="space-y-3">
      <Button variant="secondary" onClick={() => setOpen(true)}>
        Open empty state
      </Button>
      <CommandDialog
        open={open}
        onOpenChange={setOpen}
        commandProps={{ loop: true }}
      >
        <CommandInput placeholder="Search..." value="zzzzz" />
        <CommandList>
          <CommandEmpty>
            Nothing matched your search. Try a different keyword.
          </CommandEmpty>
        </CommandList>
      </CommandDialog>
    </div>
  );
}

export const CommandPalette: Story = {
  render: () => <CommandPaletteStory />,
};

export const KeyboardOnly: Story = {
  render: () => <KeyboardOnlyStory />,
};

export const EmptyState: Story = {
  render: () => <EmptyStateStory />,
};

export const Standalone: Story = {
  render: () => (
    <Command className="w-[360px] rounded-xl border border-border" loop>
      <CommandInput placeholder="Type a command…" />
      <CommandList>
        <CommandEmpty>Start typing to search.</CommandEmpty>
        <CommandGroup heading="Suggestions">
          <CommandItem>Create project</CommandItem>
          <CommandItem>Open analytics</CommandItem>
          <CommandItem>Invite member</CommandItem>
        </CommandGroup>
      </CommandList>
    </Command>
  ),
};
