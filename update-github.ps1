# Git Auto-Update Script for ShareMarket

# Navigate to your project folder
Set-Location "C:\Users\yuvar\Projects\ShareMarket"

# Ask for commit message
$commitMessage = Read-Host "Enter commit message"

# Stage all changes
git add .

# Commit changes
git commit -m "$commitMessage"

# Pull latest changes to avoid conflicts
git pull origin main --rebase

# Push changes to GitHub
git push origin main

Write-Host "Update complete! Your changes are now on GitHub."