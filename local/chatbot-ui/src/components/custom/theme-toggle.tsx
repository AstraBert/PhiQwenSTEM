import { Moon, Sun } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useTheme } from "@/context/ThemeContext"

export function ThemeToggle() {
  const { isDarkMode, toggleTheme } = useTheme()

  return (
    <Button
      variant="outline"
      className="bg-background border border-gray text-gray-600 hover:white dark:text-gray-200 h-10"
      onClick={toggleTheme}
    >
      {isDarkMode ? (
        <Moon className="h-[1.2rem] w-[1.2rem]" />
      ) : (
        <Sun className="h-[1.2rem] w-[1.2rem]" />
      )}
      <span className="sr-only">Toggle theme</span>
    </Button>
  )
}