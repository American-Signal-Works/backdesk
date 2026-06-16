import { createClient as createSupabaseClient } from "@supabase/supabase-js"

import { createClient } from "@/lib/supabase/browser"
import { getEmailRedirectTo } from "@/lib/auth/redirect"
import type { Database } from "@/lib/supabase/types"

export async function requestEmailMagicLink(email: string) {
  return withAuthFailure(
    () =>
      createMagicLinkClient().auth.signInWithOtp({
        email,
        options: {
          emailRedirectTo: getEmailRedirectTo(),
        },
      }),
    (error) => ({ data: null, error })
  )
}

function createMagicLinkClient() {
  return createSupabaseClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      auth: {
        autoRefreshToken: false,
        detectSessionInUrl: false,
        flowType: "implicit",
        persistSession: false,
      },
    }
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
