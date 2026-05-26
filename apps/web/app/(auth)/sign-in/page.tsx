import type { Metadata } from "next";
import { Command } from "lucide-react";
import { SignInForm } from "@/components/auth/SignInForm";

export const metadata: Metadata = { title: "Sign in" };

export default function SignInPage() {
  return (
    <div className="min-h-svh flex flex-col md:flex-row bg-background">
      <aside className="hidden md:flex md:flex-1 flex-col justify-between bg-muted px-8 py-8 pr-16">
        <div className="flex items-center gap-2">
          <Command className="size-6" strokeWidth={2} aria-hidden />
          <span className="text-xl font-semibold tracking-tight">Backdesk</span>
        </div>
        <blockquote className="text-base leading-6">
          <p>
            &ldquo;A workspace for your data — pages of blocks, collections,
            connections. Everything in one place, finally.&rdquo;
          </p>
          <footer className="mt-2 text-muted-foreground">
            &mdash; Backdesk team
          </footer>
        </blockquote>
      </aside>
      <div className="flex md:hidden items-center gap-2 px-6 pt-8">
        <Command className="size-6" strokeWidth={2} aria-hidden />
        <span className="text-xl font-semibold tracking-tight">Backdesk</span>
      </div>
      <main className="flex flex-1 items-center justify-center p-6 md:p-8">
        <SignInForm />
      </main>
    </div>
  );
}
