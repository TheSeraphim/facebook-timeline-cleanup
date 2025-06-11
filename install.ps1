# Facebook Timeline Cleanup - Installation Script (PowerShell)
# Creates virtual environment, installs dependencies, and sets up repository

param(
    [switch]$Force,
    [switch]$SkipChromeCheck
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Print functions
function Print-Step {
    param([string]$Message)
    Write-Host "`n[STEP] $Message"
}

function Print-Success {
    param([string]$Message)
    Write-Host "[OK] $Message"
}

function Print-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Print-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Print-Header {
    Write-Host "================================================"
    Write-Host "    Facebook Timeline Cleanup - Installer    "
    Write-Host "================================================"
}

# Check if command exists
function Test-Command {
    param([string]$Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Check Python version
function Test-PythonVersion {
    Print-Step "Checking Python installation..."
    
    $pythonCommands = @("python", "python3", "py")
    $pythonCmd = $null
    
    foreach ($cmd in $pythonCommands) {
        if (Test-Command $cmd) {
            try {
                $version = & $cmd --version 2>&1
                if ($version -match "Python (\d+)\.(\d+)\.(\d+)") {
                    $major = [int]$matches[1]
                    $minor = [int]$matches[2]
                    $patch = [int]$matches[3]
                    
                    if ($major -gt 3 -or ($major -eq 3 -and $minor -ge 7)) {
                        $script:PythonCmd = $cmd
                        Print-Success "Python $major.$minor.$patch found ($cmd)"
                        return $true
                    }
                }
            }
            catch {
                continue
            }
        }
    }
    
    Print-Error "Python 3.7+ not found. Please install Python from https://www.python.org/"
    return $false
}

# Check if we're in the right directory
function Test-ProjectDirectory {
    Print-Step "Checking project directory..."
    
    if (-not (Test-Path "facebook_timeline_cleanup.py")) {
        Print-Error "facebook_timeline_cleanup.py not found!"
        Print-Error "Please run this script from the project root directory."
        return $false
    }
    
    Print-Success "Project directory confirmed"
    return $true
}

# Create virtual environment
function New-VirtualEnvironment {
    Print-Step "Creating virtual environment..."
    
    if (Test-Path "venv") {
        if ($Force) {
            Print-Warning "Removing existing virtual environment (Force specified)"
            Remove-Item -Recurse -Force "venv"
        }
        else {
            $response = Read-Host "Virtual environment already exists. Recreate? (y/N)"
            if ($response -eq "y" -or $response -eq "Y") {
                Remove-Item -Recurse -Force "venv"
                Print-Success "Removed existing virtual environment"
            }
            else {
                Print-Success "Using existing virtual environment"
                return $true
            }
        }
    }
    
    try {
        & $script:PythonCmd -m venv venv
        Print-Success "Virtual environment created: venv\"
        return $true
    }
    catch {
        Print-Error "Failed to create virtual environment: $_"
        return $false
    }
}

# Activate virtual environment and install dependencies
function Install-Dependencies {
    Print-Step "Activating virtual environment and installing dependencies..."
    
    $venvPython = "venv\Scripts\python.exe"
    $venvPip = "venv\Scripts\pip.exe"
    
    if (-not (Test-Path $venvPython)) {
        Print-Error "Virtual environment Python not found at $venvPython"
        return $false
    }
    
    if (-not (Test-Path "requirements.txt")) {
        Print-Error "requirements.txt not found!"
        return $false
    }
    
    try {
        # Install requirements (without upgrading pip first)
        Print-Step "Installing requirements..."
        & $venvPip install -r requirements.txt
        
        if ($LASTEXITCODE -eq 0) {
            Print-Success "Dependencies installed successfully"
            return $true
        }
        else {
            Print-Error "Failed to install some dependencies"
            return $false
        }
    }
    catch {
        Print-Error "Failed to install dependencies: $_"
        return $false
    }
}

# Create directories
function New-ProjectDirectories {
    Print-Step "Creating project directories..."
    
    $directories = @("docs", "examples", "logs")
    
    foreach ($dir in $directories) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir | Out-Null
        }
    }
    
    Print-Success "Directories created: docs\, examples\, logs\"
}

# Create configuration template using base64 encoding to avoid parsing issues
function New-ConfigurationTemplate {
    Print-Step "Creating configuration template..."
    
    # Base64 encoded JSON to completely avoid PowerShell parsing issues
    $configBase64 = "ewogICAgIl9jb21tZW50IjogIkZhY2Vib29rIFRpbWVsaW5lIENsZWFudXAgQ29uZmlndXJhdGlvbiBUZW1wbGF0ZSIsCiAgICAiX2luc3RydWN0aW9ucyI6IFsKICAgICAgICAiMS4gQ29weSB0aGlzIGZpbGUgdG8gY29uZmlnLmpzb24gb3IgYW5vdGhlciBuYW1lIiwKICAgICAgICAiMi4gRmlsbCBpbiB5b3VyIGVtYWlsIGFuZCBwYXNzd29yZCAob3IgdXNlIGVudmlyb25tZW50IHZhcmlhYmxlcykiLAogICAgICAgICIzLiBBZGp1c3QgY2xlYW5pbmcgYW5kIHRpbWluZyBwYXJhbWV0ZXJzIGFzIG5lZWRlZCIsCiAgICAgICAgIjQuIEFMV0FZUyB0ZXN0IHdpdGggd2hhdGlmOiB0cnVlIGJlZm9yZSByZWFsIGRlbGV0aW9ucyIsCiAgICAgICAgIjUuIE5ldmVyIGNvbW1pdCBjb25maWd1cmF0aW9uIGZpbGVzIHdpdGggcGFzc3dvcmRzIHRvIHZlcnNpb24gY29udHJvbCIKICAgIF0sCiAgICAiY3JlZGVudGlhbHMiOiB7CiAgICAgICAgIl9jb21tZW50IjogIkxvZ2luIGNyZWRlbnRpYWxzIGZvciBGYWNlYm9vayBhY2NvdW50IiwKICAgICAgICAiZW1haWwiOiAieW91cl9lbWFpbEBleGFtcGxlLmNvbSIsCiAgICAgICAgInBhc3N3b3JkIjogIiIKICAgIH0sCiAgICAiY2xlYW5pbmciOiB7CiAgICAgICAgIl9jb21tZW50IjogIlBhcmFtZXRlcnMgY29udHJvbGxpbmcgd2hhdCBjb250ZW50IGlzIHByb2Nlc3NlZCIsCiAgICAgICAgInBvc3RzX3Blcl9zZXNzaW9uIjogMTAsCiAgICAgICAgIm1heF9zZXNzaW9ucyI6IDUsCiAgICAgICAgInRhcmdldF9wb3N0X3R5cGVzIjogWyJzdGF0dXMiLCAicGhvdG8iLCAidmlkZW8iLCAibGluayIsICJhbGwiXQogICAgfSwKICAgICJ0aW1pbmciOiB7CiAgICAgICAgIl9jb21tZW50IjogIlRpbWluZyBjb250cm9scyB0byBhdm9pZCByYXRlIGxpbWl0aW5nIGFuZCBkZXRlY3Rpb24iLAogICAgICAgICJzZXNzaW9uX2RlbGF5IjogMzAwLAogICAgICAgICJwYWdlX3RpbWVvdXQiOiAzMCwKICAgICAgICAibWluX2FjdGlvbl9kZWxheSI6IDEuMCwKICAgICAgICAibWF4X2FjdGlvbl9kZWxheSI6IDMuMCwKICAgICAgICAibWluX2RlbGV0ZV9kZWxheSI6IDMuMCwKICAgICAgICAibWF4X2RlbGV0ZV9kZWxheSI6IDcuMAogICAgfSwKICAgICJicm93c2VyIjogewogICAgICAgICJfY29tbWVudCI6ICJCcm93c2VyIGNvbmZpZ3VyYXRpb24gYW5kIGJlaGF2aW9yIiwKICAgICAgICAiaGVhZGxlc3MiOiBmYWxzZSwKICAgICAgICAidXNlcl9hZ2VudCI6ICJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTIwLjAuMC4wIFNhZmFyaS81MzcuMzYiLAogICAgICAgICJ3aW5kb3dfc2l6ZSI6IHsKICAgICAgICAgICAgIndpZHRoIjogMTM2NiwKICAgICAgICAgICAgImhlaWdodCI6IDc2OAogICAgICAgIH0KICAgIH0sCiAgICAiZXhlY3V0aW9uIjogewogICAgICAgICJfY29tbWVudCI6ICJFeGVjdXRpb24gbW9kZSBjb250cm9scyIsCiAgICAgICAgIndoYXRpZiI6IHRydWUsCiAgICAgICAgInZlcmJvc2UiOiBmYWxzZQogICAgfQp9"
    
    $configBytes = [System.Convert]::FromBase64String($configBase64)
    $configFilePath = Join-Path -Path (Get-Location) -ChildPath "config_template.json"
    [System.IO.File]::WriteAllBytes($configFilePath, $configBytes)
    
    Print-Success "Configuration template created: config_template.json"
}

# Create example configuration
function New-ExampleConfiguration {
    Print-Step "Creating example configurations..."
    
    # Ensure examples directory exists
    if (-not (Test-Path "examples")) {
        New-Item -ItemType Directory -Path "examples" -Force | Out-Null
    }
    
    # Base64 encoded JSON to completely avoid PowerShell parsing issues
    $basicConfigBase64 = "ewogICAgImRlc2NyaXB0aW9uIjogIkJhc2ljIGNvbmZpZ3VyYXRpb24gZm9yIGZpcnN0LXRpbWUgdXNlcnMiLAogICAgInVzZV9jYXNlIjogIlNhZmUgdGVzdGluZyBhbmQgc21hbGwtc2NhbGUgY2xlYW51cCIsCiAgICAicmVjb21tZW5kZWRfZm9yIjogIk5ldyB1c2VycywgdGVzdGluZywgc21hbGwgY2xlYW51cHMiLAogICAgImNyZWRlbnRpYWxzIjogewogICAgICAgICJlbWFpbCI6ICIiLAogICAgICAgICJwYXNzd29yZCI6ICIiCiAgICB9LAogICAgImNsZWFuaW5nIjogewogICAgICAgICJwb3N0c19wZXJfc2Vzc2lvbiI6IDUsCiAgICAgICAgIm1heF9zZXNzaW9ucyI6IDIKICAgIH0sCiAgICAidGltaW5nIjogewogICAgICAgICJzZXNzaW9uX2RlbGF5IjogNjAwLAogICAgICAgICJwYWdlX3RpbWVvdXQiOiAzMCwKICAgICAgICAibWluX2FjdGlvbl9kZWxheSI6IDIuMCwKICAgICAgICAibWF4X2FjdGlvbl9kZWxheSI6IDQuMCwKICAgICAgICAibWluX2RlbGV0ZV9kZWxheSI6IDQuMCwKICAgICAgICAibWF4X2RlbGV0ZV9kZWxheSI6IDguMAogICAgfSwKICAgICJicm93c2VyIjogewogICAgICAgICJoZWFkbGVzcyI6IGZhbHNlLAogICAgICAgICJ1c2VyX2FnZW50IjogIk1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMjAuMC4wLjAgU2FmYXJpLzUzNy4zNiIsCiAgICAgICAgIndpbmRvd19zaXplIjogewogICAgICAgICAgICAid2lkdGgiOiAxMzY2LAogICAgICAgICAgICAiaGVpZ2h0IjogNzY4CiAgICAgICAgfQogICAgfSwKICAgICJleGVjdXRpb24iOiB7CiAgICAgICAgIndoYXRpZiI6IHRydWUsCiAgICAgICAgInZlcmJvc2UiOiB0cnVlCiAgICB9Cn0="
    
    $basicConfigBytes = [System.Convert]::FromBase64String($basicConfigBase64)
    $exampleFilePath = Join-Path -Path (Get-Location) -ChildPath "examples\basic_config.json"
    [System.IO.File]::WriteAllBytes($exampleFilePath, $basicConfigBytes)
    
    Print-Success "Basic configuration created: examples\basic_config.json"
}

# Check Chrome installation
function Test-ChromeInstallation {
    if ($SkipChromeCheck) {
        Print-Warning "Chrome check skipped (SkipChromeCheck specified)"
        return
    }
    
    Print-Step "Checking Chrome browser..."
    
    $chromePaths = @()
    $chromePaths += "$env:ProgramFiles\Google\Chrome\Application\chrome.exe"
    $chromePaths += "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
    
    # Check 32-bit program files path
    $programFiles32 = ${env:ProgramFiles(x86)}
    if ($programFiles32) {
        $chromePaths += "$programFiles32\Google\Chrome\Application\chrome.exe"
    }
    
    $chromeFound = $false
    
    foreach ($path in $chromePaths) {
        if (Test-Path $path) {
            try {
                $version = & $path --version 2>$null
                Print-Success "Chrome found: $version"
                $chromeFound = $true
                break
            }
            catch {
                continue
            }
        }
    }
    
    if (-not $chromeFound) {
        Print-Warning "Chrome not found in common locations"
        Print-Warning "Please install Chrome from: https://www.google.com/chrome/"
    }
}

# Test installation
function Test-Installation {
    Print-Step "Testing installation..."
    
    $venvPython = "venv\Scripts\python.exe"
    
    # Test Selenium import
    try {
        $seleniumTest = & $venvPython -c "import selenium; print('OK')" 2>&1
        if ($seleniumTest -eq "OK") {
            Print-Success "Selenium import test passed"
        }
        else {
            Print-Error "Selenium import test failed"
            return $false
        }
    }
    catch {
        Print-Error "Selenium import test failed: $_"
        return $false
    }
    
    # Test script execution
    try {
        $scriptTest = & $venvPython facebook_timeline_cleanup.py --help 2>&1
        if ($LASTEXITCODE -eq 0) {
            Print-Success "Script execution test passed"
        }
        else {
            Print-Error "Script execution test failed"
            return $false
        }
    }
    catch {
        Print-Error "Script execution test failed: $_"
        return $false
    }
    
    Print-Success "Installation test completed successfully"
    return $true
}

# Create activation script
function New-ActivationScript {
    Print-Step "Creating activation script..."
    
    # Base64 encoded batch file to avoid parsing issues
    $activateBatchBase64 = "QGVjaG8gb2ZmCnRpdGxlIEZhY2Vib29rIFRpbWVsaW5lIENsZWFudXAKZWNobyBBY3RpdmF0aW5nIEZhY2Vib29rIFRpbWVsaW5lIENsZWFudXAgZW52aXJvbm1lbnQuLi4KZWNoby4KCmlmIG5vdCBleGlzdCAidmVudiIgKAogICAgZWNobyBFcnJvcjogVmlydHVhbCBlbnZpcm9ubWVudCBub3QgZm91bmQuIFJ1biBpbnN0YWxsLnBzMSBmaXJzdC4KICAgIHBhdXNlCiAgICBleGl0IC9iIDEKKQoKY2FsbCB2ZW52XFNjcmlwdHNcYWN0aXZhdGUuYmF0CgplY2hvIEVudmlyb25tZW50IGFjdGl2YXRlZCEKZWNoby4KZWNobyBVc2FnZSBleGFtcGxlczoKZWNobyAgIHB5dGhvbiBmYWNlYm9va190aW1lbGluZV9jbGVhbnVwLnB5IC0td2hhdGlmIC0tdmVyYm9zZSAtLWVtYWlsIHlvdXJAZW1haWwuY29tCmVjaG8gICBweXRob24gZmFjZWJvb2tfdGltZWxpbmVfY2xlYW51cC5weSAtLXNhdmUtY29uZmlnIG15X2NvbmZpZy5qc29uCmVjaG8gICBweXRob24gZmFjZWJvb2tfdGltZWxpbmVfY2xlYW51cC5weSAtLWNvbmZpZyBleGFtcGxlc1xiYXNpY19jb25maWcuanNvbgplY2hvLgplY2hvIFRvIGRlYWN0aXZhdGU6IGRlYWN0aXZhdGUKZWNoby4KCmNtZCAvaw=="
    
    $activateBytes = [System.Convert]::FromBase64String($activateBatchBase64)
    $activateFilePath = Join-Path -Path (Get-Location) -ChildPath "activate.bat"
    [System.IO.File]::WriteAllBytes($activateFilePath, $activateBytes)
    
    Print-Success "Activation script created: activate.bat"
}

# Main installation function
function Install-FacebookTimelineCleanup {
    Print-Header
    
    # Pre-checks
    if (-not (Test-PythonVersion)) { return $false }
    if (-not (Test-ProjectDirectory)) { return $false }
    
    # Installation steps
    if (-not (New-VirtualEnvironment)) { return $false }
    if (-not (Install-Dependencies)) { return $false }
    
    New-ProjectDirectories
    New-ConfigurationTemplate
    New-ExampleConfiguration
    Test-ChromeInstallation
    New-ActivationScript
    
    # Test installation
    if (-not (Test-Installation)) { return $false }
    
    # Final instructions
    Write-Host ""
    Write-Host "================================================"
    Write-Host "           Installation Complete!              "
    Write-Host "================================================"
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Green
    Write-Host "1. Activate the environment:"
    Write-Host "   activate.bat" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "2. Test the installation:"
    Write-Host "   python facebook_timeline_cleanup.py --whatif --verbose" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "3. Create your configuration:"
    Write-Host "   Copy-Item config_template.json my_config.json" -ForegroundColor Yellow
    Write-Host "   # Edit my_config.json with your details" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "4. Read the safety documentation if available"
    Write-Host ""
    Write-Host "IMPORTANT: Always use --whatif mode for testing first!" -ForegroundColor Red
    Write-Host ""
    
    return $true
}

# Run main installation
try {
    $success = Install-FacebookTimelineCleanup
    if (-not $success) {
        Write-Host "Installation failed. Please check the errors above." -ForegroundColor Red
        exit 1
    }
}
catch {
    $errorMsg = $_.Exception.Message
    Write-Host "[ERROR] Unexpected error during installation: $errorMsg" -ForegroundColor Red
    exit 1
}