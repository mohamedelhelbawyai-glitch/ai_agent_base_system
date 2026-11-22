# API Handoff: [Feature / Subject Name]

> **Purpose:** Backend-to-mobile integration handoff. The mobile developer and coding agent should be able to integrate this feature without guessing API behavior.
>
> **Authoring rule:** Describe the actual API behavior. Replace `[TBD]` and `[EXAMPLE]` with complete backend-provided details. If something is undecided, keep it under Open Questions. Never invent fields, endpoints, error codes, or retry policies.

## 0. Document Control

| Attribute | Value |
|---|---|
| Feature / subject | `[FEATURE_NAME]` |
| Owner / team | `[BACKEND_OWNER_OR_TEAM]` |
| API version | `[v1 / ...]` |
| Handoff version | `[1.0.0]` |
| Environments | `[dev]`, `[staging]`, `[production]` |
| Consumer | `Mobile application (Android/iOS/Flutter)` |

### Reading rules for the mobile AI agent

1. Treat the documented API behavior as the integration reference; do **not** invent missing fields, statuses, endpoints, headers, or business rules.
2. Read **Feature Flow** before implementing individual endpoints, then **Endpoint Relationships**, **Shared Models**, and each relevant endpoint.
3. Use exact wire-level names, enum values, JSON types, and nullability; preserve numeric vs string IDs.
4. If any detail in this handoff is contradictory or incomplete, flag it for clarification instead of guessing.
5. Implement explicitly documented errors and retry/refresh behavior. Do not retry non-idempotent mutations without backend-approved safeguards.
6. Track unresolved questions as blockers; do not present assumptions as implemented behavior.
7. Do not copy real tokens, personal data, or credentials into examples, tests, or logs.

## 1. Feature Overview & Business Context

- **Feature goal:** `[What the user can accomplish]`
- **Users / roles:** `[Who can access it]`
- **Entry point / UI screens:** `[Screen names and IDs, links if available]`
- **Out of scope:** `[What is NOT included]`
- **Domain terms:** `[Term: definition]`
- **Business invariants:** `[Rules that must always hold]`

## 2. Global API Configuration

| Setting | Value / behavior |
|---|---|
| Base URL by environment | `[TBD]` |
| API prefix/version | `[e.g. /v1]` |
| Authorization | `[Bearer token / session / no auth]` |
| Required headers | `[Content-Type, Accept, locale, client version, etc.]` |
| Content types | `[application/json, multipart/form-data, ...]` |
| JSON naming convention | `[camelCase / snake_case]` |
| Timezone and datetime format | `[ISO 8601, UTC / TBD]` |
| IDs, amounts, and units | `[UUID vs int; minor currency units vs decimal]` |
| Success response envelope | `[raw JSON vs { data, meta }]` |
| Error response envelope | `[actual shape; RFC 9457 only if implemented]` |
| Token expiry/refresh handling | `[TBD]` |
| Timeout, rate limits, Retry-After | `[TBD]` |
| Pagination default/style | `[cursor / offset / not applicable]` |
| Null vs missing field semantics | `[TBD]` |
| Network and caching constraints | `[TBD]` |

## 3. Feature Flow / Endpoint Sequence

Describe the real screen-to-API interaction **in order**. Never assume that endpoint names alone convey the flow.

| Step | UI action / condition | Endpoint / operationId | Data consumed / produced | On failure / alternate path |
|---|---|---|---|---|
| 1 | `[Screen opens]` | `[GET /... | operationId]` | `[List/detail DTO]` | `[Empty/error state]` |
| 2 | `[User submits]` | `[POST /... | operationId]` | `[ID/status]` | `[Validation/conflict resolution]` |
| 3 | `[User follows up]` | `[GET /... | operationId]` | `[Updated state]` | `[Polling/timeout decision]` |

**State transitions:** `[DRAFT -> PENDING -> CONFIRMED / possible transitions and illegal transitions]`

**Preconditions:** `[Authentication, required resource state, prerequisites]`

**Concurrency and timing:** `[Race conditions, expiry rules, server time, simultaneous edits]`

## 4. Endpoint Index and Relationships

| ID | Operation ID | Method + path | Purpose | Depends on / produces for |
|---|---|---|---|---|
| EP-01 | `[listResources]` | `GET /[path]` | `[Display data]` | `none -> EP-02` |
| EP-02 | `[createResource]` | `POST /[path]` | `[Create record]` | `EP-01 -> EP-03` |
| EP-03 | `[getResource]` | `GET /[path]/{id}` | `[Fetch current state]` | `EP-02 -> UI detail` |

## 5. Endpoint Documentation

> Duplicate the following **entire endpoint section** for every endpoint. Include complete, sanitized request and response examples. If a section does not apply, write `N/A` and explain why. Preserve the stable `EP-xx` identifier.

### EP-01 — [METHOD] `[PATH]` — [Action / Purpose]

#### A. Context and Usage

- **operationId:** `[stable_unique_operation_id]`
- **Business purpose:** `[What this operation achieves]`
- **Called when:** `[Triggering UI action or lifecycle event]`
- **Preconditions:** `[Required authorization, prior steps, valid resource states]`
- **Authentication and permission:** `[scheme, role, scope, ownership constraints]`
- **Result and side effects:** `[Creates/updates/deletes? What else changes?]`
- **Related endpoints:** `[EP-02 (reason), EP-03 (reason)]`

#### B. Request Contract

| Input | Location | Wire type | Required | Nullable | Constraints / enum / meaning | Example |
|---|---|---|---|---|---|---|
| `[id]` | `path` | `string` | `yes` | `no` | `[UUID or format]` | `"res_123"` |
| `[limit]` | `query` | `integer` | `no` | `no` | `[default 20, max 100]` | `20` |
| `[field]` | `body` | `string` | `yes` | `no` | `[min/max, regex, enum]` | `"example"` |

**Required headers:** `[Content-Type, Authorization, If-Match, Idempotency-Key, ... as implemented]`

**Request example (valid JSON; replace with actual payload or N/A):**

```json
{
  "field": "example"
}
```

**Request semantics:** `[Missing vs null, optional fields, default values, file limits, sorting, filtering, units, timezone]`

#### C. Success Response

- **HTTP status:** `[200 / 201 / 202 / 204, as applicable]`
- **Content-Type:** `[application/json / ...]`
- **Response envelope:** `[raw object or wrapper, if any]`
- **No-content behavior:** `[204 or empty array, not assumed]`

**Complete success example (replace with the actual response shape):**

```json
{
  "id": "res_123",
  "status": "pending",
  "updatedAt": "2026-01-01T00:00:00Z"
}
```

| Response JSON path | Type | Nullable | Presence / condition | Meaning / UI usage |
|---|---|---|---|---|
| `id` | `string` | `no` | `always` | `[Used by EP-02 and EP-03]` |
| `status` | `string` | `no` | `always` | `[Use exact enum values]` |
| `updatedAt` | `string(date-time)` | `no` | `always` | `[Display / sorting / cache]` |

**Pagination / continuation:** `[cursor, nextCursor, hasMore, totalCount; N/A if irrelevant]`

#### D. Error Handling

> Error *code strings and payloads* must match the API behavior. Status codes below are examples; remove any that do not apply.

| HTTP | Stable backend code | Trigger / condition | Mobile UI behavior | Retry policy |
|---|---|---|---|---|
| `400/422` | `[VALIDATION_ERROR]` | `[Invalid form field]` | `[Map fieldErrors to inputs]` | `No automatic retry` |
| `401` | `[UNAUTHORIZED]` | `[Expired/missing session]` | `[Refresh/re-auth per global rules]` | `[Document exact rule]` |
| `403` | `[FORBIDDEN]` | `[User lacks permission]` | `[Access denied UI]` | `No` |
| `404` | `[NOT_FOUND]` | `[Missing or inaccessible resource]` | `[Not found UI]` | `No unless documented` |
| `409` | `[CONFLICT]` | `[Business/state conflict]` | `[Refresh relevant resource; explain conflict]` | `[TBD]` |
| `429` | `[RATE_LIMITED]` | `[Throttled]` | `[Rate-limit UI]` | `[Respect Retry-After if defined]` |
| `5xx` | `[SERVER_ERROR]` | `[Unexpected server problem]` | `[Generic recoverable error]` | `[Only safe/idempotent cases]` |

**Complete error example (`[Content-Type]`; replace with actual schema):**

```json
{
  "code": "CONFLICT",
  "message": "The requested action is not allowed in the current state."
}
```

**Transport failures:** `[No network / DNS / timeout / cancellation / malformed JSON: UI fallback and whether request outcome may be unknown]`

#### E. Edge Cases and Business Rules

| Scenario / boundary | Backend outcome | Required mobile handling | Test case ID |
|---|---|---|---|
| `[Resource already changed]` | `[status and error body]` | `[refresh and show conflict]` | `[TC-01]` |
| `[Empty result]` | `[status and exact payload]` | `[empty state]` | `[TC-02]` |
| `[Duplicate tap / retry]` | `[Idempotency behavior]` | `[disable CTA / use key as approved]` | `[TC-03]` |
| `[Expired session]` | `[status/body]` | `[refresh or login]` | `[TC-04]` |
| `[Boundary values / nulls]` | `[validation result]` | `[field error and safe parse]` | `[TC-05]` |

#### F. Endpoint Relationships and Integration Notes

- **Requires output from:** `[EP-xx, JSON path, and why]`
- **Supplies input to:** `[EP-yy, which field / why]`
- **State changes affecting:** `[Other endpoints and UI sections]`
- **Invalidate/refetch:** `[Cache keys or relevant resource queries after success]`
- **Ordering:** `[Can calls run concurrently? Must await previous result?]`
- **Polling / real-time:** `[Only if explicitly supported]`
- **Retry and idempotency:** `[Idempotency-Key, duplicate protection, safe retry semantics]`
- **Mobile mapping:** `[Screen + loading/success/empty/error/unauthorized/conflict state]`

#### G. Acceptance / Test Scenarios

- [ ] `[TC-01: Valid request returns documented success status/body.]`
- [ ] `[TC-02: Invalid request returns documented error and field mapping.]`
- [ ] `[TC-03: Empty/null/missing properties handled according to contract.]`
- [ ] `[TC-04: Unauthorized/forbidden cases handled correctly.]`
- [ ] `[TC-05: Cross-endpoint sequence works with a realistic ID.]`
- [ ] `[TC-06: Retry and duplicate-request behavior matches the backend.]`

<!-- Duplicate Section 5 for each additional endpoint; use EP-02, EP-03, etc. -->

## 6. Shared DTOs, Enums, and Validation

| DTO / enum | Fields / values | Type constraints | Used by endpoints |
|---|---|---|---|
| `[ResourceDto]` | `[id, status, createdAt]` | `[types, nullability]` | `[EP-01, EP-03]` |
| `[ResourceStatus]` | `[EXACT backend enum values]` | `[allowed transitions]` | `[EP-02, EP-03]` |

**Cross-field validation:** `[Conditions where one field is required if another has a specific value]`

**Date, amount, identifier conventions:** `[Specify units, representation, rounding and timezone]`

## 7. Screen-to-API and UI State Mapping

| Screen / event | Endpoint(s) | Loading | Success | Empty | Recoverable error | Terminal error |
|---|---|---|---|---|---|---|
| `[ListScreen:onEnter]` | `[EP-01]` | `[skeleton]` | `[render items]` | `[no-items UI]` | `[retry]` | `[login/forbidden]` |
| `[CreateScreen:onSubmit]` | `[EP-02 -> EP-03]` | `[disable submit]` | `[navigate/update]` | `N/A` | `[field errors]` | `[conflict/access denied]` |

**Offline behavior:** `[read cached data / fail fast / queue allowed mutations only if implemented]`

**PII / logging policy:** `[Sensitive field list; must not be logged or persisted unsafely]`

**Performance considerations:** `[page size, response size, debounce, concurrency limits]`

## 8. End-to-End Integration Acceptance Checklist

- [ ] All endpoint methods and paths explicitly documented.
- [ ] Auth, roles, token refresh, and required headers specified.
- [ ] Every request field has wire type, required/optional, nullable, validation, and example.
- [ ] Every response field has wire type, nullable, conditional presence, and complete example.
- [ ] All expected status codes and **actual** error response shapes documented.
- [ ] Business edge cases, timeouts, empty states, and concurrency covered.
- [ ] Endpoint dependencies, ordering, IDs, and cache invalidation explicit.
- [ ] Retry policy, idempotency, and unknown-outcome handling defined for mutations.
- [ ] Tests and mock fixtures cover at least one happy path, error, and boundary per operation.
- [ ] No live credentials, tokens, or real user data included.

## 9. Open Questions / Blockers

| ID | Question / gap | Impact | Owner | Decision / resolution | Status |
|---|---|---|---|---|---|
| Q-01 | `[Example: Can a timed-out POST be retried safely?]` | `[Risk of duplicate creation]` | `[Backend]` | `[TBD]` | `OPEN` |

## 10. Changelog

| Version | Date | Author | Change | Breaking for mobile? |
|---|---|---|---|---|
| `1.0.0` | `[YYYY-MM-DD]` | `[OWNER]` | `Initial handoff` | `No` |

---

### Optional companion artifacts

- `fixtures/` — sanitized JSON success/error examples used by mobile mock tests.

This Markdown file is the standalone backend-to-mobile API handoff for the feature.
