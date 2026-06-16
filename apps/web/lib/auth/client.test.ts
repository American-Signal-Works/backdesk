import { afterEach, beforeEach, describe, expect, it, vi } from "vitest"
import { createClient as createSupabaseClient } from "@supabase/supabase-js"

import { requestEmailMagicLink, signOutCurrentSession } from "./client"
import { createClient } from "@/lib/supabase/browser"

vi.mock("@/lib/supabase/browser", () => ({
  createClient: vi.fn(),
}))

vi.mock("@supabase/supabase-js", () => ({
  createClient: vi.fn(),
}))

const createClientMock = vi.mocked(createClient)
const createSupabaseClientMock = vi.mocked(createSupabaseClient)

describe("auth client helpers", () => {
  beforeEach(() => {
    createClientMock.mockReset()
    createSupabaseClientMock.mockReset()
    vi.stubEnv("NEXT_PUBLIC_SUPABASE_URL", "https://project.supabase.co")
    vi.stubEnv("NEXT_PUBLIC_SUPABASE_ANON_KEY", "anon-key")
  })

  afterEach(() => {
    vi.unstubAllEnvs()
  })

  it("requests magic links with an implicit client so callbacks do not need a PKCE verifier", async () => {
    const signInWithOtp = vi.fn().mockResolvedValue({
      data: {},
      error: null,
    })
    createSupabaseClientMock.mockReturnValue({
      auth: {
        signInWithOtp,
      },
    } as never)

    await requestEmailMagicLink("person@example.com")

    expect(createSupabaseClientMock).toHaveBeenCalledWith(
      "https://project.supabase.co",
      "anon-key",
      {
        auth: {
          autoRefreshToken: false,
          detectSessionInUrl: false,
          flowType: "implicit",
          persistSession: false,
        },
      }
    )
    expect(signInWithOtp).toHaveBeenCalledWith({
      email: "person@example.com",
      options: {
        emailRedirectTo: "http://localhost:3000/callback",
      },
    })
  })

  it("returns errors instead of throwing when magic link requests fail at the network layer", async () => {
    createSupabaseClientMock.mockReturnValue({
      auth: {
        signInWithOtp: vi.fn().mockRejectedValue(new Error("fetch failed")),
      },
    } as never)

    const result = await requestEmailMagicLink("person@example.com")

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
