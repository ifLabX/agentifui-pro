# Phase 0 Research Findings

## shadcn Divider Foundation
- Decision: Wrap the Radix `Separator` primitive exposed by shadcn and export it as `Divider` to stay aligned with internal naming.
- Rationale: Radix provides proven accessibility defaults (role, aria-orientation) while shadcn already wires Tailwind-friendly class composition; renaming to `Divider` matches product vocabulary without forking behavior.
- Alternatives considered: (1) Raw `<hr>` element with manual classes – fails to support vertical orientation without extra work; (2) Custom div with pseudo-elements – increases maintenance and risks diverging from shadcn updates.

## Variant & Token Strategy
- Decision: Drive spacing, thickness, and color through existing Tailwind token classes (`border-border`, `bg-border`) and expose inset/full/vertical variants via `class-variance-authority` (CVA) patterns used elsewhere in `ui/`.
- Rationale: Re-using tokens guarantees light/dark alignment and keeps configuration declarative, while CVA ensures variants remain type-safe and discoverable for consumers.
- Alternatives considered: (1) Inline style props – brittle with design token changes; (2) Hard-coded utility maps inside components – reduces reuse and complicates testing.

## Storybook Documentation Approach
- Decision: Follow existing Storybook convention (`index.stories.tsx` colocated with component) with primary story, variant gallery, and controls for orientation/spacing/label props.
- Rationale: Matches current documentation patterns (see button/input stories), keeps discoverability high, and enables Chromatic/regression coverage with minimal config.
- Alternatives considered: (1) Standalone MDX docs page – slower to implement and inconsistent with the rest of the design system; (2) No controls – would limit designer self-serve evaluation.

## Accessibility & Labelling
- Decision: Default divider renders `aria-hidden` decorative separator; labeled variant wraps content in visually-aligned text using `role="separator"` + `aria-orientation` while exposing label text to screen readers.
- Rationale: Ensures decorative dividers do not create noisy screen reader output yet allows contextual labels when needed, aligning with WAI-ARIA guidance for separators.
- Alternatives considered: (1) Always hide from assistive tech – prevents labeled dividers from conveying context; (2) Always announce – creates redundant narration for purely visual separators.
