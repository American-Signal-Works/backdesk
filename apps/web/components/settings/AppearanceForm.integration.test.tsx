import { fireEvent, render, screen, waitFor } from "@testing-library/react"
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest"

import { updateAppearance } from "@/actions/settings"
import { ThemeProvider } from "@/components/theme-provider"
import { AppearanceForm } from "./AppearanceForm"

type MqlListener = (this: MediaQueryList, event: MediaQueryListEvent) => void

function createMatchMediaController(initialMatches: boolean) {
  let matches = initialMatches
  const listeners = new Set<MqlListener>()
  const mql = {
    get matches() {
      return matches
    },
    media: "(prefers-color-scheme: dark)",
    onchange: null,
    addEventListener: (
      type: string,
      listener: EventListenerOrEventListenerObject
    ) => {
      if (type === "change") listeners.add(listener as MqlListener)
    },
    removeEventListener: (
      type: string,
      listener: EventListenerOrEventListenerObject
    ) => {
      if (type === "change") listeners.delete(listener as MqlListener)
    },
    addListener: (listener: MqlListener) => listeners.add(listener),
    removeListener: (listener: MqlListener) => listeners.delete(listener),
    dispatchEvent: () => true,
  } as MediaQueryList

  return {
    matchMedia: vi.fn(() => mql),
    setMatches(value: boolean) {
      matches = value
      const event = {
        matches,
        media: mql.media,
      } as MediaQueryListEvent

      listeners.forEach((listener) => listener.call(mql, event))
      mql.onchange?.call(mql, event)
    },
  }
}

vi.mock("@/actions/settings", () => ({
  updateAppearance: vi.fn(),
}))

vi.mock("sonner", () => ({
  toast: {
    error: vi.fn(),
  },
}))

const updateAppearanceMock = vi.mocked(updateAppearance)

describe("AppearanceForm theme integration", () => {
  beforeEach(() => {
    updateAppearanceMock.mockReset()
    updateAppearanceMock.mockResolvedValue({ ok: true, data: {} })
    localStorage.clear()
    document.documentElement.className = ""
  })

  afterEach(() => {
    localStorage.clear()
    document.documentElement.className = ""
    vi.unstubAllGlobals()
  })

  it("switches from an explicit dark preference to system light immediately", async () => {
    const media = createMatchMediaController(false)
    vi.stubGlobal("matchMedia", media.matchMedia)

    render(
      <ThemeProvider defaultTheme="dark">
        <AppearanceForm initialAccent="default" initialMode="dark" />
      </ThemeProvider>
    )

    await waitFor(() => {
      expect(document.documentElement).toHaveClass("dark")
    })

    fireEvent.click(screen.getByRole("radio", { name: "System" }))

    await waitFor(() => {
      expect(localStorage.getItem("theme")).toBe("system")
      expect(document.documentElement).not.toHaveClass("dark")
      expect(updateAppearanceMock).toHaveBeenLastCalledWith({
        theme_accent: "default",
        theme_mode: "system",
      })
    })
  })

  it("keeps following operating system changes after selecting system", async () => {
    const media = createMatchMediaController(false)
    vi.stubGlobal("matchMedia", media.matchMedia)

    render(
      <ThemeProvider defaultTheme="dark">
        <AppearanceForm initialAccent="default" initialMode="dark" />
      </ThemeProvider>
    )

    fireEvent.click(screen.getByRole("radio", { name: "System" }))

    await waitFor(() => {
      expect(document.documentElement).not.toHaveClass("dark")
    })

    media.setMatches(true)

    await waitFor(() => {
      expect(document.documentElement).toHaveClass("dark")
    })

    media.setMatches(false)

    await waitFor(() => {
      expect(document.documentElement).not.toHaveClass("dark")
    })
  })
})
