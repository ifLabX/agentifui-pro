#!/usr/bin/env node
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const args = process.argv.slice(2);
const command = args[0];
// Support multiple arguments: skip '--' and take all remaining as names
const names = args[1] === "--" ? args.slice(2) : args.slice(1);

/**
 * Get display name for common locales
 */
function getLocaleDisplayName(locale) {
  const localeMap = {
    "en-US": "English",
    "en-GB": "English (UK)",
    "zh-Hans": "Chinese (Simplified)",
    "zh-Hant": "Chinese (Traditional)",
    "ja-JP": "Japanese",
    "ko-KR": "Korean",
    "fr-FR": "French",
    "de-DE": "German",
    "es-ES": "Spanish",
    "pt-BR": "Portuguese (Brazil)",
    "pt-PT": "Portuguese",
    "ru-RU": "Russian",
    "ar-SA": "Arabic",
    "hi-IN": "Hindi",
    "it-IT": "Italian",
    "nl-NL": "Dutch",
    "sv-SE": "Swedish",
    "da-DK": "Danish",
    "no-NO": "Norwegian",
    "fi-FI": "Finnish",
  };

  return localeMap[locale] || locale;
}

const configPath = path.join(__dirname, "../config.ts");

// Parse initial config state
function parseConfig() {
  const content = fs.readFileSync(configPath, "utf-8");
  const localesMatch = content.match(/export const locales = \[(.*?)\]/s);
  const namespacesMatch = content.match(/export const namespaces = \[(.*?)\]/s);

  if (!localesMatch || !namespacesMatch) {
    console.error("❌ Could not parse config.ts");
    process.exit(1);
  }

  const currentLocales =
    localesMatch[1].match(/"([^"]+)"/g)?.map(s => s.slice(1, -1)) || [];
  const currentNamespaces =
    namespacesMatch[1].match(/"([^"]+)"/g)?.map(s => s.slice(1, -1)) || [];

  return { content, currentLocales, currentNamespaces };
}

let {
  content: configContent,
  currentLocales,
  currentNamespaces,
} = parseConfig();

if (!command || names.length === 0) {
  console.log("📋 Current configuration:");
  console.log("Locales:", currentLocales);
  console.log("Namespaces:", currentNamespaces);
  console.log("");
  console.log("Usage:");
  console.log("  pnpm i18n:locale fr-FR");
  console.log("  pnpm i18n:locale fr-FR de-DE es-ES  # Multiple locales");
  console.log("  pnpm i18n:namespace dashboard");
  console.log(
    "  pnpm i18n:namespace dashboard settings profile  # Multiple namespaces"
  );
  process.exit(0);
}

switch (command) {
  case "locale":
    console.log(`🌍 Processing ${names.length} locale(s): ${names.join(", ")}`);
    names.forEach((name, index) => {
      console.log(
        `\n[${index + 1}/${names.length}] Processing locale: ${name}`
      );
      addLocale(name);
    });
    break;
  case "namespace":
    console.log(
      `📦 Processing ${names.length} namespace(s): ${names.join(", ")}`
    );
    names.forEach((name, index) => {
      console.log(
        `\n[${index + 1}/${names.length}] Processing namespace: ${name}`
      );
      addNamespace(name);
    });
    break;
  default:
    console.error("❌ Unknown command:", command);
    process.exit(1);
}

function addLocale(locale) {
  if (currentLocales.includes(locale)) {
    console.log(`✅ Locale ${locale} already exists`);
    return;
  }

  console.log(`   🌍 Adding locale: ${locale}`);

  try {
    // 1. Create messages directory and copy files
    const messagesDir = path.join(__dirname, "../../messages", locale);
    fs.mkdirSync(messagesDir, { recursive: true });
    console.log(`   ✅ Created: messages/${locale}/`);

    const enUSDir = path.join(__dirname, "../../messages/en-US");
    currentNamespaces.forEach(namespace => {
      const sourceFile = path.join(enUSDir, `${namespace}.json`);
      const targetFile = path.join(messagesDir, `${namespace}.json`);

      // Check if source file exists
      if (!fs.existsSync(sourceFile)) {
        console.warn(
          `   ⚠️  Source file not found: ${sourceFile}, creating empty file`
        );
        fs.writeFileSync(targetFile, "{\n  \n}");
      } else {
        fs.copyFileSync(sourceFile, targetFile);
      }
      console.log(`   ✅ Created: messages/${locale}/${namespace}.json`);
    });

    // 2. Update locales array and localeNames simultaneously
    const newLocales = [...currentLocales, locale].sort();
    const displayName = getLocaleDisplayName(locale);

    // Update locales array
    configContent = configContent.replace(
      /export const locales = \[.*?\] as const;/s,
      `export const locales = [${newLocales.map(l => `"${l}"`).join(", ")}] as const;`
    );

    // Add to localeNames - find the last entry and insert after it
    configContent = configContent.replace(
      /(.*"[^"]+": "[^"]+",)(\s*)(} as const;)/s,
      `$1\n  "${locale}": "${displayName}",$2$3`
    );

    fs.writeFileSync(configPath, configContent);
    console.log(`   ✅ Updated: i18n/config.ts`);

    // Update current state for next iteration
    currentLocales.push(locale);
    currentLocales.sort();

    console.log(`   🎉 Locale ${locale} added successfully!`);
    if (displayName === locale) {
      console.log(
        `📝 Next: Update localeNames["${locale}"] with proper display name`
      );
    } else {
      console.log(`✅ Display name set to: "${displayName}"`);
    }
  } catch (error) {
    console.error("❌ Error:", error.message);
    process.exit(1);
  }
}

function addNamespace(namespace) {
  // Validate namespace name
  if (!/^[a-z0-9-]+$/.test(namespace)) {
    console.error(
      "❌ Invalid namespace name. Use only lowercase letters, numbers, and hyphens."
    );
    process.exit(1);
  }

  if (currentNamespaces.includes(namespace)) {
    console.log(`✅ Namespace ${namespace} already exists`);
    return;
  }

  console.log(`   📦 Adding namespace: ${namespace}`);

  try {
    // 1. Create JSON files for all locales
    currentLocales.forEach(locale => {
      const filePath = path.join(
        __dirname,
        "../../messages",
        locale,
        `${namespace}.json`
      );
      fs.writeFileSync(filePath, "{\n  \n}");
      console.log(`   ✅ Created: messages/${locale}/${namespace}.json`);
    });

    // 2. Update namespaces array
    const newNamespaces = [...currentNamespaces, namespace].sort();
    configContent = configContent.replace(
      /export const namespaces = \[.*?\] as const;/s,
      `export const namespaces = [${newNamespaces.map(n => `"${n}"`).join(", ")}] as const;`
    );
    fs.writeFileSync(configPath, configContent);
    console.log(`   ✅ Updated: i18n/config.ts`);

    // 3. Update types
    const typesPath = path.join(__dirname, "../../types/i18n.d.ts");
    let typesContent = fs.readFileSync(typesPath, "utf-8");

    // Convert kebab-case to PascalCase for valid TypeScript type names
    const capitalizedNamespace = namespace
      .split("-")
      .map(part => part.charAt(0).toUpperCase() + part.slice(1))
      .join("");
    const typeImport = `type ${capitalizedNamespace}Messages = typeof import('../messages/en-US/${namespace}.json');`;

    // Add type import after the last type declaration
    // Find the last import line and insert after it
    const lastImportRegex =
      /(type \w+Messages = typeof import\([^)]+\);)(?=\s*\n)/g;
    const matches = [...typesContent.matchAll(lastImportRegex)];

    if (matches.length > 0) {
      const lastMatch = matches[matches.length - 1];
      const insertPosition = lastMatch.index + lastMatch[0].length;
      typesContent =
        typesContent.slice(0, insertPosition) +
        `\n${typeImport}` +
        typesContent.slice(insertPosition);
    } else {
      // Fallback: insert before the export statement
      typesContent = typesContent.replace(
        /(\n\nexport type Messages)/,
        `${typeImport}\n$1`
      );
    }

    // Add to Messages interface with unified quoted property names
    const messagesInterfaceRegex = /(export type Messages = \{[\s\S]*?)(};)/;
    typesContent = typesContent.replace(
      messagesInterfaceRegex,
      (match, interfaceContent, closingBrace) => {
        // Clean up excessive whitespace and ensure consistent formatting
        let cleanedContent = interfaceContent.replace(/\n\s*\n\s*\n/g, "\n");

        // Convert existing property names to quoted format for consistency
        cleanedContent = cleanedContent.replace(
          /(\s+)(\w+)(:(?:\s+)\w+Messages;)/g,
          '$1"$2"$3'
        );

        // Add new property with quotes for consistency
        const propertyName = `"${namespace}"`;
        return `${cleanedContent}  ${propertyName}: ${capitalizedNamespace}Messages;\n${closingBrace}`;
      }
    );

    fs.writeFileSync(typesPath, typesContent);
    console.log(`   ✅ Updated: types/i18n.d.ts`);

    // Update current state for next iteration
    currentNamespaces.push(namespace);
    currentNamespaces.sort();

    console.log(`   🎉 Namespace ${namespace} added successfully!`);
    console.log(`   📝 Next: Add content to messages/*/${namespace}.json`);
  } catch (error) {
    console.error("❌ Error:", error.message);
    process.exit(1);
  }
}
