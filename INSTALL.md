# Installation Guide

Multiple installation methods are available for Facebook Timeline Cleanup. Choose the one that best fits your system and preferences.

## Quick Installation

### Linux/macOS (Recommended)

**Option 1: Shell Script (Easiest)**
```bash
chmod +x install.sh
./install.sh
```

**Option 2: Makefile (Developer-friendly)**
```bash
make install
make run-test
```

### Windows

**Option 1: PowerShell (Recommended)**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\install.ps1
```

**Option 2: Batch Script**
```cmd
install.bat
```

## Detailed Installation Options

### 1. Shell Script Installation (Linux/macOS)

**Features:**
- Automatic Python version checking
- Virtual environment creation
- Dependency installation
- Configuration template generation
- Chrome browser detection
- Complete testing

**Usage:**
```bash
# Make executable
chmod +x install.sh

# Run installation
./install.sh

# Activate environment
source activate.sh
```

**Script performs:**
- ✅ Python 3.7+ version check
- ✅ Virtual environment creation in `venv/`
- ✅ Dependencies installation from `requirements.txt`
- ✅ Directory structure creation (`docs/`, `examples/`, `logs/`)
- ✅ Configuration templates generation
- ✅ Chrome browser detection
- ✅ Installation testing
- ✅ Activation script creation

### 2. Makefile Installation (Linux/macOS)

**Features:**
- Granular control over installation steps
- Development-friendly commands
- Easy maintenance and updates

**Usage:**
```bash
# See all available commands
make help

# Full installation
make install

# Individual steps
make check-python
make create-venv
make install-deps
make test-install

# Activate environment
make activate

# Test installation
make run-test

# Create configuration
make config
```

**Available Commands:**
- `make install` - Complete installation
- `make clean` - Remove virtual environment and temporary files
- `make test-install` - Test the installation
- `make run-test` - Run test with whatif mode
- `make config` - Create personal configuration file
- `make check-deps` - Check dependency status
- `make quick-start` - Install and test in one command

### 3. PowerShell Installation (Windows)

**Features:**
- Modern PowerShell with error handling
- Colored output and progress indicators
- Comprehensive testing
- Force options for automation

**Usage:**
```powershell
# Allow script execution (if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Basic installation
.\install.ps1

# Force recreation of virtual environment
.\install.ps1 -Force

# Skip Chrome check
.\install.ps1 -SkipChromeCheck

# Activate environment
.\activate.bat
```

**Features:**
- ✅ Multiple Python command detection (`python`, `python3`, `py`)
- ✅ Version validation with detailed output
- ✅ Force mode for CI/CD scenarios
- ✅ Optional Chrome detection skip
- ✅ UTF-8 configuration file generation
- ✅ Comprehensive error handling

### 4. Batch Script Installation (Windows)

**Features:**
- Compatible with older Windows systems
- No PowerShell required
- Simple and reliable

**Usage:**
```cmd
# Run installation
install.bat

# Activate environment
activate.bat
```

## Post-Installation Steps

### 1. Activate Environment

**Linux/macOS:**
```bash
source activate.sh
# or
source venv/bin/activate
```

**Windows:**
```cmd
activate.bat
# or
venv\Scripts\activate.bat
```

### 2. Test Installation

```bash
# Test basic functionality
python facebook_timeline_cleanup.py --whatif --verbose

# Test with example configuration
python facebook_timeline_cleanup.py --config examples/basic_config.json --whatif
```

### 3. Create Configuration

```bash
# Copy template
cp config_template.json my_config.json

# Edit with your details
nano my_config.json  # or your preferred editor
```

### 4. Run First Test

```bash
# ALWAYS test with whatif mode first
python facebook_timeline_cleanup.py --config my_config.json --whatif --verbose
```

## Manual Installation

If automated scripts don't work for your system:

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate.bat  # Windows
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install selenium>=4.15.0
```

### 3. Install ChromeDriver
- Download from [chromedriver.chromium.org](https://chromedriver.chromium.org/)
- Match your Chrome browser version
- Add to PATH or place in project directory

### 4. Test Installation
```bash
python facebook_timeline_cleanup.py --help
```

## Troubleshooting Installation

### Common Issues

**Python version errors:**
```bash
# Check Python version
python --version
python3 --version

# Use specific Python version
python3.9 -m venv venv
```

**Permission errors (Linux/macOS):**
```bash
# Make scripts executable
chmod +x install.sh
chmod +x activate.sh

# Or run with bash directly
bash install.sh
```

**PowerShell execution policy (Windows):**
```powershell
# Check current policy
Get-ExecutionPolicy

# Allow script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Restore after installation
Set-ExecutionPolicy -ExecutionPolicy Restricted -Scope CurrentUser
```

**ChromeDriver issues:**
```bash
# Check Chrome version
google-chrome --version  # Linux
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version  # macOS

# Download matching ChromeDriver version
# Add to PATH or project directory
```

**Virtual environment issues:**
```bash
# Remove and recreate
rm -rf venv
python3 -m venv venv

# Or use system Python
pip install --user selenium
```

### System-Specific Notes

**Ubuntu/Debian:**
```bash
# Install Python and pip if missing
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Install Chrome
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt update
sudo apt install google-chrome-stable
```

**macOS:**
```bash
# Install Python via Homebrew
brew install python

# Install Chrome
brew install --cask google-chrome
```

**Windows:**
- Install Python from [python.org](https://www.python.org/downloads/)
- Install Chrome from [google.com/chrome](https://www.google.com/chrome/)
- Ensure "Add Python to PATH" is checked during installation

## Verification

After installation, verify everything works:

```bash
# Check Python in virtual environment
which python  # Should show venv/bin/python or venv\Scripts\python.exe

# Check Selenium
python -c "import selenium; print('Selenium version:', selenium.__version__)"

# Check script
python facebook_timeline_cleanup.py --help

# Test with whatif
python facebook_timeline_cleanup.py --whatif --sessions 1 --posts-per-session 1
```

## Next Steps

1. **Read Safety Documentation**: Review `docs/safety.md` thoroughly
2. **Configure Tool**: Edit your configuration file with credentials
3. **Start Small**: Begin with whatif mode and small batch sizes
4. **Backup Data**: Download your Facebook data before deletion
5. **Monitor Carefully**: Watch the first few real runs closely

## Getting Help

If installation fails:
1. Check the error messages carefully
2. Verify system requirements
3. Try manual installation steps
4. Check GitHub issues for similar problems
5. Create a new issue with:
   - Operating system and version
   - Python version
   - Complete error messages
   - Installation method attempted

For support, include:
- Output from failed installation script
- System information (`python --version`, OS version)
- Any error messages or logs