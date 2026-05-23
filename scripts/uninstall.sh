#!/usr/bin/env bash
# uninstall.sh - Complete Uninstallation for Isolated App Factory Engine on macOS & Linux

DEST_FOLDER="appFactory"

# Colors
RED='\033[0;31m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${RED}=============================================${NC}"
echo -e "${RED}💀 Uninstalling Isolated App Factory Engine...${NC}"
echo -e "${RED}=============================================${NC}"

# Confirm uninstallation
read -p "Are you sure you want to remove the App Factory folder '$DEST_FOLDER'? (y/n): " confirmation
if [ "$confirmation" != "y" ]; then
    echo -e "${CYAN}Uninstallation cancelled.${NC}"
    exit 0
fi

# 1. Remove App Factory Folder
if [ -d "$DEST_FOLDER" ]; then
    echo -e "${CYAN}Removing App Factory orchestrator directory '$DEST_FOLDER'...${NC}"
    rm -rf "$DEST_FOLDER"
    echo -e "${GREEN}[OK] Orchestrator files deleted.${NC}"
else
    echo -e "${YELLOW}Orchestrator directory '$DEST_FOLDER' was not found in the current directory.${NC}"
fi

# 2. Remove system-wide Claude Code Skill if present
CLAUDE_SKILL_PATH="$HOME/.claude/skills/appfactory-spawner.md"
if [ -f "$CLAUDE_SKILL_PATH" ]; then
    echo -e "${CYAN}Removing system-wide Claude Code skill '$CLAUDE_SKILL_PATH'...${NC}"
    rm -f "$CLAUDE_SKILL_PATH"
    echo -e "${GREEN}[OK] System-wide Claude Code skill removed.${NC}"
fi

# 3. Inform user about sibling sandboxes
echo ""
echo -e "${YELLOW}Note: Any laterally spawned application sandboxes parallel to '$DEST_FOLDER' (such as ../app-xx-codename) remain intact to protect your custom code. You can manually delete those folders if no longer needed.${NC}"
echo -e "${RED}[OK] Uninstallation complete.${NC}"
