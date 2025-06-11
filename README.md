# Facebook Timeline Cleanup

A powerful Python tool for gradually and safely deleting posts from your Facebook timeline. Designed with safety, configurability, and human-like behavior in mind.

## Features

- **Safe Testing Mode**: `--whatif` option simulates all operations without actual deletions
- **Gradual Processing**: Configurable sessions with delays to avoid rate limiting
- **Comprehensive Logging**: Detailed logs of all operations with multiple verbosity levels
- **Flexible Configuration**: CLI arguments or JSON configuration files
- **Human-like Behavior**: Randomized delays and realistic browsing patterns
- **Robust Error Handling**: Automatic retries and graceful failure recovery
- **Security Focused**: Credential validation and confirmation prompts

## Quick Start

### Prerequisites

- Python 3.7 or higher
- Chrome browser installed
- ChromeDriver in PATH or same directory

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/facebook-timeline-cleanup.git
cd facebook-timeline-cleanup
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download ChromeDriver from [https://chromedriver.chromium.org/](https://chromedriver.chromium.org/) and ensure it's in your PATH.

### Basic Usage

**Always test first with whatif mode:**
```bash
python facebook_timeline_cleanup.py --whatif --verbose --email your@email.com
```

**Generate configuration template:**
```bash
python facebook_timeline_cleanup.py --save-config config.json
```

**Run with custom parameters:**
```bash
python facebook_timeline_cleanup.py --email your@email.com --sessions 3 --posts-per-session 5
```

## Configuration

The tool supports both command-line arguments and JSON configuration files. See [Configuration Guide](docs/configuration.md) for detailed options.

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

- [Installation Guide](docs/INSTALLATION.md)
- [Usage Guide](docs/USAGE.md)
- [Configuration Reference](docs/CONFIGURATION.md)
- [Safety Guidelines](docs/SAFETY.md)

## Examples

See the [examples](examples/) directory for sample configurations and use cases.

## Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests for any improvements.

## Limitations

- Requires manual login (2FA not automated)
- Only works with Chrome browser
- Facebook's interface changes may require updates
- Rate limiting may affect deletion speed

## Troubleshooting

### Common Issues

**ChromeDriver not found:**
- Download ChromeDriver and add to PATH
- Ensure Chrome browser is installed

**Login fails:**
- Check credentials
- Disable 2FA temporarily or use app password
- Clear browser data

**No posts found:**
- Verify you're on the correct account
- Check if posts exist in activity log
- Try refreshing the page

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is provided as-is without any warranties. Users are responsible for complying with Facebook's Terms of Service and applicable laws. The authors are not responsible for any account restrictions, data loss, or other consequences of using this tool.

## Support

For issues, questions, or contributions, please use the GitHub issue tracker.

---

**Remember: Always use `--whatif` mode first to test before performing actual deletions.**
