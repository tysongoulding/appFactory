#!/usr/bin/env python3
"""
spawn_app.py - Isolated App Factory Engine Orchestrator

This script automates the production line lifecycle to generate isolated mobile apps:
  Phase 1: Manifest Synthesis (reads manifest, defines configurations and blueprint.json)
  Phase 2: Hydrolysis & Workspace Cloning (creates a lateral sibling directory and replicates templates)
  Phase 3: Perimeter Injection (drops .cursorrules, agent.md, README.md, and initializes local Git repo)
  Phase 4: Dynamic CI/CD Provisioning (configures local workflows, Fastlane, and Vault OIDC)

Usage:
  python scripts/spawn_app.py [--id app-XX] [--codename Name] [--platform Platform] [--dry-run] [--template name]
"""

import os
import sys
import re
import shutil
import subprocess
import argparse

# Path definitions relative to repository root
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MANIFEST_PATH = os.path.join(REPO_ROOT, "manifest.md")
TEMPLATES_DIR = os.path.join(REPO_ROOT, "templates")

GREEK_ALPHABET = [
    "Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta", 
    "Iota", "Kappa", "Lambda", "Mu", "Nu", "Xi", "Omicron", "Pi", 
    "Rho", "Sigma", "Tau", "Upsilon", "Phi", "Chi", "Psi", "Omega"
]

def log_ok(msg):
    print(f"\033[32m[OK]\033[0m {msg}")

def log_info(msg):
    print(f"\033[36m[INFO]\033[0m {msg}")

def log_warn(msg):
    print(f"\033[33m[WARN]\033[0m {msg}")

def log_err(msg):
    print(f"\033[31m[ERR]\033[0m {msg}", file=sys.stderr)

def parse_manifest():
    """Reads manifest.md and extracts all application matrix rows."""
    if not os.path.exists(MANIFEST_PATH):
        log_err(f"Manifest file not found at: {MANIFEST_PATH}")
        sys.exit(1)
        
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Pattern to capture markdown table rows matching app entries
    # E.g.: | `app-01` | Nebula | Cross-Platform | Mobile App Builder Alpha | `Planned` | `../app-01-nebula` | ...
    pattern = re.compile(
        r"\|\s*`?(app-\d+)`?\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*`?([a-zA-Z0-9 -]+?)`?\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|"
    )
    
    apps = []
    for match in pattern.finditer(content):
        app_id = match.group(1).strip()
        codename = match.group(2).strip()
        platform = match.group(3).strip()
        agent = match.group(4).strip()
        status = match.group(5).strip()
        worktree = match.group(6).strip()
        vault_policy = match.group(7).strip()
        
        apps.append({
            "id": app_id,
            "codename": codename,
            "platform": platform,
            "agent": agent,
            "status": status,
            "worktree": worktree,
            "vault_policy": vault_policy,
            "raw_row": match.group(0)
        })
        
    return apps, content

def update_manifest_status(app_id, new_status):
    """Updates the status of a specific app in manifest.md."""
    apps, content = parse_manifest()
    target_app = next((a for a in apps if a["id"] == app_id), None)
    if not target_app:
        log_err(f"Could not find app with ID {app_id} in manifest to update status.")
        return False
        
    old_row = target_app["raw_row"]
    current_status = target_app["status"]
    
    # We update the status and target path in the row representation
    parts = old_row.split("|")
    parts[5] = f" `{new_status}` "
    
    # Check if target path needs update to lateral sibling folder notation
    current_path = target_app["worktree"]
    codename_lower = target_app["codename"].lower()
    lateral_path = f"../{app_id}-{codename_lower}"
    if current_path.startswith("/apps/") or current_path.startswith("apps/"):
        parts[6] = f" `{lateral_path}` "
        log_info(f"Updating manifest workspace tracking path for {app_id} to lateral path: {lateral_path}")
        
    new_row = "|".join(parts)
    modified_content = content.replace(old_row, new_row)
        
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        f.write(modified_content)
        
    log_ok(f"Updated status of {app_id} in manifest.md to '{new_status}'")
    return True

def generate_next_app_credentials(apps):
    """Calculates the next ID and dynamic agent assignment based on current manifest matrix."""
    highest_id = 0
    for app in apps:
        match = re.search(r"app-(\d+)", app["id"])
        if match:
            val = int(match.group(1))
            if val > highest_id:
                highest_id = val
                
    next_id_num = highest_id + 1
    next_id = f"app-{next_id_num:02d}"
    
    agent_suffix = GREEK_ALPHABET[(next_id_num - 1) % len(GREEK_ALPHABET)]
    agent_name = f"Mobile App Builder {agent_suffix}"
    
    return next_id, agent_name

def append_new_app_to_manifest(app_id, codename, platform, agent_name):
    """Appends a new application entry to the matrix in manifest.md."""
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Find the last table row containing an app ID (e.g., app-XX)
    pattern = re.compile(r"\|\s*`?(app-\d+)`?\s*\|.*\|")
    matches = list(pattern.finditer(content))
    if not matches:
        log_err("Could not find the application matrix table to append to.")
        return False
        
    last_match = matches[-1]
    end_index = last_match.end()
    
    # Format the new row
    vault_policy = f"{app_id}-{codename.lower()}-policy"
    worktree_path = f"../{app_id}-{codename.lower()}"
    new_row = f"\n| `{app_id}` | {codename} | {platform} | {agent_name} | `Planned` | `{worktree_path}` | `{vault_policy}` |"
    
    # Insert the row
    modified_content = content[:end_index] + new_row + content[end_index:]
    
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        f.write(modified_content)
        
    log_ok(f"Dynamically appended {app_id} ({codename}) to manifest.md")
    return True

def setup_lateral_directory(app_id, codename):
    """Sets up target directory lateral (sibling) to the factory root."""
    folder_name = f"{app_id}-{codename.lower()}"
    parent_dir = os.path.dirname(REPO_ROOT) # Parallel to appFactory
    target_path = os.path.join(parent_dir, folder_name)
    
    if os.path.exists(target_path):
        log_warn(f"Target path already exists laterally: {target_path}. Reusing directory.")
    else:
        os.makedirs(target_path, exist_ok=True)
        log_ok(f"Created standard lateral sandbox directory: {target_path}")
    return target_path

def copy_and_interpolate_templates(target_path, platform, app_id, codename, template_name=None):
    """Replicates template codebases and substitutes target configuration placeholders."""
    app_id_suffix = app_id.replace("app-", "") # E.g. "01"
    clean_codename = codename.replace(" ", "").replace("-", "") # E.g. "Nebula"
    
    # APP_ID_PLACEHOLDER -> app01nebula
    app_id_placeholder = f"app{app_id_suffix}{clean_codename.lower()}"
    
    replacements = {
        "APP_ID_PLACEHOLDER": app_id_placeholder,
        "APP_CODENAME_PLACEHOLDER": codename,
        "APP_ID_WITH_HYPHEN": f"{app_id}-{codename.lower()}",
        "app-[ID]-[NAME]": f"{app_id}-{codename.lower()}",
        "app-[ID]": app_id,
        "[NAME]": codename.lower(),
        "[ID]": app_id_suffix,
        "[app-id]": app_id,
        "[name]": codename.lower()
    }
    
    def replace_tokens(text):
        for k, v in replacements.items():
            text = text.replace(k, v)
        return text

    def copy_with_replacement(src_dir, dest_dir):
        if not os.path.exists(src_dir):
            return
        os.makedirs(dest_dir, exist_ok=True)
        for root, dirs, files in os.walk(src_dir):
            # Compute relative path to map directories
            rel_path = os.path.relpath(root, src_dir)
            target_root = dest_dir if rel_path == "." else os.path.join(dest_dir, rel_path)
            
            # Apply placeholder replacement to directory name
            target_root = replace_tokens(target_root)
            os.makedirs(target_root, exist_ok=True)
            
            for file in files:
                src_file_path = os.path.join(root, file)
                # Apply placeholder replacement to file name
                dest_file_name = replace_tokens(file)
                dest_file_path = os.path.join(target_root, dest_file_name)
                
                # Copy and interpolate text files
                try:
                    if file.endswith((".kt", ".swift", ".gradle", ".kts", ".xml", ".md", ".pbxproj", ".yml", ".yaml")):
                        with open(src_file_path, "r", encoding="utf-8", errors="ignore") as f:
                            file_content = f.read()
                        new_content = replace_tokens(file_content)
                        with open(dest_file_path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                    else:
                        # Binary copy
                        shutil.copy2(src_file_path, dest_file_path)
                except Exception as e:
                    log_warn(f"Failed to copy file {src_file_path} with replacements: {e}")
                    shutil.copy2(src_file_path, dest_file_path)

    has_android = "Android" in platform or "Cross-Platform" in platform
    has_ios = "iOS" in platform or "Cross-Platform" in platform
    
    # Determine template source root directory
    if template_name:
        template_dir = os.path.join(TEMPLATES_DIR, template_name)
        if not os.path.exists(template_dir):
            log_err(f"Template directory '{template_name}' not found in {TEMPLATES_DIR}")
            sys.exit(1)
    else:
        template_dir = TEMPLATES_DIR
        
    android_src = os.path.join(template_dir, "android")
    ios_src = os.path.join(template_dir, "ios")
    
    is_flat_template = not os.path.exists(android_src) and not os.path.exists(ios_src)
    
    if is_flat_template:
        log_info(f"Replicating flat template from {template_dir} into {target_path}...")
        copy_with_replacement(template_dir, target_path)
    else:
        if has_android and os.path.exists(android_src):
            log_info(f"Replicating Android template from {android_src} into {target_path}...")
            copy_with_replacement(android_src, target_path)
            
        if has_ios and os.path.exists(ios_src):
            log_info(f"Replicating iOS template from {ios_src} into {target_path}...")
            copy_with_replacement(ios_src, target_path)

def inject_perimeter_controls(target_path, app_id, codename, platform):
    """Drops .cursorrules, agent.md, blueprint.json, and a custom README.md into the sandbox root (Phase 3)."""
    log_info(f"Injecting perimeter controls (Phase 3 Context Jails) into {target_path}...")
    
    app_id_suffix = app_id.replace("app-", "")
    clean_codename = codename.replace(" ", "").replace("-", "")
    app_id_placeholder = f"app{app_id_suffix}{clean_codename.lower()}"
    
    replacements = {
        "APP_ID_PLACEHOLDER": app_id_placeholder,
        "APP_CODENAME_PLACEHOLDER": codename,
        "APP_ID_WITH_HYPHEN": f"{app_id}-{codename.lower()}",
        "APP_ID": app_id,
        "APP_CODENAME": codename,
        "PLATFORM": platform,
        "app-[ID]-[NAME]": f"{app_id}-{codename.lower()}",
        "app-[ID]": app_id,
        "[NAME]": codename.lower(),
        "[ID]": app_id_suffix,
        "[app-id]": app_id,
        "[name]": codename.lower()
    }
    
    def replace_tokens(text):
        for k, v in replacements.items():
            text = text.replace(k, v)
        return text

    # 1. Copy .cursorrules
    src_cursorrules = os.path.join(TEMPLATES_DIR, "perimeter", ".cursorrules")
    dest_cursorrules = os.path.join(target_path, ".cursorrules")
    if os.path.exists(src_cursorrules):
        with open(src_cursorrules, "r", encoding="utf-8") as f:
            content = f.read()
        with open(dest_cursorrules, "w", encoding="utf-8") as f:
            f.write(replace_tokens(content))
        log_ok("Injected [.cursorrules] absolute boundary constraint.")
    else:
        log_err("Source .cursorrules template missing from templates/perimeter/")

    # 2. Copy agent.md
    src_agent = os.path.join(TEMPLATES_DIR, "perimeter", "agent.md")
    dest_agent = os.path.join(target_path, "agent.md")
    if os.path.exists(src_agent):
        with open(src_agent, "r", encoding="utf-8") as f:
            content = f.read()
        with open(dest_agent, "w", encoding="utf-8") as f:
            f.write(replace_tokens(content))
        log_ok("Injected [agent.md] governance identity rules.")
    else:
        log_err("Source agent.md template missing from templates/perimeter/")

    # 3. Copy blueprint.json
    src_blueprint = os.path.join(TEMPLATES_DIR, "perimeter", "blueprint_template.json")
    dest_blueprint = os.path.join(target_path, "blueprint.json")
    if os.path.exists(src_blueprint):
        with open(src_blueprint, "r", encoding="utf-8") as f:
            content = f.read()
        with open(dest_blueprint, "w", encoding="utf-8") as f:
            f.write(replace_tokens(content))
        log_ok("Injected [blueprint.json] structural schema configuration.")
    else:
        log_err("Source blueprint_template.json template missing from templates/perimeter/")

    # 4. Generate README.md
    dest_readme = os.path.join(target_path, "README.md")
    readme_content = f"""# {codename} ({app_id})

This is the completely autonomous, self-contained **{codename}** application sandbox, compiled deterministically by the App Factory.

## Platform Target
- **{platform}**

## Sandbox Governance & Constraints
> [!IMPORTANT]
> **Developer Jail Bounds**:
> This sandbox contains custom perimeter jails to isolate build states and context streams.
> All developer agents must strictly adhere to the rules in [.cursorrules](.cursorrules) and inherit the localized prompt in [agent.md](agent.md).

## Project Setup & Verification
Refer to [agent.md](agent.md) for branding, dynamic Vault pathways, and type synchronization.
"""
    with open(dest_readme, "w", encoding="utf-8") as f:
        f.write(readme_content)
    log_ok("Generated custom [README.md] document.")

def inject_compilation_and_cicd(target_path, app_id, codename):
    """Copies localized CI/CD pipelines and Fastlane configuration scripts into sandbox (Phase 4)."""
    log_info(f"Injecting CI/CD and Fastlane configurations into {target_path}...")
    
    app_id_suffix = app_id.replace("app-", "")
    clean_codename = codename.replace(" ", "").replace("-", "")
    app_id_placeholder = f"app{app_id_suffix}{clean_codename.lower()}"
    
    replacements = {
        "APP_ID_PLACEHOLDER": app_id_placeholder,
        "APP_CODENAME_PLACEHOLDER": codename,
        "APP_ID_WITH_HYPHEN": f"{app_id}-{codename.lower()}",
        "APP_ID": app_id,
        "APP_CODENAME": codename,
        "app-[ID]-[NAME]": f"{app_id}-{codename.lower()}",
        "app-[ID]": app_id,
        "[NAME]": codename.lower(),
        "[ID]": app_id_suffix,
        "[app-id]": app_id,
        "[name]": codename.lower()
    }
    
    def replace_tokens(text):
        for k, v in replacements.items():
            text = text.replace(k, v)
        return text

    # 1. Inject Fastlane Appfile and Fastfile
    fastlane_dir = os.path.join(target_path, "fastlane")
    os.makedirs(fastlane_dir, exist_ok=True)
    
    for file_name in ["Appfile", "Fastfile"]:
        src_path = os.path.join(TEMPLATES_DIR, "fastlane", file_name)
        dest_path = os.path.join(fastlane_dir, file_name)
        if os.path.exists(src_path):
            with open(src_path, "r", encoding="utf-8") as f:
                content = f.read()
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(replace_tokens(content))
            log_ok(f"Injected [fastlane/{file_name}] template.")
        else:
            log_warn(f"Source Fastlane template {file_name} not found.")

    # 2. Inject Localized GitHub Actions Workflows
    workflow_dir = os.path.join(target_path, ".github", "workflows")
    os.makedirs(workflow_dir, exist_ok=True)
    
    src_pipeline = os.path.join(TEMPLATES_DIR, "workflows", "local-app-pipeline.yml")
    dest_pipeline = os.path.join(workflow_dir, "pipeline.yml")
    if os.path.exists(src_pipeline):
        with open(src_pipeline, "r", encoding="utf-8") as f:
            content = f.read()
        with open(dest_pipeline, "w", encoding="utf-8") as f:
            f.write(replace_tokens(content))
        log_ok("Injected localized [.github/workflows/pipeline.yml] workflow.")
    else:
        log_err("Source local-app-pipeline.yml template missing!")

def init_git_repo(target_path):
    """Initializes a fresh, local Git repository inside the lateral workspace and creates an initial commit (Phase 3)."""
    log_info(f"Initializing a fresh Git repository at {target_path}...")
    
    if os.path.exists(os.path.join(target_path, ".git")):
        log_warn("Target path is already a Git repository. Skipping re-initialization.")
        return
        
    try:
        # Run git init
        subprocess.run(["git", "init"], cwd=target_path, check=True, capture_output=True)
        # Stage all files
        subprocess.run(["git", "add", "."], cwd=target_path, check=True, capture_output=True)
        # First commit
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from App Factory Engine (Isolated Sandbox)"],
            cwd=target_path, check=True, capture_output=True
        )
        log_ok("Successfully initialized fresh local Git repository and created initial commit.")
    except Exception as e:
        log_err(f"Failed to initialize local Git repository: {e}")

def setup_vault_security(app_id, codename, dry_run=False):
    """Provisions Vault access configuration roles and policies dynamically mapped to its own repo."""
    setup_script = os.path.join(REPO_ROOT, "vault", "setup_vault_oidc.sh")
    if not os.path.exists(setup_script):
        log_warn("Vault setup script setup_vault_oidc.sh not found. Skipping security policies configuration.")
        return
        
    dedicated_repo = f"org/{app_id}-{codename.lower()}"
    cmd_str = f'bash -c "source {setup_script} && setup_app_security {app_id} {codename.lower()} {dedicated_repo}"'
    log_info(f"Vault configuration command:\n  {cmd_str}")
    
    if dry_run:
        log_info("[Dry-Run] Vault command skipped.")
        return
        
    try:
        vault_check = subprocess.run(["vault", "--version"], capture_output=True, text=True)
        if vault_check.returncode == 0:
            log_info("Executing Vault OIDC role mapping...")
            res = subprocess.run(
                ["bash", "-c", f"source {setup_script} && setup_app_security {app_id} {codename.lower()} {dedicated_repo}"],
                capture_output=True, text=True
            )
            if res.returncode == 0:
                log_ok("Vault security provisioned successfully.")
                print(res.stdout)
            else:
                log_warn(f"Vault security script failed (Vault server might be unreachable):\n{res.stderr}")
        else:
            log_warn("Vault command is not in system PATH. Please run the command manually inside a Vault-authenticated environment.")
    except Exception as e:
        log_warn(f"Could not run Vault integration: {e}. Make sure to setup Vault role for {app_id}-{codename.lower()} manually.")

def main():
    parser = argparse.ArgumentParser(description="Isolated App Factory Spawning Orchestrator")
    parser.add_argument("--id", help="App ID to spawn (e.g. app-01). If omitted, spawns the next Planned app.")
    parser.add_argument("--codename", help="Codename of the new application to spawn dynamically.")
    parser.add_argument("--platform", choices=["iOS", "Android", "Cross-Platform"], help="Target platform of the new application.")
    parser.add_argument("--dry-run", action="store_true", help="Print actions but do not write files or run vault commands.")
    parser.add_argument("--template", help="Name of the custom template folder under templates/ (e.g. ar-crossplatform).")
    args = parser.parse_args()

    # 1. Parse manifest check
    apps, _ = parse_manifest()
    
    # 2. Dynamic creation branch if codename and platform are provided (Manifest Synthesis)
    if args.codename and args.platform:
        if args.id:
            log_err("Cannot specify both --id and dynamic creation parameters (--codename/--platform).")
            sys.exit(1)
            
        next_id, agent_name = generate_next_app_credentials(apps)
        log_info(f"Dynamic creation request: Codename: {args.codename} | Platform: {args.platform}")
        log_info(f"Allocating next available ID: {next_id} under {agent_name}")
        
        # Append to manifest.md on-the-fly
        if not append_new_app_to_manifest(next_id, args.codename, args.platform, agent_name):
            sys.exit(1)
            
        # Re-parse manifest so it detects our appended app
        apps, _ = parse_manifest()
        target_app = next((a for a in apps if a["id"] == next_id), None)
    else:
        target_app = None
        if args.id:
            target_app = next((a for a in apps if a["id"] == args.id), None)
            if not target_app:
                log_err(f"App with ID {args.id} not found in manifest.md.")
                sys.exit(1)
        else:
            # Find next planned app in manifest
            target_app = next((a for a in apps if a["status"] == "Planned"), None)
            if not target_app:
                log_ok("No 'Planned' applications found in manifest.md to spawn automatically. Please provide --codename and --platform to build a new one dynamically.")
                sys.exit(0)
            
    app_id = target_app["id"]
    codename = target_app["codename"]
    platform = target_app["platform"]
    
    log_info(f"Target selected: {app_id} | Codename: {codename} | Platform: {platform} | Status: {target_app['status']}")
    
    if args.dry_run:
        log_info(f"[Dry-Run] Would spawn {app_id} ({codename}) laterally sibling to the factory.")
        sys.exit(0)
        
    # 3. Update status in manifest.md to 'Spawning'
    update_manifest_status(app_id, "Spawning")
    
    # 4. Create lateral sibling directory (Phase 2 Hydrolysis)
    target_path = setup_lateral_directory(app_id, codename)
    
    # 5. Copy templates and apply placeholder replacement
    copy_and_interpolate_templates(target_path, platform, app_id, codename, template_name=args.template)
    log_ok(f"Template structures copied and placeholder tokens replaced.")
    
    # 6. Inject perimeter controls (.cursorrules, agent.md, blueprint.json - Phase 3 Ingestion)
    inject_perimeter_controls(target_path, app_id, codename, platform)
    
    # 7. Inject localized Fastlane & CI/CD workflows (Phase 4 CI/CD Provisioning)
    inject_compilation_and_cicd(target_path, app_id, codename)
    
    # 8. Initialize fresh local git repository (Phase 3 Git Inception)
    init_git_repo(target_path)
    
    # 9. Setup Vault security access controls mapping to dynamic repo
    setup_vault_security(app_id, codename, dry_run=args.dry_run)
    
    # 10. Update status to 'Integrated'
    update_manifest_status(app_id, "Integrated")
    
    log_ok(f"Production line successfully completed laterally for {app_id} ({codename})!")

if __name__ == "__main__":
    main()
