import * as React from "react"
import ReactDOM from "react-dom"
import { cn } from "@/utils/cn"

// Глобальный менеджер для закрытия других select при открытии нового
const closeAllSelectsCallbacks: Set<() => void> = new Set()

const selectVariants = 
  "inline-flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"

export interface SelectProps extends VariantProps<typeof selectVariants> {
  value?: any
  defaultValue?: any
  onValueChange?: (value: any) => void
  disabled?: boolean
  open?: boolean
  defaultOpen?: boolean
  onOpenChange?: (open: boolean) => void
}

interface VariantProps<T> {
  className?: string
  size?: keyof T extends object ? keyof T : never
}

const SelectContext = React.createContext<{
  value: any
  onValueChange: (value: any) => void
  disabled?: boolean
  open: boolean
  setOpen: (open: boolean) => void
  triggerRef: React.RefObject<HTMLButtonElement | null>
  contentId: string
} | null>(null)

export const Select = ({
  className,
  children,
  value,
  defaultValue,
  onValueChange,
  disabled,
  open: controlledOpen,
  defaultOpen = false,
  onOpenChange,
  size,
}: SelectProps) => {
  const [internalValue, setInternalValue] = React.useState(defaultValue)
  const [internalOpen, setInternalOpen] = React.useState(defaultOpen)
  
  const isControlled = value !== undefined
  const isOpen = controlledOpen ?? internalOpen
  const selectedValue = isControlled ? value : internalValue
  
  const setOpen = React.useCallback((open: boolean) => {
    if (onOpenChange) {
      onOpenChange(open)
    } else {
      setInternalOpen(open)
    }
  }, [onOpenChange])
  
  const handleValueChange = React.useCallback((newValue: any) => {
    if (onValueChange) {
      onValueChange(newValue)
    } else {
      setInternalValue(newValue)
    }
    setOpen(false)
  }, [onValueChange, setOpen])
  
  const triggerRef = React.useRef<HTMLButtonElement>(null)
  const contentId = React.useId()
  
  // Register/unregister close callback
  React.useEffect(() => {
    const closeCallback = () => {
      setOpen(false)
    }
    closeAllSelectsCallbacks.add(closeCallback)
    return () => {
      closeAllSelectsCallbacks.delete(closeCallback)
    }
  }, [setOpen])
  
  // Handle click outside
  React.useEffect(() => {
    if (!isOpen) return
    
    const handleClickOutside = (event: MouseEvent | TouchEvent) => {
      const target = event.target as Node
      if (triggerRef.current && !triggerRef.current.contains(target)) {
        const contentElement = document.getElementById(contentId)
        if (contentElement && !contentElement.contains(target)) {
          setOpen(false)
        }
      }
    }
    
    document.addEventListener("mousedown", handleClickOutside)
    document.addEventListener("touchstart", handleClickOutside)
    
    return () => {
      document.removeEventListener("mousedown", handleClickOutside)
      document.removeEventListener("touchstart", handleClickOutside)
    }
  }, [isOpen, contentId, setOpen])
  
  return (
    <SelectContext.Provider
      value={{
        value: selectedValue,
        onValueChange: handleValueChange,
        disabled,
        open: isOpen,
        setOpen,
        triggerRef,
        contentId,
      }}
    >
      <div className={cn(selectVariants, className)} role="combobox" aria-expanded={isOpen}>
        {children}
      </div>
    </SelectContext.Provider>
  )
}
Select.displayName = "Select"

export const SelectTrigger = ({
  className,
  children,
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement>) => {
  const context = React.useContext(SelectContext)
  if (!context) throw new Error("SelectTrigger must be used within Select")
  
  const { disabled, open, setOpen, triggerRef } = context
  
  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    if (disabled) return
    e.preventDefault()
    
    // Close all other selects first
    closeAllSelectsCallbacks.forEach(cb => cb())
    
    // Toggle this select
    setOpen(!open)
  }
  
  return (
    <button
      ref={triggerRef}
      className={cn(
        "flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
        className
      )}
      onClick={handleClick}
      disabled={disabled}
      aria-haspopup="listbox"
      aria-expanded={open}
      type="button"
      {...props}
    >
      {children}
      <svg
        className="ml-2 h-4 w-4 shrink-0 opacity-50 transition-transform duration-200"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        style={{ transform: open ? 'rotate(180deg)' : 'rotate(0deg)' }}
      >
        <path d="m6 9 6 6 6-6"/>
      </svg>
    </button>
  )
}
SelectTrigger.displayName = "SelectTrigger"

export const SelectValue = ({
  className,
  placeholder,
  ...props
}: React.HTMLAttributes<HTMLSpanElement> & { placeholder?: string }) => {
  const context = React.useContext(SelectContext)
  if (!context) throw new Error("SelectValue must be used within Select")
  
  return (
    <span
      className={cn("truncate", className)}
      {...props}
    >
      {context.value ?? placeholder}
    </span>
  )
}
SelectValue.displayName = "SelectValue"

export const SelectContent = ({
  className,
  children,
  position = "popper",
  align = "start",
  sideOffset = 4,
  ...props
}: React.ComponentPropsWithoutRef<"div"> & {
  position?: "popper" | "item-aligned"
  align?: "start" | "center" | "end"
  sideOffset?: number
}) => {
  const context = React.useContext(SelectContext)
  if (!context) throw new Error("SelectContent must be used within Select")
  
  const { open, triggerRef, contentId, disabled } = context
  const [mounted, setMounted] = React.useState(false)
  const [positionStyles, setPositionStyles] = React.useState<React.CSSProperties>({})
  
  React.useEffect(() => {
    setMounted(true)
  }, [])
  
  // Calculate position when opened
  React.useEffect(() => {
    if (!open || !triggerRef.current || !mounted) return
    
    const updatePosition = () => {
      const trigger = triggerRef.current
      if (!trigger) return
      
      const triggerRect = trigger.getBoundingClientRect()
      const scrollX = window.scrollX || window.pageXOffset
      const scrollY = window.scrollY || window.pageYOffset
      
      let top = triggerRect.bottom + scrollY + sideOffset
      let left = triggerRect.left + scrollX
      
      // Align options
      if (align === "center") {
        left = triggerRect.left + scrollX + (triggerRect.width / 2)
      } else if (align === "end") {
        left = triggerRect.right + scrollX
      }
      
      setPositionStyles({
        position: "absolute",
        top: `${top}px`,
        left: align === "center" ? `${left}px` : `${left}px`,
        minWidth: `${triggerRect.width}px`,
        zIndex: 9999,
        transform: align === "center" ? "translateX(-50%)" : "none",
      })
    }
    
    updatePosition()
    
    // Update on scroll and resize
    window.addEventListener("scroll", updatePosition, true)
    window.addEventListener("resize", updatePosition)
    
    return () => {
      window.removeEventListener("scroll", updatePosition, true)
      window.removeEventListener("resize", updatePosition)
    }
  }, [open, mounted, align, sideOffset, triggerRef])
  
  if (!open || !mounted) return null
  
  const content = (
    <div
      id={contentId}
      className={cn(
        "relative z-50 max-h-96 min-w-[8rem] overflow-hidden rounded-md border bg-popover text-popover-foreground shadow-md data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95",
        className
      )}
      style={positionStyles}
      role="listbox"
      {...props}
    >
      <div className="p-1">
        {children}
      </div>
    </div>
  )
  
  // Render portal to body to avoid overflow/positioning issues
  if (typeof document !== "undefined") {
    const portalContainer = document.getElementById("select-portal-container") || document.body
    return ReactDOM.createPortal(content, portalContainer)
  }
  
  return content
}
SelectContent.displayName = "SelectContent"

export const SelectItem = ({
  className,
  children,
  value,
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement> & { value?: any }) => {
  const context = React.useContext(SelectContext)
  if (!context) throw new Error("SelectItem must be used within Select")
  
  const { value: selectedValue, onValueChange, disabled } = context
  const isSelected = selectedValue === value
  
  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault()
    e.stopPropagation()
    if (!disabled) {
      onValueChange(value ?? children)
    }
  }
  
  return (
    <button
      className={cn(
        "relative flex w-full cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none transition-colors focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
        isSelected && "bg-accent text-accent-foreground",
        className
      )}
      onClick={handleClick}
      disabled={disabled}
      role="option"
      aria-selected={isSelected}
      {...props}
    >
      {isSelected && (
        <svg
          className="mr-2 h-4 w-4"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <polyline points="20 6 9 17 4 12"/>
        </svg>
      )}
      <span>{children}</span>
    </button>
  )
}
SelectItem.displayName = "SelectItem"
