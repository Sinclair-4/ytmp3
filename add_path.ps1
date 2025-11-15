# Add directory to user PATH in Windows
param(
    [Parameter(Mandatory=$false)]
    [string]$PathToAdd
)

# If no path provided, use the parent directory of this script
if (-not $PathToAdd) {
    $scriptPath = $MyInvocation.MyCommand.Path
    $scriptDirectory = Split-Path -Path $scriptPath -Parent
    $PathToAdd = $scriptDirectory
    Write-Host "No path specified. Using parent directory of script: $PathToAdd" -ForegroundColor Cyan
}

# Get current user PATH
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")

# Check if path already exists
if ($currentPath -split ';' -contains $PathToAdd) {
    Write-Host "Path already exists in user PATH" -ForegroundColor Yellow
} else {
    # Add new path to user PATH
    $newPath = $currentPath + ";" + $PathToAdd
    [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
    Write-Host "Successfully added $PathToAdd to user PATH" -ForegroundColor Green
    Write-Host "You may need to restart your terminal for changes to take effect" -ForegroundColor Yellow
}