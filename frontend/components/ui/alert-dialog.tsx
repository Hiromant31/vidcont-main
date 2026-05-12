import * as React from "react"
import { cn } from "@/utils/cn"

interface AlertDialogProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode
}

const AlertDialog = React.forwardRef<
  HTMLDivElement,
  AlertDialogProps
>(({ className, children }, ref) => (
  <div
    className={cn(
      "fixed inset-0 z-50 flex min-h-screen items-center justify-center",
      className
    )}
    ref={ref}
  >
    <div className={cn(
      "relative w-full max-w-lg max-h-screen",
      className
    )}>
      <div className="relative bg-white rounded-lg shadow dark:bg-gray-900">
        {/* Backdrop */}
        <div className="absolute inset-0 bg-black/50 dark:bg-white/50" />
        <div className="p-6">{children}</div>
      </div>
    </div>
  </div>
))
AlertDialog.displayName = "AlertDialog"

interface AlertDialogTriggerProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode
}

const AlertDialogTrigger = React.forwardRef<
  HTMLButtonElement,
  AlertDialogTriggerProps
>(({ className, children, ...props }, ref) => (
  <button
    className={cn(
      "inline-flex items-center justify-center rounded-md border border-transparent bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50",
      className
    )}
    ref={ref}
    {...props}
  >
    {children}
  </button>
))
AlertDialogTrigger.displayName = "AlertDialogTrigger"

interface AlertDialogContentProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode
  className?: string
}

const AlertDialogContent = React.forwardRef<
  HTMLDivElement,
  AlertDialogContentProps
>(({ className, children, ...props }, ref) => (
  <div
    className={cn(
      "relative p-6 space-y-6 bg-white rounded-lg shadow dark:bg-gray-900",
      className
    )}
    ref={ref}
    {...props}
  >
    <div className="space-y-6">{children}</div>
  </div>
))
AlertDialogContent.displayName = "AlertDialogContent"

interface AlertDialogHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  className?: string
}

const AlertDialogHeader = React.forwardRef<
  HTMLDivElement,
  AlertDialogHeaderProps
>(({ className, ...props }, ref) => (
  <div
    className={cn("space-y-2", className)}
    ref={ref}
    {...props}
  />
))
AlertDialogHeader.displayName = "AlertDialogHeader"

interface AlertDialogTitleProps extends React.HTMLAttributes<HTMLHeadingElement> {
  className?: string
}

const AlertDialogTitle = React.forwardRef<
  HTMLHeadingElement,
  AlertDialogTitleProps
>(({ className, ...props }, ref) => (
  <h2
    className={cn(
      "text-xl font-semibold leading-tight tracking-tight text-gray-900 dark:text-gray-100",
      className
    )}
    ref={ref}
    {...props}
  />
))
AlertDialogTitle.displayName = "AlertDialogTitle"

interface AlertDialogDescriptionProps extends React.HTMLAttributes<HTMLParagraphElement> {
  className?: string
}

const AlertDialogDescription = React.forwardRef<
  HTMLParagraphElement,
  AlertDialogDescriptionProps
>(({ className, ...props }, ref) => (
  <p
    className={cn(
      "text-sm text-gray-500 dark:text-gray-400",
      className
    )}
    ref={ref}
    {...props}
  />
))
AlertDialogDescription.displayName = "AlertDialogDescription"

interface AlertDialogFooterProps extends React.HTMLAttributes<HTMLDivElement> {
  className?: string
}

const AlertDialogFooter = React.forwardRef<
  HTMLDivElement,
  AlertDialogFooterProps
>(({ className, ...props }, ref) => (
  <div
    className={cn(
      "flex items-center justify-end space-x-4 pt-6",
      className
    )}
    ref={ref}
    {...props}
  />
))
AlertDialogFooter.displayName = "AlertDialogFooter"

interface AlertDialogActionProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  className?: string
}

const AlertDialogAction = React.forwardRef<
  HTMLButtonElement,
  AlertDialogActionProps
>(({ className, children, ...props }, ref) => (
  <button
    className={cn(
      "inline-flex items-center justify-center rounded-md border border-transparent bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50",
      className
    )}
    ref={ref}
    {...props}
  >
    {children}
  </button>
))
AlertDialogAction.displayName = "AlertDialogAction"

interface AlertDialogCancelProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  className?: string
}

const AlertDialogCancel = React.forwardRef<
  HTMLButtonElement,
  AlertDialogCancelProps
>(({ className, children, ...props }, ref) => (
  <button
    className={cn(
      "inline-flex items-center justify-center rounded-md border border-input bg-background px-4 py-2 text-sm font-medium text-sm text-gray-700 hover:bg-gray-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50",
      className
    )}
    ref={ref}
    {...props}
  >
    {children}
  </button>
))
AlertDialogCancel.displayName = "AlertDialogCancel"

export { 
  AlertDialog, 
  AlertDialogTrigger, 
  AlertDialogContent, 
  AlertDialogHeader, 
  AlertDialogTitle, 
  AlertDialogDescription, 
  AlertDialogFooter, 
  AlertDialogAction, 
  AlertDialogCancel 
};
