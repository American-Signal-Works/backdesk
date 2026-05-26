"use client";

import { useState, useTransition } from "react";
import { Loader2 } from "lucide-react";
import { toast } from "sonner";
import { Button } from "@workspace/ui/components/button";
import { Input } from "@workspace/ui/components/input";
import {
  Field,
  FieldError,
  FieldGroup,
  FieldLabel,
} from "@workspace/ui/components/field";

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const MOCK_DELAY_MS = 1000;
const MOCK_FAIL_EMAIL = "error@test.com";

type FormState =
  | { kind: "idle" }
  | { kind: "validation"; message: string }
  | { kind: "submission"; message: string };

export function LoginForm() {
  const [state, setState] = useState<FormState>({ kind: "idle" });
  const [isPending, startTransition] = useTransition();

  function onSubmit(formData: FormData) {
    const email = String(formData.get("email") ?? "").trim();

    if (!email) {
      setState({ kind: "validation", message: "Email is required." });
      return;
    }
    if (!EMAIL_RE.test(email)) {
      setState({
        kind: "validation",
        message: "Enter a valid email address.",
      });
      return;
    }

    setState({ kind: "idle" });
    startTransition(async () => {
      await new Promise((resolve) => setTimeout(resolve, MOCK_DELAY_MS));
      if (email.toLowerCase() === MOCK_FAIL_EMAIL) {
        setState({
          kind: "submission",
          message: "We couldn't sign you in. Please try again.",
        });
        return;
      }
      toast.success(`Magic link sent to ${email}`);
    });
  }

  const validationError =
    state.kind === "validation" ? state.message : undefined;
  const submissionError =
    state.kind === "submission" ? state.message : undefined;

  return (
    <div className="flex w-full max-w-[21.875rem] flex-col gap-6">
      <header className="flex flex-col items-center gap-2 text-center">
        <h1 className="text-2xl font-semibold tracking-[-0.0417em]">Sign in</h1>
        <p className="text-sm text-muted-foreground">
          Enter your email below to sign into your account
        </p>
      </header>

      <form action={onSubmit} noValidate>
        <FieldGroup className="gap-6">
          <Field data-invalid={validationError ? true : undefined}>
            <FieldLabel htmlFor="email" className="sr-only">
              Email
            </FieldLabel>
            <Input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              placeholder="name@example.com"
              aria-invalid={validationError ? true : undefined}
              aria-describedby={validationError ? "email-error" : undefined}
              disabled={isPending}
              onChange={() => {
                if (state.kind !== "idle") setState({ kind: "idle" });
              }}
            />
            {validationError && (
              <FieldError id="email-error">{validationError}</FieldError>
            )}
          </Field>

          {submissionError && (
            <div
              role="alert"
              className="rounded-md border border-destructive/50 bg-destructive/10 px-3 py-2 text-sm text-destructive"
            >
              {submissionError}
            </div>
          )}

          <Button type="submit" disabled={isPending} className="w-full">
            {isPending ? (
              <>
                <Loader2 className="size-4 animate-spin" />
                Signing in…
              </>
            ) : (
              "Sign in with Email"
            )}
          </Button>
        </FieldGroup>
      </form>

      <p className="text-center text-sm text-muted-foreground">
        By clicking continue, you agree to our{" "}
        <a
          href="#"
          className="underline underline-offset-2 hover:text-foreground"
        >
          Terms of Service
        </a>{" "}
        and{" "}
        <a
          href="#"
          className="underline underline-offset-2 hover:text-foreground"
        >
          Privacy Policy
        </a>
        .
      </p>
    </div>
  );
}
