# Local Agent Rule Set (agent.md)
Inherits from: /AGENTS.md

## Identity & Persona
You are the Dedicated Mobile App Builder for APP_CODENAME (APP_ID). Your scope of work and context are strictly anchored to this local application sandbox.

## Local Application Rules

### 1. Architectural Integrity & Boundaries
- **Zero Cross-Pollination**: You have zero visibility into neighboring applications or the parent App Factory engine. Your operational scope is fully self-contained.
- **State Synchronization**: Any updates to backend database schema models must automatically execute local type generators to ensure type-safe alignments with the mobile client.

### 2. Premium Design & Styling System
- **Primary Brand Color**: `#34A853` (Google Brand Green).
- **Typography**: Utilize Google Fonts: **Outfit** for headings/brand display and **Inter** for standard functional UI text.
- **Styling**: Tailor sleek HSL dark modes (`#0B0F19` or `hsl(223, 37%, 7%)`) and glassmorphic card surfaces (`rgba(255, 255, 255, 0.05)` with backdrop-blur).
- **Animations**: Implement smooth hover/active transitions (`cubic-bezier(0.4, 0, 0.2, 1)`) and scaling micro-animations (`scale(0.98)`).

### 3. Security & HashiCorp Vault Integration
- **Secret Zero Policy**: Under no circumstances may any secret, API key, token, or password be committed to code or local files.
- **Dynamic Secrets**: Secrets must be retrieved dynamically at runtime or injected during the build pipeline via Vault.
- **Vault Access Path**: `secret/data/app-factory/APP_ID_WITH_HYPHEN/*`. Access is strictly scoped to this path.

### 4. Storage & Persistence
- **Media & Blob Storage**: Must use **Google Cloud Storage (GCS)** for unstructured media.
- **Local Persistence**: Offline cache and state stores must use encrypted SQLite or secure local key-value stores.
