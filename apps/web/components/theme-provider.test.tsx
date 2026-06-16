import { cleanup, render, waitFor } from "@testing-library/react"
import { afterEach, describe, expect, it, vi } from "vitest"

import { ThemeProvider } from "./theme-provider"

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

describe("ThemeProvider", () => {
  afterEach(() => {
    cleanup()
    localStorage.clear()
    document.documentElement.className = ""
    vi.unstubAllGlobals()
  })

  it("resolves system mode from a dark operating system preference", async () => {
    const media = createMatchMediaController(true)
    vi.stubGlobal("matchMedia", media.matchMedia)

    render(
      <ThemeProvider defaultTheme="system">
        <div />
      </ThemeProvider>
    )

    await waitFor(() => {
      expect(document.documentElement).toHaveClass("dark")
    })
  })

  it("updates system mode when the operating system preference changes", async () => {
    const media = createMatchMediaController(false)
    vi.stubGlobal("matchMedia", media.matchMedia)

    render(
      <ThemeProvider defaultTheme="system">
        <div />
      </ThemeProvider>
    )

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

  it("keeps explicit modes independent from the operating system preference", async () => {
    const media = createMatchMediaController(true)
    vi.stubGlobal("matchMedia", media.matchMedia)

    const { unmount } = render(
      <ThemeProvider defaultTheme="light">
        <div />
      </ThemeProvider>
    )

    await waitFor(() => {
      expect(document.documentElement).not.toHaveClass("dark")
    })

    unmount()
    cleanup()
    localStorage.clear()
    document.documentElement.className = ""
    media.setMatches(false)

    render(
      <ThemeProvider defaultTheme="dark">
        <div />
      </ThemeProvider>
    )

    await waitFor(() => {
      expect(document.documentElement).toHaveClass("dark")
    })
  })
})
