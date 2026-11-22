# Feature: [Feature Name]

> **Purpose:** Product and UI context for a single mobile feature. A developer or coding agent should be able to understand what to build, why, and how it should behave without guessing.
>
> **Authoring rule:** Describe the intended behavior. Replace every `[...]` placeholder. If something is undecided, put it under Section 14 (Open Questions). Never invent screens, rules, or API behavior that is not stated here or in the linked design and API documents.

## 0. Document Control

| Attribute | Value |
|---|---|
| Feature | `[FEATURE_NAME]` |
| Owner (product / design / engineering) | `[NAMES_OR_TEAMS]` |
| Platforms | `[Android / iOS / Flutter]` |
| Status | `[DRAFT / READY / IN PROGRESS / DONE]` |
| Version | `[1.0.0]` |
| Related docs | `[API contract, API handoff, design file links]` |

### Reading rules for the AI agent

1. Read all sections before implementing. Section 5 (flows) and Section 8 (rules) take priority over assumptions.
2. Use the exact names, copy, and values given here. Do not invent screens, states, or rules.
3. If a detail is missing or contradictory, flag it as a blocker instead of guessing.
4. Treat Section 3 (Out of Scope) as a hard boundary.
5. Take data shapes and endpoints from the API documents linked in Section 9, not from this file.

## 1. Feature Overview

- **Summary:** `[One or two sentences describing the feature]`
- **Problem it solves:** `[The user pain or business need]`
- **Target users / roles:** `[Who uses it]`
- **Entry points:** `[Where the user reaches it: tab, button, deep link, notification]`
- **Success metric:** `[How success is measured, if known]`

## 2. Business Goals & User Stories

### Business goals

- `[Goal 1]`
- `[Goal 2]`

### User stories

| ID | As a | I want to | So that | Priority |
|---|---|---|---|---|
| US-01 | `[role]` | `[action]` | `[value]` | `[Must / Should / Could]` |
| US-02 | `[role]` | `[action]` | `[value]` | `[Must / Should / Could]` |

## 3. Scope & Out of Scope

### In scope

- `[Capability or screen included]`

### Out of scope

- `[Explicitly excluded capability, planned for later or never]`

## 4. Screens & Design References

| Screen ID | Screen name | Purpose | Design link | Status |
|---|---|---|---|---|
| SC-01 | `[Screen name]` | `[What the user does here]` | `[Figma / image link]` | `[Final / Draft]` |
| SC-02 | `[Screen name]` | `[Purpose]` | `[Link]` | `[Final / Draft]` |

**Design system notes:** `[Tokens, components, theming, or typography this feature must reuse]`

## 5. User Flows & Navigation

### Main flow

1. `[User opens SC-01 from the entry point]`
2. `[User performs action]`
3. `[System responds / navigates to SC-02]`

### Alternate flows

| Flow | Trigger | Steps | Ends at |
|---|---|---|---|
| `[Cancel]` | `[User taps back]` | `[Steps]` | `[Screen]` |

### Navigation map

| From | Action | To | Transition / back behavior |
|---|---|---|---|
| `SC-01` | `[Tap item]` | `SC-02` | `[Push; back returns to SC-01]` |

**Deep links / entry via notification:** `[Route patterns, or N/A]`

## 6. UI Components & Interactions

| Screen | Component | Behavior / interaction | Notes (copy, validation, a11y) |
|---|---|---|---|
| `SC-01` | `[Search field]` | `[Debounced 300 ms, clears on tap of X]` | `[Placeholder: "..."]` |
| `SC-01` | `[Primary button]` | `[Disabled until form valid]` | `[Label: "..."]` |

**Gestures:** `[Swipe, long-press, pull-to-refresh, or N/A]`

**Accessibility:** `[Labels, focus order, dynamic type, contrast requirements]`

## 7. UI States

| Screen / component | Loading | Success / content | Empty | Error (recoverable) | Error (terminal) | Other (offline, partial, locked) |
|---|---|---|---|---|---|---|
| `SC-01` | `[Skeleton]` | `[List of items]` | `[Illustration + CTA]` | `[Inline message + Retry]` | `[Full-screen error]` | `[Banner when offline]` |

## 8. Business Rules & Validations

### Business rules

| ID | Rule | Applies to | Source |
|---|---|---|---|
| BR-01 | `[Rule that must always hold]` | `[Screen / flow]` | `[Product / legal / backend]` |

### Field validations

| Field | Screen | Required | Rules (format, length, range) | Error message |
|---|---|---|---|---|
| `[email]` | `SC-02` | `yes` | `[Valid email, max 254 chars]` | `"[Exact copy]"` |

**Permissions / roles:** `[Who can see or do what]`

## 9. Data Requirements & API Dependencies

### Data needed per screen

| Screen | Data displayed / collected | Source | Refresh policy |
|---|---|---|---|
| `SC-01` | `[Item list]` | `[API / local / device]` | `[On enter, pull-to-refresh]` |

### API dependencies

| Endpoint / operationId | Used by (screen / action) | Doc link | Status (ready / mocked / pending) |
|---|---|---|---|
| `[GET /resources]` | `[SC-01:onEnter]` | `[API handoff section]` | `[Ready]` |

**Local storage / caching:** `[What is persisted, for how long, and how it is invalidated]`

## 10. Edge Cases & Error Handling

| Scenario | Expected behavior | User-facing message / UI | Related rule / state |
|---|---|---|---|
| `[No network on submit]` | `[Keep form data; allow retry]` | `"[Copy]"` | `[Section 7]` |
| `[Session expired]` | `[Refresh token, else sign out]` | `"[Copy]"` | `[BR-xx]` |
| `[Duplicate tap]` | `[Disable button during request]` | `[N/A]` | `[SC-02]` |
| `[Empty / max-length / boundary data]` | `[Behavior]` | `"[Copy]"` | `[Validation]` |

## 11. Mobile-Specific Behavior

| Topic | Behavior |
|---|---|
| Offline / poor connectivity | `[Read cache, queue, or fail fast]` |
| App lifecycle (background / kill / restore) | `[State restoration, draft saving]` |
| Permissions (camera, location, notifications) | `[When requested, copy, behavior on denial]` |
| Push notifications / deep links | `[Payloads and routing, or N/A]` |
| Orientation, screen sizes, tablets | `[Supported layouts]` |
| Keyboard, safe areas, insets | `[Handling]` |
| Platform differences (Android vs iOS) | `[Deviations, if any]` |
| Performance (list size, images, startup) | `[Targets and constraints]` |
| Localization / RTL / accessibility | `[Supported locales, RTL handling]` |
| Analytics / logging / PII | `[Events to track, fields never to log]` |

## 12. Feature Dependencies

| Dependency | Type | Needed for | Status / owner |
|---|---|---|---|
| `[Auth feature]` | `[Feature / service / SDK / flag]` | `[Session and user ID]` | `[Ready / pending]` |

**Feature flags / remote config:** `[Flag names and default values, or N/A]`

**Blocks / is blocked by:** `[Other features or tickets]`

## 13. Acceptance Criteria

| ID | Criterion (Given / When / Then) | Story | Verified by |
|---|---|---|---|
| AC-01 | `Given [state], when [action], then [outcome]` | `US-01` | `[Manual / unit / widget / integration test]` |
| AC-02 | `Given [state], when [action], then [outcome]` | `US-02` | `[...]` |

### Definition of done

- [ ] All in-scope screens implemented and match the design references.
- [ ] All UI states in Section 7 implemented.
- [ ] Business rules and validations in Section 8 enforced.
- [ ] Edge cases in Section 10 handled.
- [ ] Mobile-specific behavior in Section 11 verified.
- [ ] Acceptance criteria pass.
- [ ] No open blockers remain in Section 14.

## 14. Assumptions & Open Questions

### Assumptions

| ID | Assumption | Risk if wrong | Owner to confirm |
|---|---|---|---|
| A-01 | `[Assumption]` | `[Impact]` | `[Owner]` |

### Open questions

| ID | Question / gap | Impact | Owner | Decision / resolution | Status |
|---|---|---|---|---|---|
| Q-01 | `[Question]` | `[Blocks SC-02]` | `[Owner]` | `[TBD]` | `OPEN` |

## 15. Changelog

| Version | Date | Author | Change |
|---|---|---|---|
| `1.0.0` | `[YYYY-MM-DD]` | `[OWNER]` | `Initial feature context` |
