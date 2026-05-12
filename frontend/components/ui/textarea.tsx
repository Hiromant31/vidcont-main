import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/utils/cn"

const textareaVariants = cva(
  "flex min-h-[3.5rem] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 resize-none",
  {
    variants: {
      size: {
        default: "min-h-[3.5rem] py-2",
        sm: "min-h-[3rem] rounded-md px-3",
        lg: "min-h-[4rem] rounded-md px-4",
      },
    },
    defaultVariants: {
      size: "default",
    },
  }
)
export interface TextareaProps extends Omit<React.TextareaHTMLAttributes<HTMLTextAreaElement>, 'size'> {
  size?: VariantProps<typeof textareaVariants>['size']
}

/**
 * Textarea component
 */
export const Textarea = React.forwardRef<
  HTMLTextAreaElement,
  TextareaProps
>(({ className, size, ...props }, ref) => (
  <textarea
    className={cn(textareaVariants({ size }), className)}
    ref={ref}
    {...props}
  />
))
Textarea.displayName = "Textarea"
