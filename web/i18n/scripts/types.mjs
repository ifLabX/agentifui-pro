#!/usr/bin/env node
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ANSI color codes for beautiful output - consistent with other scripts
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

// Unicode symbols for better visual feedback
const symbols = {
  success: "✅",
  error: "❌",
  warning: "⚠️",
  info: "ℹ️",
  check: "🔍",
  generate: "🔄",
  types: "📝",
  summary: "📊",
};

/**
 * Parse command line arguments
 * Supports: --check --generate --help --verbose --ci-mode
 */
function parseArguments() {
  const args = process.argv.slice(2);
  const parsed = {
    help: false,
    check: false,
    generate: false,
    verbose: false,
    ciMode: false,
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg.startsWith("--")) {
      const flag = arg.substring(2);

      if (flag === "help" || flag === "h") {
        parsed.help = true;
      } else if (flag === "check") {
        parsed.check = true;
      } else if (flag === "generate") {
        parsed.generate = true;
      } else if (flag === "verbose" || flag === "v") {
        parsed.verbose = true;
      } else if (flag === "ci-mode") {
        parsed.ciMode = true;
      } else {
        console.error(
          `${colors.red}${symbols.error} Unknown flag: ${arg}${colors.reset}`
        );
        process.exit(1);
      }
    } else if (arg.startsWith("-")) {
      // Handle short flags
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
      console.error(
        `${colors.red}${symbols.error} Unexpected argument: ${arg}${colors.reset}`
      );
      process.exit(1);
    }
  }

  return parsed;
}

/**
 * Display help information
 */
function showHelp() {
  console.log(
    `${colors.cyan}${symbols.types} I18n TypeScript Types Manager${colors.reset}`
  );
  console.log("");
  console.log(
    "Validates and generates TypeScript type definitions for i18n namespaces."
  );
  console.log("");
  console.log(`${colors.yellow}Usage:${colors.reset}`);
  console.log("  node i18n/scripts/types.mjs [options]");
  console.log("");
  console.log(`${colors.yellow}Options:${colors.reset}`);
  console.log("  --check         Check if types are synchronized with config");
  console.log("  --generate      Generate types based on current config");
  console.log("  --verbose, -v   Show detailed output");
  console.log("  --ci-mode       CI-friendly output mode");
  console.log("  --help, -h      Show this help");
  console.log("");
  console.log(`${colors.yellow}Examples:${colors.reset}`);
  console.log("  pnpm i18n:types --check      # Validate type synchronization");
  console.log("  pnpm i18n:types --generate   # Generate types from config");
  console.log("  pnpm i18n:types --check --verbose  # Detailed validation");
}

/**
 * Load and parse i18n configuration - same pattern as check.mjs
 */
async function loadI18nConfig() {
  try {
    const configPath = path.join(__dirname, "../config.ts");
    const configContent = fs.readFileSync(configPath, "utf-8");

    // Extract namespaces array using same regex pattern as generate.mjs
    const namespacesMatch = configContent.match(
      /export const namespaces = \[(.*?)\]/s
    );

    if (!namespacesMatch) {
      throw new Error("Could not parse namespaces from i18n configuration");
    }

    const namespaces =
      namespacesMatch[1].match(/"([^"]+)"/g)?.map(s => s.slice(1, -1)) || [];

    return { namespaces };
  } catch (error) {
    console.error(
      `${colors.red}${symbols.error} Failed to load i18n configuration: ${error.message}${colors.reset}`
    );
    process.exit(1);
  }
}

/**
 * Convert kebab-case to PascalCase for TypeScript type names
 * Same logic as generate.mjs line 217-220
 */
function toPascalCase(kebabCase) {
  return kebabCase
    .split("-")
    .map(part => part.charAt(0).toUpperCase() + part.slice(1))
    .join("");
}

/**
 * Parse existing type definitions from i18n.d.ts
 */
function parseExistingTypes(typesContent) {
  const typeImports = [];
  const messageProperties = [];

  // Extract type imports
  const typeImportRegex =
    /type (\w+)Messages = typeof import\(['"]([^'"]+)['"]\);/g;
  let match;
  while ((match = typeImportRegex.exec(typesContent)) !== null) {
    const typeName = match[1];
    const importPath = match[2];
    // Extract namespace from import path: '../messages/en-US/namespace.json' -> 'namespace'
    const namespaceMatch = importPath.match(/\/en-US\/([^.]+)\.json$/);
    if (namespaceMatch) {
      typeImports.push({
        typeName,
        namespace: namespaceMatch[1],
        importPath,
      });
    }
  }

  // Extract Messages interface properties
  const messagesInterfaceMatch = typesContent.match(
    /export type Messages = \{([\s\S]*?)\};/
  );
  if (messagesInterfaceMatch) {
    const interfaceContent = messagesInterfaceMatch[1];
    const propertyRegex = /["']([^"']+)["']:\s*(\w+Messages);/g;
    while ((match = propertyRegex.exec(interfaceContent)) !== null) {
      messageProperties.push({
        namespace: match[1],
        typeName: match[2],
      });
    }
  }

  return { typeImports, messageProperties };
}

/**
 * Check if types are synchronized with config
 */
async function checkTypes(verbose = false, ciMode = false) {
  if (!ciMode && verbose) {
    console.log(
      `${colors.blue}${symbols.check} Checking type synchronization...${colors.reset}`
    );
  }

  const { namespaces } = await loadI18nConfig();
  const typesPath = path.join(__dirname, "../../types/i18n.d.ts");

  if (!fs.existsSync(typesPath)) {
    console.error(
      `${colors.red}${symbols.error} Types file not found: ${typesPath}${colors.reset}`
    );
    return false;
  }

  const typesContent = fs.readFileSync(typesPath, "utf-8");
  const { typeImports, messageProperties } = parseExistingTypes(typesContent);

  // Check missing namespaces
  const missingNamespaces = [];
  const extraNamespaces = [];

  // Find missing namespaces (in config but not in types)
  for (const namespace of namespaces) {
    const hasTypeImport = typeImports.some(t => t.namespace === namespace);
    const hasMessageProperty = messageProperties.some(
      p => p.namespace === namespace
    );

    if (!hasTypeImport || !hasMessageProperty) {
      missingNamespaces.push(namespace);
    }
  }

  // Find extra namespaces (in types but not in config)
  for (const typeImport of typeImports) {
    if (!namespaces.includes(typeImport.namespace)) {
      extraNamespaces.push(typeImport.namespace);
    }
  }

  const isSync = missingNamespaces.length === 0 && extraNamespaces.length === 0;

  if (!ciMode) {
    if (isSync) {
      console.log(
        `${colors.green}${symbols.success} Types are synchronized with config${colors.reset}`
      );
      if (verbose) {
        console.log(
          `   ${symbols.info} Found ${namespaces.length} namespace(s): ${namespaces.join(", ")}`
        );
      }
    } else {
      console.log(
        `${colors.red}${symbols.error} Types are not synchronized with config${colors.reset}`
      );

      if (missingNamespaces.length > 0) {
        console.log(
          `   ${colors.yellow}${symbols.warning} Missing namespaces: ${missingNamespaces.join(", ")}${colors.reset}`
        );
      }

      if (extraNamespaces.length > 0) {
        console.log(
          `   ${colors.yellow}${symbols.warning} Extra namespaces: ${extraNamespaces.join(", ")}${colors.reset}`
        );
      }

      if (verbose) {
        console.log(
          `   ${symbols.info} Run with --generate to fix automatically`
        );
      }
    }
  }

  return isSync;
}

/**
 * Generate complete type definitions based on config
 * Using exact same patterns as generate.mjs
 */
async function generateTypes(verbose = false, ciMode = false) {
  if (!ciMode && verbose) {
    console.log(
      `${colors.blue}${symbols.generate} Generating type definitions...${colors.reset}`
    );
  }

  const { namespaces } = await loadI18nConfig();
  const typesPath = path.join(__dirname, "../../types/i18n.d.ts");

  // Generate type imports
  const typeImports = namespaces
    .map(namespace => {
      const capitalizedNamespace = toPascalCase(namespace);
      return `type ${capitalizedNamespace}Messages = typeof import("../messages/en-US/${namespace}.json");`;
    })
    .join("\n");

  // Generate Messages interface properties with quoted keys (same as generate.mjs line 259)
  const messageProperties = namespaces
    .map(namespace => {
      const capitalizedNamespace = toPascalCase(namespace);
      return `  "${namespace}": ${capitalizedNamespace}Messages;`;
    })
    .join("\n");

  // Generate complete type definition file
  const typesContent = `import type { Locale } from "@/i18n/config";

${typeImports}

export type Messages = {
${messageProperties}
};

export type { Locale };
`;

  fs.writeFileSync(typesPath, typesContent);

  if (!ciMode) {
    console.log(
      `${colors.green}${symbols.success} Generated types for ${namespaces.length} namespace(s)${colors.reset}`
    );
    if (verbose) {
      console.log(`   ${symbols.info} Updated: types/i18n.d.ts`);
      console.log(`   ${symbols.info} Namespaces: ${namespaces.join(", ")}`);
    }
  }

  return true;
}

// Main execution
async function main() {
  const args = parseArguments();

  if (args.help) {
    showHelp();
    return;
  }

  // Default to check if no specific action provided
  if (!args.check && !args.generate) {
    args.check = true;
  }

  let exitCode = 0;

  try {
    if (args.check) {
      const isSync = await checkTypes(args.verbose, args.ciMode);
      if (!isSync) {
        exitCode = 1;
      }
    }

    if (args.generate) {
      await generateTypes(args.verbose, args.ciMode);
    }
  } catch (error) {
    console.error(
      `${colors.red}${symbols.error} Operation failed: ${error.message}${colors.reset}`
    );
    exitCode = 1;
  }

  process.exit(exitCode);
}

main();
