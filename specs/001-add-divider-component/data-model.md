# Data Model: Base Divider Component

## UI Entity: Divider
- **Purpose**: Provide visual separation between content blocks while aligning with design tokens and accessibility expectations.
- **States / Variants**:
  - `orientation`: `"horizontal"` (default) or `"vertical"`.
  - `weight`: `"subtle"`, `"default"`, `"emphasized"` (controls thickness/opacities).
  - `inset`: `"none"`, `"sm"`, `"md"`, `"lg"` (adjusts horizontal padding for horizontal dividers).
  - `length`: `"full"` (default) or `"content"` (shrinks to content width for vertical dividers).
  - `label`: optional string token referencing `next-intl` key for labeled dividers.
  - `orientationLabelPosition`: `"center"`, `"start"`, or `"end"` when a label is present.
- **Attributes / Props**:
  - `id` (optional): string for automated testing hooks.
  - `className` (optional): string merged through shadcn utility for custom spacing (within design guardrails).
  - `aria-hidden`: enforced `true` when no label provided; omitted when label exists.
- **Relationships**:
  - Consumed by other UI compositions (`card`, `layouts`, feature-specific panels) but has no data persistence ties.
- **Validation Rules**:
  - Reject combination of `label` with `aria-hidden` true; component enforces accessible defaults.
  - `label` must resolve to a kebab-case translation key.
  - `orientation="vertical"` only permits `length="full"` or `"content"`; inset options map to vertical-friendly spacing tokens.
- **State Transitions**:
  - Switching `orientation` recalculates dimension classes and ARIA orientation value.
  - Adding a `label` toggles the accessible structure: wrapper exposes visually centered text while the separator remains perceivable.

## Supporting Tokens
- Relies on existing `--border`, `--muted-foreground`, and spacing tokens defined in global CSS.
- May introduce semantic aliases (`--divider-muted`, `--divider-emphasized`) if design review requires explicit naming.

## Storybook Entities
- Primary story demonstrates horizontal default variant.
- Controls: `orientation`, `weight`, `inset`, `length`, `label`.
- Docs tab includes usage guidelines and accessibility callouts referencing the above model.
