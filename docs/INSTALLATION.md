# Installation Guide

This guide covers the installation and setup of Facebook Timeline Cleanup.

## System Requirements

### Operating System
- Windows 10/11
- macOS 10.14 or later
- Linux (Ubuntu 18.04+ or equivalent)

### Software Requirements
- Python 3.7 or higher
- Google Chrome browser
- ChromeDriver (matching your Chrome version)

## Step-by-Step Installation

### 1. Install Python

#### Windows
Download Python from [python.org](https://www.python.org/downloads/) and run the installer. Make sure to check "Add Python to PATH" during installation.

#### macOS
```bash
# Using Homebrew
brew install python3

# Or download from python.org
```

#### Linux
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# CentOS/RHEL/Fedora
sudo yum install python3 python3-pip
```

### 2. Install Google Chrome

Download and install Chrome from [google.com/chrome](https://www.google.com/chrome/).

### 3. Install ChromeDriver

#### Automatic Installation (Recommended)
The required packages will handle ChromeDriver automatically.

#### Manual Installation
1. Check your Chrome version: `chrome://version/`
2. Download matching ChromeDriver from [chromedriver.chromium.org](https://chromedriver.chromium.org/)
3. Extract and place in PATH or project directory

### 4. Clone the Repository

```bash
git clone https://github.com/yourusername/facebook-timeline-cleanup.git
cd facebook-timeline-cleanup
```

### 5. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 6. Install Dependencies

```bash
pip install -r requirements.txt
```

## Verify Installation

Test your installation with the whatif mode:

```bash
python facebook_timeline_cleanup.py --whatif --verbose
```

You should see output indicating the tool is working correctly.

## Troubleshooting Installation Issues

### Python Issues

**Python not found:**
- Ensure Python is in your PATH
- Try `python3` instead of `python`
- Reinstall Python with PATH option enabled

**Permission denied:**
- Use virtual environment
- On Linux/macOS: `sudo pip install` (not recommended)

### ChromeDriver Issues

**ChromeDriver not found:**
```bash
# Check Chrome version
google-chrome --version
# or
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version

# Download matching ChromeDriver version
# Place in PATH or project directory
```

**Version mismatch:**
- Ensure ChromeDriver version matches your Chrome browser
- Update Chrome or download correct ChromeDriver version

### Selenium Issues

**WebDriver not found:**
```bash
# Reinstall selenium
pip uninstall selenium
pip install selenium
```

**Browser doesn't start:**
- Check if Chrome is properly installed
- Try running Chrome manually
- Disable headless mode for debugging

### Network Issues

**Package download fails:**
```bash
# Update pip
pip install --upgrade pip

# Use different index
pip install -r requirements.txt -i https://pypi.org/simple/
```

## Development Setup

For development or contributing:

```bash
# Clone repository
git clone https://github.com/yourusername/facebook-timeline-cleanup.git
cd facebook-timeline-cleanup

# Create development environment
python3 -m venv dev-env
source dev-env/bin/activate  # or dev-env\Scripts\activate on Windows

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # if available

# Install in development mode
pip install -e .
```

## Configuration After Installation

1. **Generate configuration template:**
```bash
python facebook_timeline_cleanup.py --save-config config.json
```

2. **Edit configuration file:**
```bash
# Edit config.json with your preferences
nano config.json  # or use your preferred editor
```

3. **Test with whatif mode:**
```bash
python facebook_timeline_cleanup.py --config config.json --whatif
```

## Security Considerations

### Credential Storage
- Never store passwords in plain text
- Use environment variables for credentials
- Consider app-specific passwords for Facebook

### Environment Variables
```bash
# Set environment variables (Linux/macOS)
export FB_EMAIL="your@email.com"
export FB_PASSWORD="your_password"

# Windows
set FB_EMAIL=your@email.com
set FB_PASSWORD=your_password
```

### App-Specific Passwords
If you use two-factor authentication:
1. Generate an app-specific password in Facebook settings
2. Use this password instead of your regular password

## Next Steps

After successful installation:
1. Read the [Usage Guide](usage.md)
2. Review [Safety Guidelines](safety.md)
3. Check [Configuration Reference](configuration.md)
4. Always start with `--whatif` mode

## Getting Help

If you encounter issues:
1. Check this troubleshooting guide
2. Search existing GitHub issues
3. Create a new issue with:
   - Your operating system
   - Python version
   - Chrome version
   - Error messages
   - Steps to reproduce