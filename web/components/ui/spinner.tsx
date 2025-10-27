import { Loader2Icon, LoaderIcon } from "lucide-react";

import { cn } from "@/lib/utils";

interface SpinnerProps extends React.ComponentProps<"svg"> {
  variant?: "default" | "loader";
}

function Spinner({ className, variant = "default", ...props }: SpinnerProps) {
  const Icon = variant === "loader" ? LoaderIcon : Loader2Icon;
  const { role, ...rest } = props;

  return (
    <Icon
      role="status"
      aria-label="Loading"
      className={cn("size-4 animate-spin", className)}
      {...rest}
    />
  );
}

export { Spinner };
export type { SpinnerProps };
export default Spinner;
