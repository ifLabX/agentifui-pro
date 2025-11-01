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

All UI components in `components/ui/` have corresponding `.stories.tsx` files that demonstrate:

- All component variants and sizes
- Interactive states (hover, focus, disabled, loading)
- Controlled and uncontrolled examples
- Edge cases and error states
- Accessibility features

Browse all stories by running `pnpm storybook` and exploring the UI category in the sidebar.

## Configuration

### Main Config (`.storybook/main.js`)

- **Framework**: `@storybook/react-vite` (Vite builder for better Next.js 15 compatibility)
- **Stories**: Automatically discovers `*.stories.tsx` in `components/` and `app/`
- **Addons**:
  - `@storybook/addon-essentials` - Core addons (controls, actions, docs, etc.)
  - `@storybook/addon-interactions` - Interactive testing
  - `@storybook/addon-a11y` - Accessibility validation
- **Vite Configuration**:
  - Path aliases matching Next.js (`@/`)
  - Tailwind CSS v4 PostCSS integration
  - Automatic JSX runtime for React
  - Next.js compatibility polyfills (`process.env`)
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

## Technical Notes

### Next.js 15 + React 19 Compatibility

This setup uses `@storybook/react-vite` instead of `@storybook/nextjs` to avoid webpack compatibility issues with Next.js 15. Key configurations:

- **Vite Builder**: Faster builds and better compatibility with modern tooling
- **Tailwind CSS v4**: Inline PostCSS configuration for the new plugin format
- **Process Polyfill**: Enables Next.js components (like `next/image`) to work in browser
- **JSX Transform**: Automatic React JSX runtime (no manual React imports needed)

### Dependency Warnings

Some peer dependency warnings may appear but are non-blocking:

- **React 19**: Storybook 8.6.14 fully supports React 19
- **Radix UI**: All components work correctly despite version warnings
- **vaul**: Peer dependency warning but functions normally

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
