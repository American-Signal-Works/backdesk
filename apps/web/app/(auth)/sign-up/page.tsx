import { LoginAuthFlow } from "@/components/auth/LoginAuthFlow"

type SignUpPageProps = {
  searchParams?: Promise<Record<string, string | string[] | undefined>>
}

export default async function SignUpPage({ searchParams }: SignUpPageProps) {
  const params = await searchParams
  const error = Array.isArray(params?.error) ? params.error[0] : params?.error

  return (
    <LoginAuthFlow
      initialFormMessage={
        error === "callback_failed"
          ? "We couldn't complete sign up. Try again."
          : null
      }
      mode="sign-up"
    />
  )
}
