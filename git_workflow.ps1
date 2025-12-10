# Quick Git workflow script
# Usage: .\git_workflow.ps1 -message "Your commit message"

param(
    [string]$message = "Update notebook"
)

Write-Host ""
Write-Host "🔄 Starting Git workflow..." -ForegroundColor Cyan
Write-Host ""

# Check if there are changes
$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "ℹ️  No changes to commit" -ForegroundColor Yellow
    exit 0
}

# Add all changes
Write-Host "📝 Staging changes..." -ForegroundColor White
git add .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to stage changes" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Staged changes" -ForegroundColor Green

# Commit
Write-Host "💾 Committing changes..." -ForegroundColor White
git commit -m $message
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to commit" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Committed: $message" -ForegroundColor Green

# Push
Write-Host "🚀 Pushing to GitHub..." -ForegroundColor White
git push
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to push to GitHub" -ForegroundColor Red
    Write-Host "ℹ️  You may need to set up the remote repository first" -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ Pushed to GitHub" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 Done!" -ForegroundColor Cyan
Write-Host ""
