# AGENTS Guidelines for This Repository

This repository contains a mobile application with a non-trivial security posture (iOS, Android, Flutter, and/or React Native). When working on the project interactively with an AI coding agent, please follow the guidelines below so the agent makes choices that are secure by default and align with OWASP MASVS.

## 1. Threat Model (Pragmatic Minimum)
Every non-trivial change should be evaluated against a lightweight threat model:
- **Attackers in scope:** network attacker (MITM, hostile Wi-Fi), local attacker (lost/stolen device, shared device), malicious app co-resident on the device, and a motivated reverse engineer with the APK/IPA.
- **Assets:** user credentials, session tokens, PII, payment data, customer content, and signing / API keys that ship with the app.
- **Not in scope by default:** nation-state actors with kernel exploits, compromised OEM firmware, and physical chip extraction — unless the product explicitly requires it.

## 2. Defense in Depth
No single control is sufficient. Layer:
- TLS + certificate pinning (network).
- Hardware-backed keys + biometric gating (storage / auth).
- App Attest / Play Integrity (API abuse).
- R8 / obfuscation + signature checks (code integrity).
- Server-side authorization and rate limits (assume the client is compromised).

Never rely on a single control. Never assume the client is trustworthy.

## 3. Secure Storage Defaults
- **Never** store secrets, tokens, or PII in `SharedPreferences`, `NSUserDefaults`, `localStorage`, or a plain SQLite DB.
- Use **platform keystores** (Android Keystore / iOS Keychain) for key material and short opaque tokens.
- Use **EncryptedSharedPreferences**, **Tink**, or `EncryptedFile` on Android, and `kSecAttrAccessible*ThisDeviceOnly` classes on iOS.
- For structured data, use **SQLCipher** (or Realm encryption) with a key wrapped by the platform keystore — not a hard-coded key.

## 4. Certificate Pinning (With Kill Switch)
- Pin to the **SPKI SHA-256** of the leaf or an intermediate — never the full certificate.
- Ship **at least one backup pin** that is not currently live.
- Provide a remote kill switch (server-driven config flag) so a misissued pin cannot brick the app.
- Pin only production hostnames; do not pin debug / staging traffic.

## 5. No Secrets in Source
- API keys, OAuth client secrets, signing keys, and third-party tokens must not live in the repo, `gradle.properties`, `Info.plist`, `.env`, or `strings.xml`.
- Public keys (for pinning, verification) are fine.
- Use **gitleaks** in CI and block merges on findings.
- Rotate any secret that has ever been committed, including in history.

## 6. Authentication on Mobile
- **OAuth 2.1 + PKCE** is the default for user login. No password grant. No implicit flow.
- Use **AppAuth** (Android / iOS) or an equivalent audited library — do not hand-roll the flow.
- Store refresh tokens in the keystore/keychain, access tokens in memory where feasible.
- Biometric-gated operations must be bound to a **keystore key** that requires user authentication — not a boolean "user unlocked".

## 7. OWASP MASVS Alignment
All code changes should preserve or improve the project's standing against OWASP MASVS v2:
- **MASVS-STORAGE** — sensitive data is not left in insecure locations.
- **MASVS-CRYPTO** — only platform / audited crypto; no hand-rolled primitives.
- **MASVS-AUTH** — authentication and session management follow the flows above.
- **MASVS-NETWORK** — TLS everywhere, pinning on sensitive endpoints.
- **MASVS-PLATFORM** — safe IPC, safe WebView, safe deep links.
- **MASVS-CODE** — updated dependencies, safe handling of user input.
- **MASVS-RESILIENCE** — reasonable anti-tamper and integrity checks for high-risk apps (banking, crypto, health).
- **MASVS-PRIVACY** — collect the minimum, disclose it, and honor user choices.

## 8. Privacy by Default
- Collect the **minimum** data needed for the feature to work.
- Bind every collection to a **documented purpose**; do not repurpose silently.
- Honor platform consent frameworks: **App Tracking Transparency** on iOS, **User Messaging Platform** (UMP) on Android where applicable.
- Provide working data-export and data-deletion paths (DSAR) — they are both a legal and an engineering requirement.

## 9. Vulnerability & Dependency Hygiene
- Enable **Dependabot** / **Snyk** / `gradle-versions-plugin` / `pod outdated` in CI.
- Fail the build on **critical** CVEs in direct dependencies.
- Review transitive dependency changes in PRs — do not merge "update 87 packages" without a diff.

## 10. Useful Agent Skills Recap

| Skill Folder    | Purpose                                                    |
| --------------- | ---------------------------------------------------------- |
| `storage/`      | Keystore / Keychain, encrypted prefs, SQLCipher.           |
| `auth/`         | OAuth + PKCE, biometric auth, MFA, token handling.         |
| `network/`      | TLS pinning, App Attest / Play Integrity, MITM posture.    |
| `code/`         | Obfuscation, anti-tampering, root / jailbreak detection.   |
| `secrets/`      | No-secrets-in-client policy, build-time secret scanning.   |
| `privacy/`      | Privacy-by-design, ATT / UMP consent flows.                |
| `vuln/`         | MASVS alignment, dependency scanning.                      |
| `compliance/`   | GDPR / CCPA on mobile, DSAR and deletion.                  |

---

Following these practices keeps the agent-assisted development workflow aligned with a realistic, defensible mobile security posture. When in doubt, always refer to the specific agent skills provided in `.github/skills/`.

*Note to developers: Update this file whenever the threat model, platform baseline, or compliance posture changes so AI agents stay aligned with reality.*
