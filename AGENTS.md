# Backdesk Agent Instructions

## Repo-Owned Codex Skills

- Use `.codex/skills/orchestrator/SKILL.md` when the user asks for Orchestrator, a Figma-to-implementation workflow, design contract, orchestrated subagent implementation, QA review loop, or release-ready feature delivery.
- For shadcn-backed Figma designs, make the handoff explicit: Figma frames, component primitive inventory, then flow map. Use the shadcn skill or shadcn CLI context before implementing UI.
- Keep workflow artifacts under `docs/codex/runs/<yyyy-mm-dd-feature-slug>/` so product, QA, and release decisions are reviewable by the team.
- Treat the design contract as an approval gate: do not implement until the user approves it.
- After implementation starts, loop through implementation, verification, QA, and fixes until acceptance criteria pass, required checks pass, security/privacy review passes, or a real blocker is documented.
- Before merge or release, clean up temporary workflow docs so draft contracts, plans, QA notes, and fix lists are not merged unless intentionally durable or explicitly requested.

## Existing Project Direction

- Preserve the product direction in `docs/superpowers/specs/2026-04-28-backdesk-v1-design.md`.
- Prefer existing Turborepo, Next.js, Supabase, shadcn/ui, and test patterns before adding new frameworks or abstractions.
