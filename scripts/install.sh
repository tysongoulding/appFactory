#!/usr/bin/env bash
# install.sh - Automated Setup for the Isolated App Factory Engine on macOS & Linux

REPO_URL="https://github.com/tysongoulding/appFactory.git"
DEST_FOLDER="appFactory"

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=============================================${NC}"
echo -e "${GREEN}🏭 Installing Isolated App Factory Engine...${NC}"
echo -e "${GREEN}=============================================${NC}"

# 1. Check Git
if ! command -v git &> /dev/null; then
    echo -e "${RED}ERROR: Git is not installed on this system. Please install Git and try again.${NC}"
    exit 1
fi

# 2. Check Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 is not installed or not in PATH. Please install Python and try again.${NC}"
    exit 1
fi

# 3. Clone Repository
if [ -d "$DEST_FOLDER" ]; then
    echo -e "${YELLOW}WARN: Destination folder '$DEST_FOLDER' already exists. Pulling latest updates...${NC}"
    git -C "$DEST_FOLDER" pull
else
    echo -e "${CYAN}Cloning orchestrator repository from GitHub...${NC}"
    git clone "$REPO_URL" "$DEST_FOLDER"
fi

# 4. Install AI Editor & Agent Skills
echo -e "${CYAN}Configuring AI editor rules and agent skills...${NC}"
if [ -f "$DEST_FOLDER/scripts/install_skills.py" ]; then
    if command -v python3 &> /dev/null; then
        python3 "$DEST_FOLDER/scripts/install_skills.py"
    else
        python "$DEST_FOLDER/scripts/install_skills.py"
    fi
fi

echo ""
echo -e "${GREEN}[OK] Isolated App Factory Engine successfully installed!${NC}"
echo -e "${YELLOW}Navigate into the directory to begin spawning apps:${NC}"
echo -e "  cd $DEST_FOLDER"
echo -e "  python3 scripts/spawn_app.py --codename Horizon --platform iOS"
