import { afterEach, beforeEach, describe, expect, it, vi } from "vitest"

import {
  requestEmailMagicLink,
  requestOAuthSignIn,
  signOutCurrentSession,
} from "./client"
import { createClient } from "@/lib/supabase/browser"

vi.mock("@/lib/supabase/browser", () => ({
  createClient: vi.fn(),
}))

const createClientMock = vi.mocked(createClient)

describe("auth client helpers", () => {
  beforeEach(() => {
    createClientMock.mockReset()
  })

  afterEach(() => {
    vi.unstubAllEnvs()
  })

  it("returns errors instead of throwing when magic link requests fail at the network layer", async () => {
    createClientMock.mockReturnValue({
      auth: {
        signInWithOtp: vi.fn().mockRejectedValue(new Error("fetch failed")),
      },
    } as never)

    const result = await requestEmailMagicLink("person@example.com")

    expect(result.error).toBeInstanceOf(Error)
    expect(result.error?.message).toBe("fetch failed")
  })

  it("requests email magic links with callback and sign-up intent", async () => {
    vi.stubEnv("NEXT_PUBLIC_SITE_URL", "https://usebackdesk.com")
    const signInWithOtp = vi.fn().mockResolvedValue({
      data: {},
      error: null,
    })
    createClientMock.mockReturnValue({
      auth: {
        signInWithOtp,
      },
    } as never)

    await requestEmailMagicLink("person@example.com", {
      shouldCreateUser: true,
    })

    expect(signInWithOtp).toHaveBeenCalledWith({
      email: "person@example.com",
      options: {
        emailRedirectTo:
          "https://usebackdesk.com/callback?next=%2Flogin%3Fauth%3Dsuccess",
        shouldCreateUser: true,
      },
    })
  })

  it("starts Google sign-on through Supabase OAuth", async () => {
    vi.stubEnv("NEXT_PUBLIC_SITE_URL", "https://usebackdesk.com")
    const signInWithOAuth = vi.fn().mockResolvedValue({
      data: { url: "https://provider.example.com" },
      error: null,
    })
    createClientMock.mockReturnValue({
      auth: {
        signInWithOAuth,
      },
    } as never)

    await requestOAuthSignIn("google")

    expect(signInWithOAuth).toHaveBeenCalledWith({
      provider: "google",
      options: {
        redirectTo:
          "https://usebackdesk.com/callback?next=%2Flogin%3Fauth%3Dsuccess",
      },
    })
  })

  it("requests email scope for Microsoft sign-on", async () => {
    vi.stubEnv("NEXT_PUBLIC_SITE_URL", "https://usebackdesk.com")
    const signInWithOAuth = vi.fn().mockResolvedValue({
      data: { url: "https://provider.example.com" },
      error: null,
    })
    createClientMock.mockReturnValue({
      auth: {
        signInWithOAuth,
      },
    } as never)

    await requestOAuthSignIn("azure")

    expect(signInWithOAuth).toHaveBeenCalledWith({
      provider: "azure",
      options: {
        redirectTo:
          "https://usebackdesk.com/callback?next=%2Flogin%3Fauth%3Dsuccess",
        scopes: "email",
      },
    })
  })

  it("returns errors instead of throwing when OAuth start fails at the network layer", async () => {
    createClientMock.mockReturnValue({
      auth: {
        signInWithOAuth: vi.fn().mockRejectedValue(new Error("fetch failed")),
      },
    } as never)

    const result = await requestOAuthSignIn("google")

    expect(result.error).toBeInstanceOf(Error)
    expect(result.error?.message).toBe("fetch failed")
  })

  it("returns errors instead of throwing when sign-out fails at the network layer", async () => {
    createClientMock.mockReturnValue({
      auth: {
        signOut: vi.fn().mockRejectedValue(new Error("fetch failed")),
      },
    } as never)

    const result = await signOutCurrentSession()

    expect(result.error).toBeInstanceOf(Error)
    expect(result.error?.message).toBe("fetch failed")
  })
})
