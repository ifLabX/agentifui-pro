import { useTheme as useBaseTheme } from "next-themes";

import { Theme } from "@/types/app";

function isValidTheme(value: unknown): value is Theme {
  return Object.values(Theme).includes(value as Theme);
}

const useTheme = () => {
  const { theme, resolvedTheme, ...rest } = useBaseTheme();
  let selectedTheme: Theme | undefined;
  if (theme === Theme.system) {
    selectedTheme = isValidTheme(resolvedTheme) ? resolvedTheme : undefined;
  } else {
    selectedTheme = isValidTheme(theme) ? theme : undefined;
  }
  return {
    theme: selectedTheme,
    ...rest,
  };
};

export default useTheme;
