import { createClient } from "@/lib/supabase/browser"
import { getAuthCallbackUrl, getEmailRedirectTo } from "@/lib/auth/redirect"

export type OAuthProvider = "google" | "azure"

type EmailMagicLinkOptions = {
  shouldCreateUser?: boolean
}

export async function requestEmailMagicLink(
  email: string,
  options: EmailMagicLinkOptions = {}
) {
  return withAuthFailure(
    () =>
      createClient().auth.signInWithOtp({
        email,
        options: {
          emailRedirectTo: getEmailRedirectTo(),
          shouldCreateUser: options.shouldCreateUser,
        },
      }),
    (error) => ({ data: null, error })
  )
}

export async function requestOAuthSignIn(provider: OAuthProvider) {
  return withAuthFailure(
    () =>
      createClient().auth.signInWithOAuth({
        provider,
        options: {
          redirectTo: getAuthCallbackUrl(),
          ...(provider === "azure" ? { scopes: "email" } : {}),
        },
      }),
    (error) => ({ data: null, error })
  )
}

export async function signOutCurrentSession() {
  return withAuthFailure(
    () => createClient().auth.signOut(),
    (error) => ({ error })
  )
}

async function withAuthFailure<T, F>(
  request: () => Promise<T>,
  fallback: (error: Error) => F
) {
  try {
    return await request()
  } catch (error) {
    return fallback(toAuthClientError(error))
  }
}

function toAuthClientError(error: unknown) {
  if (error instanceof Error) {
    return error
  }

  return new Error("Authentication request failed.")
}
