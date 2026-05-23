# App Factory Monorepo Manifest

This manifest is the canonical contract for all sub-repository applications managed within the App Factory. It is read and enforced by the **Lead Architect** and **Factory Manager** agents to orchestrate workspace initialization, template spawning, quality checks, and integration.

---

## 📜 Global Technical Contract

All applications generated and maintained in this monorepo MUST comply with the following architectural, design, and security specifications. Any deviation will be flagged by the **Quality Gatekeeper (Threat Detection Engineer)** and block integration.

### 1. Architectural Integrity
*   **Decoupled State**: No app is permitted to import or share code directly from another app directory. Contexts must remain completely isolated.
*   **Shared Abstractions**: Reusable modules must be published as independent packages in the `shared/` namespace or consumed via internal library references.
*   **Template Alignment**: All new apps must be bootstrapped from the corresponding `/templates` codebase.

### 2. Premium Design & Styling System
*   **Typography**: All user interfaces must utilize Google Fonts (**Inter** for functional UI, **Outfit** for headings and premium brand layouts).
*   **Color Palette**: All applications must inherit the following primary and accent brand colors:
    *   `Primary Brand Green`: `#34A853` (Google Brand Green)
    *   `Dark Background`: HSL-tailored slate (`#0B0F19` / `hsl(223, 37%, 7%)`)
    *   `Glassmorphic Surfaces`: Semi-transparent whites with backdrop-blur (`rgba(255, 255, 255, 0.05)`)
*   **Animations**: Micro-animations must be implemented on all interactive states (hover transitions: `cubic-bezier(0.4, 0, 0.2, 1)`, active scale down `scale(0.98)`).

### 3. Security & HashiCorp Vault Integration
*   **Secret Zero Policy**: Under no circumstances may any secret, API key, token, or password be committed to code or local files.
*   **Dynamic Secrets**: Apps must retrieve configuration values at runtime or during build pipelines via **HashiCorp Vault**.
*   **OIDC Authentication**: GitHub Actions workflows must authenticate to Vault using **OpenID Connect (OIDC)** claims.
*   **Namespace Scoping**: Each app is strictly restricted to its scoped Vault path (`secret/data/app-factory/app-x/*`). No app may access another app's secrets.

### 4. Storage & Persistence
*   **Blob/Media Storage**: Always prefer **Google Cloud Storage (GCS)** for unstructured media and blob storage.
*   **Local Caching**: App-level state and simple offline support must use secure SQLite databases or encrypted key-value stores.

---

## 📊 Application Matrix

The Factory Manager tracks the lifecycle of all generated apps using the matrix below.

| App ID | Codename | Platform | Assigned Agent | Status | Git Worktree/Submodule | Vault Policy Scoping |
|:---|:---|:---|:---|:---|:---|:---|
| `app-01` | Nebula | Cross-Platform | Mobile App Builder Alpha | `Integrated` | `../app-01-nebula` | `app-01-nebula-policy` |
| `app-02` | Orbital | iOS | Mobile App Builder Beta | `Integrated` | `../app-02-orbital` | `app-02-orbital-policy` |
| `app-03` | Pulsar | Android | Mobile App Builder Gamma | `Integrated` | `../app-03-pulsar` | `app-03-pulsar-policy` |
| `app-04` | Quasar | Cross-Platform | Mobile App Builder Delta | `Integrated` | `../app-04-quasar` | `app-04-quasar-policy` |
| `app-05` | Horizon | iOS | Mobile App Builder Epsilon | `Integrated` | `../app-05-horizon` | `app-05-horizon-policy` |


---

## 🛠️ Update Trigger Rules

1. **Manifest Mutations**: When the Lead Architect updates this manifest (e.g. changing status of `app-01` to `Spawning`), the Factory Manager reads the updated table, checks for diffs, and executes a delegation command using `AGENTS.md` parameters.
2. **Global Rules Changes**: If any brand colors, fonts, or policy variables are updated in the "Global Technical Contract" section, the Pipeline Orchestrator executes a workspace-wide check and triggers a re-validation script on all active sub-directories.
