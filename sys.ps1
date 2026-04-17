# ==============================================================================
# setup-env.ps1
# Installs Node.js 20, pnpm, and app dependencies.
# Compatible with Windows Server 2012 R2 and above (no winget required).
#
# USAGE (run as Administrator in PowerShell):
#   powershell -ExecutionPolicy Bypass -File .\setup-env.ps1 -AppDir "C:\apps\frontend"
# ==============================================================================

param (
    [string]$AppDir      = "C:\apps\frontend",
    [string]$NodeVersion = "20"
)

$ErrorActionPreference = "Stop"

# ---- Force TLS 1.2 (required on Windows Server 2012 R2) ---------------------
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# ---- Helpers -----------------------------------------------------------------

function Log { param($msg) Write-Host "[INFO]  $msg" -ForegroundColor Cyan }
function Ok  { param($msg) Write-Host "[OK]    $msg" -ForegroundColor Green }
function Err { param($msg) Write-Host "[ERROR] $msg" -ForegroundColor Red; exit 1 }

function Refresh-Path {
    $machine  = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
    $user     = [System.Environment]::GetEnvironmentVariable("Path", "User")
    $env:Path = $machine + ";" + $user
}

# ---- 0. Pre-flight -----------------------------------------------------------

$currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent()
$principal   = New-Object System.Security.Principal.WindowsPrincipal($currentUser)
$adminRole   = [System.Security.Principal.WindowsBuiltInRole]::Administrator

if (-not $principal.IsInRole($adminRole)) {
    Err "This script must be run as Administrator. Right-click PowerShell and select Run as administrator."
}

if (-not (Test-Path $AppDir)) {
    Err "AppDir '$AppDir' does not exist. Copy your source code there first."
}

# ---- 1. Install Node.js 20 ---------------------------------------------------

Log "Checking for Node.js $NodeVersion..."

$nodeExe   = Get-Command node -ErrorAction SilentlyContinue
$needsNode = $true

if ($nodeExe) {
    $installedMajor = (node --version) -replace "v(\d+).*", '$1'
    if ([int]$installedMajor -ge [int]$NodeVersion) {
        Ok "Node.js $(node --version) already installed -- skipping."
        $needsNode = $false
    } else {
        Log "Found Node.js v$installedMajor but need >= $NodeVersion. Upgrading..."
    }
}

if ($needsNode) {
    # Fetch the index.json from nodejs.org to find the exact latest v20 version string
    Log "Looking up latest Node.js $NodeVersion release..."
    try {
        $indexUrl  = "https://nodejs.org/dist/latest-v$NodeVersion.x/SHASUMS256.txt"
        $shaText   = Invoke-WebRequest -Uri $indexUrl -UseBasicParsing | Select-Object -ExpandProperty Content
        # Extract the x64 msi filename from the checksum file
        $msiName   = ($shaText -split "`n" | Where-Object { $_ -match "node-v[\d.]+-x64\.msi" }) `
                         -replace "^[a-f0-9]+\s+", "" | Select-Object -First 1
        $msiName   = $msiName.Trim()
    } catch {
        Err "Failed to fetch Node.js version info from nodejs.org. Check internet connectivity. Error: $_"
    }

    if (-not $msiName) {
        Err "Could not parse MSI filename from nodejs.org index. Please install Node.js $NodeVersion manually from https://nodejs.org"
    }

    $msiUrl  = "https://nodejs.org/dist/latest-v$NodeVersion.x/$msiName"
    $msiPath = "$env:TEMP\$msiName"

    Log "Downloading $msiName ..."
    try {
        Invoke-WebRequest -Uri $msiUrl -OutFile $msiPath -UseBasicParsing
    } catch {
        Err "Download failed: $_"
    }

    Log "Installing Node.js (this may take a minute)..."
    Start-Process msiexec.exe -ArgumentList "/i `"$msiPath`" /qn /norestart ADDLOCAL=ALL" -Wait -NoNewWindow
    Remove-Item $msiPath -Force

    Refresh-Path

    $nodeCheck = Get-Command node -ErrorAction SilentlyContinue
    if (-not $nodeCheck) {
        Err "Node.js installed but 'node' command not found. Please open a new PowerShell window and re-run the script."
    }
    Ok "Node.js $(node --version) installed."
}

# ---- 2. Install pnpm globally ------------------------------------------------

Log "Checking for pnpm..."
$pnpmExe = Get-Command pnpm -ErrorAction SilentlyContinue

if (-not $pnpmExe) {
    Log "Installing pnpm globally..."
    npm install -g pnpm
    if ($LASTEXITCODE -ne 0) { Err "pnpm global install failed." }
    Refresh-Path
    Ok "pnpm $(pnpm --version) installed."
} else {
    Ok "pnpm $(pnpm --version) already installed -- skipping."
}

# ---- 3. Install app dependencies ---------------------------------------------

Log "Installing app dependencies in '$AppDir'..."
Push-Location $AppDir
    pnpm install
    if ($LASTEXITCODE -ne 0) { Err "pnpm install failed." }
Pop-Location
Ok "Dependencies installed."

# ---- Done --------------------------------------------------------------------

Write-Host ""
Write-Host "====================================================" -ForegroundColor Yellow
Write-Host "  Environment ready!" -ForegroundColor Yellow
Write-Host "  Node.js : $(node --version)" -ForegroundColor Yellow
Write-Host "  pnpm    : v$(pnpm --version)" -ForegroundColor Yellow
Write-Host "  App dir : $AppDir" -ForegroundColor Yellow
Write-Host "" -ForegroundColor Yellow
Write-Host "  To run locally, open two terminals and run:" -ForegroundColor Yellow
Write-Host "    cd $AppDir" -ForegroundColor Yellow
Write-Host "    pnpm run dev       <- terminal 1" -ForegroundColor Yellow
Write-Host "    node watcher.js    <- terminal 2" -ForegroundColor Yellow
Write-Host "====================================================" -ForegroundColor Yellow