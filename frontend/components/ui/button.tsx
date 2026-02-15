import { cn } from "@/lib/utils"
import React from "react"

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "danger" | "outline" | "ghost"
  size?: "sm" | "md" | "lg"
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
          {
            "bg-blue-600 text-white hover:bg-blue-700 shadow-sm": variant === "primary",
            "bg-gray-100 text-gray-900 hover:bg-gray-200": variant === "secondary",
            "bg-red-500 text-white hover:bg-red-600": variant === "danger",
            "border border-gray-200 bg-transparent hover:bg-gray-100": variant === "outline",
            "bg-transparent hover:bg-gray-50 text-gray-700": variant === "ghost",
            "h-8 px-3 text-xs": size === "sm",
            "h-10 px-4 py-2": size === "md",
            "h-12 px-8 text-lg": size === "lg",
          },
          className
        )}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"
