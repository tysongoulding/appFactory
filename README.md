# 🏭 The Isolated App Factory Engine

Welcome to the **App Factory Orchestration Engine**—a centralized, read-only orchestration pipeline designed to ingest high-level software prompts and compile them into fully operational, self-contained, and completely isolated mobile application sandboxes (iOS and Android). 

Using the **agency-agents** paradigm, the factory serves as a deterministic compiler, remaining structurally decoupled from the applications it generates.

---

## 🚀 Quick Start: Installation & Uninstallation

Since this is a public repository, you can set up or tear down the orchestrator using automated one-liners in your local terminal:

### 1. One-Line Install

#### Windows (PowerShell):
```powershell
irm https://raw.githubusercontent.com/tysongoulding/appFactory/main/scripts/install.ps1 | iex
```

#### macOS & Linux (Bash/Zsh):
```bash
curl -sSL https://raw.githubusercontent.com/tysongoulding/appFactory/main/scripts/install.sh | bash
```

### 2. One-Line Uninstall

#### Windows (PowerShell):
```powershell
irm https://raw.githubusercontent.com/tysongoulding/appFactory/main/scripts/uninstall.ps1 | iex
```

#### macOS & Linux (Bash/Zsh):
```bash
curl -sSL https://raw.githubusercontent.com/tysongoulding/appFactory/main/scripts/uninstall.sh | bash
```
*Note: Any laterally spawned application sandboxes parallel to the factory are safely preserved to prevent custom source code deletion. You can manually remove those when desired.*

---

## 🏗️ Topographical Strategy & Lateral Sandboxes

To prevent context drift, token cross-pollination, and directory fragmentation, the monorepo enforces a strict **lateral workspace structure**:

*   **Core App Factory (The Orchestrator)**: The `appFactory` folder contains pristine starter seeds (`/templates`), OIDC deployment blueprints, and specialized generation personas. It holds **no application-specific code** or nested workspace logic.
*   **Generated Applications (The Sandboxes)**: Spawned laterally/parallel to the factory root (e.g. `../app-05-horizon`). Each sandbox represents a completely autonomous Git repository (`git init`) containing its own independent frontend client, isolated backend server, local GitHub Actions pipelines, Fastlane configurations, and distinct Git history.

---

## 🔄 The Ingestion Production Line

When asked to generate a new software idea, the factory executes the following four sequential phases without human intervention:

```
[ Prompt / Spec ] ──> (1) Phase 1: Manifest Synthesis ──> Generates blueprint.json
                                                               │
┌──────────────────────────────────────────────────────────────┘
│
├──> (2) Phase 2: Hydrolysis & Workspace Cloning ──> Spawns lateral sibling folder & copies template
│
├──> (3) Phase 3: Perimeter Injection ──> Drops .cursorrules / agent.md & runs git init
│
└──> (4) Phase 4: Dynamic CI/CD Provisioning ──> Generates local workflows, Fastlane Match & Vault OIDC
```

### 1. Phase 1: Manifest Synthesis (Plan)
The Product Architect translates high-level prompts into a single structured configuration document (`blueprint.json`) defining the application's core relational data models, page routing tables, styling tokens (Google Fonts `Outfit`/`Inter` and Brand Green `#34A853`), and bundle identifiers.

### 2. Phase 2: Hydrolysis & Workspace Cloning (Spawn)
The API Engineer and UI Component Generator copy pristine starter templates (`/templates`) into a brand-new lateral directory parallel to the factory. They execute an internal string-replacement engine to bind unique bundle IDs, app names, and repository paths directly into the code and configuration files.

### 3. Phase 3: Perimeter Injection (Jail Context)
The UI Component Generator drops context boundary perimeters at the sandbox root:
*   `.cursorrules`: Enforces strict Absolute Path Containment, preventing developer agents from exiting the sandbox.
*   `agent.md`: The primary local system prompt outlining HSL dark modes (`#0B0F19`), GCS storage paths, and local SQLite persistence.
*   The sandbox is then initialized as an independent repository (`git init`) with its own initial commit to establish a distinct history.

### 4. Phase 4: Dynamic CI/CD Provisioning (Integrate)
The API Engineer copies localized workflow configurations inside `.github/workflows/pipeline.yml` and Fastlane configurations (`Appfile`/`Fastfile`). It provisions dynamic Vault roles and policies (`secret/data/app-factory/app-x/*`) mapped to the sandbox's dedicated remote GitHub repository and registers code-signing parameters.

---

## 🚀 Spawning a New Application Dynamically

To compile a new application dynamically, run `spawn_app.py` with the `--codename` and `--platform` (choices: `iOS`, `Android`, `Cross-Platform`) parameters:

```powershell
python scripts/spawn_app.py --codename Horizon --platform iOS
```

### Automatic Orchestration Flow:
1.  **Next available ID**: Scans existing entries in [`manifest.md`](manifest.md), auto-calculates the next available ID (e.g. `app-05`), and assigns the next builder agent dynamically using the Greek alphabet (e.g. `Mobile App Builder Epsilon`).
2.  **Manifest Appending**: Appends the new tracking row to the table matrix in `manifest.md` on-the-fly.
3.  **Lateral Compilation**: Spawns the sandbox at `C:\repo\personal\app-05-horizon`, copies iOS template seeds, injects perimeter files, writes custom `blueprint.json`, generates Fastlane setups, runs `git init`, and configures OIDC authentication.

---

## 🛡️ Code Quality & Quality Gatekeeper (Vibecop Audits)

To guarantee software integrity across dozens of applications, the **Quality Gatekeeper** enforces strict AI code quality standards utilizing the **Vibecop** MCP server:

*   **Gatekeeper Audits**: During Phase 3/4 validation, the gatekeeper automatically triggers a `vibecop_scan` across the sandbox directory.
*   **Strict Blocking Policy**: Builds are blocked and branch merges are refused on any codebase containing unencrypted credential keys or unresolved `warning`/`critical` findings (such as cyclomatic complexity warnings or `god-function` alerts).
*   **Developer Rule**: Downstream developers opening a sandbox workspace are governed by the local [`agent.md`](templates/perimeter/agent.md) context, which strictly instructs them to run `vibecop_scan` and resolve any warnings before staging changes.
