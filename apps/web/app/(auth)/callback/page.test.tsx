import { render, waitFor } from "@testing-library/react"
import { beforeEach, describe, expect, it, vi } from "vitest"

import AuthCallbackPage from "./page"
import { createClient } from "@/lib/supabase/browser"

const routerReplaceMock = vi.fn()

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    replace: routerReplaceMock,
  }),
}))

vi.mock("@/lib/supabase/browser", () => ({
  createClient: vi.fn(),
}))

const createClientMock = vi.mocked(createClient)

describe("AuthCallbackPage", () => {
  beforeEach(() => {
    routerReplaceMock.mockReset()
    createClientMock.mockReset()
    window.history.replaceState(null, "", "/")
  })

  it("exchanges OAuth codes and redirects to the success screen", async () => {
    const exchangeCodeForSession = vi.fn().mockResolvedValue({ error: null })
    const getSession = vi.fn()

    createClientMock.mockReturnValue({
      auth: {
        exchangeCodeForSession,
        getSession,
      },
    } as never)
    window.history.replaceState(
      null,
      "",
      "/callback?code=oauth-code&next=%2Flogin%3Fauth%3Dsuccess"
    )

    render(<AuthCallbackPage />)

    await waitFor(() => {
      expect(exchangeCodeForSession).toHaveBeenCalledWith("oauth-code")
    })
    await waitFor(() => {
      expect(routerReplaceMock).toHaveBeenCalledWith("/login?auth=success")
    })
    expect(getSession).not.toHaveBeenCalled()
  })
})
