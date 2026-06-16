export function getEmailRedirectTo() {
  const configuredSiteUrl = process.env.NEXT_PUBLIC_SITE_URL?.trim()
  const origin =
    configuredSiteUrl ||
    (typeof window === "undefined" ? "" : window.location.origin)

  return `${origin.replace(/\/+$/, "")}/callback`
}

export function getSafeRedirectPath(rawNext: string | null | undefined) {
  const fallbackPath = "/"

  if (!rawNext || !rawNext.startsWith("/") || rawNext.startsWith("//")) {
    return fallbackPath
  }

  let decodedNext = rawNext

  try {
    decodedNext = decodeURIComponent(rawNext)
  } catch {
    return fallbackPath
  }

  if (
    !decodedNext.startsWith("/") ||
    decodedNext.startsWith("//") ||
    decodedNext.includes("\\")
  ) {
    return fallbackPath
  }

  const baseUrl = "https://backdesk.local"
  const redirectUrl = new URL(decodedNext, baseUrl)

  if (redirectUrl.origin !== baseUrl) {
    return fallbackPath
  }

  return `${redirectUrl.pathname}${redirectUrl.search}${redirectUrl.hash}`
}
