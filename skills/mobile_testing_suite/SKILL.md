---
name: mobil_testing_suite
description: End-to-end guide for building a complete test suite for a Flutter/Dart mobile app and auditing the tests that already exist. Combines unit tests, mocking, widget tests, integration tests, `package:checks` assertions and coverage into one workflow. Use this skill whenever the user asks to "test the app", "build a test suite", "add tests", "check/audit/review existing tests", "improve coverage", "find untested code", or "set up testing" for a Flutter or Dart project, even if they only mention one kind of test (unit, widget, integration, mocks, coverage).
metadata:
  composes: dart-add-unit-test, dart-generate-test-mocks, dart-migrate-to-checks-package, flutter-add-widget-test, flutter-add-integration-test, dart-collect-coverage, dart-run-static-analysis
---
# Mobile Testing Suite (Flutter/Dart)

Orchestrates the individual testing skills into one pipeline: **audit what exists → plan what is missing → build tests layer by layer → measure coverage → report.** Each phase points to the specialised skill that holds the detailed syntax; load it when you reach that phase rather than up front.

| Layer | Specialised skill | Lives in |
|---|---|---|
| Unit (logic, models, repos, cubits/blocs) | `dart-add-unit-test` | `test/` mirroring `lib/` |
| Mocks for external dependencies | `dart-generate-test-mocks` | `*.mocks.dart` next to the test |
| Widget (single screen/component) | `flutter-add-widget-test` | `test/` |
| Integration (full user flows) | `flutter-add-integration-test` | `integration_test/` |
| Assertion style | `dart-migrate-to-checks-package` | all test files |
| Coverage | `dart-collect-coverage` | `coverage/lcov.info` |
| Static quality gate | `dart-run-static-analysis` | whole package |

Work in the order below. Skipping the audit leads to duplicate tests and to building on a suite that was already broken, so do it first even when the user only asked for new tests.

---

## Phase 0 — Orient

1. Confirm the project type: `pubspec.yaml` has `flutter:` → use `flutter test`; pure Dart → `dart test`. For a monorepo/workspace, handle each package separately.
2. Detect the stack so tests match it: state management (`bloc`/`flutter_bloc`, `riverpod`, `provider`), networking (`http`, `dio`), storage, DI (`get_it`), routing (`go_router`), serialization. Check `dev_dependencies` for `flutter_test`, `test`, `mockito`, `mocktail`, `bloc_test`, `integration_test`, `checks`, `coverage`, `build_runner`.
3. **Reuse the project's existing choices** (mockito vs mocktail, `expect` vs `checks`). Only introduce a new library when none exists. Do not mix mocking libraries.
4. Read the project's architecture (layers like data/domain/presentation, or UI/logic/data). Test targets follow those layers.

## Phase 1 — Audit existing tests

Skip to Phase 2 only if `test/` and `integration_test/` do not exist. Otherwise gather facts before judging:

1. **Run the suite as-is**: `flutter test` (or `dart test`), then `flutter test integration_test` if a device/emulator is available. Record pass/fail/skip counts and every failure's cause. Distinguish *broken tests* (stale after refactors) from *real bugs*.
2. **Static check**: run `dart analyze` (see `dart-run-static-analysis`) on `test/` and `integration_test/`.
3. **Inventory**: list every `lib/**/*.dart` file that has logic (exclude generated `*.g.dart`, `*.freezed.dart`, `*.mocks.dart`, `l10n`) and map it to its `*_test.dart`. Files with no counterpart are the **gap list**.
4. **Quality smells** to grep for and report:
   - Structure: test file not mirroring `lib/` path, missing `_test.dart` suffix, tests not wrapped in `group()`.
   - Skipped/disabled tests: `skip:`, `// TODO`, commented-out tests.
   - Weak assertions: tests with no `expect`/`check`, only `isNotNull`, or only asserting that nothing threw.
   - Over-mocking: mocking the class under test, or `verify` with no outcome assertion.
   - Async mistakes: `thenReturn` on a `Future`/`Stream` (must be `thenAnswer`), un-awaited futures, `pumpAndSettle` with infinite animations, missing `pump` after interaction.
   - Flakiness: real network, real clock/`DateTime.now()`, `Future.delayed` waits, shared mutable state across tests (missing `setUp`).
   - Fragile finders: `find.byType` for repeated widgets where a `ValueKey` is needed.
   - Legacy assertions: `expect(...)` across the suite (candidate for `package:checks`; migrate only if the user wants it or the project already uses checks).
   - Happy-path only: no error, empty, loading, boundary, or offline cases.
5. **Baseline coverage**: follow `dart-collect-coverage` (`dart run coverage:test_with_coverage`, or `flutter test --coverage`). Summarise per-file percentages from `coverage/lcov.info`; list files under ~60% and untested logic-heavy files first.

**Deliver an audit report before writing code** (see the template at the end). Fix broken tests as part of the audit only when the cause is clearly a stale test; if a failure looks like a real app bug, report it and ask rather than "fixing" the assertion to match buggy behaviour.

## Phase 2 — Plan the suite

Prioritise by risk and by test-pyramid cost. Aim for many unit tests, a moderate number of widget tests, and few integration tests.

1. Build the target list from the gap list, ranked: business logic and state holders → data layer (repositories, API clients, serialization) → screens with conditional UI → shared widgets → critical user journeys.
2. For each target write one line: *what behaviour is verified* and *which layer*. Present the plan to the user when it is large (more than ~15 files) so they can trim scope.
3. Identify testability blockers (hard-coded `http.Client()`, singletons, `DateTime.now()`, static calls). Prefer small refactors that inject the dependency through the constructor over testing around them. Tell the user about any production-code change you make.

## Phase 3 — Build, layer by layer

Always run each layer's tests green before moving up. A failing lower layer makes upper-layer failures misleading.

### 3a. Unit tests (`dart-add-unit-test`)
- `test/<path mirroring lib>/<name>_test.dart`, with `main()`, `group()` per class/method, `setUp()` for fresh instances.
- Test: normal paths, boundaries, invalid input, thrown errors, and async completion/error.
- Pure model/serialization tests: round-trip `fromJson`/`toJson`, missing and null fields.
- State holders (Cubit/Bloc): initial state, each event/method → expected state sequence, failure states. Use `bloc_test` if the project already depends on it.

### 3b. Mocks (`dart-generate-test-mocks`)
- Mock only *external boundaries* (API client, database, platform plugins, repositories when testing a cubit) — never the class under test.
- `@GenerateNiceMocks([MockSpec<T>()])` in the test file, import `<test>.mocks.dart`, then `dart run build_runner build --delete-conflicting-outputs`.
- `thenAnswer((_) async => v)` for any `Future`/`Stream`; `thenReturn` only for synchronous values.
- Assert on outcomes first; use `verify(...)` to confirm the interaction that matters, not every call.

### 3c. Widget tests (`flutter-add-widget-test`)
- One file per screen/reusable widget. Wrap in `MaterialApp` (plus the project's providers/blocs/localizations/theme) via a shared `pumpApp` helper in `test/helpers/` so each test stays short.
- Cover: initial render, loading, data, empty, and error states; taps, text entry, scrolling, validation messages, navigation triggers.
- `pump()` after a simple state change; `pumpAndSettle()` for animations/transitions. If it times out, an animation never ends — pump explicit durations instead.
- Feed the widget fake/mocked dependencies; no real network.
- Use `ValueKey`s for elements that repeat or are hard to target; add the keys to production code when missing.

### 3d. Integration tests (`flutter-add-integration-test`)
- Reserve for critical journeys (launch → login → main task → logout, purchase, onboarding). Keep each flow independent.
- Setup: `integration_test` dependency, `integration_test/<flow>_test.dart` with `IntegrationTestWidgetsFlutterBinding.ensureInitialized()`, `test_driver/integration_test.dart` for `flutter drive`.
- Use fakes or a test backend/flavor so results are deterministic. If the Dart MCP server is connected, explore the flow interactively first (as that skill describes), then convert it into a permanent test.
- Needs a device/emulator; if none is available, write the tests, verify they compile (`dart analyze`), and say clearly that they were not executed.

### 3e. Assertion style (`dart-migrate-to-checks-package`)
- Match what the project already uses. Do not migrate the whole suite unprompted; new tests may use `package:checks` only if it is already a dependency or the user asks. When migrating, use `deepEquals` for collections, `RegExp` objects for patterns, and `because:` instead of `reason:`.

## Phase 4 — Verify and measure

1. `dart analyze` / `flutter analyze` clean on the test code (`dart fix --apply` for mechanical lints).
2. Full run: `flutter test` (or `dart test`). Everything green, nothing newly skipped. Run twice, or with `--test-randomize-ordering-seed random`, to expose order-dependent or flaky tests.
3. Coverage again with `dart-collect-coverage`. Compare to the Phase 1 baseline. Use `// coverage:ignore-*` only for generated or genuinely untestable code, never to hide gaps.
4. Treat coverage as a gap-finder, not a goal: a high number from tests without assertions is worse than a lower honest one. If the user gave a target (e.g. 80%), report how far each layer is from it.

## Phase 5 — Report

Finish with a short report, in this shape:

```
## Test suite report
**Audit (before):** X tests, Y passing / Z failing / S skipped; coverage N%
**Issues found:** grouped by severity (broken, flaky, weak, structural) with file refs
**Added:** unit (n files / m tests), widget (…), integration (…), mocks generated
**Fixed/changed:** stale tests repaired, production code changed for testability (list)
**After:** X' tests, coverage N'%, lowest-covered files remaining
**Not done / needs the user:** e.g. integration tests not executed (no device), suspected app bugs
**How to run:** exact commands
```

## Ground rules

- Never weaken or delete a failing test to get a green run; explain why it was changed.
- Never modify production behaviour beyond injection-style refactors without telling the user.
- Do not commit generated coverage output (`coverage/`) or mocks unless the project already tracks them.
- Keep tests deterministic: no real network, time, randomness, or ordering dependence.
- If the project is not Flutter/Dart, say so and stop; this skill does not apply.
