import { beforeEach, describe, expect, it, vi } from "vitest"

import {
  requestEmailOtp,
  signOutCurrentSession,
  verifyEmailOtp,
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

  it("returns errors instead of throwing when OTP requests fail at the network layer", async () => {
    createClientMock.mockReturnValue({
      auth: {
        signInWithOtp: vi.fn().mockRejectedValue(new Error("fetch failed")),
      },
    } as never)

    const result = await requestEmailOtp("person@example.com")

    expect(result.error).toBeInstanceOf(Error)
    expect(result.error?.message).toBe("fetch failed")
  })

  it("returns errors instead of throwing when OTP verification fails at the network layer", async () => {
    createClientMock.mockReturnValue({
      auth: {
        verifyOtp: vi.fn().mockRejectedValue(new Error("fetch failed")),
      },
    } as never)

    const result = await verifyEmailOtp("person@example.com", "123456")

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
