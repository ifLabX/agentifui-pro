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
| `length` | `'full' \| 'content'` | No (defaults to `full`) | Determines physical length; for vertical orientation, `content` collapses to the label stack. |
| `label` | `string` | No | Translation key providing contextual text alongside the separator. Pass the translated string (e.g. `t('common.layout.divider-overview')`). |
| `labelPosition` | `'start' \| 'center' \| 'end'` | No (defaults to `center`) | Places optional label relative to divider line. |
| `className` | `string` | No | Utility classes merged onto the visual rule. When a label is present, the value is applied to each rendered rule segment. |
| `id` | `string` | No | DOM identifier used for automated testing hooks. |
| `decorative` | `boolean` | No (defaults to `true`) | Forwards the Radix `decorative` prop. Automatically forced to `false` when a label is provided so assistive tech announces context. |

### Behavioral Guarantees
- When `label` is omitted, the component renders as a decorative separator with `aria-hidden="true"`.
- When `label` is provided, the component renders a visually balanced layout around the text, exposes `role="separator"` with `aria-orientation`, and ties the label via `aria-labelledby` so screen readers announce the descriptor exactly once.
- Inset variants apply padding on the wrapper for labeled dividers and margins for unlabeled dividers, preventing layout shifts when mixing orientations.
- Orientation-specific spacing and border styles reference divider design tokens (`--divider-muted-color`, `--divider-default-color`, `--divider-emphasized-color`) and adjust thickness based on the selected weight without ad-hoc overrides.

### Usage Notes
- Consumers must pass translation keys (kebab-case) for `label`; author new keys under `common.layout.divider-*` if necessary.
- Component emits no events and manages no internal state. Any dynamic changes should be handled by parent components.

## Non-Goals
- No backend contracts or API endpoints are introduced by this component.
- Does not include analytics hooks; observability remains the responsibility of parent surfaces.
