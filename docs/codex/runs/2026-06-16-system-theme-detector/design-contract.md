# Design Contract: System Theme Detector

Date: 2026-06-16
Status: Approved
Owner: Backdesk
Mode: feature

## Source

- Figma: n/a
- Flow frames inspected: n/a
- Component sources inspected: repo fallback in `apps/web/components/theme-provider.tsx`, `apps/web/components/settings/AppearanceForm.tsx`, `apps/web/app/layout.tsx`, `apps/web/components/auth/LoginAuthFlow.tsx`
- Asset/icon sources inspected: n/a
- Issue/brief: user request, "Add a theme detector if system is in light or dark mode and auto switch."
- Screenshots inspected: n/a
- Design system/kit: shadcn/ui via `apps/web/components.json` and `packages/ui/components.json`
- Kit-specific skills/tools: Orchestrator skill, shadcn skill guidance, `pnpm dlx shadcn@latest info --json -c apps/web`

## Subagent Discovery

- Used: no
- If no, reason: simple single-surface behavior change with one primary provider and known repo files.
- Runtime/model limitation: none

| Agent | Role | Question/task | Model | Effort | Scope | Output |
| ----- | ---- | ------------- | ----- | ------ | ----- | ------ |
| n/a   | n/a  | n/a           | n/a   | n/a    | n/a   | n/a    |

## Goal

When a user selects System theme mode, Backdesk should detect whether the operating system is currently light or dark, apply the matching app theme, and update automatically when the OS preference changes. Explicit Light and Dark modes should remain fixed until the user changes them.

## Scope

### In

- Use the existing `next-themes` dependency and `ThemeProvider` instead of adding a new theme package.
- Ensure the root app theme can initialize from `profiles.theme_mode` when available, falling back to `system`.
- Preserve `enableSystem` behavior so `system` follows `prefers-color-scheme` and live OS changes.
- Keep the Appearance settings `Light / Dark / System` control as the user-facing mode selector.
- Remove forced-dark styling from the login/auth surface so auth can follow the resolved theme.
- Add focused tests around the changed behavior where practical.

### Out

- New visual theme switcher UI beyond the existing Appearance settings control.
- Changing accent colors, shadcn preset tokens, or the global palette.
- Adding a new theme dependency.
- Persisting command-palette or keyboard-shortcut theme changes to Supabase.
- Reworking auth UI layout or copy.

## Scope Size And Slice Recommendation

- Recommended shape: Single issue
- Reason: the change is provider/settings/auth-surface wiring with no schema, external service, or multi-route product flow.
- Approved implementation slice: Slice 1

| Slice | Goal                                         | In                                                                                     | Out                                               | Dependencies                                           | Release boundary          |
| ----- | -------------------------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------------ | ------------------------- |
| 1     | System mode follows OS light/dark preference | Provider initialization, settings mode wiring, auth forced-dark cleanup, focused tests | New theme UI, palette redesign, DB schema changes | Existing `next-themes`, existing `profiles.theme_mode` | Can release independently |

## Affected Surface

- Routes: all routes through `apps/web/app/layout.tsx`; `/settings/appearance`; login/auth route using `LoginAuthFlow`
- Components: `ThemeProvider`, `AppearanceForm`, `LoginAuthFlow`, possibly command-palette theme commands for compatibility checks
- Packages: `apps/web`; no expected `packages/ui` edits unless a test needs shared CSS behavior documented
- Server actions/API/data: read existing `profiles.theme_mode`; keep existing `updateAppearance`
- Auth/permissions: no auth logic change; root layout already reads the current user profile
- Analytics/observability: no change

## Figma Frames

| Frame | Node ID | State | Screenshot | Notes                            |
| ----- | ------- | ----- | ---------- | -------------------------------- |
| n/a   | n/a     | n/a   | n/a        | No Figma source for this feature |

## Figma Library State Discovery

- Access status: Not needed
- Method: repo fallback
- Consuming frame source: n/a
- Direct component-set or state-matrix source: n/a
- Library/component-set links inspected: n/a
- Component source fallback needed: yes
- Permission or runtime limitation: n/a
- Fallback source when unresolved: installed shadcn primitives and current repo components

| Instance/control  | Instance node | Source link      | Discovery path | Main component | Component set | Remote | Key available | Variant/property metadata        | Source/result |
| ----------------- | ------------- | ---------------- | -------------- | -------------- | ------------- | ------ | ------------- | -------------------------------- | ------------- |
| Theme mode toggle | n/a           | `AppearanceForm` | repo fallback  | `ToggleGroup`  | n/a           | no     | no            | `light`, `dark`, `system` values | resolved      |

## Asset And Icon Inventory

| Asset | Figma node | Type | Source/library | Export/source decision | Destination | Notes                           |
| ----- | ---------- | ---- | -------------- | ---------------------- | ----------- | ------------------------------- |
| n/a   | n/a        | n/a  | n/a            | Defer/omit             | n/a         | No new assets or icons expected |

## Component Primitive Inventory

| Figma primitive/block | Figma node/doc | Component source link | Repo component                   | Status    | Notes                                                                   |
| --------------------- | -------------- | --------------------- | -------------------------------- | --------- | ----------------------------------------------------------------------- |
| Theme provider        | n/a            | repo fallback         | `next-themes` provider wrapper   | Installed | Current provider already has `defaultTheme="system"` and `enableSystem` |
| Theme mode selector   | n/a            | repo fallback         | `ToggleGroup`, `ToggleGroupItem` | Installed | Existing values are `light`, `dark`, `system`                           |
| Login shell           | n/a            | repo fallback         | custom `LoginAuthFlow`           | Installed | Currently has a forced `dark` class that should be removed or scoped    |

## Design-Visible Controls

| Control                        | Visible in Figma | Implementation decision    | Functional scope | Notes                                                                      |
| ------------------------------ | ---------------- | -------------------------- | ---------------- | -------------------------------------------------------------------------- |
| Appearance theme mode toggle   | no Figma source  | Implemented                | In               | Continue selecting and saving Light, Dark, or System                       |
| Command palette theme commands | no Figma source  | Existing behavior retained | Out              | Current commands call `setTheme`; DB persistence is not part of this slice |
| `d` keyboard theme hotkey      | no Figma source  | Existing behavior retained | Out              | Hotkey toggles explicit light/dark based on resolved theme                 |

## Component State Matrix

| Component/control            | Figma state source link | Figma visual states | Repo behavior source                                   | Required runtime states                                                                      | Fallback/gaps                                        | Acceptance impact |
| ---------------------------- | ----------------------- | ------------------- | ------------------------------------------------------ | -------------------------------------------------------------------------------------------- | ---------------------------------------------------- | ----------------- |
| `ThemeProvider`              | repo fallback           | n/a                 | `next-themes` with `attribute="class"`, `enableSystem` | system resolves to light/dark, updates on OS change, avoids transition flash where supported | Need ensure persisted profile mode is passed at boot | Required          |
| `AppearanceForm` mode toggle | repo fallback           | n/a                 | `ToggleGroup`                                          | selected light/dark/system, keyboard focus, click selection                                  | No new visual state requested                        | Required          |
| `LoginAuthFlow` wrapper      | repo fallback           | n/a                 | app theme class on `<html>`                            | follows app resolved theme instead of forcing dark                                           | Current hardcoded `dark` class blocks light mode     | Required          |

## Flow Map

- Entry: app loads through `RootLayout`.
- Step 1: root reads the signed-in user's `profiles.theme_mode` and `profiles.theme_accent` when available.
- Step 2: `ThemeProvider` initializes with the persisted theme mode or `system`.
- Step 3: when mode is `system`, `next-themes` detects `prefers-color-scheme` and applies the matching `light` or `dark` class behavior.
- Success: changing OS appearance from light to dark, or dark to light, updates Backdesk automatically while System is active.
- Error/validation: invalid profile values fall back to `system`; unauthenticated users use `system`.
- Recovery: users can override with explicit Light or Dark in Appearance settings.

## Shadcn Context

- Workspace checked: `apps/web`
- Command run: `pnpm dlx shadcn@latest info --json -c apps/web`
- Style/base: `radix-vega`, `radix`
- Icon library: `lucide`
- Installed components: includes `button`, `field`, `toggle-group`, `sonner`, `tooltip`, and related primitives
- Missing components: none expected
- Docs/search/view commands used: not needed; no new component added

## Shadcndesign Context

- Applies: no
- Docs inspected: n/a
- Figma MCP available: unknown
- shadcn MCP/tooling available: shadcn CLI available
- Kit-specific Codex skill available: not used
- Kit capabilities used: none
- Registry alias: `@shadcndesign`
- Registry configured in: `apps/web/components.json`, `packages/ui/components.json`
- License env var present: unknown
- License env var name: `SHADCNDESIGN_LICENSE_KEY`
- Registry commands run: none
- Component/variable generation output: none
- Blockers or fallbacks: none for this feature

## UX Contract

### Visual

- Layout: no layout changes.
- Typography: no typography changes.
- Color/theme: resolved app theme follows OS when System is active; explicit Light/Dark remain stable.
- Spacing: no spacing changes.
- Icons/media: no icon or media changes.

### Responsive

- Desktop: system theme follows OS preference.
- Tablet: same behavior as desktop.
- Mobile: same behavior as desktop where the browser exposes `prefers-color-scheme`.

### Interaction States

- Default: unauthenticated and first-time users default to System.
- Hover/focus/active: unchanged shadcn `ToggleGroup` behavior.
- Loading: no new loading state.
- Empty: no new empty state.
- Error: invalid or absent profile theme falls back to System.
- Disabled: no new disabled state.

### Accessibility

- Keyboard: existing ToggleGroup keyboard behavior remains intact.
- Focus management: no focus management changes.
- Labels/roles: no new visible controls; existing settings labels remain.
- Color contrast: both light and dark token sets must remain usable.

## Data Contract

- Inputs: `profiles.theme_mode`, `profiles.theme_accent`, `window.matchMedia("(prefers-color-scheme: dark)")`.
- Outputs: app theme class behavior on `<html>` via `next-themes`; existing `data-accent` attribute.
- Persistence: Appearance settings continue writing `theme_mode` and `theme_accent` through `updateAppearance`.
- Validation: accepted theme modes remain `light`, `dark`, `system`.
- Failure modes: missing user, missing profile, or unknown values fall back to `system` without throwing.

## Security And Privacy

- Auth/authz impact: root layout still only reads the current authenticated user's profile.
- Tenant/data isolation: no workspace or tenant data touched.
- User data/PII: theme preference only; no PII added.
- Secrets/config: no new env vars or secrets.
- Input handling: theme mode stays constrained to existing enum values.
- External services: Supabase profile read already exists; no new external service.
- File uploads/downloads: none.
- Database/RLS/migrations: no migration expected.
- New dependencies or registry installs: none.
- Required security review: lightweight review only; no sensitive flow change expected.

## Acceptance Criteria

- [ ] With `theme_mode` unset or `system`, the app resolves to dark when the OS/browser preference is dark.
- [ ] With `theme_mode` unset or `system`, the app resolves to light when the OS/browser preference is light.
- [ ] While System mode is active, changing the OS/browser color scheme updates the app without a manual refresh.
- [ ] Explicit Light mode stays light even if OS preference is dark.
- [ ] Explicit Dark mode stays dark even if OS preference is light.
- [ ] `/settings/appearance` still saves Light, Dark, and System using the existing `profiles.theme_mode` path.
- [ ] Login/auth UI no longer forces dark mode and follows the resolved app theme.
- [ ] No new dependency, schema migration, or shadcn component install is introduced.

## Test Plan

- Unit: add or update Vitest tests for `ThemeProvider`/system behavior if practical with JSDOM `matchMedia`; add a `LoginAuthFlow` assertion that the root auth wrapper no longer forces `dark`.
- Integration: verify `AppearanceForm` still calls the existing update action when selecting Light, Dark, and System if existing mocks allow it.
- E2E: optional local browser check with emulated light and dark color schemes if the app can run without missing auth/env blockers.
- Manual/browser: start the web app after implementation and inspect light/dark/system behavior on a route that renders without additional setup.
- Visual comparison: confirm no layout regressions on login and appearance settings.
- Security/privacy: confirm no new secrets, dependencies, schema changes, or broader profile reads.

## Open Questions

- None. Approval means implement the single slice above.

## Approval

- Status: Approved
- Approver: User
- Approved at: 2026-06-16
- Notes: Approved in chat with "Looks good".
