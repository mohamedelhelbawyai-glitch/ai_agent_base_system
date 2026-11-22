---
description: Global rule for any mobile project (Flutter, React Native, native Android/iOS, KMP). Forces the AI to discover and respect the project's README, packages, tools, structure, framework version, configs, and OS configs before changing anything.
alwaysApply: true
---

# Mobile Project Awareness Rule (Global)

> **Priority: HIGHEST.** This rule applies to every mobile project and runs before any other rule.
> The AI MUST NOT write, edit, or delete code, config, or dependencies until it has completed
> the **Context Gate**. Never assume a version, package, path, or convention. **Discover it from the repo.**

---

## 0. Core Principles

1. **Discover, don't assume.** Every fact about the project (versions, packages, structure, configs) must come from a file in the repo or from the user. If it can't be found, **ask**.
2. **Code and configs beat docs.** When the README (or any doc) disagrees with the actual files, trust the files, tell the user about the drift, and update the doc if your change touches it.
3. **Reuse before adding.** Use existing packages, helpers, handlers, and patterns before introducing new ones.
4. **Both platforms, always.** Any change that touches a permission, plugin, native API, or build setting must be checked for Android **and** iOS.
5. **Never touch secrets or generated files** (see §9).

---

## 1. The Context Gate (mandatory before every task)

Read these, in order, **before** making any change. Skip an item only if it doesn't exist.

| # | What to read | Why |
|---|--------------|-----|
| 1 | `README.md` (and `CONTRIBUTING.md`, `docs/`) | Purpose, setup, run/build commands. May be stale. |
| 2 | Agent/AI rule files: `.agents/`, `.cursor/rules/`, `CLAUDE.md`, `AGENTS.md`, `.github/copilot-instructions.md`, `.specify/memory/constitution.md` | Project-specific rules that add to this one. |
| 3 | Architecture docs: `ARCHITECTURE.md`, `docs/architecture*`, feature `.md` files | Layering, naming, state management. |
| 4 | Mistakes/lessons log, if present (e.g. `ai_agent_mistakes_log.md`) | Don't repeat past errors. |
| 5 | The dependency manifest + lockfile (see §3) | What packages and versions exist. |
| 6 | Lint/format/analysis config (see §8) | Rules the code must pass. |
| 7 | Env/config code (see §8) | How environments and secrets are loaded. |
| 8 | Spec/plan/task docs for the feature being changed (`specs/`, `docs/features/`, issues) | Requirements and contracts. |
| 9 | Android config files (see §6) | Only when the change touches native/Android-relevant things. |
| 10 | iOS config files (see §7) | Same triggers as Android. |

Then **start your reply with this block** (fill it with real values, no placeholders):

```
CONTEXT CHECK
- Framework & version: <e.g. Flutter 3.x / RN 0.7x / Kotlin+Swift native> (source: <file>)
- Language/SDK constraint: <file → value>
- Architecture & state mgmt: <pattern + library found in repo>
- Feature(s) touched: <names> (spec/docs read: yes/no)
- Packages used or added: <list> (already in manifest? yes/no)
- Platforms affected: Android / iOS / both / none
- Native config that must change too: <files or "none">
- README/doc drift found: <list or "none">
```

If you can't fill a line from the repo, ask the user before continuing.

---

## 2. Framework & Toolchain Versions

Find the real versions here. **Never use a version from memory.**

| Stack | Where to find the version |
|-------|---------------------------|
| **Flutter/Dart** | `pubspec.yaml` → `environment`; `pubspec.lock` → `sdks`; `.metadata`; `.fvm/fvm_config.json` / `.fvmrc`; CI `FLUTTER_VERSION` |
| **React Native** | `package.json` → `react-native`, `engines`; `.nvmrc` / `.node-version`; `app.json`/`app.config.*` (Expo SDK) |
| **Native Android** | `gradle/libs.versions.toml`, `build.gradle(.kts)`, `gradle-wrapper.properties`, `settings.gradle` (AGP, Kotlin, Gradle) |
| **Native iOS** | `Package.swift`, `Podfile`, `*.xcodeproj/project.pbxproj` (Swift version, deployment target), `.xcode-version` |
| **KMP** | `gradle/libs.versions.toml`, `build.gradle.kts`, `Podfile` for the iOS side |
| **CI/CD** | `.github/workflows/*`, `bitrise.yml`, `.gitlab-ci.yml`, `codemagic.yaml`, `fastlane/` |

Also record: Java/JDK version, Node/Ruby version (if used), minimum Android SDK, target/compile SDK, minimum iOS version.

Rules:
- Never use an API, lint, or package that requires a newer SDK than the project's without telling the user and bumping it **everywhere it's declared** (manifest, lockfile, CI, native files).
- Never downgrade a version to "make it compile" without asking.
- Never run SDK/dependency upgrade commands (`flutter upgrade`, `npm update`, `pod update`, major version bumps) unless asked.

---

## 3. Packages / Dependencies

**Manifest files to read:** `pubspec.yaml`, `package.json`, `build.gradle(.kts)` / `libs.versions.toml`, `Podfile`, `Package.swift`, `Cartfile`.
**Lockfiles (resolved versions):** `pubspec.lock`, `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml`, `Podfile.lock`, `Package.resolved`.

Before writing any import, check that the package is in the manifest. Before adding one:

1. **Check whether something already does the job**: an existing dependency, a project handler/helper/util, or the platform SDK.
2. **Justify it** to the user in one or two lines: what it does, why existing options don't, maintenance status.
3. **Verify it supports both Android and iOS**, plus the project's minimum OS versions and framework version.
4. **Add native setup in the same change**: manifest permissions, `Info.plist` usage strings, Podfile/Gradle settings, capabilities.
5. Respect the manifest's organization (groups, comments, ordering) and update the lockfile.
6. Don't add a second package for something the project already solves (e.g. a second state-management library, HTTP client, or DI container). **Follow the library the project already uses.**
7. If the architecture docs mention a package that is **not** in the manifest, trust the manifest and tell the user about the mismatch.

---

## 4. Tools & Workflow

Detect which of these exist and follow them. **Don't bypass them.**

| Tool | Detect via | Obligation |
|------|-----------|------------|
| Spec-driven workflow (Spec Kit etc.) | `.specify/`, `specs/` | Follow specify → plan → tasks → implement. Read the feature's spec, plan, contracts, and tasks first. Update `tasks.md`. |
| AI rules/skills | `.agents/`, `.claude/`, `.cursor/` | Load the skill that matches the area you're working in. |
| Code generation | `build_runner`, `freezed`, `json_serializable`, `openapi`, `codegen`, `graphql codegen` | Never hand-edit generated files. Re-run the generator. |
| Backend/service CLIs | `firebase.json`, `.firebaserc`, `supabase/`, `amplify/` | Use their CLIs to regenerate config. Never hand-edit generated config. |
| Release automation | `fastlane/`, `scripts/`, `Gemfile`, `eas.json`, `codemagic.yaml` | Use the lanes/scripts. Don't invent new release steps. |
| CI | `.github/workflows/`, etc. | Know what CI runs (analyze, test, build, deploy) and which platforms it covers. Report gaps (e.g. no iOS pipeline). |
| Env/version managers | `.fvm*`, `.nvmrc`, `.tool-versions`, `asdf` | Use the pinned version. |
| Linters/formatters | See §8 | Run before finishing. |

**Verification commands** (use the ones that match the stack, taken from README/CI/scripts):

| Stack | Typical commands |
|-------|------------------|
| Flutter | `flutter pub get`, `dart format .`, `flutter analyze`, `flutter test`, `flutter build apk|appbundle|ios` |
| React Native | `npm|yarn install`, `npx tsc --noEmit`, `npm run lint`, `npm test`, `npx pod-install` |
| Android | `./gradlew lint test assembleDebug` |
| iOS | `xcodebuild test`, `pod install`, `swiftlint` |

If the project defines its own run/build flags (e.g. `--dart-define`, flavors, schemes, build variants), **use them exactly as documented in CI or scripts.**

---

## 5. Project Folder Structure

Before creating, moving, or importing any file:

1. **Map the tree.** List the top-level directories and the source root (`lib/`, `src/`, `app/src/main/`, `Sources/`).
2. **Identify the organization style**: feature-first, layer-first, modular (multi-module/monorepo), or MVVM/MVC/Clean/BLoC/Redux.
3. **Open an existing, similar feature** and mirror its layout, file naming, and class naming exactly.
4. **Locate the shared homes** for: global state, models, widgets/components, utilities/extensions, handlers/services, constants/configs, routes/navigation, theme/styles, localization, assets.
5. **Reuse before duplicating.** Check shared state/models/components before creating new ones. Duplicating something that already has a global owner is a violation.

Rules:
- Put files where the project's pattern says they go. Don't invent new top-level folders.
- Respect dependency direction (e.g. presentation → domain ← data). Don't import across features if the project forbids it. Share via the shared layer instead.
- Match layering depth to the feature's complexity. Don't build a full multi-layer stack for a thin UI screen if sibling UI-only features don't.
- New routes go in the route registry. New strings go in **every** localization file plus the keys file. New assets go in the asset folder, the asset keys/registry, and the manifest (`pubspec.yaml` assets, etc.).
- Tests mirror the source path. Keep that convention.
- Keep a feature context `.md` up to date if the project uses one.

---

## 6. Android Config Awareness

Read the relevant ones before any change that touches permissions, plugins, builds, signing, notifications, deep links, or native code.

| File | What to extract |
|------|-----------------|
| `android/app/build.gradle(.kts)` or `app/build.gradle(.kts)` | `namespace`, `applicationId`, `minSdk`, `targetSdk`, `compileSdk`, Java/Kotlin target, desugaring, flavors, build types, signing config, ProGuard/R8 |
| `android/build.gradle(.kts)`, `settings.gradle(.kts)` | AGP, Kotlin, Gradle plugin versions, repositories, project-wide workarounds (don't remove them without understanding why) |
| `gradle.properties`, `gradle/wrapper/gradle-wrapper.properties` | JVM args, AndroidX/Jetifier, Gradle version, feature flags |
| `src/main/AndroidManifest.xml` (+ `debug/`, `profile/`, flavor manifests) | Permissions, `uses-feature`, activities, services, receivers, intent filters, `queries`, meta-data (e.g. notification channel/icon), launch mode |
| `src/main/res/**` | Themes, launch screen, icons, `values-night`, strings, network security config |
| `google-services.json` / `local.properties` / `key.properties` | Backend config (generated), SDK path, signing (secret) |
| `MainActivity.(kt|java)` / `Application` class | Package must match `applicationId`/`namespace`; custom native init |
| `fastlane/`, `Gemfile` | Release lanes, tracks, stages |

Rules:
- **New permission** → update the manifest, add the runtime request, add rationale where required, and update the privacy policy.
- Respect Android-version behavior (Android 13+ notification permission, exact alarms on 12+, background location rules, foreground service types, 16 KB page size, edge-to-edge).
- Never change `applicationId`/`namespace`, notification channel IDs, or deep-link schemes without asking. That can break updates and existing pushes.
- Never commit keystores, `key.properties`, or service-account JSON.

---

## 7. iOS Config Awareness

Read the relevant ones before any change that touches permissions, plugins, builds, signing, push, deep links, or native code.

| File | What to extract |
|------|-----------------|
| `ios/Podfile` (+ `Podfile.lock`) / `Package.swift` | Minimum iOS platform, `use_frameworks!`/static linking, `post_install` fixes, target structure |
| `*.xcodeproj/project.pbxproj` | Bundle ID(s), deployment target, Swift version, build configurations, schemes, signing team, entitlements path, extensions/targets |
| `Runner|<App>/Info.plist` | Display name, `NS*UsageDescription` strings, `UIBackgroundModes`, URL schemes, `LSApplicationQueriesSchemes`, scene manifest, orientations, ATS exceptions |
| `*.entitlements` | Push (`aps-environment`), Sign in with Apple, associated domains, app groups, keychain sharing |
| `AppDelegate.swift` / `SceneDelegate.swift` | Lifecycle, plugin registration, push registration, deep-link handling |
| `GoogleService-Info.plist` | Backend config (generated). Don't edit by hand. |
| `Assets.xcassets`, `*.storyboard`, `LaunchScreen` | Icons, launch screen |
| `*.xcconfig`, `Flutter/` or `ios/.xcode.env` | Build settings (framework-managed. Edit with care.) |

Rules:
- **Any plugin that touches a protected resource** (camera, mic, photos, location, contacts, Bluetooth, tracking, etc.) needs a matching `NS*UsageDescription` in plain user-facing language. Template/placeholder strings are an App Store rejection risk. Flag them.
- **Don't declare capabilities the app doesn't use** (e.g. "Always" location when only when-in-use is needed). Flag mismatches.
- **Push notifications** need the entitlement, the Background Modes capability, and APNs configuration. Check that they exist before claiming push works on iOS.
- Raising the minimum iOS version means changing the Podfile (or Package.swift) **and** the deployment target together.
- Treat `project.pbxproj` as fragile. Make minimal, targeted edits and never reformat it.
- Don't run `pod update` or alter lockfiles unless asked.
- If something can only be verified on macOS/Xcode, say so instead of claiming it works.

**Cross-platform parity check.** For every native-touching change, state the Android side and the iOS side explicitly. If one is intentionally not needed, say why.

---

## 8. Project Configs

Locate and obey:

| Area | Files to look for |
|------|-------------------|
| Lint / format | `analysis_options.yaml`, `.eslintrc*`, `.prettierrc*`, `.editorconfig`, `ktlint`/`detekt` configs, `.swiftlint.yml` |
| Type/compile | `tsconfig.json`, `babel.config.js`, `metro.config.js` |
| Environments | `.env*`, `assets/env/`, `app_env.*`, `config/`, build flavors/schemes, `--dart-define`, `app.config.*`, `BuildConfig` |
| Endpoints / constants | `*end_points*`, `constants/`, `configurations/` |
| Localization | `assets/lang/`, `l10n.yaml`, `*.arb`, `strings.xml`, `Localizable.strings`, i18n JSON |
| Theme / design tokens | `theme`, `colors`, `typography`, design-system folders |
| Navigation | route files, navigator/router setup |
| App entry & boot order | `main.dart`, `index.js`, `App.tsx`, `Application`, `AppDelegate`. Note the **initialization order**, because it often matters. |
| Backend/services | Firebase, Supabase, Sentry, analytics, crash reporting configs |
| Hosting / legal | privacy policy, terms, store listing metadata |

Rules:
- Access env/config **only through the project's config layer**. Never read raw env vars or files from feature code.
- Don't hardcode endpoints, keys, persistence keys, error strings, or colors if the project has a home for them.
- Code must pass the project's linter and formatter with **no new warnings**.
- Don't relax lint rules to hide problems.

---

## 9. Secrets & Generated Files (never touch)

- **Never commit or print**: `.env*` (except `.env.example`), keystores (`*.jks`, `*.keystore`), `key.properties`, `*.p12`, `*.mobileprovision`, service-account JSON, API keys, tokens, signing passwords.
- **Never hand-edit generated files**: `*.g.dart`, `*.freezed.dart`, `firebase_options.dart`, `google-services.json`, `GoogleService-Info.plist`, `GeneratedPluginRegistrant.*`, `Podfile.lock`/`pubspec.lock`/`package-lock.json` (only tools update these), build outputs. Regenerate with the proper CLI.
- If you find a hardcoded secret, **report it. Don't copy it** into replies, logs, tests, or docs.
- Release/signing secrets come from CI secrets or local untracked files, never from the repo.

---

## 10. README & Docs Awareness

- The README is a **starting point, not truth**. Compare it with the manifest, configs, and CI. List any drift in your CONTEXT CHECK block.
- If your change alters anything the README documents (setup, env, run/build commands, folder structure, features, tech stack), **update the README in the same change**.
- If your change adds a data type, permission, SDK, or third-party processor, update the privacy policy/store disclosures or tell the user they need updating.
- Keep architecture docs and feature context files in sync with what you build.

---

## 11. When Unsure

Stop and ask the user when:
- A version, flavor, environment, or platform target can't be determined from the repo.
- Two sources conflict and the code doesn't settle it.
- The change needs a new dependency, new permission, new capability, or a version bump.
- The change would modify signing, bundle/app ID, notification channels, deep-link schemes, or CI/release flow.
- The task seems to require an action only possible on the other OS (e.g. Xcode steps while on Linux).

Ask one concise question with a recommended default. Don't guess and proceed.

---

## 12. Final Checklist (end of every task)

- [ ] Context Gate completed and CONTEXT CHECK block shown
- [ ] Used existing packages/helpers. New dependency justified, with native setup for **both** platforms
- [ ] Android and iOS impact stated (permissions, manifest, plist, entitlements, min versions)
- [ ] Files placed following the project's structure and naming
- [ ] Strings/routes/assets registered in every place the project requires
- [ ] Linter/analyzer clean, formatter run, tests pass, new logic covered by tests in the mirrored path
- [ ] README / architecture docs / privacy policy / spec tasks updated where affected
- [ ] No secrets, generated files, or signing material edited or exposed
- [ ] Anything that couldn't be verified (e.g. iOS on a non-Mac) is stated plainly
- [ ] New AI mistakes appended to the project's mistakes log, if one exists
