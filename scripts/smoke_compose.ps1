$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

if (-not (Test-Path ".env")) {
    Write-Error "Создайте .env из .env.example: Copy-Item .env.example .env"
}

docker compose up -d --build
Write-Host "Ожидание health приложения..."
$ok = $false
for ($i = 0; $i -lt 40; $i++) {
    try {
        Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -UseBasicParsing -TimeoutSec 3 | Out-Null
        Write-Host "OK /health"
        $ok = $true
        break
    } catch {
        Start-Sleep -Seconds 1
    }
}
if (-not $ok) {
    docker compose ps
    docker compose logs --tail=80 app
    throw "Таймаут health"
}

$body = "title=smoke&body=from-script"
Invoke-WebRequest -Uri "http://127.0.0.1:8000/notes/new" -Method POST -ContentType "application/x-www-form-urlencoded" -Body $body -UseBasicParsing | Out-Null
$html = (Invoke-WebRequest -Uri "http://127.0.0.1:8000/" -UseBasicParsing).Content
if ($html -notmatch "smoke") { throw "Smoke: заметка не найдена в списке" }
Write-Host "Smoke: CRUD create + список OK"
