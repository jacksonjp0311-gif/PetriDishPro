# PETRI DISH PRO — STANDALONE ALL-ONE DEMO RUNNER
# Creates no external mutations beyond this repo's reports/artifacts/node_modules.

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

function Say($Message, $Glyph) {
    Write-Host "$Glyph $Message" -ForegroundColor Cyan
}

Say "Petri Dish Pro root anchored: $Root" "🜂"

$Dirs = @("reports", "artifacts", "artifacts\runs")
foreach ($Dir in $Dirs) {
    if (-not (Test-Path $Dir)) {
        New-Item -ItemType Directory -Path $Dir -Force | Out-Null
    }
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python was not found. Install Python 3.10+ and add it to PATH." -ForegroundColor Red
    exit 1
}

Say "Running Python tests." "∿"
python -m unittest discover -s tests

Say "Running demo simulation." "🜄"
python -m petri_lab.cli --root . --preset microbial_competition --json

Say "Artifacts written under reports/ and artifacts/runs/." "🜁"

if (Get-Command npm -ErrorAction SilentlyContinue) {
    Say "npm found. Preparing Electron UI." "🜂"
    Set-Location "$Root\electron"
    if (-not (Test-Path ".\node_modules")) {
        npm install
    }
    npm start
}

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Host "npm not found, so Electron was skipped. Python engine is ready." -ForegroundColor Yellow
}

Set-Location $Root
Say "Returned to repo root." "∿"
