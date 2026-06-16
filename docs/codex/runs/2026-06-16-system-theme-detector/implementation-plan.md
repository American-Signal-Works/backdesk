# Implementation Plan: System Theme Detector

Date: 2026-06-16
Contract: ./design-contract.md
Status: Complete

## Approved Slice

- Parent flow: Appearance/theme behavior
- Slice: System mode follows OS/browser light or dark preference
- Scope boundary: provider initialization, settings compatibility, auth forced-dark cleanup, focused tests
- Deferred slices: command-palette and keyboard-shortcut persistence to Supabase

## Component Plan

- Existing primitives to reuse: `next-themes`, `ToggleGroup`, existing shadcn semantic theme tokens
- Missing primitives to add: none
- shadcn docs/search/view/dry-run commands: none; `pnpm dlx shadcn@latest info --json -c apps/web` already verified installed context
- Components intentionally not added: new theme selector, new theme icons

## Asset Plan

- Icons/assets to use from repo libraries: none
- Icons/assets to export from Figma: none
- New asset/icon dependencies: none

## Work Packages

| Package                  | Owner      | Edit scope                                                          | Do not edit                                        | Verification                                                       |
| ------------------------ | ---------- | ------------------------------------------------------------------- | -------------------------------------------------- | ------------------------------------------------------------------ |
| Provider wiring          | main agent | `apps/web/app/layout.tsx`, `apps/web/components/theme-provider.tsx` | schema, Supabase auth helpers                      | typecheck, tests, browser check                                    |
| Auth forced-dark cleanup | main agent | `apps/web/components/auth/LoginAuthFlow.tsx`, focused auth test     | auth action behavior, copy/layout beyond class fix | Vitest auth test                                                   |
| Test updates             | main agent | focused tests under `apps/web/components/**`                        | broad snapshots, unrelated tests                   | `pnpm --filter web test -- --run ...` or nearest available command |

## Security Notes

- No new dependency, env var, schema migration, or external service.
- Profile read remains scoped to the authenticated user in `RootLayout`.
- Theme preference is not sensitive; no additional logging or client payload of secrets.

## Verification Plan

- Run focused unit tests for changed components.
- Run `pnpm --filter web typecheck`.
- Run broader `pnpm --filter web test` if focused tests pass and runtime cost is acceptable.
- Start local web app and inspect theme behavior with browser tooling if the app starts with available env.

## Progress

- [x] Contract approved
- [x] Code changes complete
- [x] Tests updated
- [x] Verification complete
- [x] QA recorded

## Simplification

- Result: No separate simplification pass needed.
- Reason: the implementation reused the existing provider and theme primitives, added one small value guard, and removed one forced class. Prettier-only formatting was applied to touched files.
- Checks rerun: `pnpm --filter web test`, `pnpm --filter web typecheck`, changed-file eslint, targeted Prettier check.

## Deviations

- Full `pnpm --filter web lint` is blocked by existing generated shadcndesign skill files under `apps/web/.agents/skills/import-variables/scripts/convert-colors.js` using `process` without a Node eslint environment. Changed-file eslint passed.
