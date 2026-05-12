import * as React from "react"
import { cn } from "@/utils/cn"

interface TableProps extends React.TableHTMLAttributes<HTMLTableElement> {
  className?: string
}

export const Table = React.forwardRef<
  HTMLTableElement,
  TableProps
>(({ className, ...props }, ref) => (
  <table
    ref={ref}
    className={cn(
      "w-full text-sm text-left rtl:text-right border-collapse",
      className
    )}
    {...props}
  />
))
Table.displayName = "Table"

interface TableHeaderProps extends React.HTMLAttributes<HTMLTableSectionElement> {
  className?: string
}

export const TableHeader = React.forwardRef<
  HTMLTableSectionElement,
  TableHeaderProps
>(({ className, ...props }, ref) => (
  <thead
    ref={ref}
    className={cn("", className)}
    {...props}
  />
))
TableHeader.displayName = "TableHeader"

interface TableBodyProps extends React.HTMLAttributes<HTMLTableSectionElement> {
  className?: string
}

export const TableBody = React.forwardRef<
  HTMLTableSectionElement,
  TableBodyProps
>(({ className, ...props }, ref) => (
  <tbody
    ref={ref}
    className={cn("", className)}
    {...props}
  />
))
TableBody.displayName = "TableBody"

interface TableFooterProps extends React.HTMLAttributes<HTMLTableSectionElement> {
  className?: string
}

export const TableFooter = React.forwardRef<
  HTMLTableSectionElement,
  TableFooterProps
>(({ className, ...props }, ref) => (
  <tfoot
    ref={ref}
    className={cn("", className)}
    {...props}
  />
))
TableFooter.displayName = "TableFooter"

interface TableRowProps extends React.HTMLAttributes<HTMLTableRowElement> {
  className?: string
}

export const TableRow = React.forwardRef<
  HTMLTableRowElement,
  TableRowProps
>(({ className, ...props }, ref) => (
  <tr
    ref={ref}
    className={cn(
      "border-b",
      className
    )}
    {...props}
  />
))
TableRow.displayName = "TableRow"

interface TableCellProps extends React.HTMLAttributes<HTMLTableCellElement> {
  align?: "left" | "center" | "right" | "justify"
  className?: string
}

export const TableCell = React.forwardRef<
  HTMLTableCellElement,
  TableCellProps
>(({ className, align, ...props }, ref) => {
  const alignClass = align === "right"
    ? "text-right"
    : align === "center"
    ? "text-center"
    : align === "justify"
    ? "text-justify"
    : "text-left"
  return (
    <td
      ref={ref}
      className={cn(
        "p-4",
        alignClass,
        className
      )}
      {...props}
    />
  )
})
TableCell.displayName = "TableCell"
