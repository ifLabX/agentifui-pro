"use client";

import { cn } from "@/lib/utils";

interface TypingDotsProps {
  className?: string;
  size?: "sm" | "md" | "lg";
}

const sizeClasses = {
  sm: {
    container: "space-x-0.5",
    dot: "h-1 w-1",
  },
  md: {
    container: "space-x-1",
    dot: "h-1.5 w-1.5",
  },
  lg: {
    container: "space-x-1.5",
    dot: "h-2 w-2",
  },
};

export function TypingDots({ className, size = "md" }: TypingDotsProps) {
  const currentSizeClasses = sizeClasses[size];

  return (
    <div
      className={cn(
        "flex items-center",
        currentSizeClasses.container,
        className
      )}
    >
      {[0, 1, 2].map(i => (
        <div
          key={i}
          className={cn(
            "rounded-full",
            currentSizeClasses.dot,
            "bg-muted-foreground",
            "animate-pulse"
          )}
          style={{
            animationDelay: `${i * 200}ms`,
          }}
        />
      ))}
    </div>
  );
}
