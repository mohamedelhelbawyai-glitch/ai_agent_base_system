# Awesome Mobile Security Agent Skills

[![Agent Skills](https://img.shields.io/badge/Agent-Skills-blue?style=flat&logo=github)](https://agentskills.io)
[![Security](https://img.shields.io/badge/Mobile-Security-critical?style=flat&logo=owasp)](https://owasp.org/www-project-mobile-app-security/)
[![OWASP MASVS](https://img.shields.io/badge/OWASP-MASVS-orange?style=flat&logo=owasp)](https://mas.owasp.org/MASVS/)
[![License: MIT](https://img.shields.io/badge/Code-MIT-green?style=flat)](LICENSE-CODE)
[![License: CC BY 4.0](https://img.shields.io/badge/Docs-CC%20BY%204.0-lightgrey?style=flat)](LICENSE-DOCS)

A collection of **20 agent skills** that give AI coding assistants (GitHub Copilot, Claude, Gemini, Cursor, etc.) expert-level knowledge of modern mobile application security across iOS, Android, Flutter, and React Native.

Drop the `.github/skills/` folder into your project and your agent automatically enforces MASVS-aligned defaults, avoids common footguns (hard-coded secrets, disabled TLS, world-readable storage), and ships code that passes review.

> Learn more about the Agent Skills standard at [agentskills.io](https://agentskills.io).

---

## Why use this

- **Platform-aware defaults** -- Android Keystore, iOS Keychain, StrongBox/SE, Secure Enclave, and their cross-platform wrappers covered as first-class.
- **MASVS-aligned** -- each skill maps to OWASP MASVS v2 controls (MASVS-STORAGE, MASVS-CRYPTO, MASVS-AUTH, MASVS-NETWORK, MASVS-PLATFORM, MASVS-CODE, MASVS-RESILIENCE, MASVS-PRIVACY).
- **Pragmatic, not paranoid** -- skills explain where RASP, jailbreak detection, and obfuscation actually help and where they don't.
- **Actionable checklists** -- every skill ends with a verification checklist the agent can self-audit against.

---

## How it works

The `Agent.md` file is the foundation. Every AI agent reads it first to understand your security conventions. Individual skills layer on top for specific tasks.

```text
       ┌───────────────────────────────────────────┐
       │                  Agent.md                 │
       │     (read by all AI agents implicitly)    │
       └─────────────────────┬─────────────────────┘
                             │
     ┌──────────┬────────────┼────────────┬──────────┐
     ▼          ▼            ▼            ▼          ▼
┌─────────┐ ┌───────┐ ┌───────────┐ ┌─────────┐ ┌──────────┐
│ Storage │ │ Auth  │ │  Network  │ │  Code   │ │ Privacy  │
├─────────┤ ├───────┤ ├───────────┤ ├─────────┤ ├──────────┤
│keystore │ │oauth  │ │tls-pin    │ │obfusc.  │ │ by-design│
│secure-  │ │tokens │ │app-attest │ │anti-    │ │ consent  │
│ storage │ │biometr│ │mitm       │ │ tamper  │ │ gdpr     │
│sqlcipher│ │mfa    │ │           │ │rootjail │ │          │
└─────────┘ └───────┘ └───────────┘ └─────────┘ └──────────┘
```

---

## Available Skills

All skills live in `.github/skills/<category>/<skill-name>/SKILL.md`.

### Storage

| Skill | What it covers |
|-------|----------------|
| [Secure Storage](.github/skills/storage/secure-storage/SKILL.md) | EncryptedSharedPreferences / Tink, iOS Keychain, `flutter_secure_storage`, `react-native-keychain` |
| [Keystore & Keychain](.github/skills/storage/keystore-keychain/SKILL.md) | Android Keystore (StrongBox / TEE), iOS Keychain access control, biometric-gated keys |
| [Encrypted Databases](.github/skills/storage/encrypted-databases/SKILL.md) | SQLCipher, Room + `EncryptedFile`, Realm encryption |

### Authentication

| Skill | What it covers |
|-------|----------------|
| [OAuth on Mobile](.github/skills/auth/oauth-mobile/SKILL.md) | OAuth 2.1 + PKCE, redirect URIs, AppAuth libraries |
| [Token Storage & Rotation](.github/skills/auth/token-storage/SKILL.md) | Access / refresh token handling, rotation, revocation |
| [Biometric Auth](.github/skills/auth/biometric-auth/SKILL.md) | `BiometricPrompt`, `LAContext`, keys gated by biometry |
| [MFA on Mobile](.github/skills/auth/mfa-on-mobile/SKILL.md) | TOTP, push-based MFA, recovery UX |

### Network

| Skill | What it covers |
|-------|----------------|
| [TLS Certificate Pinning](.github/skills/network/tls-pinning/SKILL.md) | Pin sets, backup pins, kill switch; OkHttp / URLSession / Dio / TrustKit |
| [API Abuse Protection](.github/skills/network/api-abuse-protection/SKILL.md) | App Attest, Play Integrity, device binding |
| [MITM Prevention](.github/skills/network/mitm-prevention/SKILL.md) | User CA posture on newer Android / iOS, cleartext traffic |

### Code Protection

| Skill | What it covers |
|-------|----------------|
| [Code Obfuscation](.github/skills/code/code-obfuscation/SKILL.md) | R8, SwiftShield (limitations), ProGuard rules hygiene |
| [Anti-Tampering](.github/skills/code/anti-tampering/SKILL.md) | Signature checks, RASP pros/cons, realistic ROI |
| [Root / Jailbreak Detection](.github/skills/code/root-jailbreak-detection/SKILL.md) | Signals, not silver bullets; business policies |

### Secrets

| Skill | What it covers |
|-------|----------------|
| [Secrets Management](.github/skills/secrets/secrets-management/SKILL.md) | No secrets in client; config server, App Check |
| [Build-Time Secrets](.github/skills/secrets/build-time-secrets/SKILL.md) | gitleaks, `.gitignore` discipline, CI secret scopes |

### Privacy

| Skill | What it covers |
|-------|----------------|
| [Privacy by Design](.github/skills/privacy/privacy-by-design/SKILL.md) | Data minimization, purpose binding, consent |
| [Consent Management](.github/skills/privacy/consent-management/SKILL.md) | iOS ATT, Android User Messaging Platform (GDPR / CCPA) |

### Vulnerability Management

| Skill | What it covers |
|-------|----------------|
| [OWASP MASVS Alignment](.github/skills/vuln/mobile-owasp-masvs/SKILL.md) | MASVS v2 controls mapped to practical checks |
| [Dependency Scanning](.github/skills/vuln/dependency-scanning/SKILL.md) | Gradle Versions, Snyk, Dependabot, CocoaPods Audit |

### Compliance

| Skill | What it covers |
|-------|----------------|
| [GDPR on Mobile](.github/skills/compliance/gdpr-mobile/SKILL.md) | Lawful basis, DSAR flows, deletion on request |

---

## Quick Start

1. **Copy** the `.github/skills/` folder and `Agent.md` to your project root.
2. **Verify** the structure:
   ```text
   my-mobile-project/
   ├── Agent.md
   ├── .github/
   │   └── skills/
   │       ├── storage/
   │       │   ├── secure-storage/
   │       │   │   └── SKILL.md
   │       │   └── ...
   │       └── ...
   ├── app/ or ios/ or android/
   └── ...
   ```
3. **Reload** your editor (Copilot and similar extensions may need a window reload to index new skills).

Then just ask your agent naturally:

> "Store the user's refresh token securely on both Android and iOS."
> "Add certificate pinning with a kill switch to our Dio client."

The agent picks the right skill automatically.

---

## Other Environments

- **Claude**: copy or symlink `.github/skills` to `.claude/skills/`.
- **OpenCode**: supports `.opencode/skill/` and `.claude/skills/`. Global skills go in `~/.config/opencode/skill/`.

---

## Adding Custom Skills

Create a folder in `.github/skills/` with a `SKILL.md` containing the required frontmatter:

```markdown
---
name: my-custom-skill
description: What this skill does
---
# Instructions
...
```

---

## License

Dual-licensed:

- **Code** (snippets, configs, scripts) -- [MIT](LICENSE-CODE)
- **Documentation** (SKILL.md, README, Agent.md) -- [CC BY 4.0](LICENSE-DOCS)

See [LICENSE](LICENSE) for details.
