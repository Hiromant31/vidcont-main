import { cn } from "@/utils/cn";

interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {
  className?: string;
  height?: number | string;
  width?: number | string;
  radius?: string;
}

export function Skeleton({
  className,
  height = 16,
  width = "100%",
  radius = "sm",
  ...props
}: SkeletonProps) {
  const radii: Record<string, string> = {
    none: "0",
    sm: "0.125rem",
    default: "0.25rem",
    lg: "0.5rem",
    full: "9999px",
  };

  return (
    <div
      className={cn(
        "animate-pulse",
        "bg-gray-500",
        "rounded-" + radii[radius],
        className
      )}
      style={{
        height: typeof height === "number" ? `${height}px` : height,
        width: typeof width === "number" ? `${width}px` : width,
      }}
      {...props}
    />
  );
}
