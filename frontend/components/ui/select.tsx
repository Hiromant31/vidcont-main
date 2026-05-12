import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/utils/cn"

const selectVariants = cva(
  "inline-flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
  {
    variants: {
      size: {
        default: "h-10 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-4",
      },
    },
    defaultVariants: {
      size: "default",
    },
  }
)
export interface SelectProps extends React.ComponentPropsWithoutRef<"div">, VariantProps<typeof selectVariants> {
  value: any
  onValueChange: (value: any) => void
  disabled?: boolean
}

const SelectContext = React.createContext<SelectProps | null>(null)

export const Select = ({
  className,
  children,
  value,
  onValueChange,
  disabled,
  ...props
}: SelectProps) => {
  return (
    <SelectContext.Provider value={{ value, onValueChange, disabled }}>
      <div className={cn(selectVariants(), className)} {...props}>
        {children}
      </div>
    </SelectContext.Provider>
  );
}
Select.displayName = "Select"

export const SelectTrigger = ({
  className,
  children,
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement>) => {
  const context = React.useContext(SelectContext);
  return (
    <button
      className={cn(
        "flex h-10 w-full items-center justify-between rounded-md border border-bg bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
        className
      )}
      {...props}
      disabled ={context?.disabled || context?.value === undefined}
    >
      {children}
      <Slot className="ml-2 h-4 w-4 shrink-0 opacity-50" />
    </button>
  );
}
SelectTrigger.displayName = "SelectTrigger"

export const SelectValue = ({
  className,
  children,
  placeholder,
  ...props
}: React.HTMLAttributes<HTMLSpanElement> & { placeholder?: string }) => {
  const context = React.useContext(SelectContext);
  return (
    <span
      className={cn("truncate", className)}
      {...props}
    >
      {context?.value ?? children ?? placeholder}
    </span>
  );
}
SelectValue.displayName = "SelectValue"

export const SelectContent = ({
  className,
  children,
  ...props
}: React.ComponentPropsWithoutRef<"div">) => {
  return (
    <div
      className={cn(
        "relative z-50 mt-2 max-h-96 w-full overflow-hidden rounded-md border bg-popover text-popover-foreground shadow-lg",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}
SelectContent.displayName = "SelectContent"

export const SelectItem = ({
  className,
  children,
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement>) => {
  const context = React.useContext(SelectContext);
  const handleClick = () => {
    if (context?.onValueChange && !(context?.disabled)) {
      context.onValueChange(children);
    }
  };
  return (
    <button
      className={cn(
        "flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none focus:bg-accent focus:text-accent-foreground disabled:pointer-events-none disabled:opacity-50",
        className
      )}
      onClick={handleClick}
      disabled ={context?.disabled}
      {...props}
    >
      {children}
    </button>
  );
}
SelectItem.displayName = "SelectItem"
