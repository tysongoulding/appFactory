# 🏭 App Factory Monorepo

Welcome to the **App Factory**, a highly automated monorepo designed to scale the creation, testing, security auditing, and deployment of 30 isolated mobile applications. This factory uses the **agency-agents** orchestration paradigm, where specialized AI agents hold specific controller roles and manage the lifecycle of each application subdirectory.

---

## 🏗️ Factory Architecture & Roles

The App Factory runs on a hierarchy of specialized AI personas defined under `lib/agents/engineering/`. These agents collaborate based on the rules outlined in `AGENTS.md` and track state using `manifest.md`.

### 👥 The Core Agent Team

| Role | Agency Agent File | Primary Mandate |
| :--- | :--- | :--- |
| **Factory Manager** | `AGENTS.md` (Root System Agent) | Orchestrates workspace spawning, directory mapping, and lifecycle steps. |
| **Lead Architect** | [`engineering-backend-architect.md`](lib/agents/engineering/engineering-backend-architect.md) | Enforces the global technical contract, structure, and database/storage decisions. |
| **Pipeline Orchestrator** | [`engineering-devops-automator.md`](lib/agents/engineering/engineering-devops-automator.md) | Generates GitHub Actions workflows, provisions HashiCorp Vault access, and OIDC claims. |
| **Quality Gatekeeper** | [`engineering-threat-detection-engineer.md`](lib/agents/engineering/engineering-threat-detection-engineer.md) | Runs static security analysis and prevents credential leaks before merging branches. |
| **Mobile App Builder** | [`engineering-mobile-app-builder.md`](lib/agents/engineering/engineering-mobile-app-builder.md) | Assigned to isolated app worktrees to build premium user interfaces (Google Brand Green `#34A853`, Inter/Outfit fonts). |

---

## 🔄 The Production Line Pattern

To initialize, configure, and integrate a new app, follow the automated production line phases:

```
[ manifest.md ] ──(Spawning Status)──> [ Factory Manager ]
                                             │
                                   (1) Plan: Create worktree / Write specs
                                             │
                                   (2) Spawn: Clone template folder
                                             │
                                   (3) Validate: Vault/OIDC and Security Scan
                                             │
                                   (4) Integrate: Push feature/app-* & merge
```

### 1. Workspace Initialization & Planning
When an app status shifts to `Spawning` in `manifest.md`, the **Lead Architect** spawns an isolated workspace for that app:
```bash
# Create an isolated Git worktree for the app
git worktree add apps/app-01-nebula -b feature/app-01-nebula
```
This isolates the codebase so the **Mobile App Builder** assigned to `app-01-nebula` has zero visibility into adjacent apps, keeping build files and cache namespaces separated.

### 2. Spawning the Template
The **Pipeline Orchestrator** replicates the appropriate project structure from `/templates` into the isolated workspace:
*   `/templates/ios`: Swift / SwiftUI boilerplates with custom styling rules.
*   `/templates/android`: Kotlin / Jetpack Compose boilerplates.
*   `/templates/workflows`: Reusable workflows and caller configurations.

### 3. Vault & OIDC Configuration
To maintain a strict "Secret Zero" policy, the **Pipeline Orchestrator** runs `vault/setup_vault_oidc.sh` to configure OpenID Connect (OIDC) access:
1.  Mounts the JWT auth engine to trust GitHub Actions: `https://token.actions.githubusercontent.com`.
2.  Creates a Vault Policy limiting the app to its path: `secret/data/app-factory/app-01-nebula/*`.
3.  Binds a JWT role mapping the GitHub runner to that policy based on repository name (`org/appFactory`) and the branch pattern (`refs/heads/feature/app-01-nebula`).

### 4. Gatekeeper Validation & Merge
Before a pull request can be merged:
1.  The **Quality Gatekeeper** runs verification checks (linting, OIDC workflow audits, scanning for hardcoded secrets).
2.  Upon approval, changes are merged into the target branch, and the GitHub runner retrieves the API endpoints dynamically from Vault to run compilation.

---

## 📈 Skill Accumulation (Agent Skills)

As bug fixes or configuration enhancements are resolved in individual applications, they are codified in `/lib/agents/scripts/skills/`. The **Pipeline Orchestrator** reads these definitions and automatically propagates the fixes across all other active application contexts.

---

## 🚀 How to Run the Agents

### A. Using Claude Code (Recommended)
Add the agents to your Claude Code configuration:
```bash
cp lib/agents/engineering/*.md ~/.claude/agents/
```
In your session, activate them explicitly:
*   *“Hey Claude, activate Backend Architect mode and audit manifest.md”*
*   *“Hey Claude, activate DevOps Automator mode and provision OIDC for app-02-orbital”*

### B. Using Cursor (.cursorrules)
Run the install script to generate and link `.mdc` rule files:
```bash
./lib/agents/scripts/install.sh --tool cursor
```
Reference them in Cursor composer or chat:
*   *“Use @engineering-security-engineer to audit the caller workflows in templates/workflows”*
