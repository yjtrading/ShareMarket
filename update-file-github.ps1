# Git Auto-Update Script for a Specific File

# Navigate to your project folder
Set-Location "C:\Users\yuvar\Projects\ShareMarket"

# Ask for the file to update
$fileToUpdate = Read-Host "Enter the file name to update (e.g., index.html)"

# Check if the file exists
if (-Not (Test-Path $fileToUpdate)) {
    Write-Host "File not found! Please check the name and try again."
    exit
}

# Ask for commit message
$commitMessage = Read-Host "Enter commit message"

# Stage only the specified file
git add $fileToUpdate

# Commit changes
git commit -m "$commitMessage"

# Pull latest changes to avoid conflicts
git pull origin main --rebase

# Push changes to GitHub
git push origin main

Write-Host "Update complete! '$fileToUpdate' is now updated on GitHub."
