# Divider Component Contract

## Purpose
Defines the public interface for the shared Divider component consumed across frontend features.

## Exported API
- **Default Export**: `Divider`
- **Named Export**: `DividerProps`

### DividerProps
| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `orientation` | `'horizontal' \| 'vertical'` | No (defaults to `horizontal`) | Controls layout axis and ARIA orientation. |
| `weight` | `'subtle' \| 'default' \| 'emphasized'` | No (defaults to `default`) | Adjusts thickness/contrast aligned with design tokens. |
| `inset` | `'none' \| 'sm' \| 'md' \| 'lg'` | No (defaults to `none`) | Applies horizontal padding for horizontal dividers; ignored for vertical unless `length='content'`. |
| `length` | `'full' \| 'content'` | No (defaults to `full`) | Determines physical length; for vertical orientation, `content` collapses to children height. |
| `label` | `string` | No | Translation key providing contextual text alongside the separator. |
| `labelPosition` | `'start' \| 'center' \| 'end'` | No (defaults to `center`) | Places optional label relative to divider line. |
| `className` | `string` | No | Additional utility classes merged through design-system helper for layout-specific tweaks. |
| `id` | `string` | No | DOM identifier used for automated testing hooks. |

### Behavioral Guarantees
- When `label` is omitted, the component renders as a decorative separator with `aria-hidden="true"`.
- When `label` is provided, the component exposes `role="separator"` and sets `aria-orientation` based on `orientation`, ensuring the label remains screen-reader visible.
- Orientation-specific spacing and border styles must reference design tokens, preventing ad-hoc colors or sizes.

### Usage Notes
- Consumers must pass translation keys (kebab-case) for `label`; author new keys under `common.layout.divider-*` if necessary.
- Component emits no events and manages no internal state. Any dynamic changes should be handled by parent components.

## Non-Goals
- No backend contracts or API endpoints are introduced by this component.
- Does not include analytics hooks; observability remains the responsibility of parent surfaces.
