# Facebook Timeline Cleanup - Installation Script (PowerShell)
# Creates virtual environment, installs dependencies, and sets up repository

param(
    [switch]$Force,
    [switch]$SkipChromeCheck
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Colors for output
$Red = "`e[91m"
$Green = "`e[92m"
$Yellow = "`e[93m"
$Blue = "`e[94m"
$Bold = "`e[1m"
$Reset = "`e[0m"

# Print functions
function Print-Step {
    param([string]$Message)
    Write-Host "`n$Blue$Bold[STEP]$Reset $Message"
}

function Print-Success {
    param([string]$Message)
    Write-Host "$Green✓$Reset $Message"
}

function Print-Warning {
    param([string]$Message)
    Write-Host "$Yellow⚠$Reset $Message"
}

function Print-Error {
    param([string]$Message)
    Write-Host "$Red✗$Reset $Message"
}

function Print-Header {
    Write-Host "$Bold================================================$Reset"
    Write-Host "$Bold    Facebook Timeline Cleanup - Installer    $Reset"
    Write-Host "$Bold================================================$Reset"
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
            Print-Warning "Removing existing virtual environment (--Force specified)"
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
        # Upgrade pip
        & $venvPip install --upgrade pip | Out-Null
        
        # Install requirements
        & $venvPip install -r requirements.txt
        
        Print-Success "Dependencies installed successfully"
        return $true
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

# Create configuration template
function New-ConfigurationTemplate {
    Print-Step "Creating configuration template..."
    
    $configContent = @'
{
    "_comment": "Facebook Timeline Cleanup Configuration Template",
    "_instructions": [
        "1. Copy this file to 'config.json' or another name",
        "2. Fill in your email and password (or use environment variables)",
        "3. Adjust cleaning and timing parameters as needed",
        "4. ALWAYS test with 'whatif': true before real deletions",
        "5. Never commit configuration files with passwords to version control"
    ],
    
    "credentials": {
        "_comment": "Login credentials for Facebook account",
        "email": "your_email@example.com",
        "password": ""
    },
    
    "cleaning": {
        "_comment": "Parameters controlling what content is processed",
        "posts_per_session": 10,
        "max_sessions": 5,
        "target_post_types": ["status", "photo", "video", "link", "all"]
    },
    
    "timing": {
        "_comment": "Timing controls to avoid rate limiting and detection",
        "session_delay": 300,
        "page_timeout": 30,
        "min_action_delay": 1.0,
        "max_action_delay": 3.0,
        "min_delete_delay": 3.0,
        "max_delete_delay": 7.0
    },
    
    "browser": {
        "_comment": "Browser configuration and behavior",
        "headless": false,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "window_size": {
            "width": 1366,
            "height": 768
        }
    },
    
    "execution": {
        "_comment": "Execution mode controls",
        "whatif": true,
        "verbose": false
    }
}
'@
    
    $configContent | Out-File -FilePath "config_template.json" -Encoding UTF8
    Print-Success "Configuration template created: config_template.json"
}

# Create example configuration
function New-ExampleConfiguration {
    Print-Step "Creating example configurations..."
    
    $basicConfig = @'
{
    "description": "Basic configuration for first-time users",
    "use_case": "Safe testing and small-scale cleanup",
    "recommended_for": "New users, testing, small cleanups",
    
    "credentials": {
        "email": "",
        "password": ""
    },
    
    "cleaning": {
        "posts_per_session": 5,
        "max_sessions": 2
    },
    
    "timing": {
        "session_delay": 600,
        "page_timeout": 30,
        "min_action_delay": 2.0,
        "max_action_delay": 4.0,
        "min_delete_delay": 4.0,
        "max_delete_delay": 8.0
    },
    
    "browser": {
        "headless": false,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "window_size": {
            "width": 1366,
            "height": 768
        }
    },
    
    "execution": {
        "whatif": true,
        "verbose": true
    }
}
'@
    
    $basicConfig | Out-File -FilePath "examples\basic_config.json" -Encoding UTF8
    Print-Success "Basic configuration created: examples\basic_config.json"
}

# Check Chrome installation
function Test-ChromeInstallation {
    if ($SkipChromeCheck) {
        Print-Warning "Chrome check skipped (--SkipChromeCheck specified)"
        return
    }
    
    Print-Step "Checking Chrome browser..."
    
    $chromePaths = @(
        "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
        "$env:ProgramFiles(x86)\Google\Chrome\Application\chrome.exe",
        "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
    )
    
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
        & $venvPython -c "import selenium; print('Selenium imported successfully')" | Out-Null
        Print-Success "Selenium import test passed"
    }
    catch {
        Print-Error "Selenium import test failed"
        return $false
    }
    
    # Test script execution
    try {
        & $venvPython facebook_timeline_cleanup.py --help | Out-Null
        Print-Success "Script execution test passed"
    }
    catch {
        Print-Error "Script execution test failed"
        return $false
    }
    
    Print-Success "Installation test completed successfully"
    return $true
}

# Create activation script
function New-ActivationScript { 
    Print-Step "Creating activation script..."
    
    $activateContent = @'
@echo off
title Facebook Timeline Cleanup
echo Activating Facebook Timeline Cleanup environment...
echo.

if not exist "venv" (
    echo Error: Virtual environment not found. Run install.ps1 or install.bat first.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo Environment activated!
echo.
echo Usage examples:
echo   python facebook_timeline_cleanup.py --whatif --verbose --email your@email.com
echo   python facebook_timeline_cleanup.py --save-config my_config.json
echo   python facebook_timeline_cleanup.py --config examples\basic_config.json
echo.
echo To deactivate: deactivate
echo.

cmd /k
'@
    
    $activateContent | Out-File -FilePath "activate.bat" -Encoding ASCII
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
    Write-Host "$Bold================================================$Reset"
    Write-Host "$Bold           Installation Complete!              $Reset"
    Write-Host "$Bold================================================$Reset"
    Write-Host ""
    Write-Host "${Green}Next steps:$Reset"
    Write-Host "1. Activate the environment:"
    Write-Host "   ${Yellow}.\activate.bat$Reset"
    Write-Host ""
    Write-Host "2. Test the installation:"
    Write-Host "   ${Yellow}python facebook_timeline_cleanup.py --whatif --verbose$Reset"
    Write-Host ""
    Write-Host "3. Create your configuration:"
    Write-Host "   ${Yellow}Copy-Item config_template.json my_config.json$Reset"
    Write-Host "   ${Yellow}# Edit my_config.json with your details$Reset"
    Write-Host ""
    Write-Host "4. Read the safety documentation if available"
    Write-Host ""
    Write-Host "${Red}IMPORTANT:$Reset Always use --whatif mode for testing first!"
    Write-Host ""
    
    return $true
}

# Run main installation
try {
    $success = Install-FacebookTimelineCleanup
    if (-not $success) {
        Write-Host "${Red}Installation failed. Please check the errors above.$Reset"
        exit 1
    }
}
catch {
    Print-Error "Unexpected error during installation: $_"
    exit 1
}