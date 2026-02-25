$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Join-Path $projectRoot "backend"
$pythonExe = Join-Path $backendDir ".venv\\Scripts\\python.exe"

if (-not (Test-Path $pythonExe)) {
  Write-Host "未找到虚拟环境 Python：" -ForegroundColor Yellow
  Write-Host $pythonExe -ForegroundColor Yellow
  Write-Host "请先在 quant-news-site/backend 中创建并安装依赖。" -ForegroundColor Yellow
  exit 1
}

Write-Host "启动后端服务..." -ForegroundColor Cyan
Start-Process "http://127.0.0.1:8000/"

Push-Location $backendDir
try {
  & $pythonExe -m uvicorn app.main:app --reload
}
finally {
  Pop-Location
}

