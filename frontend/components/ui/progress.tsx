import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/utils/cn"

const progressVariants = cva(
  "relative w-full h-2.5 overflow-hidden rounded-md bg-accent",
  {
    variants: {},
    defaultVariants: {},
  }
)
export interface ProgressProps extends React.HTMLAttributes<HTMLDivElement>, VariantProps<typeof progressVariants> {
  value: number
}

/**
 * Progress component
 */
export const Progress = React.forwardRef<
  HTMLDivElement,
  ProgressProps
>(({ className, value, ...props }, ref) => (
  <div
    className={cn(progressVariants(), className)}
    ref={ref}
    {...props}
  >
    <div
      className="flex h-2.5 w-0 overflow-hidden rounded-md bg-primary transition-width duration-500"
      style={{ width: `${value}%` }}
    />
  </div>
))
Progress.displayName = "Progress"
