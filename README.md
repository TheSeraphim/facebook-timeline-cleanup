# Facebook Timeline Cleanup

A powerful Python tool for gradually and safely deleting posts from your Facebook timeline. Designed with safety, configurability, and human-like behavior in mind.

## Features

- **Automated Installation**: Cross-platform scripts for easy setup (Linux/macOS/Windows)
- **Safe Testing Mode**: `--whatif` option simulates all operations without actual deletions
- **Gradual Processing**: Configurable sessions with delays to avoid rate limiting
- **Comprehensive Logging**: Detailed logs of all operations with multiple verbosity levels
- **Flexible Configuration**: CLI arguments or JSON configuration files
- **Human-like Behavior**: Randomized delays and realistic browsing patterns
- **Robust Error Handling**: Automatic retries and graceful failure recovery
- **Security Focused**: Credential validation and confirmation prompts
- **Virtual Environment**: Isolated dependencies for clean installation

## Quick Start

### Automated Installation

**Linux/macOS (Shell Script):**
```bash
git clone https://github.com/yourusername/facebook-timeline-cleanup.git
cd facebook-timeline-cleanup
chmod +x install.sh
./install.sh
source activate.sh
```

**Linux/macOS (Makefile):**
```bash
git clone https://github.com/yourusername/facebook-timeline-cleanup.git
cd facebook-timeline-cleanup
make quick-start
```

**Windows (PowerShell):**
```powershell
git clone https://github.com/yourusername/facebook-timeline-cleanup.git
cd facebook-timeline-cleanup
.\install.ps1
.\activate.bat
```

**Windows (Batch):**
```cmd
git clone https://github.com/yourusername/facebook-timeline-cleanup.git
cd facebook-timeline-cleanup
install.bat
activate.bat
```

### First Run (Essential Safety Step)

**ALWAYS test with whatif mode first:**
```bash
python facebook_timeline_cleanup.py --whatif --verbose --email your@email.com
```

### Installation

**Quick Install (Recommended):**

**Linux/macOS:**
```bash
git clone https://github.com/yourusername/facebook-timeline-cleanup.git
cd facebook-timeline-cleanup
chmod +x install.sh
./install.sh
```

**Windows (PowerShell):**
```powershell
git clone https://github.com/yourusername/facebook-timeline-cleanup.git
cd facebook-timeline-cleanup
.\install.ps1
```

**Windows (Command Prompt):**
```cmd
git clone https://github.com/yourusername/facebook-timeline-cleanup.git
cd facebook-timeline-cleanup
install.bat
```

### Manual Setup (Alternative)

**If automated scripts don't work:**

1. **Prerequisites:**
   - Python 3.7 or higher
   - Chrome browser installed
   - ChromeDriver in PATH or same directory

2. **Manual Installation:**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or venv\Scripts\activate.bat on Windows
pip install -r requirements.txt
```

3. **Download ChromeDriver:**
   - Get it from [chromedriver.chromium.org](https://chromedriver.chromium.org/)
   - Ensure it matches your Chrome version
   - Add to PATH or project directory

### Configuration and Usage

**Generate configuration template:**
```bash
python facebook_timeline_cleanup.py --save-config config.json
```

**Run with custom parameters:**
```bash
python facebook_timeline_cleanup.py --email your@email.com --sessions 3 --posts-per-session 5
```

## Configuration

The tool supports both command-line arguments and JSON configuration files. See [docs/CONFIGURATION.md](docs/CONFIGURATION.md) for detailed options.

### Basic Configuration Example

```json
{
    "credentials": {
        "email": "your@email.com",
        "password": "your_password"
    },
    "cleaning": {
        "posts_per_session": 10,
        "max_sessions": 5
    },
    "timing": {
        "session_delay": 300
    },
    "execution": {
        "whatif": true,
        "verbose": true
    }
}
```

## Command Line Options

### Credentials
- `--email EMAIL`: Facebook login email
- `--password PASSWORD`: Facebook login password

### Cleaning Parameters
- `--sessions N`: Maximum number of sessions (default: 5)
- `--posts-per-session N`: Posts to delete per session (default: 10)
- `--session-delay N`: Pause between sessions in seconds (default: 300)

### Execution Modes
- `--whatif`, `--dry-run`: Simulation mode - no actual deletions
- `--verbose`, `-v`: Detailed output of all operations
- `--headless`: Run browser in headless mode

### Configuration
- `--config FILE`: Load configuration from JSON file
- `--save-config FILE`: Save configuration template

## Safety Features

### Whatif Mode
Always use `--whatif` for your first run to understand what the tool will do:
```bash
python facebook_timeline_cleanup.py --whatif --verbose --email your@email.com
```

### Confirmation Prompts
For real deletions, you must type 'DELETE' to confirm the operation.

### Comprehensive Logging
All operations are logged with timestamps and detailed information. Log files are automatically saved with format `facebook_timeline_cleanup_YYYYMMDD_HHMMSS.log`.

## Important Warnings

- **This tool permanently deletes your Facebook posts**
- **Deletions are NOT reversible**
- **Always backup your data first** using Facebook's "Download Your Information" feature
- **Start with small batches** to test the tool's behavior
- **Use at your own risk** - this tool may violate Facebook's Terms of Service

## Technical Details

- **Language**: Python 3.7+
- **Browser Automation**: Selenium WebDriver
- **Supported Browsers**: Chrome/Chromium
- **Rate Limiting**: Built-in delays and session management
- **Error Recovery**: Automatic retries and graceful degradation

## Documentation

- [Installation Guide](INSTALL.md)
- [Usage Guide](docs/USAGE.md)
- [Configuration Reference](docs/CONFIGURATION.md)
- [Safety Guidelines](docs/SAFETY.md)
- [Contributing Guidelines](CONTRIBUTING.md)

## Examples

See the [examples](examples/) directory for sample configurations and use cases.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute safely and effectively to this project.

## Limitations

- Requires manual login (2FA not automated)
- Only works with Chrome browser
- Facebook's interface changes may require updates
- Rate limiting may affect deletion speed

## Troubleshooting

### Common Issues

**Installation Problems:**
- Run the appropriate install script for your system
- Check [INSTALL.md](INSTALL.md) for detailed troubleshooting
- Ensure Python 3.7+ is installed
- Try manual installation if scripts fail

**ChromeDriver not found:**
- Installation scripts should handle this automatically
- Manual download: [chromedriver.chromium.org](https://chromedriver.chromium.org/)
- Ensure Chrome browser is installed

**Login fails:**
- Check credentials in configuration
- Disable 2FA temporarily or use app password
- Try whatif mode first to test login

**No posts found:**
- Verify you're on the correct account
- Check if posts exist in activity log
- Try different browser window size settings

**Environment Issues:**
- Rerun installation script
- Check virtual environment activation
- Verify all dependencies installed correctly

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is provided as-is without any warranties. Users are responsible for complying with Facebook's Terms of Service and applicable laws. The authors are not responsible for any account restrictions, data loss, or other consequences of using this tool.

## Support

For issues, questions, or contributions:
- Check [INSTALL.md](INSTALL.md) for installation problems  
- Review [docs/safety.md](docs/SAFETY.md) for safety guidelines
- Search existing GitHub issues
- Create a new issue with detailed information

## Installation Scripts

This project includes automated installation scripts:
- `install.sh` - Linux/macOS shell script
- `install.ps1` - Windows PowerShell script  
- `install.bat` - Windows batch script
- `Makefile` - Linux/macOS make commands

All scripts create isolated virtual environments and handle dependencies automatically.

---

**Remember: Always use `--whatif` mode first to test before performing actual deletions.**
