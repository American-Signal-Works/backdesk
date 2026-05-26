import type { Metadata } from "next";
import { Command } from "lucide-react";
import { LoginForm } from "@/components/auth/LoginForm";

export const metadata: Metadata = { title: "Log in" };

export default function LoginPage() {
  return (
    <div className="min-h-svh flex flex-col md:flex-row bg-background">
      <aside className="hidden md:flex md:flex-1 flex-col justify-between bg-muted px-8 py-8 pr-16">
        <div className="flex items-center gap-2">
          <Command className="size-6" strokeWidth={2} />
          <span className="text-xl font-semibold tracking-tight">Acme Inc</span>
        </div>
        <blockquote className="text-base leading-6">
          <p>
            &ldquo;This library has saved me countless hours of work and helped
            me deliver stunning designs to my clients faster than ever
            before.&rdquo;
          </p>
          <footer className="mt-2">&mdash; Sofia Davis</footer>
        </blockquote>
      </aside>
      <div className="flex md:hidden items-center gap-2 px-6 pt-8">
        <Command className="size-6" strokeWidth={2} />
        <span className="text-xl font-semibold tracking-tight">Acme Inc</span>
      </div>
      <main className="flex flex-1 items-center justify-center p-6 md:p-8">
        <LoginForm />
      </main>
    </div>
  );
}
