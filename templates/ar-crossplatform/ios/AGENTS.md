# Application Agent Rule Set (iOS AR Instance)

This agent manifest inherits from the root `/AGENTS.md` configuration and defines the execution constraints for this application.

## 🚀 Inherited Context
*   **Root Governance**: [Global Governance Architecture](../../AGENTS.md)
*   **Lead Architect Prompts**: [Backend Architect](../../lib/agents/engineering/engineering-backend-architect.md)
*   **Pipeline Orchestrator Prompts**: [DevOps Automator](../../lib/agents/engineering/engineering-devops-automator.md)
*   **Assigned Specialist**: [Mobile App Builder](../../lib/agents/engineering/engineering-mobile-app-builder.md)

## 📌 Local Application Compliance Rules

1.  **Strict Color Palette**: 
    *   Accent highlight: `#34A853` (Google Green)
    *   Theme: Premium Dark Mode with HSL slate base.
2.  **Typography**: Use Google Fonts (`Outfit-Bold` for headlines, `Inter` for content details).
3.  **Storage**: Unstructured assets (media, logs) must be pushed to Google Cloud Storage (GCS). No AWS S3 allowed.
4.  **Secrets & Variables**: All endpoints and key strings (including Google Cloud Maps API keys and Firebase configurations) must bind to Vault values at build or runtime. Zero hardcoding.
5.  **Branch Isolation**: Commits must target `feature/[app-id]-[name]` and undergo automated QA checks before PR validation.
6.  **AR Frameworks**: Native iOS must utilize RealityKit, ARKit, and CoreLocation frameworks.
