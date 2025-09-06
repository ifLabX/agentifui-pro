# i18n Scripts Documentation

This directory contains automation scripts for managing internationalization (i18n) in the project.

## Scripts Overview

### 🔍 check.mjs

**Purpose**: Validates translation completeness and consistency  
**Entry point**: `pnpm i18n:check`

```bash
# Check all languages and namespaces
pnpm i18n:check

# Check specific languages
pnpm i18n:check --lang zh-Hans ja-JP

# Check specific namespaces
pnpm i18n:check --file common auth

# Auto-fix extra keys (CI-friendly)
pnpm i18n:check --fix-extra

# Verbose output with detailed issues
pnpm i18n:check --verbose
```

**Features**:

- Detects missing and extra translation keys
- Validates JSON structure and syntax
- Auto-fixes extra keys with `--fix-extra`
- CI-friendly with proper exit codes
- Beautiful table output with color coding

### 🔄 translate.mjs

**Purpose**: Automatically translates missing keys using MyMemory API  
**Entry point**: `pnpm i18n:translate`

```bash
# Translate all missing keys
pnpm i18n:translate

# Translate specific languages
pnpm i18n:translate --lang zh-Hans ja-JP

# Translate specific namespaces
pnpm i18n:translate --file common auth

# Preview mode (no actual translation)
pnpm i18n:translate --dry-run

# Detailed translation process output
pnpm i18n:translate --verbose
```

**Features**:

- Smart text filtering (skips code, variables, URLs)
- Rate limiting and retry logic for API stability
- Preserves existing translations
- Supports dry-run mode for testing
- Comprehensive error handling

### 🏗️ generate.mjs

**Purpose**: Generates new locales and namespaces with proper file structure  
**Entry points**: `pnpm i18n:locale`, `pnpm i18n:namespace`

```bash
# Add single locale
pnpm i18n:locale fr-FR

# Add multiple locales
pnpm i18n:locale fr-FR de-DE es-ES

# Add single namespace
pnpm i18n:namespace dashboard

# Add multiple namespaces
pnpm i18n:namespace dashboard settings profile
```

**Features**:

- Creates proper directory structure
- Updates TypeScript definitions automatically
- Handles display names from unified configuration
- Validates namespace naming conventions
- Updates all related configuration files

### 📝 types.mjs

**Purpose**: Validates and generates TypeScript type definitions for i18n namespaces  
**Entry point**: `pnpm i18n:types`

```bash
# Check if types are synchronized with config
pnpm i18n:types --check

# Generate types based on current config
pnpm i18n:types --generate

# Check with detailed output
pnpm i18n:types --check --verbose

# CI-friendly mode (quiet output)
pnpm i18n:types --check --ci-mode
```

**Features**:

- Validates type synchronization with config.ts
- Generates complete type definitions from namespaces
- Handles manual namespace additions gracefully
- CI-friendly with proper exit codes
- Follows same patterns as generate.mjs for consistency

## Configuration Files

### 📋 languages.json

Central configuration for all supported languages with MyMemory API mappings.

**Structure**:

```json
{
  "supported": {
    "zh-Hans": {
      "displayName": "Chinese (Simplified)",
      "nativeName": "简体中文",
      "myMemoryCode": "zh-CN",
      "isDefault": false,
      "isSupported": true
    }
  }
}
```

## Common Workflows

### Adding New Language

```bash
# 1. Add locale and generate files
pnpm i18n:locale ja-JP

# 2. Translate missing keys
pnpm i18n:translate --lang ja-JP

# 3. Validate completeness
pnpm i18n:check --lang ja-JP
```

### Adding New Feature Namespace

```bash
# 1. Create namespace and files
pnpm i18n:namespace user-profile

# 2. Add content to messages/en-US/user-profile.json
# 3. Translate to other languages
pnpm i18n:translate --file user-profile

# 4. Validate all languages
pnpm i18n:check --file user-profile
```

### CI/CD Integration

```bash
# Check for translation issues (fails on problems)
pnpm i18n:check

# Auto-fix extra keys in CI
pnpm i18n:check --fix-extra

# Validate type synchronization (fails if out of sync)
pnpm i18n:types --check --ci-mode

# Auto-generate types if needed
pnpm i18n:types --generate

# Validate specific changes
pnpm i18n:check --file common --lang zh-Hans ja-JP
```

## Flags Reference

### Common Flags

- `--help, -h`: Show help message
- `--verbose, -v`: Detailed output
- `--lang <locales...>`: Target specific languages
- `--file <namespaces...>`: Target specific namespaces

### Script-Specific Flags

- `--fix-extra` (check): Auto-remove extra keys
- `--dry-run, -d` (translate): Preview mode only
- `--force, -f` (translate): Skip confirmations
- `--check` (types): Validate type synchronization
- `--generate` (types): Generate types from config
- `--ci-mode` (types): Quiet output for CI environments

## Error Handling

All scripts:

- Validate input parameters against configuration
- Provide clear error messages with suggestions
- Use proper exit codes for CI integration
- Handle file system errors gracefully
- Support verbose error reporting for debugging
