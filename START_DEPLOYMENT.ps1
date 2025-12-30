# Family Budget Tracker - Deployment Helper Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Family Budget Tracker - Mobile Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if GitHub Desktop is installed
$githubDesktop = Get-ChildItem "C:\Users\$env:USERNAME\AppData\Local\GitHubDesktop\GitHubDesktop.exe" -ErrorAction SilentlyContinue

if ($githubDesktop) {
    Write-Host "✓ GitHub Desktop is installed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Open GitHub Desktop"
    Write-Host "2. File → Add Local Repository"
    Write-Host "3. Select: $PWD"
    Write-Host "4. Click 'Publish repository' (make it PUBLIC)"
    Write-Host ""
    $open = Read-Host "Open GitHub Desktop now? (Y/N)"
    if ($open -eq "Y" -or $open -eq "y") {
        Start-Process $githubDesktop.FullName
    }
} else {
    Write-Host "GitHub Desktop not found." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please install GitHub Desktop:" -ForegroundColor Yellow
    Write-Host "1. Download from: https://desktop.github.com" -ForegroundColor Cyan
    Write-Host "2. Install and sign in with GitHub"
    Write-Host "3. Then run this script again"
    Write-Host ""
    $open = Read-Host "Open download page in browser? (Y/N)"
    if ($open -eq "Y" -or $open -eq "y") {
        Start-Process "https://desktop.github.com"
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deployment Steps:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Step 1: Create GitHub Repository" -ForegroundColor Yellow
Write-Host "  → Go to: https://github.com/new" -ForegroundColor Cyan
Write-Host "  → Name: family-budget-tracker" -ForegroundColor White
Write-Host "  → Make it PUBLIC" -ForegroundColor White
Write-Host "  → DO NOT initialize with README" -ForegroundColor White
Write-Host ""
Write-Host "Step 2: Upload Code with GitHub Desktop" -ForegroundColor Yellow
Write-Host "  → File → Add Local Repository" -ForegroundColor White
Write-Host "  → Select this folder: $PWD" -ForegroundColor White
Write-Host "  → Publish repository (make it PUBLIC)" -ForegroundColor White
Write-Host ""
Write-Host "Step 3: Deploy to Streamlit Cloud" -ForegroundColor Yellow
Write-Host "  → Go to: https://share.streamlit.io" -ForegroundColor Cyan
Write-Host "  → Sign in with GitHub" -ForegroundColor White
Write-Host "  → New app → Select repository" -ForegroundColor White
Write-Host "  → Main file: app.py" -ForegroundColor White
Write-Host "  → Deploy!" -ForegroundColor White
Write-Host ""
Write-Host "Step 4: Access on Your Phone!" -ForegroundColor Yellow
Write-Host "  → You'll get a URL like: https://your-app.streamlit.app" -ForegroundColor Cyan
Write-Host "  → Open it on your phone and bookmark it!" -ForegroundColor White
Write-Host ""

$openGuide = Read-Host "Open detailed guide (SETUP_FOR_DEPLOYMENT.md)? (Y/N)"
if ($openGuide -eq "Y" -or $openGuide -eq "y") {
    Start-Process notepad "$PWD\SETUP_FOR_DEPLOYMENT.md"
}

Write-Host ""
Write-Host "All files are ready in: $PWD" -ForegroundColor Green
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

