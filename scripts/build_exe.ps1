# Empaqueta 6SNT.ADIF-HUB como un .exe unico (Windows).
# Sirve la SPA compilada desde el backend FastAPI y abre el navegador al arrancar.
# Uso:  pwsh -File scripts\build_exe.ps1
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$py = Join-Path $root "backend\.venv\Scripts\python.exe"

Write-Host "[1/4] Generando icono de marca..." -ForegroundColor Cyan
& $py (Join-Path $root "scripts\make_icon.py")

Write-Host "[2/4] Compilando frontend (vite build)..." -ForegroundColor Cyan
Push-Location (Join-Path $root "frontend")
npm run build
Pop-Location

Write-Host "[3/4] Asegurando PyInstaller..." -ForegroundColor Cyan
& $py -m pip install --quiet pyinstaller

Write-Host "[4/4] Empaquetando .exe..." -ForegroundColor Cyan
& $py -m PyInstaller --noconfirm --onefile --name "6SNT.ADIF-HUB" `
  --icon (Join-Path $root "branding\6snt-icon.ico") `
  --distpath (Join-Path $root "dist_exe") `
  --workpath (Join-Path $root "build_exe") `
  --specpath (Join-Path $root "build_exe") `
  --paths (Join-Path $root "backend") `
  --add-data ("{0};frontend_dist" -f (Join-Path $root "frontend\dist")) `
  --collect-submodules uvicorn `
  --hidden-import python_multipart --hidden-import multipart `
  --hidden-import openpyxl --hidden-import defusedxml `
  --collect-all webview --hidden-import webview.platforms.edgechromium `
  --collect-all clr_loader --collect-all pythonnet --hidden-import clr `
  (Join-Path $root "backend\desktop.py")

Write-Host "Listo: dist_exe\6SNT.ADIF-HUB.exe" -ForegroundColor Green
