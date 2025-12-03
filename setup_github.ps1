# GitHub Setup Script
# Run this script to set up GitHub

Write-Host "=== GitHub Setup ===" -ForegroundColor Green
Write-Host ""

# Check if Git is configured
$gitName = git config --global user.name
$gitEmail = git config --global user.email

if (-not $gitName -or -not $gitEmail) {
    Write-Host "Git is not configured yet." -ForegroundColor Yellow
    Write-Host ""
    $name = Read-Host "Enter your name (for Git commits)"
    $email = Read-Host "Enter your email (for Git commits)"
    
    git config --global user.name "$name"
    git config --global user.email "$email"
    
    Write-Host "Git configured!" -ForegroundColor Green
} else {
    Write-Host "Git is already configured:" -ForegroundColor Green
    Write-Host "  Name: $gitName"
    Write-Host "  Email: $gitEmail"
}

Write-Host ""
Write-Host "=== Next Steps ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Go to https://github.com and create a new repository"
Write-Host "2. Copy the repository URL"
Write-Host "3. Run these commands:"
Write-Host ""
Write-Host "   git remote add origin YOUR_REPO_URL" -ForegroundColor Yellow
Write-Host "   git commit -m 'Initial commit'" -ForegroundColor Yellow
Write-Host "   git branch -M main" -ForegroundColor Yellow
Write-Host "   git push -u origin main" -ForegroundColor Yellow
Write-Host ""
Write-Host "Or see GITHUB_SETUP.md for detailed instructions" -ForegroundColor Gray

