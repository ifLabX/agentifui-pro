import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";
import oxlint from "eslint-plugin-oxlint";
import reactCompiler from "eslint-plugin-react-compiler";
import storybook from "eslint-plugin-storybook";
import stylistic from "@stylistic/eslint-plugin";
import { defineConfig, globalIgnores } from "eslint/config";

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,
  reactCompiler.configs.recommended,
  {
    plugins: {
      "@stylistic": stylistic,
    },
    settings: {
      react: {
        version: "detect",
      },
    },
    rules: {
      "@stylistic/arrow-parens": ["error", "as-needed"],
      "@stylistic/array-bracket-spacing": ["error", "never"],
      "@stylistic/block-spacing": ["error", "always"],
      "@stylistic/comma-dangle": [
        "error",
        {
          arrays: "always-multiline",
          objects: "always-multiline",
          imports: "always-multiline",
          exports: "always-multiline",
          functions: "never",
        },
      ],
      "@stylistic/comma-spacing": ["error", { before: false, after: true }],
      "@stylistic/indent": ["error", 2, { SwitchCase: 1 }],
      "@stylistic/key-spacing": ["error", { beforeColon: false, afterColon: true }],
      "@stylistic/no-extra-semi": "error",
      "@stylistic/no-multiple-empty-lines": ["error", { max: 1, maxEOF: 0 }],
      "@stylistic/object-curly-spacing": ["error", "always"],
      "@stylistic/quotes": ["error", "double", { avoidEscape: true }],
      "@stylistic/semi": ["error", "always"],
      "@stylistic/space-before-function-paren": ["error", { anonymous: "never", named: "never", asyncArrow: "always" }],
      "react/jsx-key": "error",
      "react/jsx-no-duplicate-props": "error",
      "react/jsx-no-undef": "error",
      "react/no-children-prop": "error",
      "react/no-danger-with-children": "error",
      "react/no-deprecated": "error",
      "react/no-direct-mutation-state": "error",
      "react/no-find-dom-node": "error",
      "react/no-render-return-value": "error",
      "react/no-string-refs": "error",
      "react/no-unescaped-entities": "error",
      "react/no-unknown-property": "error",
      "react/no-unsafe": "error",
      "react/require-render-return": "error",
      "react/void-dom-elements-no-children": "error",
      "react-hooks/rules-of-hooks": "error",
      "react-hooks/exhaustive-deps": "warn",
    },
  },
  globalIgnores([
    "node_modules/**",
    ".next/**",
    "out/**",
    "build/**",
    "storybook-static/**",
    "coverage/**",
    "next-env.d.ts",
    "*.config.*",
  ]),
  {
    rules: {
      "no-unused-vars": "off",
      "@typescript-eslint/no-unused-vars": [
        "error",
        {
          argsIgnorePattern: "^_",
          varsIgnorePattern: "^_",
        },
      ],
      "no-console":
        process.env.NODE_ENV === "production"
          ? ["error", { allow: ["warn", "error", "info"] }]
          : "off",
    },
  },
  {
    files: ["**/*.test.{ts,tsx}", "**/*.spec.{ts,tsx}"],
    rules: {
      "@typescript-eslint/no-unused-vars": "warn",
      "no-console": "off",
    },
  },
  ...storybook.configs["flat/recommended"],
  ...oxlint.buildFromOxlintConfigFile("./.oxlintrc.json"),
]);

export default eslintConfig;
