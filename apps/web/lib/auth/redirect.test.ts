import { afterEach, describe, expect, it, vi } from "vitest"

import { getEmailRedirectTo, getSafeRedirectPath } from "./redirect"

describe("auth redirect helpers", () => {
  afterEach(() => {
    vi.unstubAllEnvs()
  })

  it("builds the email callback URL from configured site URL", () => {
    vi.stubEnv("NEXT_PUBLIC_SITE_URL", "https://preview.vercel.app/")

    expect(getEmailRedirectTo()).toBe("https://preview.vercel.app/callback")
  })

  it("falls back to the current browser origin for email callbacks", () => {
    vi.stubEnv("NEXT_PUBLIC_SITE_URL", "")

    expect(getEmailRedirectTo()).toBe("http://localhost:3000/callback")
  })

  it("allows only path-relative callback redirects", () => {
    expect(getSafeRedirectPath("/")).toBe("/")
    expect(getSafeRedirectPath("/settings")).toBe("/settings")
    expect(getSafeRedirectPath("https://evil.example")).toBe("/")
    expect(getSafeRedirectPath("//evil.example")).toBe("/")
    expect(getSafeRedirectPath("/\\evil.example")).toBe("/")
    expect(getSafeRedirectPath("/%5Cevil.example")).toBe("/")
    expect(getSafeRedirectPath("/%2F%2Fevil.example")).toBe("/")
    expect(getSafeRedirectPath("settings")).toBe("/")
    expect(getSafeRedirectPath(null)).toBe("/")
  })

  it("preserves same-origin path details", () => {
    expect(getSafeRedirectPath("/settings?tab=team#invite")).toBe(
      "/settings?tab=team#invite",
    )
  })
})
