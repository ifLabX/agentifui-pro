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
 * Supports: --lang zh-Hans ja-JP --file common auth -v --verbose --fix-extra
 */
function parseArguments() {
  const args = process.argv.slice(2);
  const parsed = {
    lang: [],
    file: [],
    help: false,
    verbose: false,
    fixExtra: false,
    ciMode: false,
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
      } else if (currentFlag === "fix-extra") {
        parsed.fixExtra = true;
      } else if (currentFlag === "ci-mode") {
        parsed.ciMode = true;
      } else if (!["lang", "file"].includes(currentFlag)) {
        console.error(
          `${colors.red}${symbols.error} Unknown flag: ${arg}${colors.reset}`
        );
        process.exit(1);
      }
    } else if (arg.startsWith("-")) {
      // Handle short flags like -v
      const shortFlag = arg.substring(1);
      if (shortFlag === "v") {
        parsed.verbose = true;
      } else if (shortFlag === "h") {
        parsed.help = true;
      } else {
        console.error(
          `${colors.red}${symbols.error} Unknown short flag: ${arg}${colors.reset}`
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
  --fix-extra             Automatically remove extra keys from target languages
  --ci-mode               CI-friendly mode (no exit on missing keys)
  --verbose, -v           Show detailed output
  --help, -h              Show this help message

${colors.white}EXAMPLES:${colors.reset}
  pnpm i18n:check                           # Check all languages and files
  pnpm i18n:check --lang zh-Hans ja-JP      # Check only Chinese and Japanese
  pnpm i18n:check --file common auth        # Check only common and auth namespaces
  pnpm i18n:check --fix-extra               # Remove extra keys from all languages
  pnpm i18n:check --lang zh-Hans --fix-extra --verbose

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
 * Remove a nested key from JSON object
 * @param {Object} obj - JSON object to modify
 * @param {string} keyPath - Dot-notation key path (e.g., "actions.delete")
 */
function removeNestedKey(obj, keyPath) {
  const keys = keyPath.split(".");
  const lastKey = keys.pop();

  // Navigate to the parent object
  let current = obj;
  for (let i = 0; i < keys.length; i++) {
    if (!(keys[i] in current) || typeof current[keys[i]] !== "object") {
      // Key path doesn't exist, nothing to remove
      return false;
    }
    current = current[keys[i]];
  }

  // Remove the final key
  if (lastKey in current) {
    delete current[lastKey];

    // Clean up empty parent objects recursively
    cleanupEmptyParents(obj, keys);
    return true;
  }

  return false;
}

/**
 * Recursively remove empty parent objects
 * @param {Object} obj - Root JSON object
 * @param {string[]} parentKeys - Array of parent keys to check
 */
function cleanupEmptyParents(obj, parentKeys) {
  if (parentKeys.length === 0) return;

  // Navigate to the parent object
  let current = obj;
  for (let i = 0; i < parentKeys.length - 1; i++) {
    current = current[parentKeys[i]];
  }

  const parentKey = parentKeys[parentKeys.length - 1];
  const parentObj = current[parentKey];

  // Check if parent object is empty
  if (typeof parentObj === "object" && Object.keys(parentObj).length === 0) {
    delete current[parentKey];

    // Recursively check grandparents
    cleanupEmptyParents(obj, parentKeys.slice(0, -1));
  }
}

/**
 * Fix extra keys in target translation files
 * @param {Object} sourceData - Source translation data
 * @param {Object} targetData - Target translation data to fix
 * @param {string[]} extraKeys - Array of extra keys to remove
 * @returns {Object} Fixed translation data
 */
function fixExtraKeys(sourceData, targetData, extraKeys) {
  // Deep clone to avoid modifying original
  const fixedData = JSON.parse(JSON.stringify(targetData));

  let removedCount = 0;
  const removedKeys = [];

  extraKeys.forEach(keyPath => {
    const success = removeNestedKey(fixedData, keyPath);
    if (success) {
      removedCount++;
      removedKeys.push(keyPath);
    }
  });

  return {
    data: fixedData,
    removedCount,
    removedKeys,
  };
}

/**
 * Write fixed translation file with proper formatting
 * @param {string} filePath - Path to the file
 * @param {Object} data - JSON data to write
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
  let fixedFiles = [];

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

      // Auto-fix extra keys if requested
      let fixResult = null;
      if (args.fixExtra && comparison.extra.length > 0) {
        fixResult = fixExtraKeys(
          sourceFile.data,
          targetFile.data,
          comparison.extra
        );

        // Write the fixed file
        const success = writeTranslationFile(
          targetFile.filePath,
          fixResult.data
        );
        if (success) {
          fixedFiles.push({
            locale,
            namespace,
            filePath: targetFile.filePath,
            removedCount: fixResult.removedCount,
            removedKeys: fixResult.removedKeys,
          });

          // Update comparison result to reflect the fix
          comparison.extra = [];
          comparison.extraCount = 0;
          comparison.isComplete = comparison.missing.length === 0;
        } else {
          hasErrors = true;
        }
      }

      results.push({
        locale,
        namespace,
        ...comparison,
        isComplete: comparison.isComplete,
        fixed: fixResult !== null,
        removedCount: fixResult?.removedCount || 0,
      });

      if (!comparison.isComplete) {
        hasIssues = true;
      }
    }
  }

  // Display results
  displaySummaryTable(results, config);

  // Show detailed issues only in verbose mode, or when there are errors/issues and not in fix mode
  if (args.verbose || (!args.fixExtra && (hasErrors || hasIssues))) {
    results.forEach(result => displayDetailedIssues(result));
  }

  // Display fix summary if fixes were applied
  if (args.fixExtra && fixedFiles.length > 0) {
    console.log(
      `\n${colors.cyan}${colors.bright}🔧 Fix Summary${colors.reset}`
    );
    console.log(
      `${colors.green}${symbols.success} Fixed ${fixedFiles.length} translation file(s):${colors.reset}`
    );

    fixedFiles.forEach(fix => {
      console.log(
        `  ${colors.white}${fix.locale}/${fix.namespace}: ${colors.green}removed ${fix.removedCount} extra key(s)${colors.reset}`
      );
      if (args.verbose) {
        fix.removedKeys.forEach(key => {
          console.log(`    ${colors.yellow}• ${key}${colors.reset}`);
        });
      }
    });
  }

  // Final status
  console.log(
    `\n${colors.white}${symbols.info} Validation complete${colors.reset}`
  );

  if (hasErrors) {
    console.log(
      `${colors.red}${symbols.error} Found critical errors - files missing or corrupted${colors.reset}`
    );
    process.exit(args.ciMode ? 0 : 1);
  } else if (hasIssues) {
    console.log(
      `${colors.yellow}${symbols.warning} Found translation inconsistencies${colors.reset}`
    );
    process.exit(args.ciMode ? 0 : 1);
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
