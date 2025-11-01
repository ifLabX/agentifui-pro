# Storybook Integration

This project uses Storybook 8.6.14 for component development and documentation.

## Quick Start

```bash
# Start Storybook dev server
pnpm storybook

# Build static Storybook
pnpm build-storybook
```

Storybook runs on [http://localhost:6006](http://localhost:6006)

## Component Stories

All UI components have corresponding `.stories.tsx` files with comprehensive examples:

### Available Stories

- **Button** (`components/ui/button.stories.tsx`)
  - All variants: default, destructive, outline, secondary, ghost, link
  - All sizes: sm, default, lg, icon
  - With icons and disabled states

- **Dropdown Menu** (`components/ui/dropdown-menu.stories.tsx`)
  - Basic menu
  - With labels and keyboard shortcuts
  - Checkbox items with state management
  - Radio groups
  - Nested submenus
  - Disabled items

- **Spinner** (`components/ui/spinner.stories.tsx`)
  - Default and loader variants
  - All sizes: sm, md, lg, xl
  - With custom aria-labels
  - Inline with text

- **Popover** (`components/ui/popover/index.stories.tsx`)
  - Uncontrolled and controlled states
  - With header, body, and footer
  - Modal variant with backdrop
  - Custom width
  - With icons
  - Disabled items

- **Tooltip** (`components/ui/tooltip/index.stories.tsx`)
  - Default with help icon trigger
  - Custom triggers
  - All positions: top, right, bottom, left
  - Different alignments
  - Controlled state
  - Tooltip manager (mutual exclusion)
  - Variable delay duration
  - SSR-safe wrapper variant

- **ChatInput** (`components/ui/chat-input/index.stories.tsx`)
  - Basic input with submit
  - File upload via button
  - Drag and drop
  - Paste from clipboard
  - Multiline text support
  - Disabled state
  - All interactive states

## Configuration

### Main Config (`.storybook/main.js`)

- **Framework**: @storybook/nextjs
- **Stories**: Automatically discovers `*.stories.tsx` in `components/` and `app/`
- **Addons**:
  - `@storybook/addon-essentials` - Core addons (controls, actions, docs, etc.)
  - `@storybook/addon-interactions` - Interactive testing
  - `@storybook/addon-a11y` - Accessibility validation
- **Path Aliases**: Configured to match Next.js `@/` alias
- **TypeScript**: React-docgen-typescript for automatic prop documentation

### Preview Config (`.storybook/preview.ts`)

- **Global Styles**: Imports `app/globals.css` for Tailwind styles
- **next-intl Provider**: Wraps stories with NextIntlClientProvider and mock messages
- **Polyfills**:
  - PointerEvent for Radix UI components
  - ResizeObserver for Floating UI
  - URL.createObjectURL for file handling in ChatInput
- **Next.js App Router**: Configured with `parameters.nextjs.appDirectory = true`

## Writing Stories

### Basic Story Example

```typescript
import type { Meta, StoryObj } from "@storybook/react";

import { MyComponent } from "./my-component";

const meta = {
  title: "UI/MyComponent",
  component: MyComponent,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  argTypes: {
    variant: {
      control: "select",
      options: ["default", "primary"],
    },
  },
} satisfies Meta<typeof MyComponent>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    children: "Hello World",
    variant: "default",
  },
};
```

### Interactive Stories with State

```typescript
export const Controlled: Story = {
  render: () => {
    const ControlledDemo = () => {
      const [state, setState] = useState(false);

      return (
        <MyComponent value={state} onChange={setState} />
      );
    };

    return <ControlledDemo />;
  },
};
```

## Known Issues

### Next.js 15 + Storybook 8 Compatibility

There's a known webpack compatibility issue between Next.js 15 and Storybook 8.6.14:

```
TypeError: Cannot read properties of undefined (reading 'tap')
```

**Workaround Options:**

1. **Use Dev Server** (Recommended):

   ```bash
   pnpm storybook
   ```

   The development server works correctly for component development.

2. **Wait for Updates**:
   - Storybook 9+ will have better Next.js 15 support
   - Next.js 15 is still relatively new, updates expected

3. **Temporary Downgrade** (Not Recommended):
   - Downgrade to Next.js 14.x for static builds
   - Not recommended as it affects the main application

### React 19 Compatibility

Some warnings may appear about React 19 peer dependencies. These are non-blocking:

- Radix UI components work correctly
- Storybook 8.6.14 supports React 19
- `vaul` package shows peer dependency warnings but functions normally

## Best Practices

1. **Component-First Development**: Build components in isolation before integrating
2. **Interactive Testing**: Use `play` functions for user interaction testing
3. **Accessibility**: Leverage `@storybook/addon-a11y` to catch a11y issues early
4. **Documentation**: Use `autodocs` tag to generate prop tables automatically
5. **State Examples**: Provide both controlled and uncontrolled variants
6. **Edge Cases**: Include disabled, loading, error states in stories
7. **Responsive Testing**: Use viewport addon to test different screen sizes

## Troubleshooting

### Storybook won't start

1. Clear cache: `rm -rf node_modules/.cache/storybook`
2. Reinstall dependencies: `pnpm install`
3. Check for conflicting versions in `package.json`

### Stories not appearing

1. Verify file naming: `*.stories.tsx`
2. Check `main.js` stories glob patterns
3. Ensure default export exists in story file

### Styling issues

1. Verify `app/globals.css` is imported in `preview.ts`
2. Check Tailwind config is correctly referenced
3. Ensure CSS variables are defined in globals.css

## Resources

- [Storybook Docs](https://storybook.js.org/docs)
- [Next.js Integration](https://storybook.js.org/recipes/next)
- [Component Story Format](https://storybook.js.org/docs/api/csf)
- [Writing Stories](https://storybook.js.org/docs/writing-stories)
