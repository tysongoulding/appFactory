#!/usr/bin/env python3
"""
install_skills.py - Unified AI Editor & Agent Skill Integrator

This script installs App Factory spawner rules, contexts, and prompts across
Cursor, Claude CLI, Windsurf, PearAI, Trae, Aider, Conductor, Superset, AWS Kiro,
Codex, and Opencode.
"""

import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def log_ok(msg):
    print(f"\033[32m[OK]\033[0m {msg}")

def main():
    print("Installing AI Editor & Agent Skills...")
    
    # 1. Editor Rules (.cursorrules, .windsurfrules, .pearairules, .traerules)
    editor_rules = """# App Factory Orchestrator Context Rules

# Role Configuration
- You are the Factory Manager AI agent supervising the App Factory orchestrator workspace.
- Ingest README.md and AGENTS.md to understand the monorepo architecture.

# Spawning Applications
- To build a new application, execute the dynamic spawning CLI:
  `python scripts/spawn_app.py --codename <Name> --platform <Platform>`
- Do NOT manually write application-specific code inside the orchestrator folder; all apps must remain completely decoupled in lateral sibling directories.

# Code Quality & Vibecop Audits
- You must run the `vibecop_scan` tool from the `vibecop` MCP server on any orchestrator code changes.
- Resolve any warnings (such as god-functions or debug print statements) before committing.
"""

    for rule_file in [".cursorrules", ".windsurfrules", ".pearairules", ".traerules"]:
        dest_path = os.path.join(REPO_ROOT, rule_file)
        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(editor_rules)
        log_ok(f"Generated {rule_file} rules inside workspace.")

    # 2. Aider Configuration
    aider_config = """# Aider Configuration for App Factory
system-prompt: |
  You are the Factory Manager AI agent inside the App Factory. Your main duty is to use the python spawning orchestrator script scripts/spawn_app.py to compile lateral applications and maintain the central manifest.md database.
"""
    aider_path = os.path.join(REPO_ROOT, ".aider.conf.yml")
    with open(aider_path, "w", encoding="utf-8") as f:
        f.write(aider_config)
    log_ok("Generated .aider.conf.yml configuration.")

    # 3. Antigravity / Claude Code Skill
    skill_content = """# App Factory Spawner Skill (appfactory-spawner)

This skill provides an automated pipeline to compile new, isolated mobile application sandboxes sibling to the factory.

## Actions
To spawn a new application, execute the spawning orchestrator command:
`python scripts/spawn_app.py --codename <Name> --platform <Platform> [--template <Template>]`

## Features
- Phase 1: Ingests parameters and generates blueprint.json
- Phase 2: Clones selected templates laterally
- Phase 3: Injects context perimeters (.cursorrules, agent.md) and runs git init
- Phase 4: Configures localized CI/CD Fastlane Match and Vault OIDC permissions
"""
    skill_dir = os.path.join(REPO_ROOT, "lib", "agents", "scripts", "skills", "appfactory-spawner")
    os.makedirs(skill_dir, exist_ok=True)
    with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(skill_content)
    log_ok("Generated Claude SKILL.md under lib/agents/scripts/skills/")

    # Also attempt to copy to system-wide ~/.claude/skills if directory exists
    home_dir = os.path.expanduser("~")
    claude_skills_dir = os.path.join(home_dir, ".claude", "skills")
    if os.path.exists(claude_skills_dir):
        try:
            with open(os.path.join(claude_skills_dir, "appfactory-spawner.md"), "w", encoding="utf-8") as f:
                f.write(skill_content)
            log_ok("Installed appfactory-spawner skill system-wide to ~/.claude/skills/")
        except Exception as e:
            print(f"Skipped system-wide Claude install: {e}")

    # Also attempt to copy to system-wide ~/.gemini/config/skills or ~/.gemini/antigravity/skills if directories exist
    gemini_config_skills = os.path.join(home_dir, ".gemini", "config", "skills")
    gemini_antigravity_skills = os.path.join(home_dir, ".gemini", "antigravity", "skills")
    
    gemini_skill_content = """---
name: appfactory-spawner
description: Compiles and spawns isolated, self-contained application sandboxes parallel (lateral) to the App Factory orchestrator directory using spawn_app.py.
risk: low
source: local
date_added: '2026-05-22'
---

# App Factory Spawner Skill

This skill provides an automated pipeline to compile new, isolated mobile application sandboxes sibling to the factory.

## Actions
To spawn a new application, execute the spawning orchestrator command:
`python scripts/spawn_app.py --codename <Name> --platform <Platform> [--template <Template>]`

## Features
- Phase 1: Ingests parameters and generates blueprint.json
- Phase 2: Clones selected templates laterally
- Phase 3: Injects context perimeters (.cursorrules, agent.md) and runs git init
- Phase 4: Configures localized CI/CD Fastlane Match and Vault OIDC permissions
"""

    for target_dir in [gemini_config_skills, gemini_antigravity_skills]:
        if os.path.exists(target_dir):
            try:
                dest_dir = os.path.join(target_dir, "appfactory-spawner")
                os.makedirs(dest_dir, exist_ok=True)
                with open(os.path.join(dest_dir, "SKILL.md"), "w", encoding="utf-8") as f:
                    f.write(gemini_skill_content)
                log_ok(f"Installed appfactory-spawner skill to Gemini/Antigravity path: {dest_dir}")
            except Exception as e:
                print(f"Skipped Gemini/Antigravity skill install: {e}")

    # 4. AI System Prompt (AWS Kiro, Codex, Conductor, Superset, Opencode)
    system_prompt = """# App Factory System Prompt Instructions

You are the Factory Manager AI agent. Your primary function is to serve as an orchestration compiler, transforming software specifications into self-contained lateral repositories.

## Commands Reference
To generate a new application, run the Python spawner CLI:
`python scripts/spawn_app.py --codename <Name> --platform <Platform>`

## Isolation Rules
Do not create nested applications or traverse directories. Keep all generated repositories lateral (sibling) to the factory root.
"""
    prompt_path = os.path.join(REPO_ROOT, "AI_SYSTEM_PROMPT.md")
    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write(system_prompt)
    log_ok("Generated AI_SYSTEM_PROMPT.md instruction prompt.")

    print("\nAll AI Editor & Agent Skills successfully installed!")

if __name__ == "__main__":
    main()
