#!/usr/bin/env node
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ANSI color codes for beautiful output
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
  bgRed: "\x1b[41m",
  bgGreen: "\x1b[42m",
  bgYellow: "\x1b[43m",
};

// Unicode symbols for better visual feedback
const symbols = {
  success: "✅",
  error: "❌",
  warning: "⚠️",
  info: "ℹ️",
  missing: "🔍",
  extra: "➕",
  check: "🔍",
  summary: "📊",
};

/**
 * Parse command line arguments
 * Supports: --lang zh-Hans ja-JP --file common auth
 */
function parseArguments() {
  const args = process.argv.slice(2);
  const parsed = {
    lang: [],
    file: [],
    help: false,
    verbose: false,
  };

  let currentFlag = null;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg.startsWith("--")) {
      currentFlag = arg.substring(2);

      if (currentFlag === "help" || currentFlag === "h") {
        parsed.help = true;
      } else if (currentFlag === "verbose" || currentFlag === "v") {
        parsed.verbose = true;
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
 * Load and parse i18n configuration dynamically
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
 * Recursively extract all translation keys from a JSON object
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
 * Load translation file and extract keys
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
      return { exists: false, keys: [], error: `File not found: ${filePath}` };
    }

    const content = fs.readFileSync(filePath, "utf-8");
    const data = JSON.parse(content);
    const keys = extractKeys(data);

    return { exists: true, keys, data, filePath };
  } catch (error) {
    return { exists: false, keys: [], error: error.message };
  }
}

/**
 * Compare keys between source and target locales
 */
function compareKeys(sourceKeys, targetKeys) {
  const sourceSet = new Set(sourceKeys);
  const targetSet = new Set(targetKeys);

  const missing = sourceKeys.filter(key => !targetSet.has(key));
  const extra = targetKeys.filter(key => !sourceSet.has(key));

  return {
    missing,
    extra,
    missingCount: missing.length,
    extraCount: extra.length,
    totalSource: sourceKeys.length,
    totalTarget: targetKeys.length,
    isComplete: missing.length === 0 && extra.length === 0,
  };
}

/**
 * Display help message
 */
function showHelp() {
  console.log(`
${colors.cyan}${colors.bright}i18n Translation Checker${colors.reset}

${colors.white}USAGE:${colors.reset}
  pnpm i18n:check [OPTIONS]

${colors.white}OPTIONS:${colors.reset}
  --lang <locales...>     Check specific languages (e.g., --lang zh-Hans ja-JP)
  --file <namespaces...>  Check specific namespaces (e.g., --file common auth)
  --verbose, -v           Show detailed output
  --help, -h              Show this help message

${colors.white}EXAMPLES:${colors.reset}
  pnpm i18n:check                           # Check all languages and files
  pnpm i18n:check --lang zh-Hans ja-JP      # Check only Chinese and Japanese
  pnpm i18n:check --file common auth        # Check only common and auth namespaces
  pnpm i18n:check --lang zh-Hans --file common --verbose

${colors.white}OUTPUT:${colors.reset}
  ${symbols.success} Complete translations (no missing or extra keys)
  ${symbols.warning} Incomplete translations (missing or extra keys)
  ${symbols.error} File errors (missing files, JSON parse errors)
`);
}

/**
 * Display beautiful summary table
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
    "Extra",
    "Status",
  ].join(" │ ");

  console.log(`${colors.white}${header}${colors.reset}`);
  console.log("─".repeat(header.length));

  // Rows
  results.forEach(result => {
    const status = result.isComplete
      ? `${colors.green}${symbols.success} Complete${colors.reset}`
      : result.error
        ? `${colors.red}${symbols.error} Error${colors.reset}`
        : `${colors.yellow}${symbols.warning} Issues${colors.reset}`;

    const row = [
      result.locale.padEnd(maxLocaleWidth),
      result.namespace.padEnd(maxNamespaceWidth),
      result.missingCount?.toString().padStart(7) || "N/A".padStart(7),
      result.extraCount?.toString().padStart(5) || "N/A".padStart(5),
      status,
    ].join(" │ ");

    console.log(row);
  });
}

/**
 * Display detailed issues for a specific locale/namespace
 */
function displayDetailedIssues(result) {
  if (result.error) {
    console.log(
      `\n${colors.red}${symbols.error} ${result.locale}/${result.namespace}: ${result.error}${colors.reset}`
    );
    return;
  }

  if (result.isComplete) {
    console.log(
      `\n${colors.green}${symbols.success} ${result.locale}/${result.namespace}: Complete (${result.totalTarget} keys)${colors.reset}`
    );
    return;
  }

  console.log(
    `\n${colors.yellow}${symbols.warning} ${result.locale}/${result.namespace}:${colors.reset}`
  );

  if (result.missing?.length > 0) {
    console.log(
      `  ${colors.red}${symbols.missing} Missing keys (${result.missing.length}):${colors.reset}`
    );
    result.missing.forEach(key => {
      console.log(`    ${colors.red}• ${key}${colors.reset}`);
    });
  }

  if (result.extra?.length > 0) {
    console.log(
      `  ${colors.yellow}${symbols.extra} Extra keys (${result.extra.length}):${colors.reset}`
    );
    result.extra.forEach(key => {
      console.log(`    ${colors.yellow}• ${key}${colors.reset}`);
    });
  }
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
    `${colors.cyan}${colors.bright}${symbols.check} i18n Translation Checker${colors.reset}`
  );
  console.log(`${colors.white}Starting validation...${colors.reset}\n`);

  // Load configuration
  const config = await loadI18nConfig();

  // Determine locales and namespaces to check
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

  const results = [];
  let hasErrors = false;
  let hasIssues = false;

  // Check each combination of locale and namespace
  for (const namespace of targetNamespaces) {
    // Load source file
    const sourceFile = loadTranslationFile(config.defaultLocale, namespace);

    if (!sourceFile.exists) {
      console.error(
        `${colors.red}${symbols.error} Source file missing: ${config.defaultLocale}/${namespace}${colors.reset}`
      );
      hasErrors = true;
      continue;
    }

    for (const locale of targetLocales) {
      const targetFile = loadTranslationFile(locale, namespace);

      if (!targetFile.exists) {
        results.push({
          locale,
          namespace,
          error: targetFile.error,
          isComplete: false,
        });
        hasErrors = true;
        continue;
      }

      const comparison = compareKeys(sourceFile.keys, targetFile.keys);

      results.push({
        locale,
        namespace,
        ...comparison,
        isComplete: comparison.isComplete,
      });

      if (!comparison.isComplete) {
        hasIssues = true;
      }
    }
  }

  // Display results
  displaySummaryTable(results, config);

  if (args.verbose || hasErrors || hasIssues) {
    results.forEach(result => displayDetailedIssues(result));
  }

  // Final status
  console.log(
    `\n${colors.white}${symbols.info} Validation complete${colors.reset}`
  );

  if (hasErrors) {
    console.log(
      `${colors.red}${symbols.error} Found critical errors - files missing or corrupted${colors.reset}`
    );
    process.exit(1);
  } else if (hasIssues) {
    console.log(
      `${colors.yellow}${symbols.warning} Found translation inconsistencies${colors.reset}`
    );
    process.exit(1);
  } else {
    console.log(
      `${colors.green}${symbols.success} All translations are complete and consistent${colors.reset}`
    );
    process.exit(0);
  }
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
