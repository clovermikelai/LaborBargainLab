# push_to_github.ps1
# Automates the creation of the GitHub repository under clovermikelai and pushes the local main branch.

param(
    [string]$Token = $env:GITHUB_TOKEN
)

$env:Path = [Environment]::GetEnvironmentVariable("Path", "User") + ";" + [Environment]::GetEnvironmentVariable("Path", "Machine")
$repoName = "LaborBargainLab"
$orgOrUser = "clovermikelai"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "LaborBargainLab - GitHub Repository Deployment Tool" -ForegroundColor Cyan
Write-Host "Target: https://github.com/$orgOrUser/$repoName" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# Check if repo already exists on GitHub
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$repoExists = $false
try {
    $check = Invoke-RestMethod -Uri "https://api.github.com/repos/$orgOrUser/$repoName" -Headers @{ "User-Agent" = "PowerShell" } -ErrorAction SilentlyContinue
    if ($check) { $repoExists = $true }
} catch {
    $repoExists = $false
}

if (-not $repoExists) {
    Write-Host "[1/2] Creating new repository on GitHub: $orgOrUser/$repoName..." -ForegroundColor Yellow

    # If gh CLI is logged in
    $ghStatus = & gh auth status 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  -> Using GitHub CLI (gh) to create repo..." -ForegroundColor Green
        & gh repo create "$orgOrUser/$repoName" --public --description "Multi-Agent Strike Negotiation Simulator & Labor Decision Support System"
    } elseif ($Token) {
        Write-Host "  -> Using GitHub Personal Access Token to create repo via API..." -ForegroundColor Green
        $body = @{
            name = $repoName
            description = "Multi-Agent Strike Negotiation Simulator & Labor Decision Support System"
            private = $false
        } | ConvertTo-Json
        $headers = @{
            "Authorization" = "token $Token"
            "User-Agent" = "LaborBargainLab-Deployer"
            "Accept" = "application/vnd.github.v3+json"
        }
        $created = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post -Headers $headers -Body $body -ContentType "application/json"
        Write-Host "  -> Created successfully: $($created.html_url)" -ForegroundColor Green
    } else {
        Write-Host "  [!] Notice: GitHub authentication credential is needed to push automatically." -ForegroundColor Yellow
        Write-Host "  Please choose one of the following simple steps:" -ForegroundColor Yellow
        Write-Host "    Option A: Run 'gh auth login' (select GitHub.com -> HTTPS -> Login with a web browser), then re-run this script." -ForegroundColor Cyan
        Write-Host "    Option B: Run .\scripts\push_to_github.ps1 -Token <YOUR_GITHUB_PAT>" -ForegroundColor Cyan
        Write-Host "    Option C: Create repo '$repoName' on https://github.com/new, then run 'git push -u origin main'" -ForegroundColor Cyan
        return
    }
} else {
    Write-Host "[1/2] Repository exists on GitHub: $orgOrUser/$repoName" -ForegroundColor Green
}

Write-Host "[2/2] Pushing main branch to GitHub..." -ForegroundColor Yellow
if ($Token) {
    git push "https://$($Token)@github.com/$orgOrUser/$repoName.git" main -u
} else {
    git push origin main -u
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "Success! Project published to https://github.com/$orgOrUser/$repoName" -ForegroundColor Green
} else {
    Write-Host "Push completed or requires authentication." -ForegroundColor Yellow
}
