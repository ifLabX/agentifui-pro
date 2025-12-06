import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react-vite";
import { ChevronDownIcon, FileTextIcon } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";

const meta = {
  title: "UI/Collapsible",
  component: Collapsible,
  tags: ["autodocs"],
  parameters: {
    layout: "centered",
  },
} satisfies Meta<typeof Collapsible>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => {
    const [open, setOpen] = useState(false);

    return (
      <Collapsible open={open} onOpenChange={setOpen}>
        <CollapsibleTrigger className="flex w-[420px] items-center justify-between rounded-md border px-4 py-3 text-left text-sm font-medium shadow-sm">
          Project summary
          <ChevronDownIcon
            className={`size-4 transition-transform ${
              open ? "rotate-180" : "rotate-0"
            }`}
          />
        </CollapsibleTrigger>
        <CollapsibleContent className="mt-2 w-[420px] rounded-md border bg-muted/30 px-4 py-3 text-sm text-muted-foreground">
          Keep non-critical content hidden by default to keep pages scannable.
          Use collapsibles for FAQs, advanced options, or audit details.
        </CollapsibleContent>
      </Collapsible>
    );
  },
};

export const WithActions: Story = {
  render: () => (
    <Collapsible defaultOpen>
      <CollapsibleTrigger asChild>
        <Button
          variant="outline"
          className="flex w-[420px] items-center justify-between"
        >
          <span className="flex items-center gap-2">
            <FileTextIcon className="size-4" />
            Release notes
          </span>
          <ChevronDownIcon className="size-4 transition-transform data-[state=open]:rotate-180" />
        </Button>
      </CollapsibleTrigger>
      <CollapsibleContent className="mt-3 space-y-2 rounded-md border p-4 text-sm leading-relaxed">
        <div className="flex items-center justify-between">
          <div>
            <p className="font-medium">v2.8.0</p>
            <p className="text-muted-foreground">
              Performance improvements and bug fixes.
            </p>
          </div>
          <Button variant="ghost" size="sm">
            View diff
          </Button>
        </div>
        <ul className="list-disc space-y-1 pl-4 text-muted-foreground">
          <li>Reduced cold-start times for the API.</li>
          <li>Added audit logs for permission updates.</li>
          <li>Improved error messages on failed imports.</li>
        </ul>
      </CollapsibleContent>
    </Collapsible>
  ),
};
