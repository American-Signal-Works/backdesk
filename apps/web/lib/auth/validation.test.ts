import { describe, expect, it } from "vitest"

import {
  getEmailValidationError,
  getOtpValidationError,
  normalizeEmail,
  normalizeOtp,
} from "./validation"

describe("auth validation helpers", () => {
  it("normalizes email before auth calls", () => {
    expect(normalizeEmail("  Test.User@Example.COM  ")).toBe(
      "test.user@example.com"
    )
  })

  it("rejects empty and malformed email addresses", () => {
    expect(getEmailValidationError("")).toBe("Enter your email address.")
    expect(getEmailValidationError("not-an-email")).toBe(
      "Enter a valid email address."
    )
    expect(getEmailValidationError("person@example.com")).toBeNull()
  })

  it("keeps OTP input numeric and bounded to six digits", () => {
    expect(normalizeOtp("12a 34-5678")).toBe("123456")
  })

  it("requires a complete six-digit OTP", () => {
    expect(getOtpValidationError("12345")).toBe(
      "Enter the 6-digit verification code."
    )
    expect(getOtpValidationError("123456")).toBeNull()
  })
})
