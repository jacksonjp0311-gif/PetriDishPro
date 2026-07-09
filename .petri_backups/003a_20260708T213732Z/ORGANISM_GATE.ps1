# PETRI DISH PRO â€” ORGANISM GATE ENTRYPOINT
# Terminal cockpit for launching Electron, running organism presets, and inspecting receipts.

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

function Write-GateLine($Text, $Color) {
    Write-Host $Text -ForegroundColor $Color
}

function Pause-Gate {
    Write-Host ""
    Write-Host "Press ENTER to return to ORGANISM GATE..." -ForegroundColor DarkCyan
    [void][System.Console]::ReadLine()
}

function Ensure-Dirs {
    $Dirs = @("reports", "artifacts", "artifacts\runs")
    foreach ($Dir in $Dirs) {
        if (-not (Test-Path $Dir)) {
            New-Item -ItemType Directory -Path $Dir -Force | Out-Null
        }
    }
}

function Assert-Python {
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Host "Python was not found. Install Python 3.10+ and add it to PATH." -ForegroundColor Red
        return $false
    }
    return $true
}

function Invoke-PetriPreset($Preset, $Grid, $Steps) {
    Ensure-Dirs
    $Ok = Assert-Python
    if (-not $Ok) { return }
    Write-GateLine "ðŸœ‚ Running preset: $Preset  grid=$Grid  steps=$Steps" Cyan
    python -m petri_lab.cli --root . --preset $Preset --grid $Grid --steps $Steps --json
    Write-GateLine "âˆ¿ Latest artifacts refreshed under reports/ and artifacts/runs/." Green
}

function Invoke-PetriTests {
    $Ok = Assert-Python
    if (-not $Ok) { return }
    Write-GateLine "âˆ¿ Running Petri Dish Pro validation tests." Cyan
    python -m unittest discover -s tests
}

function Start-PetriElectron {
    Ensure-Dirs
    if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
        Write-Host "npm was not found. Install Node.js LTS, then run this again." -ForegroundColor Yellow
        return
    }
    Write-GateLine "ðŸœ„ Entering Electron organism microscope HUD." Cyan
    Set-Location "$Root\electron"
    if (-not (Test-Path ".\node_modules")) {
        Write-GateLine "âˆ¿ Installing Electron dependencies locally." Yellow
        npm install
    }
    npm start
    Set-Location $Root
}

function Show-LatestReceipt {
    Write-GateLine "ðŸœ Latest validation / run receipt" Cyan
    $Validation = Join-Path $Root "reports\latest_validation.json"
    $Summary = Join-Path $Root "reports\latest_summary.md"
    if (Test-Path $Validation) {
        Write-Host ""
        Get-Content $Validation -Raw | Write-Host -ForegroundColor Gray
    }
    if (-not (Test-Path $Validation)) {
        Write-Host "No validation receipt found yet. Run a preset first." -ForegroundColor Yellow
    }
    if (Test-Path $Summary) {
        Write-Host ""
        Write-GateLine "--- SUMMARY ---" DarkCyan
        Get-Content $Summary -Raw | Write-Host -ForegroundColor Gray
    }
}

function Open-ArtifactFolder {
    Ensure-Dirs
    $Path = Join-Path $Root "artifacts\runs"
    Write-GateLine "Opening artifact folder: $Path" Cyan
    Invoke-Item $Path
}

function Show-Roadmap {
    $Roadmap = Join-Path $Root "ROADMAP.md"
    if (Test-Path $Roadmap) {
        Get-Content $Roadmap -Raw | Write-Host -ForegroundColor Gray
    }
    if (-not (Test-Path $Roadmap)) {
        Write-Host "ROADMAP.md not found." -ForegroundColor Yellow
    }
}

function Build-PortableZip {
    $Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $Out = Join-Path (Split-Path -Parent $Root) "PetriDishPro_$Stamp.zip"
    Write-GateLine "Compressing repo to: $Out" Cyan
    $Temp = Join-Path $Root ".zip_exclude_marker"
    if (Test-Path $Out) { Remove-Item $Out -Force }
    Compress-Archive -Path "$Root\*" -DestinationPath $Out -Force
    Write-GateLine "Zip complete: $Out" Green
}

function Show-Gate {
    Clear-Host
    Write-Host ""
    Write-GateLine "        [     ""LIFE DOES NOT OBEY CHAOS. IT NEGOTIATES THRESHOLDS.""     ]" Blue
    Write-GateLine "        [     ""A CULTURE IS ONLY REAL WHEN ITS ARTIFACTS SURVIVE.""      ]" Blue
    Write-Host ""
    Write-GateLine "              .        +          .             +         ." Cyan
    Write-GateLine "          .        .::::-----::::.       .              ." Cyan
    Write-GateLine "                .:-=+***********+=-:.        +" Cyan
    Write-GateLine "             .:-+***###*******###***+-:." Cyan
    Write-GateLine "           .:=**##+-:.   .---.   .:-+##**=." Cyan
    Write-GateLine "          :=*##*-.     .-+   +-.     .-*##*=:" Cyan
    Write-GateLine "        .-+##+:.      .+  ( )  +.      .:+##+-." Cyan
    Write-GateLine "        :=###:        :  MICRO  :        :###=:" Blue
    Write-GateLine "        :=###:        : CULTURE :        :###=:" Blue
    Write-GateLine "        .-+##+:.      .+       +.      .:+##+-." Cyan
    Write-GateLine "          :=*##*-.     '-.___.-'     .-*##*=:" Cyan
    Write-GateLine "            .:=**##+-:.         .:-+##**=." Cyan
    Write-GateLine "                .:-=+***********+=-:." Cyan
    Write-GateLine "          .        .::::-----::::.       .              +" Cyan
    Write-Host ""
    Write-GateLine "             [<]  ORGANISM GATE      <|>      CULTURE LOCK  [>]" Blue
    Write-Host ""
    Write-GateLine "Rule: models simulate; humans validate claims; receipts govern promotion." Cyan
    Write-GateLine "Flow: organism preset -> field simulation -> density map -> validation -> artifact." Cyan
    Write-Host ""
    Write-GateLine " [1]  Open Electron Microscope HUD          -> full organism cockpit" Cyan
    Write-GateLine " [2]  Run Microbial Competition             -> predator / resistant / colony interaction" Cyan
    Write-GateLine " [3]  Run Antibiotic Selection              -> gradient pressure / resistant variant" Cyan
    Write-GateLine " [4]  Run Cellular Tissue Interaction       -> immune / infected / cancer-like toy model" Cyan
    Write-GateLine " [5]  Validation Tests                      -> engine sanity / artifact safety" Cyan
    Write-GateLine " [6]  Latest Run Receipt                    -> validation + summary" Cyan
    Write-GateLine " [7]  Open Artifact Folder                  -> inspect run bundles" Cyan
    Write-GateLine " [8]  Roadmap                               -> next evolution layers" Cyan
    Write-GateLine " [9]  Build Portable Zip                    -> package current repo" Cyan
    Write-GateLine " [Q]  Quit" Blue
    Write-Host ""
    Write-GateLine "====================================================================================================" DarkCyan
}

Ensure-Dirs
$Running = $true
while ($Running) {
    Show-Gate
    $Choice = Read-Host "Choose"

    if ($Choice -eq "1") {
        Start-PetriElectron
        Pause-Gate
        continue
    }
    if ($Choice -eq "2") {
        Invoke-PetriPreset "microbial_competition" 76 220
        Pause-Gate
        continue
    }
    if ($Choice -eq "3") {
        Invoke-PetriPreset "antibiotic_selection" 76 240
        Pause-Gate
        continue
    }
    if ($Choice -eq "4") {
        Invoke-PetriPreset "cellular_tissue" 72 220
        Pause-Gate
        continue
    }
    if ($Choice -eq "5") {
        Invoke-PetriTests
        Pause-Gate
        continue
    }
    if ($Choice -eq "6") {
        Show-LatestReceipt
        Pause-Gate
        continue
    }
    if ($Choice -eq "7") {
        Open-ArtifactFolder
        Pause-Gate
        continue
    }
    if ($Choice -eq "8") {
        Show-Roadmap
        Pause-Gate
        continue
    }
    if ($Choice -eq "9") {
        Build-PortableZip
        Pause-Gate
        continue
    }
    if ($Choice -match "^[Qq]$") {
        $Running = $false
        continue
    }

    Write-Host "Unknown option: $Choice" -ForegroundColor Yellow
    Pause-Gate
}

Set-Location $Root
Write-GateLine "ORGANISM GATE closed. Returned to repo root." Green

