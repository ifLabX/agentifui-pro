# i18n Architecture

Modern next-intl with namespace support, kebab-case naming, single t() function, and automated locale management.

## Quick Commands

```bash
# Add new languages
pnpm i18n:locale fr-FR de-DE es-ES

# Add feature namespace
pnpm i18n:namespace dashboard

# Check translation completeness
pnpm i18n:check

# Auto-translate missing keys
pnpm i18n:translate
```

## Usage Pattern

```typescript
// Single t() function for all translations
const t = useTranslations(); // Client component
const t = await getTranslations(); // Server component

// Dot notation access
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

## Configuration Files

| File              | Purpose                | When to Edit                               |
| ----------------- | ---------------------- | ------------------------------------------ |
| `config.ts`       | Main configuration     | Auto-updated by scripts                    |
| `languages.json`  | Supported locales      | Add new languages                          |
| `scripts/`        | Automation tools       | See [scripts/README.md](scripts/README.md) |
| `messages/`       | Translation files      | Add actual translations                    |
| `types/i18n.d.ts` | TypeScript definitions | Auto-updated by scripts                    |

## Import Rules

```typescript
// Server components (no 'use client')

// Client components ('use client')
import { useTranslations } from "next-intl";
import { getTranslations } from "next-intl/server";
```

## Supported Languages

**20+ languages with auto-detection**: English, Chinese (Simplified/Traditional), Japanese, Korean, French, German, Spanish, Portuguese (Brazil/Portugal), Italian, Dutch, Russian, Arabic, Hindi, Swedish, Danish, Norwegian, Finnish.

For complete list with MyMemory API codes, see [`languages.json`](languages.json).
