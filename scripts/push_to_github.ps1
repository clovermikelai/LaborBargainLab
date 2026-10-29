# push_to_github.ps1
# Automates the creation of the GitHub repository under clovermikelai and pushes the local main branch.

param(
    [string]$Token = $env:GITHUB_TOKEN
)

$env:Path = [Environment]::GetEnvironmentVariable("Path", "User") + ";" + [Environment]::GetEnvironmentVariable("Path", "Machine")
$repoName = "LaborBargainLab"
$orgOrUser = "clovermikelai"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "🚀 LaborBargainLab - GitHub Repository Deployment Tool" -ForegroundColor Cyan
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
    Write-Host "[1/2] 正在 GitHub 上建立新 Repository: $orgOrUser/$repoName..." -ForegroundColor Yellow

    # If gh CLI is logged in
    $ghStatus = gh auth status 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  -> 使用 GitHub CLI (gh) 建立 Repo..." -ForegroundColor Green
        gh repo create "$orgOrUser/$repoName" --public --description "Multi-Agent Strike Negotiation Simulator & Labor Decision Support System"
    } elseif ($Token) {
        Write-Host "  -> 使用 GitHub Personal Access Token 建立 Repo..." -ForegroundColor Green
        $body = @{
            name = $repoName
            description = "Multi-Agent Strike Negotiation Simulator & Labor Decision Support System (美光罷工協商模擬器)"
            private = $false
        } | ConvertTo-Json
        $headers = @{
            "Authorization" = "token $Token"
            "User-Agent" = "LaborBargainLab-Deployer"
            "Accept" = "application/vnd.github.v3+json"
        }
        $created = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post -Headers $headers -Body $body -ContentType "application/json"
        Write-Host "  -> Repo 建立成功: $($created.html_url)" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️ 尚未偵測到 GitHub 登入憑證或 Token。" -ForegroundColor Yellow
        Write-Host "  請選擇以下任一方式完成建立與推送：" -ForegroundColor Yellow
        Write-Host "    方式 A: 執行 'gh auth login'（選擇 GitHub.com -> HTTPS -> 瀏覽器登入），再重新執行此腳本。"
        Write-Host "    方式 B: .\scripts\push_to_github.ps1 -Token <你的_GITHUB_PAT>"
        Write-Host "    方式 C: 到 https://github.com/new 建立名稱為 '$repoName' 的 Public Repo，然後執行 'git push -u origin main'"
        return
    }
} else {
    Write-Host "[1/2] GitHub 上已存在 Repository: $orgOrUser/$repoName" -ForegroundColor Green
}

Write-Host "[2/2] 正在推送 main 分支到 GitHub..." -ForegroundColor Yellow
if ($Token) {
    git push "https://$($Token)@github.com/$orgOrUser/$repoName.git" main -u
} else {
    git push origin main -u
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "🎉 恭喜！專案已成功推送到 https://github.com/$orgOrUser/$repoName" -ForegroundColor Green
} else {
    Write-Host "❌ 推送遇到問題，請確認 GitHub 存取權限。" -ForegroundColor Red
}
