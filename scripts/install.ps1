# install.ps1 - Automated Setup for the Isolated App Factory Engine
$RepoUrl = "https://github.com/tysongoulding/appFactory.git"
$DestFolder = "appFactory"

Write-Host "=============================================" -ForegroundColor Green
Write-Host "🏭 Installing Isolated App Factory Engine..." -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

# 1. Check Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "Git is not installed on this system. Please install Git and try again."
    exit 1
}

# 2. Check Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python 3 is not installed or not in PATH. Please install Python and try again."
    exit 1
}

# 3. Clone Repository
if (Test-Path $DestFolder) {
    Write-Warning "Destination folder '$DestFolder' already exists. Pulling latest updates..."
    git -C $DestFolder pull
} else {
    Write-Host "Cloning orchestrator repository from GitHub..." -ForegroundColor Cyan
    git clone $RepoUrl $DestFolder
}

Write-Host ""
Write-Host "[OK] Isolated App Factory Engine successfully installed!" -ForegroundColor Green
Write-Host "Navigate into the directory to begin spawning apps:" -ForegroundColor Yellow
Write-Host "  cd $DestFolder" -ForegroundColor Yellow
Write-Host "  python scripts/spawn_app.py --codename Horizon --platform iOS" -ForegroundColor Yellow
