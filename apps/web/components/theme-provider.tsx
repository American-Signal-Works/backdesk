"use client"

import * as React from "react"
import { ThemeProvider as NextThemesProvider, useTheme } from "next-themes"

function ThemeProvider({
  children,
  ...props
}: React.ComponentProps<typeof NextThemesProvider>) {
  const defaultTheme =
    typeof props.defaultTheme === "string" ? props.defaultTheme : "system"

  return (
    <NextThemesProvider
      attribute="class"
      defaultTheme={defaultTheme}
      enableSystem
      disableTransitionOnChange
      {...props}
    >
      <ThemePreferenceSync theme={defaultTheme} />
      <ThemeHotkey />
      {children}
    </NextThemesProvider>
  )
}

function isThemeMode(value: string): value is "light" | "dark" | "system" {
  return value === "light" || value === "dark" || value === "system"
}

function ThemePreferenceSync({ theme }: { theme: string }) {
  const { setTheme } = useTheme()
  const hasSynced = React.useRef(false)

  React.useEffect(() => {
    if (hasSynced.current || !isThemeMode(theme)) {
      return
    }

    hasSynced.current = true
    setTheme(theme)
  }, [setTheme, theme])

  return null
}

function isTypingTarget(target: EventTarget | null) {
  if (!(target instanceof HTMLElement)) {
    return false
  }

  return (
    target.isContentEditable ||
    target.tagName === "INPUT" ||
    target.tagName === "TEXTAREA" ||
    target.tagName === "SELECT"
  )
}

function ThemeHotkey() {
  const { resolvedTheme, setTheme } = useTheme()

  React.useEffect(() => {
    function onKeyDown(event: KeyboardEvent) {
      if (event.defaultPrevented || event.repeat) {
        return
      }

      if (event.metaKey || event.ctrlKey || event.altKey) {
        return
      }

      if (event.key.toLowerCase() !== "d") {
        return
      }

      if (isTypingTarget(event.target)) {
        return
      }

      setTheme(resolvedTheme === "dark" ? "light" : "dark")
    }

    window.addEventListener("keydown", onKeyDown)

    return () => {
      window.removeEventListener("keydown", onKeyDown)
    }
  }, [resolvedTheme, setTheme])

  return null
}

export { ThemeProvider }
