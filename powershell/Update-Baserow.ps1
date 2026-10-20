[CmdletBinding()]

# Set error handling and navigate to your compose directory
$ErrorActionPreference = "Stop"
$ComposeDir = "C:\Projects\Docker\Baserow"

Write-Host "1/5 Starting Docker Desktop..." -ForegroundColor Cyan
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"

# Wait for Docker daemon to become responsive
Write-Host "Waiting for Docker engine to initialize..." -ForegroundColor Yellow
while (-not (docker info 2>$null)) {
    Start-Sleep -Seconds 2
}
Write-Host "Docker is up and running!" -ForegroundColor Green

# Change directory to the compose file location
Set-Location -Path $ComposeDir

# Pull latest image and recreate container
Write-Host "2/5 Pulling latest Baserow image..." -ForegroundColor Cyan
docker compose pull

Write-Host "3/5 Recreating container with updated image..." -ForegroundColor Cyan
docker compose up -d

# Prune old untagged (<none>) images
Write-Host "4/5 Cleaning up old dangling images..." -ForegroundColor Cyan
docker image prune -f

# Stop Docker Desktop to free system resources
Write-Host "5/5 Shutting down Docker Desktop to save system memory..." -ForegroundColor Cyan
Stop-Process -Name "Docker Desktop" -Force -ErrorAction SilentlyContinue
Get-Process -Name "com.docker.backend" -ErrorAction SilentlyContinue | Stop-Process -Force

Write-Host "Update complete! Baserow updated and Docker shut down successfully." -ForegroundColor Green
Pause

