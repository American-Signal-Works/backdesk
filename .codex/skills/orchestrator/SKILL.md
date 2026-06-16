---
name: orchestrator
description: Run a Codex-owned product delivery orchestration workflow from a Figma design, feature brief, or bug report through design contract, user approval, Codex subagent implementation, QA review, fix pass, and merge or release. Use when the user asks for Orchestrator, a design-to-code workflow, Figma-to-implementation handoff, PRD/design contract generation, orchestrated subagents for feature implementation or bug fixing, QA review loops, or release-ready implementation from an approved contract.
---

# Orchestrator

## Purpose

Use this skill to convert a design or feature request into an auditable repo workflow:

1. Inspect Figma or source input.
2. Inventory components and primitives.
3. Map the user flow.
4. Generate a design contract.
5. Stop for user approval or edits.
6. Implement from the approved contract.
7. Run QA against the contract.
8. Fix QA notes.
9. Repeat implementation and QA until done or blocked.
10. Clean up temporary workflow artifacts.
11. Prepare merge or release artifacts.

The skill is Codex-discoverable, but the repo copy remains the team-reviewed source of truth. Write generated artifacts under `docs/codex/runs/<yyyy-mm-dd-feature-slug>/` unless the user specifies another location.

## Required Gates

- Do not implement before the design contract is approved.
- Do not broaden scope beyond the approved contract without updating the contract and getting approval.
- Do not merge, push, deploy, or release unless the user explicitly asks for that action.
- Keep artifacts in the repo so other team members can review the workflow history.
- Do not declare done while required acceptance criteria, verification, QA, or security/privacy checks are failing.
- Do not merge temporary run artifacts by default. Before release, decide what documentation is durable, summarize the rest, and remove unnecessary docs from the worktree.

## Completion Loop

After implementation begins, keep looping through implementation, verification, QA, and fixes until one of these outcomes is true:

- **Done**: all approved acceptance criteria pass, required verification commands pass or are documented as unavailable, QA has no unresolved required findings, and the security/privacy gate passes.
- **Blocked**: progress requires user approval, unavailable credentials, missing external services, an unresolved product decision, or a conflicting scope change.
- **Deferred by approval**: the user explicitly accepts a remaining issue as deferred.

When QA or verification fails, update `fix-list.md`, fix required notes, rerun the relevant checks, and update artifacts with the new result. Do not stop after producing a review if fixes are still in scope.

## Documentation Hygiene

Workflow docs are useful during orchestration, but they should not automatically become permanent repo content.

Before PR, merge, deploy, or release prep:

1. Review all docs created or modified during the run.
2. Keep only docs that are intentionally durable product, architecture, API, migration, or operational documentation.
3. Move useful temporary details into the PR description, release notes, commit message, or a compact `cleanup-summary.md` if the user wants an artifact.
4. Delete temporary run artifacts that would add noise to the codebase, especially draft contracts, intermediate plans, QA scratch notes, browser notes, and stale fix lists.
5. Keep generated artifacts only when the user explicitly wants the workflow history committed or the repo convention requires it.

Never delete user-authored docs or unrelated docs you did not create. When unsure whether a doc is durable, ask before deletion.

## Intake

Collect only the missing facts needed for the next gate. Prefer using available repo and Figma context over asking broad questions.

Required inputs:

- Source: Figma node URL, issue, bug report, or feature brief.
- Target surface: route, screen, component, flow, or package.
- Mode: `feature`, `bugfix`, `design-polish`, or `release`.
- Release expectation: local implementation, PR, merge, deploy, or release notes.

If a Figma URL is provided, use available Figma tooling to inspect the node and screenshot. If the URL is not node-specific, ask for a node-specific link before producing the final contract.

## Figma To Components To Flow

For Figma-backed work, structure intake in this order:

1. **Figma**: list frames, node IDs, screenshots inspected, frame names, and the state each frame represents.
2. **Components**: inventory Figma blocks, primitives, component variants, design-system docs links, repo component matches, and missing repo components.
3. **Flow**: describe the user actions, transitions, validation paths, and success/error states between frames.

Do not treat generated Figma code as implementation-ready. Use it as a visual and structural reference, then adapt it to the repo's framework, component library, tokens, and interaction patterns.

## Shadcn-Backed Designs

When the repo uses shadcn/ui or has `components.json`, use the shadcn skill or shadcn CLI context before writing a contract or implementation plan.

Required checks:

- Run project-aware shadcn context, for example `pnpm dlx shadcn@latest info --json`; in monorepos, pass the target workspace with `-c <workspace>`.
- Map each Figma primitive to an installed repo component before planning custom markup.
- For missing primitives, use `shadcn docs`, `shadcn search`, `shadcn view`, or `shadcn add --dry-run` before proposing an implementation.
- Prefer built-in component variants and semantic tokens over copied Figma CSS variables or raw color classes.
- Use form primitives correctly: `FieldGroup`, `Field`, `FieldLabel`, `FieldDescription`, `FieldError`, validation with `data-invalid` on `Field` and `aria-invalid` on the control.
- Use `Button`, `Separator`, `Skeleton`, `Empty`, `Badge`, `Card`, and related primitives instead of custom styled `div` replacements.
- For icons inside shadcn buttons, follow the project icon-library conventions and component icon API.

## Phase 1: Design Contract

Create `design-contract.md` using the template in `references/artifact-templates.md`.

The contract must include:

- Goal and user value.
- Source links and screenshots inspected.
- Figma frame inventory when applicable.
- Component primitive inventory and repo mapping.
- Flow map between frames or states.
- Affected routes, components, packages, data flows, and permissions.
- Visual, responsive, interaction, loading, empty, and error states.
- Accessibility expectations.
- Security and privacy risks.
- Test plan and acceptance criteria.
- Non-goals and open questions.

After writing the contract, stop and ask the user to approve or edit it. The next phase starts only after approval.

## Phase 2: Implementation Plan

After approval, create `implementation-plan.md` using the template in `references/artifact-templates.md`.

Plan work as small packages with clear ownership:

- Files or modules each worker may edit.
- Files or modules each worker must not edit.
- Installed component primitives to reuse.
- Missing components to add, update, or intentionally avoid.
- Security-sensitive files, flows, data, permissions, and dependencies.
- Dependencies between tasks.
- Verification expected from each task.

Use subagents when useful and available for disjoint work. The main agent remains the orchestrator and owns integration. Tell workers they are not alone in the codebase, must not revert others' edits, and must list changed paths in their final response.

Recommended roles:

- `contract-explorer`: answer specific codebase or Figma questions before implementation.
- `prd-writer`: produce or revise the design contract and acceptance criteria.
- `ui-worker`: implement component and styling changes.
- `data-worker`: implement server actions, API, schema, or data-flow changes.
- `test-worker`: add or update focused tests.
- `qa-reviewer`: review the integrated result against the contract.
- `security-reviewer`: review auth, data, secrets, external services, and dependency risk.
- `release-manager`: prepare PR description, release notes, or deployment checklist.

## Model Policy

When subagent tooling supports model or reasoning-effort overrides, assign them in the implementation plan before spawning agents. Use the smallest capable setting for bounded work and reserve highest reasoning for decisions that steer downstream work.

Default routing:

- `prd-writer`, contract approval analysis, and final QA: strongest available model, `xhigh` effort.
- `qa-reviewer` and `security-reviewer`: strongest available model, `xhigh` effort.
- `contract-explorer`: strong model, `high` effort; use `xhigh` only for ambiguous product, Figma, security, or architecture questions.
- `ui-worker`, `test-worker`, and routine implementation: workhorse model, `medium` effort.
- `data-worker`: workhorse model with `high` effort when touching auth, permissions, database, migrations, external services, or irreversible data changes; otherwise `medium`.
- `release-manager`: workhorse model, `medium` effort unless release risk is high.

Escalate planning and review to strongest model with `xhigh` effort when the feature touches authentication, authorization, secrets, PII, email delivery, payments, RLS, database migrations, dependency changes, public routes, generated content, or external APIs. Do not downgrade QA to save cost when the implementation affects security, privacy, data integrity, or release readiness.

Record model choices in the implementation plan's agent roster. If the runtime cannot enforce model choices, treat the roster as policy and state the limitation in the plan.

## Phase 3: Implementation

Implement from the approved plan.

Rules:

- Keep changes scoped to the contract.
- Follow existing repo patterns before adding new abstractions.
- Preserve user or unrelated worktree changes.
- Update the plan checklist as tasks complete.
- Record material deviations in `implementation-plan.md`.

## Security And Privacy Gate

Run a security/privacy review whenever the contract or diff touches authentication, authorization, user data, secrets, file uploads, external integrations, payments, database policies, migrations, dependency changes, public routes, or generated content.

Check for:

- Authentication bypass or broken redirect/callback behavior.
- Authorization and tenant isolation failures, including RLS policy gaps where applicable.
- Secret exposure in source, logs, browser payloads, screenshots, or generated artifacts.
- Unsafe input handling, XSS, injection, upload, SSRF, or open redirect paths.
- Overbroad data access, excessive logging, PII leakage, and missing retention/deletion expectations.
- New dependencies, scripts, or registry installs that need review.

For security-sensitive changes, use available security review skills/tools when present, especially diff-focused review before release. Record the outcome in `qa-review.md`.

## External Dependency Gate

If acceptance criteria require an external service such as Resend, Stripe, Supabase production resources, Sentry, or a model/API provider, the dependency is part of completion.

Before declaring done:

- Identify required accounts, domains, DNS, API keys, webhooks, env vars, rate limits, and billing or quota assumptions.
- Implement code behind documented env vars and never commit secrets.
- Mock the service in unit or integration tests where practical.
- Verify a real staging or production path when credentials and setup are available.
- Mark the run `Blocked` when required credentials, verified domains, DNS, billing, or service access are missing.
- Mark any unverified live-service behavior as `Deferred by approval` only when the user explicitly accepts it.

## Phase 4: QA Review

Create `qa-review.md` using the template in `references/artifact-templates.md`.

QA must compare the actual result against:

- Approved contract.
- Figma screenshot or feature source.
- Component primitive mapping.
- Flow transitions and validation paths.
- Desktop and mobile behavior when UI is involved.
- Test, lint, typecheck, and build output.
- Accessibility and keyboard interaction where relevant.

For frontend work, start the local dev server when needed and inspect the running app with browser tooling. Do not rely only on static code review for visual changes.

## Phase 5: Fix Notes

If QA finds issues, create or update `fix-list.md` with each note, owner, status, and verification. Fix all required notes before release preparation. If a note is intentionally deferred, mark it as deferred with the reason and get user approval when it changes shipped behavior.

After fixes, rerun the smallest meaningful verification set first, then rerun broader checks needed for release readiness. Continue the loop until the completion criteria are satisfied or the work is blocked.

## Phase 6: Merge Or Release

Only proceed when the user asks for PR, merge, deploy, or release.

Prepare:

- Summary of contract scope.
- Files changed.
- Verification run and results.
- Known limitations or deferred items.
- Rollback or follow-up notes when relevant.
- Documentation cleanup result: kept, summarized, deleted, or intentionally deferred.

Use `release-notes.md` from `references/artifact-templates.md` when release artifacts are requested.

## References

- Read `references/artifact-templates.md` when creating workflow artifacts.
