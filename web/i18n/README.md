# Internationalization (i18n) Configuration

This directory contains the complete i18n configuration for the application using `next-intl` with **storage-based** locale detection (no URL routing).

## Architecture Overview

```
i18n/
├── config.ts          # Centralized locale and namespace configuration
├── request.ts          # Dynamic message loading and locale detection
├── locale-actions.ts   # Server actions for locale management
└── README.md          # This file

messages/
├── en-US/             # English (US) translations
│   ├── common.json    # Common UI elements
│   └── auth.json      # Authentication related
├── zh-Hans/           # Chinese (Simplified) translations
│   ├── common.json
│   └── auth.json
└── ja-JP/             # Japanese translations
    ├── common.json
    └── auth.json
```

## Configuration

### Supported Locales

Currently configured locales (modify in `config.ts`):

- `en-US` - English (US) [Default]
- `zh-Hans` - Chinese (Simplified)
- `ja-JP` - Japanese

### Namespaces

Available namespaces (modify in `config.ts`):

- `common` - Navigation, actions, general messages
- `auth` - Authentication forms and errors

## Adding New Languages

1. Add locale to `config.ts`:

```typescript
export const locales = ["en-US", "zh-Hans", "ja-JP", "fr-FR"] as const;
```

2. Add display name:

```typescript
export const localeNames: Record<Locale, string> = {
  "fr-FR": "Français",
  // ... other locales
};
```

3. Create message files:

```bash
mkdir messages/fr-FR
cp messages/en-US/*.json messages/fr-FR/
# Then translate the content
```

## Adding New Namespaces

1. Add namespace to `config.ts`:

```typescript
export const namespaces = ["common", "auth", "dashboard"] as const;
```

2. Create JSON files for all locales:

```bash
# Create for each locale
touch messages/en-US/dashboard.json
touch messages/zh-Hans/dashboard.json
touch messages/ja-JP/dashboard.json
```

3. The namespace files will be automatically loaded and merged.

## Usage Examples

### In Server Components

```typescript
import { getTranslations } from 'next-intl/server';

export default async function Page() {
  const t = await getTranslations('common.Navigation');

  return <h1>{t('home')}</h1>;
}
```

### In Client Components

```typescript
'use client';
import { useTranslations } from 'next-intl';

export default function Component() {
  const t = useTranslations('auth.SignIn');

  return <button>{t('submit')}</button>;
}
```

### Changing Locale

```typescript
'use client';
import { setLocale } from '@/i18n/locale-actions';

export default function LocaleSwitcher() {
  return (
    <button onClick={() => setLocale('zh-Hans')}>
      Switch to Chinese
    </button>
  );
}
```

## Message Structure

Messages use nested JSON structure for organization:

```json
{
  "Navigation": {
    "home": "Home",
    "settings": "Settings"
  },
  "Actions": {
    "save": "Save",
    "cancel": "Cancel"
  }
}
```

Access with dot notation: `t('Navigation.home')` or use namespace: `useTranslations('Navigation')` then `t('home')`.

## Type Safety

TypeScript declarations are automatically generated from the English (en-US) message files. All message keys are type-checked at compile time.

## Storage

- **Locale Detection**: Cookies → Default locale
- **Cookie Name**: `locale`
- **Cookie Expiry**: 1 year
- **Server Action**: `setLocale(locale)` for updating

## Technical Details

- **Framework**: next-intl v4.3.5+
- **Routing**: Storage-based (no URL locale segments)
- **Message Loading**: Dynamic namespace-based loading
- **Type Safety**: Full TypeScript support with auto-completion
- **Fallback**: Always falls back to `en-US` for missing translations
