import { fireEvent, render, screen, waitFor } from "@testing-library/react"
import { beforeEach, describe, expect, it, vi } from "vitest"

import { updateAppearance } from "@/actions/settings"
import { AppearanceForm } from "./AppearanceForm"
import { useTheme } from "next-themes"

vi.mock("next-themes", () => ({
  useTheme: vi.fn(),
}))

vi.mock("@/actions/settings", () => ({
  updateAppearance: vi.fn(),
}))

vi.mock("sonner", () => ({
  toast: {
    error: vi.fn(),
  },
}))

const updateAppearanceMock = vi.mocked(updateAppearance)
const useThemeMock = vi.mocked(useTheme)

describe("AppearanceForm", () => {
  beforeEach(() => {
    useThemeMock.mockReset()
    updateAppearanceMock.mockReset()
    updateAppearanceMock.mockResolvedValue({ ok: true, data: {} })
  })

  it("syncs the persisted initial mode into next-themes on mount", async () => {
    const setTheme = vi.fn()
    useThemeMock.mockReturnValue({ setTheme } as never)

    render(<AppearanceForm initialAccent="default" initialMode="system" />)

    await waitFor(() => {
      expect(setTheme).toHaveBeenCalledWith("system")
    })
  })

  it("persists mode changes and uses the selected mode for accent changes", async () => {
    const setTheme = vi.fn()
    useThemeMock.mockReturnValue({ setTheme } as never)

    render(<AppearanceForm initialAccent="default" initialMode="system" />)

    fireEvent.click(screen.getByText("Dark"))

    await waitFor(() => {
      expect(setTheme).toHaveBeenCalledWith("dark")
      expect(updateAppearanceMock).toHaveBeenCalledWith({
        theme_accent: "default",
        theme_mode: "dark",
      })
    })

    fireEvent.click(screen.getByLabelText("blue"))

    await waitFor(() => {
      expect(updateAppearanceMock).toHaveBeenLastCalledWith({
        theme_accent: "blue",
        theme_mode: "dark",
      })
    })
  })
})
