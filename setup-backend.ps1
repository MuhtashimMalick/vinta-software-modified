# ==============================================================================
# setup-backend.ps1
# Installs Python 3.12, creates .venv, installs requirements, runs backend.bat
# Compatible with Windows Server 2012 R2 (no winget required).
#
# USAGE (run as Administrator in PowerShell):
#   powershell -ExecutionPolicy Bypass -File .\setup-backend.ps1
# ==============================================================================

param (
    [string]$BackendDir = "C:\Users\Administrator\Documents\vinta-software-modified\fastapi_backend"
)

$ErrorActionPreference = "Stop"

# ---- Force TLS 1.2 (required on Windows Server 2012 R2) ---------------------
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# ---- Helpers -----------------------------------------------------------------

function Log  { param($msg) Write-Host "[INFO]  $msg" -ForegroundColor Cyan }
function Ok   { param($msg) Write-Host "[OK]    $msg" -ForegroundColor Green }
function Err  { param($msg) Write-Host "[ERROR] $msg" -ForegroundColor Red; exit 1 }
function Step { param($msg) Write-Host "`n-------- $msg" -ForegroundColor Magenta }

function Refresh-Path {
    $machine  = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
    $user     = [System.Environment]::GetEnvironmentVariable("Path", "User")
    $env:Path = $machine + ";" + $user
}

# ---- 0. Pre-flight -----------------------------------------------------------

Step "Pre-flight checks"

$currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent()
$principal   = New-Object System.Security.Principal.WindowsPrincipal($currentUser)
$adminRole   = [System.Security.Principal.WindowsBuiltInRole]::Administrator

if (-not $principal.IsInRole($adminRole)) {
    Err "This script must be run as Administrator. Right-click PowerShell and select Run as administrator."
}

if (-not (Test-Path $BackendDir)) {
    Err "Backend folder not found: '$BackendDir'"
}

$requirementsTxt = Join-Path $BackendDir "req.txt"
if (-not (Test-Path $requirementsTxt)) {
    Err "requirements.txt not found in '$BackendDir'"
}

$backendBat = Join-Path $BackendDir "backend.bat"
if (-not (Test-Path $backendBat)) {
    Err "backend.bat not found in '$BackendDir'"
}

Ok "All paths verified."

# ---- 1. Install Python 3.12 --------------------------------------------------

Step "Checking Python 3.12"

$pythonExe   = $null
$needsPython = $true

# Check if python 3.12 is already installed
$existingPython = Get-Command python -ErrorAction SilentlyContinue
if ($existingPython) {
    $pyVersion = & python --version 2>&1
    Log "Found: $pyVersion"
    if ($pyVersion -match "3\.12") {
        Ok "Python 3.12 already installed -- skipping."
        $pythonExe   = "python"
        $needsPython = $false
    } else {
        Log "Installed Python is not 3.12. Will install 3.12 alongside it."
    }
}

if ($needsPython) {
    # Python 3.12 latest stable - direct MSI download
    $pyInstallerUrl  = "https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe"
    $pyInstallerPath = "$env:TEMP\python-3.12.9-amd64.exe"

    Log "Downloading Python 3.12.9 installer..."
    try {
        Invoke-WebRequest -Uri $pyInstallerUrl -OutFile $pyInstallerPath -UseBasicParsing
    } catch {
        Err "Failed to download Python installer. Check internet connection. Error: $_"
    }

    Log "Installing Python 3.12.9 (this may take a minute)..."
    # /quiet         = silent install
    # PrependPath=1  = add Python to system PATH
    # Include_pip=1  = ensure pip is included
    # Include_test=0 = skip test suite to save space
    Start-Process -FilePath $pyInstallerPath `
                  -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_pip=1 Include_test=0" `
                  -Wait -NoNewWindow

    Remove-Item $pyInstallerPath -Force
    Refresh-Path

    # Verify install
    $pythonCheck = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pythonCheck) {
        Err "Python installed but 'python' command not found in PATH. Close this window, open a new Admin PowerShell, and re-run the script."
    }

    $pyVersion = & python --version 2>&1
    Ok "$pyVersion installed successfully."
    $pythonExe = "python"
}

# ---- 2. Verify pip is available ----------------------------------------------

Step "Checking pip"

$pipCheck = & $pythonExe -m pip --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Log "pip not found, installing via ensurepip..."
    & $pythonExe -m ensurepip --upgrade
    if ($LASTEXITCODE -ne 0) { Err "Failed to install pip via ensurepip." }
}

# Upgrade pip to latest
Log "Upgrading pip..."
& $pythonExe -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { Err "pip upgrade failed." }

$pipVersion = & $pythonExe -m pip --version 2>&1
Ok "$pipVersion"

# ---- 3. Create .venv virtual environment ------------------------------------

Step "Creating .venv in '$BackendDir'"

$venvDir     = Join-Path $BackendDir ".venv"
$venvPython  = Join-Path $venvDir "Scripts\python.exe"
$venvPip     = Join-Path $venvDir "Scripts\pip.exe"
$venvActivate = Join-Path $venvDir "Scripts\activate.bat"

if (Test-Path $venvDir) {
    Log ".venv already exists -- recreating to ensure clean state..."
    Remove-Item $venvDir -Recurse -Force
}

& $pythonExe -m venv $venvDir
if ($LASTEXITCODE -ne 0) { Err "Failed to create virtual environment." }

if (-not (Test-Path $venvPython)) {
    Err ".venv created but python.exe not found inside it. Something went wrong."
}

Ok ".venv created at '$venvDir'."

# ---- 4. Install requirements.txt --------------------------------------------

Step "Installing requirements from '$requirementsTxt'"

Log "Running pip install -r req.txt inside .venv..."
& $venvPip install -r $requirementsTxt
if ($LASTEXITCODE -ne 0) { Err "pip install -r requirements.txt failed. Check the output above for details." }

Ok "All requirements installed."

# ---- 5. Launch backend.bat --------------------------------------------------

Step "Starting backend"

Log "Launching '$backendBat'..."
Log "The backend will run in this window. Press Ctrl+C to stop."
Write-Host ""

Set-Location $BackendDir
& cmd.exe /c $backendBat

# ---- Done --------------------------------------------------------------------
# (Execution reaches here only if backend.bat exits on its own)
Write-Host ""
Ok "backend.bat has exited."