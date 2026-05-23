# uninstall.ps1 - Complete Uninstallation for Isolated App Factory Engine
$DestFolder = "appFactory"

Write-Host "=============================================" -ForegroundColor Red
Write-Host "💀 Uninstalling Isolated App Factory Engine..." -ForegroundColor Red
Write-Host "=============================================" -ForegroundColor Red

# Confirm uninstallation
$Confirmation = Read-Host "Are you sure you want to remove the App Factory folder '$DestFolder'? (y/n)"
if ($Confirmation -ne "y") {
    Write-Host "Uninstallation cancelled." -ForegroundColor Cyan
    exit 0
}

# 1. Remove App Factory Folder
if (Test-Path $DestFolder) {
    Write-Host "Removing App Factory orchestrator directory '$DestFolder'..." -ForegroundColor Cyan
    Remove-Item -Recurse -Force $DestFolder
    Write-Host "[OK] Orchestrator files deleted." -ForegroundColor Green
} else {
    Write-Host "Orchestrator directory '$DestFolder' was not found in the current working directory." -ForegroundColor Yellow
}

# 2. Remove system-wide Claude Code Skill if present
$ClaudeSkillPath = "$HOME\.claude\skills\appfactory-spawner.md"
if (Test-Path $ClaudeSkillPath) {
    Write-Host "Removing system-wide Claude Code skill '$ClaudeSkillPath'..." -ForegroundColor Cyan
    Remove-Item -Force $ClaudeSkillPath
    Write-Host "[OK] System-wide Claude Code skill removed." -ForegroundColor Green
}

# 3. Inform user about sibling sandboxes
Write-Host ""
Write-Host "Note: Any laterally spawned application sandboxes parallel to '$DestFolder' (such as ../app-xx-codename) remain intact to protect your custom code. You can manually delete those folders if no longer needed." -ForegroundColor Yellow
Write-Host "[OK] Uninstallation complete." -ForegroundColor Red
