# Quickstart: Base Divider Component

## Prerequisites
- Install dependencies: `pnpm install` (run within `/web` if new packages were added; not expected for this feature).
- Ensure Storybook tooling is ready: `pnpm dlx storybook@latest upgrade` is **not** required unless Storybook config changes.

## Local Development Steps
1. **Start Storybook**: `cd web && pnpm storybook` to review divider variants interactively.
2. **Create/Update Component**:
   - Add implementation under `web/components/ui/divider/index.tsx` following shadcn conventions (CVA for variants, `cn` helper for classes).
   - Export the component through `web/components/ui/index.ts` if consumers rely on barrel exports.
3. **Design Tokens**: If additional tokens are needed, update `web/app/globals.css` and confirm both light/dark modes render correctly.
4. **Documentation**: Author `web/components/ui/divider/index.stories.tsx` with controls for orientation, inset, weight, length, and label.
5. **Localization**: Register any new translation keys within `web/messages/<locale>/common.json` (e.g., `common.layout.divider-label`) and reference them through `t()` in consuming features.

## Validation Checklist
- `pnpm test` – Add or update unit tests/RTL snapshots covering divider variants.
- `pnpm type-check` – Ensure component props and story args remain type-safe.
- `pnpm quality` – Runs linting, formatting, and composite checks for the web workspace.
- Manual Storybook review for light/dark themes and accessibility panel warnings.

## Handoff Notes
- Document intended usage patterns and guardrails in the Storybook docs tab.
- Capture screenshots or Chromatic snapshots for each primary variant before requesting review.
- Mention in PR description that this feature impacts the shared design system and requires at least one designer sign-off.
