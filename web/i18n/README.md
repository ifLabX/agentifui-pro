# i18n Architecture

Modern next-intl with namespace support, kebab-case naming, single t() function, and automated locale management.

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
# ✅ Auto-detects common languages (French, German, etc.)
# ✅ Creates messages/fr-FR/*.json for all namespaces
# ✅ Updates config.ts and adds intelligent display name
# ✅ Ready to translate JSON files
```

### New Feature Namespace

```bash
pnpm i18n:namespace dashboard
# ✅ Creates messages/*/dashboard.json for all locales
# ✅ Updates config.ts and types/i18n.d.ts automatically
# ✅ Type-safe immediately, ready to add translations
```

## Configuration

**Single source of truth**: `i18n/config.ts`

- `locales`: Supported language codes
- `namespaces`: Feature-based translation groups
- `localeNames`: Display names (auto-generated for 20+ languages)

## Data Flow

```
config.ts → automated scripts → messages/*.json → request.ts → types → components
```

**No manual configuration needed** - scripts handle all updates automatically.

## Import Rules

```typescript
// Server component (no 'use client')

// Client component ('use client')
import { useTranslations } from "next-intl";
import { getTranslations } from "next-intl/server";
```

## Supported Auto-Locales

English, French, German, Spanish, Portuguese, Italian, Dutch, Russian, Chinese, Japanese, Korean, Arabic, Hindi, and 7 more common languages with intelligent display names.
