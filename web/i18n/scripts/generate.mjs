#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const args = process.argv.slice(2);
const command = args[0];
const name = args[1] === '--' ? args[2] : args[1];

/**
 * Get display name for common locales
 */
function getLocaleDisplayName(locale) {
  const localeMap = {
    'en-US': 'English',
    'en-GB': 'English (UK)',
    'zh-Hans': 'Chinese (Simplified)',
    'zh-Hant': 'Chinese (Traditional)',
    'ja-JP': 'Japanese',
    'ko-KR': 'Korean',
    'fr-FR': 'French',
    'de-DE': 'German',
    'es-ES': 'Spanish',
    'pt-BR': 'Portuguese (Brazil)',
    'pt-PT': 'Portuguese',
    'ru-RU': 'Russian',
    'ar-SA': 'Arabic',
    'hi-IN': 'Hindi',
    'it-IT': 'Italian',
    'nl-NL': 'Dutch',
    'sv-SE': 'Swedish',
    'da-DK': 'Danish',
    'no-NO': 'Norwegian',
    'fi-FI': 'Finnish'
  };
  
  return localeMap[locale] || locale;
}

const configPath = path.join(__dirname, '../config.ts');
let configContent = fs.readFileSync(configPath, 'utf-8');

const localesMatch = configContent.match(/export const locales = \[(.*?)\]/s);
const namespacesMatch = configContent.match(/export const namespaces = \[(.*?)\]/s);

if (!localesMatch || !namespacesMatch) {
  console.error('❌ Could not parse config.ts');
  process.exit(1);
}

const currentLocales = localesMatch[1].match(/"([^"]+)"/g)?.map(s => s.slice(1, -1)) || [];
const currentNamespaces = namespacesMatch[1].match(/"([^"]+)"/g)?.map(s => s.slice(1, -1)) || [];

if (!command || !name) {
  console.log('📋 Current configuration:');
  console.log('Locales:', currentLocales);
  console.log('Namespaces:', currentNamespaces);
  console.log('');
  console.log('Usage:');
  console.log('  pnpm i18n:locale fr-FR');
  console.log('  pnpm i18n:namespace dashboard');
  process.exit(0);
}

switch (command) {
  case 'locale':
    addLocale(name);
    break;
  case 'namespace': 
    addNamespace(name);
    break;
  default:
    console.error('❌ Unknown command:', command);
    process.exit(1);
}

function addLocale(locale) {
  if (currentLocales.includes(locale)) {
    console.log(`✅ Locale ${locale} already exists`);
    return;
  }

  console.log(`🌍 Adding locale: ${locale}`);

  try {
    // 1. Create messages directory and copy files
    const messagesDir = path.join(__dirname, '../../messages', locale);
    fs.mkdirSync(messagesDir, { recursive: true });
    console.log(`   ✅ Created: messages/${locale}/`);

    const enUSDir = path.join(__dirname, '../../messages/en-US');
    currentNamespaces.forEach(namespace => {
      const sourceFile = path.join(enUSDir, `${namespace}.json`);
      const targetFile = path.join(messagesDir, `${namespace}.json`);
      fs.copyFileSync(sourceFile, targetFile);
      console.log(`   ✅ Created: messages/${locale}/${namespace}.json`);
    });

    // 2. Update locales array
    const newLocales = [...currentLocales, locale].sort();
    configContent = configContent.replace(
      /export const locales = \[.*?\] as const;/s,
      `export const locales = [${newLocales.map(l => `"${l}"`).join(', ')}] as const;`
    );

    // 3. Add to localeNames
    const displayName = getLocaleDisplayName(locale);
    configContent = configContent.replace(
      /(\} as const;)$/m,
      `  "${locale}": "${displayName}",\n$1`
    );

    fs.writeFileSync(configPath, configContent);
    console.log(`   ✅ Updated: i18n/config.ts`);

    console.log(`\n🎉 Locale ${locale} added successfully!`);
    if (displayName === locale) {
      console.log(`📝 Next: Update localeNames["${locale}"] with proper display name`);
    } else {
      console.log(`✅ Display name set to: "${displayName}"`);
    }
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

function addNamespace(namespace) {
  if (currentNamespaces.includes(namespace)) {
    console.log(`✅ Namespace ${namespace} already exists`);
    return;
  }

  console.log(`📦 Adding namespace: ${namespace}`);

  try {
    // 1. Create JSON files for all locales
    currentLocales.forEach(locale => {
      const filePath = path.join(__dirname, '../../messages', locale, `${namespace}.json`);
      fs.writeFileSync(filePath, '{\n  \n}');
      console.log(`   ✅ Created: messages/${locale}/${namespace}.json`);
    });

    // 2. Update namespaces array
    const newNamespaces = [...currentNamespaces, namespace].sort();
    configContent = configContent.replace(
      /export const namespaces = \[.*?\] as const;/s,
      `export const namespaces = [${newNamespaces.map(n => `"${n}"`).join(', ')}] as const;`
    );
    fs.writeFileSync(configPath, configContent);
    console.log(`   ✅ Updated: i18n/config.ts`);

    // 3. Update types
    const typesPath = path.join(__dirname, '../../types/i18n.d.ts');
    let typesContent = fs.readFileSync(typesPath, 'utf-8');
    
    const capitalizedNamespace = namespace.charAt(0).toUpperCase() + namespace.slice(1);
    const typeImport = `type ${capitalizedNamespace}Messages = typeof import('../messages/en-US/${namespace}.json');`;

    // Add type import after the last type declaration
    typesContent = typesContent.replace(
      /(type \w+Messages = typeof import\("[^"]+"\);)(?=\n\nexport)/,
      `$1\n${typeImport}`
    );

    // Add to Messages interface before the closing brace
    typesContent = typesContent.replace(
      /(\s+)(\w+:\s+\w+Messages;)(\s*};)/,
      `$1$2\n$1${namespace}: ${capitalizedNamespace}Messages;$3`
    );

    fs.writeFileSync(typesPath, typesContent);
    console.log(`   ✅ Updated: types/i18n.d.ts`);

    console.log(`\n🎉 Namespace ${namespace} added successfully!`);
    console.log(`📝 Next: Add content to messages/*/${namespace}.json`);
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}