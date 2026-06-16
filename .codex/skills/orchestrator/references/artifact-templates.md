# Artifact Templates

Use these templates as starting points. Delete sections that are truly irrelevant, but do not remove approval, scope, acceptance, or verification fields.

## design-contract.md

```markdown
# Design Contract: <feature name>

Date: <yyyy-mm-dd>
Status: Draft | Approved | Superseded
Owner: <requesting user/team>
Mode: feature | bugfix | design-polish | release

## Source

- Figma: <node URL or n/a>
- Flow frames inspected: <frame links or n/a>
- Component sources inspected: <component-set, state-matrix, library component, docs, or repo fallback links>
- Asset/icon sources inspected: <icon/library/asset links or n/a>
- Issue/brief: <URL or description>
- Screenshots inspected: <paths or URLs>
- Design system/kit: <shadcn, shadcndesign.com, custom, or n/a>
- Kit-specific skills/tools: <shadcndesign skills-codex, Figma MCP, shadcn MCP, shadcn CLI, or n/a>

## Subagent Discovery

- Used: yes | no
- If no, reason:
- Runtime/model limitation:

| Agent | Role | Question/task | Model | Effort | Scope | Output |
|---|---|---|---|---|---|---|
| <A1 or n/a> | <contract-explorer/security-reviewer/etc.> | <bounded ask> | <model or inherited> | <medium/high/xhigh> | <read-only paths/Figma/docs> | <finding or artifact> |

## Goal

<One paragraph describing the user value and product outcome.>

## Bugfix Context

- Applies: yes | no
- Bug summary:
- Severity: P0 | P1 | P2 | P3
- User impact:
- Affected surface:
- First known bad version/commit/deploy:
- Last known good version/commit/deploy:
- Frequency: always | intermittent | unknown
- Environment: local | preview | staging | production | CI | unknown
- Expected behavior:
- Actual behavior:
- Reproduction status: Reproduced | Not reproduced | Intermittent | Blocked | Not needed
- Reproduction steps:
- Evidence: <logs, screenshots, traces, failing commands, CI links, browser console/network errors>
- Suspected root cause:
- Suspect files/systems:
- Mitigation or rollback:
- Regression test plan:

## Scope

### In

- <Specific screen, route, component, behavior, data flow, or test>

### Out

- <Explicit non-goals>

## Scope Size And Slice Recommendation

- Recommended shape: Single issue | Parent flow with slices
- Reason:
- Approved implementation slice:

| Slice | Goal | In | Out | Dependencies | Release boundary |
|---|---|---|---|---|---|
| <1> | <outcome> | <scope> | <non-goals> | <blocked by/needs> | <can release independently?> |

## Affected Surface

- Routes:
- Components:
- Packages:
- Server actions/API/data:
- Auth/permissions:
- Analytics/observability:

## Figma Frames

| Frame | Node ID | State | Screenshot | Notes |
|---|---|---|---|---|
| <name> | <id> | <empty/loading/success/error/etc.> | <path or URL> | <notes> |

## Figma Library State Discovery

- Access status: Resolved | Partial | Blocked | Not needed
- Method: get_design_context | get_metadata | Figma Plugin API probe | component-set link | repo fallback
- Consuming frame source:
- Direct component-set or state-matrix source:
- Library/component-set links inspected:
- Component source fallback needed: yes | no
- Permission or runtime limitation:
- Fallback source when unresolved:

| Instance/control | Instance node | Source link | Discovery path | Main component | Component set | Remote | Key available | Variant/property metadata | Source/result |
|---|---|---|---|---|---|---|---|---|---|
| <Button> | <node id> | <frame/component/doc/repo link> | consuming frame/direct component link/repo fallback | <name> | <set name> | yes/no | yes/no | <State, Variant, Size, etc.> | <resolved/partial/blocked> |

## Asset And Icon Inventory

List every icon, logo, brand mark, illustration, photo, SVG/vector, bitmap, and external asset URL used by the target frames.

| Asset | Figma node | Type | Source/library | Export/source decision | Destination | Notes |
|---|---|---|---|---|---|---|
| <layers icon> | <node id> | icon/svg | HugeIcons/lucide/custom/unknown | Use repo library/Add dependency/Export asset/Approved fallback/Defer | <path or package> | <license or visual risk> |

## Component Primitive Inventory

| Figma primitive/block | Figma node/doc | Component source link | Repo component | Status | Notes |
|---|---|---|---|---|---|
| <Button> | <node/doc link> | <component-set/state-matrix/repo fallback> | `<Button>` | Installed/Missing/Custom | <variant, size, state> |

## Design-Visible Controls

List every visible interactive control from the design, even when it is not functional in this delivery.

| Control | Visible in Figma | Implementation decision | Functional scope | Notes |
|---|---|---|---|---|
| <Apple login button> | yes | Implemented/Visual placeholder/Hidden/Deferred/Open question | In/Out/Pending | <OAuth/provider/setup implications> |

## Component State Matrix

Map Figma visual states to repo runtime behavior. If the Figma library cannot be resolved, use repo primitives as the behavior source and state the limitation.

| Component/control | Figma state source link | Figma visual states | Repo behavior source | Required runtime states | Fallback/gaps | Acceptance impact |
|---|---|---|---|---|---|---|
| <Button primary> | <component-set/state-matrix/repo fallback> | <default/hover/pressed/disabled or unresolved> | `<Button>` / shadcn docs | hover, focus-visible, active, disabled, pointer, click/submit | <none or limitation> | <criterion or n/a> |

## Flow Map

- Entry:
- Step 1:
- Step 2:
- Success:
- Error/validation:
- Recovery:

## Shadcn Context

- Workspace checked:
- Command run:
- Style/base:
- Icon library:
- Installed components:
- Missing components:
- Docs/search/view commands used:

## Shadcndesign Context

- Applies: yes | no
- Docs inspected: https://www.shadcndesign.com/docs/agent-skills | n/a
- Figma MCP available: yes | no | unknown
- shadcn MCP/tooling available: yes | no | unknown
- Kit-specific Codex skill available: yes | no | unknown
- Kit capabilities used: generate-code | import-variables | none
- Registry alias: @shadcndesign | n/a
- Registry configured in: <components.json path or n/a>
- License env var present: yes | no | unknown
- License env var name: SHADCNDESIGN_LICENSE_KEY | n/a
- Registry commands run:
- Component/variable generation output:
- Blockers or fallbacks:

## UX Contract

### Visual

- Layout:
- Typography:
- Color/theme:
- Spacing:
- Icons/media:

### Responsive

- Desktop:
- Tablet:
- Mobile:

### Interaction States

- Default:
- Hover/focus/active:
- Loading:
- Empty:
- Error:
- Disabled:

### Accessibility

- Keyboard:
- Focus management:
- Labels/roles:
- Color contrast:

## Data Contract

- Inputs:
- Outputs:
- Persistence:
- Validation:
- Failure modes:

## Root Cause And Fix Contract

- Applies: bugfix | n/a
- Root cause:
- Fix strategy:
- Non-goals:
- Regression risk:
- Compatibility/migration impact:
- Observability/logging impact:
- Rollback plan:

## Security And Privacy

- Auth/authz impact:
- Tenant/data isolation:
- User data/PII:
- Secrets/config:
- Input handling:
- External services:
- File uploads/downloads:
- Database/RLS/migrations:
- New dependencies or registry installs:
- Required security review:

## Acceptance Criteria

- [ ] <Observable acceptance criterion>
- [ ] <For bugfix: original bug is reproduced before the fix or reproduction blocker is documented>
- [ ] <For bugfix: expected behavior is verified after the fix>
- [ ] <For bugfix: regression test added or test gap explicitly justified>

## Test Plan

- Unit:
- Integration:
- E2E:
- Browser E2E gate: Required | Optional | Not applicable
- Browser E2E scope:
- Browser E2E happy path:
- Browser E2E negative/recovery path:
- Browser E2E data/env:
- Browser E2E viewports:
- Browser E2E blockers:
- Manual/browser:
- Visual comparison:
- Security/privacy:

## Open Questions

- <Question or "None">

## Approval

- Status: Pending | Approved | Approved with edits
- Approver:
- Approved at:
- Notes:
```

## implementation-plan.md

```markdown
# Implementation Plan: <feature name>

Date: <yyyy-mm-dd>
Contract: ./design-contract.md
Status: Draft | In progress | Complete

## Approved Slice

- Parent flow:
- Slice:
- Scope boundary:
- Deferred slices:

## Bugfix Plan

- Applies: yes | no
- Reproduction command/path:
- Failing test or missing test:
- Suspected root cause:
- Minimal fix:
- Files allowed:
- Files off-limits:
- Regression test:
- Verification:
- Rollback/mitigation:

## Component Plan

- Existing primitives to reuse:
- Missing primitives to add:
- shadcn docs/search/view/dry-run commands:
- Components intentionally not added:

## Asset Plan

- Icons/assets to use from repo libraries:
- Icons/assets to export from Figma:
- New asset/icon dependencies:
- Approved substitutions:
- Assets intentionally deferred:
- Verification:

## Security Plan

- Sensitive surfaces:
- Auth/authz checks:
- Data isolation checks:
- Secret handling:
- Input validation:
- Dependency/registry review:
- External services and env vars:
- Security review owner:

## Simplification Plan

- Required: yes | no
- Owner: main agent | simplification-engineer
- Timing: after initial checks, before QA
- Frontend review scope:
- Backend review scope:
- Test review scope:
- Behavior-preservation checks:
- Result: Pending | Applied | No simplification needed | Blocked

## Browser E2E Plan

- Required: yes | no
- Reason:
- Owner: main agent | test-engineer | qa-reviewer
- Command:
- Routes/flows:
- Happy path:
- Negative/recovery path:
- Viewports:
- Test data/env:
- External service handling:
- Artifacts: screenshots | trace | console/network notes | none
- Result: Pending | Pass | Fail | Blocked | Deferred by approval

## Agent Roster

| Agent | Role | Task | Model | Effort | Write scope | Verification |
|---|---|---|---|---|---|---|
| <A1> | <prd-writer/frontend-engineer/backend-engineer/simplification-engineer/etc.> | <task> | <model or inherited> | <medium/high/xhigh> | <paths or read-only> | <checks> |

## Definition Of Done

- [ ] Acceptance criteria pass.
- [ ] Required verification commands pass or are documented as unavailable.
- [ ] Simplification pass completed or explicitly marked unnecessary.
- [ ] Browser E2E gate passes or is explicitly blocked/deferred with approval.
- [ ] QA has no unresolved required findings.
- [ ] Security/privacy gate passes.
- [ ] Required external services are verified or explicitly blocked/deferred with approval.
- [ ] Temporary workflow docs are summarized or removed unless explicitly kept.
- [ ] Deferred items are explicitly approved.

## Work Packages

### Package 1: <name>

- Owner: main agent | frontend-engineer | backend-engineer | test-engineer | simplification-engineer | qa-reviewer
- Write scope:
- Read scope:
- Must not edit:
- Depends on:
- Tasks:
  - [ ] <task>
- Verification:

## Integration Notes

- <Cross-package coordination, migrations, or sequencing>

## Simplification Result

- Frontend:
- Backend:
- Tests:
- Checks rerun:
- Behavior changes: none | <describe approved deviation>

## Deviations From Contract

- <Deviation, reason, approval status>
```

## qa-review.md

```markdown
# QA Review: <feature name>

Date: <yyyy-mm-dd>
Contract: ./design-contract.md
Status: Pass | Pass with notes | Fail

## Verification

- Lint:
- Typecheck:
- Unit tests:
- E2E tests:
- Browser E2E gate:
- Browser E2E command:
- Browser E2E environment/data:
- Browser E2E artifacts:
- Build:
- Browser/manual:
- Desktop/mobile:
- Bug reproduction:
- Bug regression test:
- Root cause verified:
- Approved slice boundary:
- Figma comparison:
- Asset/icon fidelity:
- Component primitive mapping:
- Flow transitions:
- Simplification pass:
- Security/privacy:

## Findings

| Priority | Finding | Evidence | Required Fix |
|---|---|---|---|
| P0/P1/P2/P3 | <issue> | <file, screenshot, command, or URL> | <fix> |

## Bugfix Verification

- Applies: yes | no
- Original bug reproduced before fix: yes | no | blocked
- Reproduction evidence:
- Root cause:
- Fix verified:
- Regression test:
- Remaining risk:

## Acceptance Criteria Check

- [ ] <criterion from contract>

## Accessibility Check

- Keyboard:
- Focus:
- Labels/roles:
- Contrast:

## Browser E2E Check

- Required: yes | no
- Reason:
- Happy path result:
- Negative/recovery path result:
- Desktop viewport:
- Mobile viewport:
- Console/network issues:
- Screenshots/traces:
- Blockers/deferred items:

## Security And Privacy Check

- Auth/authz:
- Tenant/data isolation:
- Secrets/config:
- Input handling:
- PII/logging:
- Dependencies/registry changes:
- Result: Pass | Pass with notes | Fail

## Release Readiness

- Ready: yes | no
- Blockers:
- Deferred notes:
- Loop status: Done | Continue fixes | Blocked
- Documentation cleanup: Done | Not needed | Blocked
```

## cleanup-summary.md

```markdown
# Cleanup Summary: <feature name>

Date: <yyyy-mm-dd>

## Durable Repo Docs Kept

- <path and reason, or "None">

## Temporary Docs Deleted

- <path and reason, or "None">

## Details Moved To PR Or Release Notes

- <summary>

## Deferred Cleanup

- <item and reason, or "None">
```

## fix-list.md

```markdown
# Fix List: <feature name>

Date: <yyyy-mm-dd>
QA Review: ./qa-review.md

| Status | Priority | Owner | Note | Verification |
|---|---|---|---|---|
| Todo/In progress/Done/Deferred | P0/P1/P2/P3 | <owner> | <note> | <result> |
```

## release-notes.md

```markdown
# Release Notes: <feature name>

Date: <yyyy-mm-dd>
Contract: ./design-contract.md

## Summary

<What changed and why.>

## User-Facing Changes

- <change>

## Technical Changes

- <change>

## Verification

- <command or manual check>: <result>

## Known Limitations

- <limitation or "None">

## Rollback

- <rollback path or "Revert the release commit/PR">
```
