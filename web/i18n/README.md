# i18n Architecture

Modern next-intl with namespace support, kebab-case naming, single t() function.

## Quick Start

```typescript
// Usage - Single t() function for everything
const t = useTranslations(); // Client component
const t = await getTranslations(); // Server component

// Access any translation with dot notation
{
  t("common.navigation.home");
}
{
  t("auth.sign-in.email");
}
{
  t("dashboard.analytics.revenue");
}
```

## Adding Content

### New Language

```bash
pnpm i18n:locale fr-FR
# Creates: messages/fr-FR/*.json + updates config
# Then: translate JSON files
```

### New Feature Namespace

```bash
pnpm i18n:namespace dashboard
# Creates: messages/*/dashboard.json + updates types
# Then: add your translations
```

## File Structure

```
i18n/config.ts          # Single source of truth
messages/[locale]/[namespace].json
types/i18n.d.ts         # Auto-generated types
```

## Architecture Principles

**Single Source**: All config in `i18n/config.ts`
**Auto-Loading**: `request.ts` loops through namespaces
**Type Safety**: Auto-generated from JSON structure  
**Kebab-Case**: Consistent naming throughout

## Data Flow

```
config.ts → messages/*.json → request.ts → types → components
```

Only modify `config.ts` - everything else follows automatically.

## Import Rules

```typescript
// Server component (no 'use client')

// Client component ('use client')
import { useTranslations } from "next-intl";
import { getTranslations } from "next-intl/server";
```
