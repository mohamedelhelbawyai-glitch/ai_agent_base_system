# API Contract: [API Name]

> **Purpose:** Single source of truth for an API design, from requirements to a validated OpenAPI spec. Follows the `design-api` method: requirements → domain → standards → stories → OpenAPI spec → lint → review.
>
> **Authoring rule:** Describe the intended API behavior. Replace every `[...]` placeholder. Undecided items go under Open Questions. Never invent resources, fields, enum values, or error codes that are not in the Domain or Stories sections. The standards and best-practices rulesets win over personal preference.

## 0. Document Control

| Attribute | Value |
|---|---|
| API name | `[API_NAME]` |
| Owner / team | `[OWNER_OR_TEAM]` |
| Contract version | `[1.0.0]` |
| OpenAPI version | `[3.1.0]` |
| Spec file | `[path/to/openapi.json]` |
| Status | `[DRAFT / IN REVIEW / APPROVED / IMPLEMENTED]` |
| Consumers | `[Humans, mobile app, web app, AI agents, partners]` |
| Environments | `[dev]`, `[staging]`, `[production]` |

### Pipeline status

| Phase | Skill | Artifact | Status |
|---|---|---|---|
| 1. Stories | `design-api-stories` | Section 4 | `[PENDING / REVIEWED / APPROVED]` |
| 2. Spec | `design-api-spec` | Section 5 + spec file | `[PENDING / GENERATED / LINTED]` |
| 3. Review | `design-api-review` | Section 7 | `[PENDING / REPORTED / FIXED]` |

### Reading rules for the AI agent

1. Read sections in order: Requirements → Domain → Standards → Stories → Spec Summary → Review.
2. Use exact names, casing, enum values, and types from the Domain section. Do not rename or abbreviate.
3. Follow the Standards section for every convention. If it conflicts with the Domain or Stories, flag it instead of guessing.
4. Stories are the human's design decisions (nesting, grouping, parameters). Do not restructure them without approval.
5. Save the reviewed stories before generating the spec. The saved stories are the source of truth for the spec.
6. Review first, fix after. Do not modify the spec until the user has chosen which findings to fix.

## 1. Requirements

- **API goal:** `[What outcome this API enables]`
- **ICP / consumers:** `[Who calls this API and why]`
- **Needs and pain points:** `[What they struggle with today]`
- **Benefits:** `[What improves once the API exists]`
- **Out of scope:** `[What is NOT included]`

### Use cases

| ID | Actor | Use case | Theme |
|---|---|---|---|
| UC-01 | `[Actor]` | `[Goal in one sentence]` | `[Theme name]` |
| UC-02 | `[Actor]` | `[Goal in one sentence]` | `[Theme name]` |

## 2. Domain Model

> Source of truth for schemas. Every object becomes a component schema and every enum becomes its own component schema (never inline).

### Objects

#### `[ObjectName]`

| Property | Type | Required | Nullable | Description | Example |
|---|---|---|---|---|---|
| `id` | `string (uuid)` | `yes` | `no` | `[Unique identifier]` | `"1c6764cb-..."` |
| `[propertyName]` | `[type / enum ref / object ref]` | `[yes/no]` | `[yes/no]` | `[Meaning]` | `[value]` |
| `createdAt` | `string (date-time)` | `yes` | `no` | `[Creation time]` | `"2026-01-01T00:00:00Z"` |
| `updatedAt` | `string (date-time)` | `yes` | `no` | `[Last change]` | `"2026-01-01T00:00:00Z"` |

### Enums

| Enum | Allowed values | Used by |
|---|---|---|
| `[EnumName]` | `[value1, value2, value3]` | `[ObjectName.property]` |

### Relations

| From | Relation | To | Cardinality | Reference field |
|---|---|---|---|---|
| `[Parent]` | `has many` | `[Child]` | `1..*` | `[parentId]` |

## 3. API Standards

> Conventions the spec must follow. Replace defaults only where the project requires it, and justify each deviation in the last column.

| Area | Rule | Deviation / justification |
|---|---|---|
| Style | `HTTP REST, JSON only` | `[None]` |
| JSON fields | `camelCase; acronyms are words; primary key is "id"` | `[None]` |
| Query params | `camelCase, matched case-insensitively` | `[None]` |
| Path segments | `lowercase, kebab-case, pluralized, no trailing slash` | `[None]` |
| Path params | `camelCase, e.g. {taskId}` | `[None]` |
| Headers | `Hyphenated-Pascal-Case` | `[None]` |
| Enum values | `lowercase words` | `[None]` |
| Timestamps / booleans | `end in At; bare adjectives (completed, not isCompleted)` | `[None]` |
| Base path / versioning | `No /api or /v1 prefix; unversioned until a breaking change` | `[None]` |
| Nesting | `Nest collections to follow relations, max 3 levels; item operations stay flat` | `[None]` |
| IDs | `UUID; references named <resource>Id` | `[None]` |
| Collections | `Wrapper { data, meta }; every collection has a list endpoint` | `[None]` |
| Pagination | `offset / limit, documented default and max, stable default sort` | `[None]` |
| Creation | `201 + Location header` | `[None]` |
| Deletion | `204 No Content` | `[None]` |
| Errors | `RFC 9457 Problem Details, application/problem+json, field-level errors[]` | `[None]` |
| Auth | `[Bearer / OAuth2 / none]; 401 on every authenticated operation` | `[None]` |
| Rate limiting | `[Headers and 429 + Retry-After]` | `[None]` |
| Money / dates | `Decimal string + currency; ISO 8601 UTC` | `[None]` |

### OpenAPI best practices

- [ ] Every operation, parameter, schema property, response, and header has a `description` and an `example`.
- [ ] Every operation has a `summary` and a unique `operationId`.
- [ ] No inline schemas: everything lives in `components` and is referenced with `$ref`.
- [ ] Reusable parameters, responses, and headers live in `components`.
- [ ] No orphaned components.
- [ ] 3.1 nullability uses `"type": ["string", "null"]`, never `nullable`.
- [ ] `info` has contact and license, and `servers` has at least one entry with a description.
- [ ] One tag per story theme.

## 4. Stories

> Output of `design-api-stories`. Simple format by default (method, resource, parameters). Add the detailed fields only if requested. The approved stories drive the spec.

### Theme 1: [Theme Name]

#### Story 1.1: [Name]

**As a** [actor],
**I want** to [action],
**So that** [business value].

* **Method:** `[GET | POST | PUT | PATCH | DELETE]`
* **Resource:** `[/resources/{resourceId}]`
* **Parameters:**
  * `[paramName]` (`[type]`, `[required|optional]`): `[Description]`
* **Use case:** `[UC-01]`

<!-- Detailed format only (on request): -->
<!-- * **Success:** `[status]` — `[what is returned]` -->
<!-- * **Errors:** `[status]` — `[when it occurs]` -->
<!-- * **Headers:** `[rate limit, pagination, ...]` -->

### Story review checkpoint

| Date | Reviewer | Decision | Changes requested |
|---|---|---|---|
| `[YYYY-MM-DD]` | `[Name]` | `[APPROVED / CHANGES]` | `[Summary]` |

## 5. OpenAPI Spec Summary

> Generated by `design-api-spec`. The spec file is authoritative. This section is a readable index and must match it.

### Endpoint index

| ID | Operation ID | Method + path | Story | Purpose | Success | Errors |
|---|---|---|---|---|---|---|
| EP-01 | `[listResources]` | `GET /[resources]` | `1.1` | `[Purpose]` | `200` | `400, 401, 429, 500` |
| EP-02 | `[createResource]` | `POST /[resources]` | `1.2` | `[Purpose]` | `201` | `400, 401, 409, 429, 500` |
| EP-03 | `[getResource]` | `GET /[resources]/{resourceId}` | `1.3` | `[Purpose]` | `200` | `401, 404, 429, 500` |

### Component inventory

| Kind | Names |
|---|---|
| Schemas | `[Resource, ResourceCollection, ResourceCreate, ProblemDetails, ...]` |
| Parameters | `[offset, limit, resourceId, ...]` |
| Responses | `[BadRequest, Unauthorized, NotFound, TooManyRequests, InternalServerError]` |
| Headers | `[X-RateLimit-Limit, X-RateLimit-Remaining, Retry-After, ...]` |
| Security schemes | `[bearerAuth]` |

### Request and response examples

#### EP-02 — `POST /[resources]`

**Request:**

```json
{
  "[field]": "[example]"
}
```

**Success (`201`, `Location: /[resources]/{id}`):**

```json
{
  "id": "1c6764cb-0000-0000-0000-000000000000",
  "[field]": "[example]",
  "createdAt": "2026-01-01T00:00:00Z",
  "updatedAt": "2026-01-01T00:00:00Z"
}
```

**Error (`400`, `application/problem+json`):**

```json
{
  "type": "https://example.com/problems/validation-error",
  "title": "Validation failed",
  "status": 400,
  "detail": "One or more fields are invalid.",
  "errors": [
    { "field": "[field]", "message": "[What is wrong and how to fix it]" }
  ]
}
```

### Collection response shape

```json
{
  "data": [],
  "meta": { "totalCount": 0, "offset": 0, "limit": 20 }
}
```

## 6. Lint Results (RateMyOpenAPI)

| Run | Overall | Docs | Completeness | SDK generation | Security | Report |
|---|---|---|---|---|---|---|
| `1` | `[/100]` | `[/100]` | `[/100]` | `[/100]` | `[/100]` | `[URL or skipped]` |

**Target:** 100/100 in every category.

**Issues ignored by design (user-approved):**

| Issue code | Reason | Approved by |
|---|---|---|
| `[e.g. missing 401 on no-auth API]` | `[Intentional]` | `[Name]` |

## 7. Design Review

> Output of `design-api-review`. Findings only; fixes are applied after the user decides.

**Rulesets used:** `[Bundled / user-supplied standards]`, `[Bundled / user-supplied best practices]`
**Spec reviewed:** `[path / URL]`

### Verdict per standards section

| Section | Verdict | Findings |
|---|---|---|
| Casing | `[PASS / DIVERGES / N/A]` | `[count]` |
| Naming | `[...]` | `[...]` |
| Paths & Resources | `[...]` | `[...]` |
| Methods & Status Codes | `[...]` | `[...]` |
| IDs & References | `[...]` | `[...]` |
| Properties | `[...]` | `[...]` |
| Requests & Responses | `[...]` | `[...]` |
| Query Parameters & Pagination | `[...]` | `[...]` |
| Errors | `[...]` | `[...]` |
| Rate Limiting | `[...]` | `[...]` |
| Security | `[...]` | `[...]` |
| Versioning & Deprecation | `[...]` | `[...]` |
| OpenAPI best practices | `[...]` | `[...]` |

### Findings

| ID | Location in spec | Rule broken (cite section + number) | Severity | Decision | Status |
|---|---|---|---|---|---|
| F-01 | `[paths./resources.get]` | `[Standards §Paths, rule 3]` | `[ERROR / WARN]` | `[FIX / ACCEPT / DEFER]` | `OPEN` |

## 8. Acceptance Checklist

- [ ] Requirements, Domain, Standards, and OpenAPI best practices are all filled in.
- [ ] Every use case maps to at least one story.
- [ ] Every story maps to exactly one endpoint in the spec.
- [ ] Stories were reviewed and approved before spec generation.
- [ ] Every domain object and enum is a component schema, with exact property names.
- [ ] Every collection has a list endpoint with the standard wrapper and pagination.
- [ ] Every operation documents success and error responses (RFC 9457).
- [ ] Auth scheme and 401/403 responses match the Standards.
- [ ] Lint score is 100/100, or remaining issues are listed as approved deviations.
- [ ] Design review is complete and every finding has a decision.
- [ ] No credentials, tokens, or real user data appear in examples.

## 9. Open Questions / Blockers

| ID | Question / gap | Impact | Owner | Decision / resolution | Status |
|---|---|---|---|---|---|
| Q-01 | `[Example: Is cursor pagination required for this API?]` | `[Affects every list endpoint]` | `[Owner]` | `[TBD]` | `OPEN` |

## 10. Changelog

| Version | Date | Author | Change | Breaking? |
|---|---|---|---|---|
| `1.0.0` | `[YYYY-MM-DD]` | `[OWNER]` | `Initial contract` | `No` |

---

### Companion artifacts

- `[openapi.json]` — the generated OpenAPI spec (authoritative).
- `[swagger-preview.html]` — optional local Swagger UI preview.
