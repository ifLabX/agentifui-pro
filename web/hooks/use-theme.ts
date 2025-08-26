import { useTheme as useBaseTheme } from "next-themes";

import { Theme } from "@/types/app";

const useTheme = () => {
  const { theme, resolvedTheme, ...rest } = useBaseTheme();
  return {
    theme: theme === Theme.system ? (resolvedTheme as Theme) : (theme as Theme),
    ...rest,
  };
};

export default useTheme;
