#!/usr/bin/env node
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ANSI color codes and symbols - consistent with check.mjs
const colors = {
  reset: "\x1b[0m",
  bright: "\x1b[1m",
  red: "\x1b[31m",
  green: "\x1b[32m",
  yellow: "\x1b[33m",
  blue: "\x1b[34m",
  magenta: "\x1b[35m",
  cyan: "\x1b[36m",
  white: "\x1b[37m",
};

const symbols = {
  success: "✅",
  error: "❌",
  warning: "⚠️",
  info: "ℹ️",
  translate: "🔄",
  skip: "⏭️",
  summary: "📊",
  world: "🌍",
  rocket: "🚀",
  celebration: "🎉",
};

/**
 * Parse command line arguments
 * Supports: --lang zh-Hans ja-JP --file common auth --dry-run
 */
function parseArguments() {
  const args = process.argv.slice(2);
  const parsed = {
    lang: [],
    file: [],
    help: false,
    dryRun: false,
    verbose: false,
    force: false,
  };

  let currentFlag = null;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg.startsWith("--")) {
      currentFlag = arg.substring(2);

      if (currentFlag === "help" || currentFlag === "h") {
        parsed.help = true;
      } else if (currentFlag === "dry-run" || currentFlag === "d") {
        parsed.dryRun = true;
      } else if (currentFlag === "verbose" || currentFlag === "v") {
        parsed.verbose = true;
      } else if (currentFlag === "force" || currentFlag === "f") {
        parsed.force = true;
      } else if (!["lang", "file"].includes(currentFlag)) {
        console.error(
          `${colors.red}${symbols.error} Unknown flag: ${arg}${colors.reset}`
        );
        process.exit(1);
      }
    } else {
      // Add value to current flag
      if (currentFlag && ["lang", "file"].includes(currentFlag)) {
        parsed[currentFlag].push(arg);
      } else {
        console.error(
          `${colors.red}${symbols.error} Unexpected argument: ${arg}${colors.reset}`
        );
        process.exit(1);
      }
    }
  }

  return parsed;
}

/**
 * Load and parse i18n configuration dynamically - consistent with check.mjs
 */
async function loadI18nConfig() {
  try {
    const configPath = path.join(__dirname, "../config.ts");
    const configContent = fs.readFileSync(configPath, "utf-8");

    // Extract locales array
    const localesMatch = configContent.match(
      /export const locales = \[(.*?)\]/s
    );
    const namespacesMatch = configContent.match(
      /export const namespaces = \[(.*?)\]/s
    );
    const defaultLocaleMatch = configContent.match(
      /export const defaultLocale.*?=\s*["']([^"']+)["']/
    );

    if (!localesMatch || !namespacesMatch || !defaultLocaleMatch) {
      throw new Error("Could not parse i18n configuration");
    }

    const locales =
      localesMatch[1].match(/"([^"]+)"/g)?.map(s => s.slice(1, -1)) || [];
    const namespaces =
      namespacesMatch[1].match(/"([^"]+)"/g)?.map(s => s.slice(1, -1)) || [];
    const defaultLocale = defaultLocaleMatch[1];

    return { locales, namespaces, defaultLocale };
  } catch (error) {
    console.error(
      `${colors.red}${symbols.error} Failed to load i18n configuration: ${error.message}${colors.reset}`
    );
    process.exit(1);
  }
}

/**
 * Get supported locales from generate.mjs for consistency
 * Extract the same locales that generate.mjs supports
 */
function getSupportedLocales() {
  // Same locale keys as in generate.mjs getLocaleDisplayName function
  return [
    "en-US",
    "en-GB",
    "zh-Hans",
    "zh-Hant",
    "ja-JP",
    "ko-KR",
    "fr-FR",
    "de-DE",
    "es-ES",
    "pt-BR",
    "pt-PT",
    "ru-RU",
    "ar-SA",
    "hi-IN",
    "it-IT",
    "nl-NL",
    "sv-SE",
    "da-DK",
    "no-NO",
    "fi-FI",
  ];
}

/**
 * Map locale codes to translation API language codes
 * Uses the same locale keys as generate.mjs but different mapping purpose
 */
function getTranslationLanguageCode(locale) {
  const supportedLocales = getSupportedLocales();

  // Ensure the locale is supported
  if (!supportedLocales.includes(locale)) {
    console.warn(
      `${colors.yellow}${symbols.warning} Unsupported locale: ${locale}, using fallback${colors.reset}`
    );
  }

  const langMap = {
    "en-US": "en",
    "en-GB": "en",
    "zh-Hans": "zh-CN",
    "zh-Hant": "zh-TW",
    "ja-JP": "ja",
    "ko-KR": "ko",
    "fr-FR": "fr",
    "de-DE": "de",
    "es-ES": "es",
    "pt-BR": "pt",
    "pt-PT": "pt",
    "ru-RU": "ru",
    "ar-SA": "ar",
    "hi-IN": "hi",
    "it-IT": "it",
    "nl-NL": "nl",
    "sv-SE": "sv",
    "da-DK": "da",
    "no-NO": "no",
    "fi-FI": "fi",
  };

  return langMap[locale] || locale.split("-")[0];
}

/**
 * Check if text should be translated
 */
function isTranslatableText(text) {
  if (typeof text !== "string") return false;
  if (!text.trim()) return false;

  // Skip patterns that shouldn't be translated
  const skipPatterns = [
    /^\{\{.*\}\}$/, // Template variables
    /^\$\{.*\}$/, // JavaScript template literals
    /^<[^>]+>$/, // HTML tags
    /function\s*\(/, // JavaScript functions
    /^\w+\s*=.*$/, // Variable assignments
    /^[A-Z_][A-Z0-9_]*$/, // Constants
    /^\d+(\.\d+)?$/, // Numbers
    /^[a-z]+:[a-z0-9-]+$/i, // URLs/protocols
    /^#[0-9a-f]{3,6}$/i, // Color codes
    /^[a-z0-9-_.]+@[a-z0-9-_.]+$/i, // Email addresses
  ];

  return !skipPatterns.some(pattern => pattern.test(text.trim()));
}

/**
 * Translate text using MyMemory API (same as example)
 */
async function translateText(text, targetLanguage) {
  try {
    if (text.length > 450) {
      console.warn(
        `${colors.yellow}${symbols.warning} Text too long for "${text.substring(0, 50)}..."${colors.reset}`
      );
      return text;
    }

    const url = new URL("https://api.mymemory.translated.net/get");
    url.searchParams.append("q", text);
    url.searchParams.append("langpair", `en|${targetLanguage}`);
    url.searchParams.append("de", "agentifui@example.com");

    const translationResponse = await fetch(url.toString(), {
      method: "GET",
      headers: {
        "User-Agent": "AgentifUI-Pro/1.0",
      },
    });

    if (!translationResponse.ok) {
      throw new Error(
        `HTTP ${translationResponse.status}: ${translationResponse.statusText}`
      );
    }

    const data = await translationResponse.json();

    if (data.responseStatus === 200 && data.responseData) {
      const translated = data.responseData.translatedText;

      if (translated && translated !== text && translated.length > 0) {
        return translated;
      }
    }

    throw new Error(
      `Translation API error: ${data.responseDetails || "Unknown error"}`
    );
  } catch (error) {
    console.warn(
      `${colors.yellow}${symbols.warning} Translation failed for "${text}" to ${targetLanguage}: ${error.message}${colors.reset}`
    );
    return text;
  }
}

/**
 * Translate with exponential backoff retry - same logic as example
 */
async function translateWithBackoff(text, targetLanguage, retries = 3) {
  for (let attempt = 0; attempt < retries; attempt++) {
    try {
      const result = await translateText(text, targetLanguage);
      if (result !== text) {
        return result;
      }
    } catch (error) {
      if (attempt === retries - 1) {
        throw error;
      }

      const delay = Math.min(1000 * Math.pow(2, attempt), 5000);
      console.warn(
        `${colors.yellow}${symbols.warning} Translation attempt ${attempt + 1} failed, retrying in ${delay}ms...${colors.reset}`
      );
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  return text;
}

/**
 * Recursively extract all keys from JSON object - consistent with check.mjs
 */
function extractKeys(obj, prefix = "") {
  const keys = [];

  for (const [key, value] of Object.entries(obj)) {
    const fullKey = prefix ? `${prefix}.${key}` : key;

    if (typeof value === "object" && value !== null) {
      keys.push(...extractKeys(value, fullKey));
    } else {
      keys.push(fullKey);
    }
  }

  return keys.sort();
}

/**
 * Load translation file - consistent with check.mjs
 */
function loadTranslationFile(locale, namespace) {
  try {
    const filePath = path.join(
      __dirname,
      "../../messages",
      locale,
      `${namespace}.json`
    );

    if (!fs.existsSync(filePath)) {
      return {
        exists: false,
        keys: [],
        data: {},
        filePath,
        error: `File not found: ${filePath}`,
      };
    }

    const content = fs.readFileSync(filePath, "utf-8");
    const data = JSON.parse(content);
    const keys = extractKeys(data);

    return { exists: true, keys, data, filePath };
  } catch (error) {
    return { exists: false, keys: [], data: {}, error: error.message };
  }
}

/**
 * Get value from nested object using dot notation
 */
function getNestedValue(obj, keyPath) {
  const keys = keyPath.split(".");
  let current = obj;

  for (const key of keys) {
    if (current && typeof current === "object" && key in current) {
      current = current[key];
    } else {
      return undefined;
    }
  }

  return current;
}

/**
 * Set value in nested object using dot notation
 */
function setNestedValue(obj, keyPath, value) {
  const keys = keyPath.split(".");
  const lastKey = keys.pop();
  let current = obj;

  // Create nested structure if needed
  for (const key of keys) {
    if (!(key in current)) {
      current[key] = {};
    }
    current = current[key];
  }

  current[lastKey] = value;
}

/**
 * Translate missing keys for a specific locale and namespace
 */
async function translateMissingKeys(
  sourceData,
  targetData,
  sourceKeys,
  targetKeys,
  locale,
  namespace,
  dryRun = false
) {
  const translationCode = getTranslationLanguageCode(locale);
  const missingKeys = sourceKeys.filter(key => !targetKeys.includes(key));

  const stats = {
    translated: 0,
    skipped: 0,
    errors: 0,
    total: missingKeys.length,
  };

  if (missingKeys.length === 0) {
    return { data: targetData, stats };
  }

  console.log(
    `  ${colors.blue}${symbols.translate} Found ${missingKeys.length} missing key(s)${colors.reset}`
  );

  // Deep clone target data to avoid modifying original
  const updatedData = JSON.parse(JSON.stringify(targetData));

  for (const keyPath of missingKeys) {
    const sourceText = getNestedValue(sourceData, keyPath);

    if (typeof sourceText !== "string") {
      console.log(
        `    ${colors.yellow}${symbols.skip} Skipping non-string key: ${keyPath}${colors.reset}`
      );
      setNestedValue(updatedData, keyPath, sourceText);
      stats.skipped++;
      continue;
    }

    if (!isTranslatableText(sourceText)) {
      console.log(
        `    ${colors.yellow}${symbols.skip} Skipping non-translatable: ${keyPath}: "${sourceText}"${colors.reset}`
      );
      setNestedValue(updatedData, keyPath, sourceText);
      stats.skipped++;
      continue;
    }

    if (dryRun) {
      console.log(
        `    ${colors.cyan}[DRY RUN]${colors.reset} Would translate: ${keyPath}: "${sourceText}"`
      );
      stats.translated++;
      continue;
    }

    try {
      console.log(
        `    ${colors.blue}${symbols.translate} Translating: ${keyPath}: "${sourceText}"${colors.reset}`
      );

      const translatedText = await translateWithBackoff(
        sourceText,
        translationCode
      );
      setNestedValue(updatedData, keyPath, translatedText);

      console.log(`      ${colors.green}→ "${translatedText}"${colors.reset}`);
      stats.translated++;

      // Rate limiting - same as example
      await new Promise(resolve => setTimeout(resolve, 200));
    } catch (error) {
      console.error(
        `    ${colors.red}${symbols.error} Error translating ${keyPath}: ${error.message}${colors.reset}`
      );
      setNestedValue(updatedData, keyPath, sourceText);
      stats.errors++;
    }
  }

  return { data: updatedData, stats };
}

/**
 * Write translation file with proper formatting - consistent with check.mjs
 */
function writeTranslationFile(filePath, data) {
  try {
    // Use 2-space indentation to match existing format
    const content = JSON.stringify(data, null, 2) + "\n";
    fs.writeFileSync(filePath, content, "utf-8");
    return true;
  } catch (error) {
    console.error(
      `${colors.red}${symbols.error} Failed to write ${filePath}: ${error.message}${colors.reset}`
    );
    return false;
  }
}

/**
 * Display help message
 */
function showHelp() {
  console.log(`
${colors.cyan}${colors.bright}i18n Translation Generator${colors.reset}

${colors.white}USAGE:${colors.reset}
  pnpm i18n:translate [OPTIONS]

${colors.white}OPTIONS:${colors.reset}  
  --lang <locales...>     Translate specific languages (e.g., --lang zh-Hans ja-JP)
  --file <namespaces...>  Translate specific namespaces (e.g., --file common auth)
  --dry-run, -d           Preview mode (show what would be translated)
  --force, -f             Skip confirmation prompts (useful for CI)
  --verbose, -v           Show detailed output
  --help, -h              Show this help message

${colors.white}EXAMPLES:${colors.reset}
  pnpm i18n:translate                           # Translate missing keys for all languages
  pnpm i18n:translate --lang zh-Hans ja-JP      # Translate only Chinese and Japanese
  pnpm i18n:translate --file common auth        # Translate only common and auth namespaces
  pnpm i18n:translate --dry-run                 # Preview what would be translated
  pnpm i18n:translate --lang zh-Hans --verbose  # Detailed output for Chinese

${colors.white}WORKFLOW:${colors.reset}
  ${symbols.info} Only translates missing keys (preserves existing translations)
  ${symbols.info} Uses intelligent text filtering (skips code, variables, etc.)
  ${symbols.info} Includes rate limiting and retry logic for API stability
  ${symbols.info} Maintains JSON formatting consistency with project standards

${colors.white}API:${colors.reset}
  Uses MyMemory Translation API (free tier with rate limits)
  Supports automatic language detection and fallbacks
`);
}

/**
 * Display summary table - consistent style with check.mjs
 */
function displaySummaryTable(results, config) {
  console.log(
    `\n${colors.cyan}${colors.bright}${symbols.summary} Translation Summary${colors.reset}`
  );
  console.log(
    `${colors.white}Source: ${config.defaultLocale}${colors.reset}\n`
  );

  // Calculate column widths
  const maxLocaleWidth = Math.max(...results.map(r => r.locale.length), 8);
  const maxNamespaceWidth = Math.max(
    ...results.map(r => r.namespace.length),
    9
  );

  // Header
  const header = [
    "Locale".padEnd(maxLocaleWidth),
    "Namespace".padEnd(maxNamespaceWidth),
    "Missing",
    "Translated",
    "Skipped",
    "Errors",
    "Status",
  ].join(" │ ");

  console.log(`${colors.white}${header}${colors.reset}`);
  console.log("─".repeat(header.length));

  // Rows
  results.forEach(result => {
    const status = result.error
      ? `${colors.red}${symbols.error} Error${colors.reset}`
      : result.stats.total === 0
        ? `${colors.green}${symbols.success} Complete${colors.reset}`
        : result.stats.errors > 0
          ? `${colors.yellow}${symbols.warning} Issues${colors.reset}`
          : `${colors.green}${symbols.success} Done${colors.reset}`;

    const row = [
      result.locale.padEnd(maxLocaleWidth),
      result.namespace.padEnd(maxNamespaceWidth),
      result.stats?.total?.toString().padStart(7) || "N/A".padStart(7),
      result.stats?.translated?.toString().padStart(10) || "N/A".padStart(10),
      result.stats?.skipped?.toString().padStart(7) || "N/A".padStart(7),
      result.stats?.errors?.toString().padStart(6) || "N/A".padStart(6),
      status,
    ].join(" │ ");

    console.log(row);
  });
}

/**
 * Main execution function
 */
async function main() {
  const args = parseArguments();

  if (args.help) {
    showHelp();
    return;
  }

  console.log(
    `${colors.cyan}${colors.bright}${symbols.rocket} i18n Translation Generator${colors.reset}`
  );
  console.log(
    `${colors.white}Starting translation process...${colors.reset}\n`
  );

  // Load configuration
  const config = await loadI18nConfig();

  // Determine locales and namespaces to process
  const targetLocales =
    args.lang.length > 0
      ? args.lang
      : config.locales.filter(l => l !== config.defaultLocale);
  const targetNamespaces = args.file.length > 0 ? args.file : config.namespaces;

  // Validate provided arguments
  const invalidLocales = args.lang.filter(
    lang => !config.locales.includes(lang)
  );
  const invalidNamespaces = args.file.filter(
    ns => !config.namespaces.includes(ns)
  );

  if (invalidLocales.length > 0) {
    console.error(
      `${colors.red}${symbols.error} Invalid locales: ${invalidLocales.join(", ")}${colors.reset}`
    );
    console.error(
      `${colors.white}Available locales: ${config.locales.join(", ")}${colors.reset}`
    );
    process.exit(1);
  }

  if (invalidNamespaces.length > 0) {
    console.error(
      `${colors.red}${symbols.error} Invalid namespaces: ${invalidNamespaces.join(", ")}${colors.reset}`
    );
    console.error(
      `${colors.white}Available namespaces: ${config.namespaces.join(", ")}${colors.reset}`
    );
    process.exit(1);
  }

  console.log(`${colors.white}Configuration:${colors.reset}`);
  console.log(
    `  Source locale: ${colors.green}${config.defaultLocale}${colors.reset}`
  );
  console.log(
    `  Target locales: ${colors.blue}${targetLocales.join(", ")}${colors.reset}`
  );
  console.log(
    `  Namespaces: ${colors.magenta}${targetNamespaces.join(", ")}${colors.reset}`
  );
  console.log(
    `  Mode: ${args.dryRun ? `${colors.yellow}DRY RUN${colors.reset}` : `${colors.green}LIVE TRANSLATION${colors.reset}`}`
  );

  const results = [];
  let totalStats = { translated: 0, skipped: 0, errors: 0, total: 0 };

  // Process each combination of locale and namespace
  for (const namespace of targetNamespaces) {
    // Load source file
    const sourceFile = loadTranslationFile(config.defaultLocale, namespace);

    if (!sourceFile.exists) {
      console.error(
        `${colors.red}${symbols.error} Source file missing: ${config.defaultLocale}/${namespace}${colors.reset}`
      );
      continue;
    }

    console.log(
      `\n${colors.white}Processing namespace: ${colors.magenta}${namespace}${colors.reset}`
    );

    for (const locale of targetLocales) {
      console.log(`\n${colors.world} ${locale}/${namespace}:`);

      const targetFile = loadTranslationFile(locale, namespace);

      if (!targetFile.exists) {
        // Create new file with empty object
        targetFile.data = {};
        targetFile.keys = [];
        targetFile.exists = true;

        // Ensure directory exists
        const dir = path.dirname(targetFile.filePath);
        fs.mkdirSync(dir, { recursive: true });
      }

      try {
        const translationResult = await translateMissingKeys(
          sourceFile.data,
          targetFile.data,
          sourceFile.keys,
          targetFile.keys,
          locale,
          namespace,
          args.dryRun
        );

        if (!args.dryRun && translationResult.stats.translated > 0) {
          const success = writeTranslationFile(
            targetFile.filePath,
            translationResult.data
          );
          if (!success) {
            translationResult.stats.errors++;
          }
        }

        results.push({
          locale,
          namespace,
          stats: translationResult.stats,
          error: null,
        });

        // Update total stats
        totalStats.translated += translationResult.stats.translated;
        totalStats.skipped += translationResult.stats.skipped;
        totalStats.errors += translationResult.stats.errors;
        totalStats.total += translationResult.stats.total;
      } catch (error) {
        console.error(
          `${colors.red}${symbols.error} Error processing ${locale}/${namespace}: ${error.message}${colors.reset}`
        );

        results.push({
          locale,
          namespace,
          error: error.message,
          stats: { translated: 0, skipped: 0, errors: 1, total: 0 },
        });

        totalStats.errors++;
      }
    }
  }

  // Display results
  displaySummaryTable(results, config);

  // Final status
  console.log(
    `\n${colors.celebration} Translation process complete!${colors.reset}`
  );
  console.log(
    `${colors.white}${symbols.summary} Total Summary:${colors.reset}`
  );
  console.log(
    `  ${colors.green}✅ Total translated: ${totalStats.translated}${colors.reset}`
  );
  console.log(
    `  ${colors.yellow}⏭️ Total skipped: ${totalStats.skipped}${colors.reset}`
  );
  console.log(
    `  ${colors.red}❌ Total errors: ${totalStats.errors}${colors.reset}`
  );

  if (args.dryRun) {
    console.log(
      `\n${colors.cyan}${symbols.info} Run without --dry-run to perform actual translation${colors.reset}`
    );
  } else if (totalStats.translated > 0) {
    console.log(
      `\n${colors.cyan}${symbols.info} Run 'pnpm i18n:check' to validate the translations${colors.reset}`
    );
  }

  // Exit with appropriate code
  process.exit(totalStats.errors > 0 ? 1 : 0);
}

// Execute main function
main().catch(error => {
  console.error(
    `${colors.red}${symbols.error} Unexpected error: ${error.message}${colors.reset}`
  );
  if (process.env.NODE_ENV === "development") {
    console.error(error.stack);
  }
  process.exit(1);
});
