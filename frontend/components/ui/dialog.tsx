import * as React from "react"
import { cn } from "@/utils/cn"

interface DialogProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode
  className?: string
}

const Dialog = React.forwardRef<
  HTMLDivElement,
  DialogProps
>(({ className, children, ...props }, ref) => (
  <div
    className={cn(
      "fixed inset-0 z-50 flex min-h-screen items-center justify-center",
      className
    )}
    ref={ref}
    {...props}
  >
    <div className="relative w-full max-w-lg max-h-screen">
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/50 dark:bg-white/50" />
      <div className="relative bg-white rounded-lg shadow dark:bg-gray-900 p-6">
        {children}
      </div>
    </div>
  </div>
))
Dialog.displayName = "Dialog"

interface DialogTriggerProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode
}

const DialogTrigger = React.forwardRef<
  HTMLButtonElement,
  DialogTriggerProps
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
DialogTrigger.displayName = "DialogTrigger"

interface DialogContentProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode
  className?: string
}

const DialogContent = React.forwardRef<
  HTMLDivElement,
  DialogContentProps
>(({ className, children, ...props }, ref) => (
  <div
    className={cn("p-6 space-y-6", className)}
    ref={ref}
    {...props}
  >
    {children}
  </div>
))
DialogContent.displayName = "DialogContent"

interface DialogHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  className?: string
}

const DialogHeader = React.forwardRef<
  HTMLDivElement,
  DialogHeaderProps
>(({ className, ...props }, ref) => (
  <div
    className={cn("space-y-2", className)}
    ref={ref}
    {...props}
  />
))
DialogHeader.displayName = "DialogHeader"

interface DialogTitleProps extends React.HTMLAttributes<HTMLHeadingElement> {
  className?: string
}

const DialogTitle = React.forwardRef<
  HTMLHeadingElement,
  DialogTitleProps
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
DialogTitle.displayName = "DialogTitle"

interface DialogDescriptionProps extends React.HTMLAttributes<HTMLParagraphElement> {
  className?: string
}

const DialogDescription = React.forwardRef<
  HTMLParagraphElement,
  DialogDescriptionProps
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
DialogDescription.displayName = "DialogDescription"

interface DialogFooterProps extends React.HTMLAttributes<HTMLDivElement> {
  className?: string
}

const DialogFooter = React.forwardRef<
  HTMLDivElement,
  DialogFooterProps
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
DialogFooter.displayName = "DialogFooter"

interface DialogActionProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  className?: string
}

const DialogAction = React.forwardRef<
  HTMLButtonElement,
  DialogActionProps
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
DialogAction.displayName = "DialogAction"

interface DialogCancelProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  className?: string
}

const DialogCancel = React.forwardRef<
  HTMLButtonElement,
  DialogCancelProps
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
DialogCancel.displayName = "DialogCancel"

export { 
  Dialog, 
  DialogTrigger, 
  DialogContent, 
  DialogHeader, 
  DialogTitle, 
  DialogDescription, 
  DialogFooter, 
  DialogAction, 
  DialogCancel 
};
