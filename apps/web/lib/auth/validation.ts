const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const otpPattern = /^\d{6}$/

export function normalizeEmail(email: string) {
  return email.trim().toLowerCase()
}

export function getEmailValidationError(email: string) {
  const normalizedEmail = normalizeEmail(email)

  if (!normalizedEmail) {
    return "Enter your email address."
  }

  if (!emailPattern.test(normalizedEmail)) {
    return "Enter a valid email address."
  }

  return null
}

export function normalizeOtp(otp: string) {
  return otp.replace(/\D/g, "").slice(0, 6)
}

export function getOtpValidationError(otp: string) {
  if (!otpPattern.test(otp)) {
    return "Enter the 6-digit verification code."
  }

  return null
}
