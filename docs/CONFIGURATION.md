# Configuration Reference

Complete reference for all configuration options in Facebook Timeline Cleanup.

## Configuration Methods

### 1. Command Line Arguments
```bash
python facebook_timeline_cleanup.py --email user@email.com --sessions 5 --verbose
```

### 2. JSON Configuration File
```bash
python facebook_timeline_cleanup.py --config config.json
```

### 3. Environment Variables
```bash
export FB_EMAIL="your@email.com"
export FB_PASSWORD="your_password"
python facebook_timeline_cleanup.py
```

### 4. Mixed Configuration
Command line arguments override config file settings:
```bash
python facebook_timeline_cleanup.py --config config.json --sessions 10 --verbose
```

## Complete Configuration Schema

### Full Configuration File Example

```json
{
    "credentials": {
        "email": "your@email.com",
        "password": "your_password"
    },
    "cleaning": {
        "posts_per_session": 10,
        "max_sessions": 5,
        "target_post_types": ["status", "photo", "video", "link", "all"]
    },
    "timing": {
        "session_delay": 300,
        "page_timeout": 30,
        "min_action_delay": 1.0,
        "max_action_delay": 3.0,
        "min_delete_delay": 3.0,
        "max_delete_delay": 7.0
    },
    "browser": {
        "headless": false,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "window_size": {
            "width": 1366,
            "height": 768
        }
    },
    "execution": {
        "whatif": false,
        "verbose": false
    }
}
```

## Configuration Sections

### Credentials Section

**Purpose:** Authentication settings for Facebook login.

```json
{
    "credentials": {
        "email": "your@email.com",
        "password": "your_password"
    }
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `email` | string | Yes | Facebook account email address |
| `password` | string | No* | Facebook account password |

*Required for actual deletions, optional for whatif mode.

**Security Notes:**
- Use environment variables instead of storing passwords in files
- Consider app-specific passwords for accounts with 2FA
- Never commit configuration files with passwords to version control

**Environment Variable Alternatives:**
```bash
export FB_EMAIL="your@email.com"
export FB_PASSWORD="your_password"
```

### Cleaning Section

**Purpose:** Controls what and how much content is processed.

```json
{
    "cleaning": {
        "posts_per_session": 10,
        "max_sessions": 5,
        "target_post_types": ["status", "photo", "video", "link", "all"]
    }
}
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `posts_per_session` | integer | 10 | Number of posts to process per session |
| `max_sessions` | integer | 5 | Maximum number of sessions to run |
| `target_post_types` | array | ["all"] | Types of posts to target (future feature) |

**Guidelines:**
- Start with low values (5-10 posts per session)
- Increase gradually based on success rate
- Consider Facebook's rate limiting
- Total posts processed = `posts_per_session` × `max_sessions`

**Recommended Values:**
- **Conservative:** 5 posts/session, 3 sessions
- **Moderate:** 10 posts/session, 5 sessions  
- **Aggressive:** 20 posts/session, 10 sessions

### Timing Section

**Purpose:** Controls delays and timeouts to avoid detection and rate limiting.

```json
{
    "timing": {
        "session_delay": 300,
        "page_timeout": 30,
        "min_action_delay": 1.0,
        "max_action_delay": 3.0,
        "min_delete_delay": 3.0,
        "max_delete_delay": 7.0
    }
}
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `session_delay` | integer | 300 | Seconds to wait between sessions |
| `page_timeout` | integer | 30 | Maximum seconds to wait for page loads |
| `min_action_delay` | float | 1.0 | Minimum seconds between browser actions |
| `max_action_delay` | float | 3.0 | Maximum seconds between browser actions |
| `min_delete_delay` | float | 3.0 | Minimum seconds between post deletions |
| `max_delete_delay` | float | 7.0 | Maximum seconds between post deletions |

**Timing Strategy:**
- **Human-like delays:** Random delays between min/max values simulate human behavior
- **Rate limiting avoidance:** Longer delays reduce chance of triggering Facebook's limits
- **Session gaps:** Allow Facebook's systems to "cool down" between batches

**Timing Profiles:**

**Conservative (recommended):**
```json
{
    "session_delay": 600,
    "min_action_delay": 2.0,
    "max_action_delay": 5.0,
    "min_delete_delay": 5.0,
    "max_delete_delay": 10.0
}
```

**Fast (higher risk):**
```json
{
    "session_delay": 120,
    "min_action_delay": 0.5,
    "max_action_delay": 1.5,
    "min_delete_delay": 1.0,
    "max_delete_delay": 3.0
}
```

### Browser Section

**Purpose:** Controls browser behavior and appearance.

```json
{
    "browser": {
        "headless": false,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "window_size": {
            "width": 1366,
            "height": 768
        }
    }
}
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `headless` | boolean | false | Run browser without visible window |
| `user_agent` | string | Chrome default | Custom browser user agent string |
| `window_size.width` | integer | 1366 | Browser window width in pixels |
| `window_size.height` | integer | 768 | Browser window height in pixels |

**Browser Considerations:**
- **Headless mode:** Faster but harder to debug issues
- **Window size:** Some elements may not be visible in small windows
- **User agent:** Default should work fine, custom ones for specific needs

### Execution Section

**Purpose:** Controls program execution behavior.

```json
{
    "execution": {
        "whatif": false,
        "verbose": false
    }
}
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `whatif` | boolean | false | Simulation mode - no actual deletions |
| `verbose` | boolean | false | Detailed logging output |

**Execution Modes:**
- **whatif=true:** Safe testing mode, no deletions performed
- **verbose=true:** Detailed logs for troubleshooting

## Command Line Arguments Reference

### Credential Arguments
```bash
--email EMAIL              Facebook login email
--password PASSWORD         Facebook login password
```

### Configuration Arguments
```bash
--config FILE               Load settings from JSON file
--save-config FILE          Save configuration template
```

### Cleaning Arguments
```bash
--sessions N                Maximum number of sessions (default: 5)
--posts-per-session N       Posts per session (default: 10)
--session-delay N           Seconds between sessions (default: 300)
```

### Timing Arguments
```bash
--page-timeout N            Page load timeout seconds (default: 30)
--min-delay FLOAT           Minimum action delay seconds (default: 1.0)
--max-delay FLOAT           Maximum action delay seconds (default: 3.0)
```

### Browser Arguments
```bash
--headless                  Run browser in headless mode
--user-agent STRING         Custom browser user agent
```

### Execution Arguments
```bash
--whatif, --dry-run         Simulation mode (no deletions)
--verbose, -v               Detailed output
```

## Preset Configurations

### Conservative Setup
Safe for first-time users:
```json
{
    "cleaning": {
        "posts_per_session": 5,
        "max_sessions": 2
    },
    "timing": {
        "session_delay": 600,
        "min_delete_delay": 5.0,
        "max_delete_delay": 10.0
    },
    "execution": {
        "whatif": true,
        "verbose": true
    }
}
```

### Standard Setup
Balanced approach:
```json
{
    "cleaning": {
        "posts_per_session": 10,
        "max_sessions": 5
    },
    "timing": {
        "session_delay": 300,
        "min_delete_delay": 3.0,
        "max_delete_delay": 7.0
    },
    "execution": {
        "whatif": false,
        "verbose": false
    }
}
```

### Power User Setup
Maximum throughput:
```json
{
    "cleaning": {
        "posts_per_session": 20,
        "max_sessions": 10
    },
    "timing": {
        "session_delay": 180,
        "min_delete_delay": 2.0,
        "max_delete_delay": 4.0
    },
    "browser": {
        "headless": true
    }
}
```

## Environment Variables

All configuration can be overridden with environment variables:

```bash
# Credentials
FB_EMAIL="your@email.com"
FB_PASSWORD="your_password"

# Cleaning
FB_POSTS_PER_SESSION=10
FB_MAX_SESSIONS=5

# Timing
FB_SESSION_DELAY=300
FB_PAGE_TIMEOUT=30

# Execution
FB_WHATIF=true
FB_VERBOSE=true
FB_HEADLESS=false
```

## Configuration Validation

The tool validates configuration on startup:

**Required Fields:**
- `credentials.email` (always required)
- `credentials.password` (required unless whatif=true)

**Range Validations:**
- Sessions and posts must be positive integers
- Delays cannot be negative
- Min delays cannot exceed max delays

**Example Validation Errors:**
```
ERROR: Email missing. Use --email or specify in configuration file.
ERROR: Number of sessions must be greater than 0.
ERROR: Minimum delay cannot be greater than maximum delay.
```

## Advanced Configuration

### Custom User Agents
```json
{
    "browser": {
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
}
```

### Multiple Configuration Files
```bash
# Base configuration
python facebook_timeline_cleanup.py --config base_config.json --sessions 10

# Override specific settings
python facebook_timeline_cleanup.py --config conservative_config.json --verbose
```

### Configuration Templates

**Generate specific templates:**
```bash
# Conservative template
python facebook_timeline_cleanup.py --save-config conservative.json --sessions 3 --posts-per-session 5

# Fast template  
python facebook_timeline_cleanup.py --save-config fast.json --sessions 10 --session-delay 120
```

## Best Practices

1. **Start Conservative:** Use small values and whatif mode initially
2. **Version Control:** Keep configuration files in version control (without passwords)
3. **Environment Specific:** Use different configs for different scenarios
4. **Security:** Never commit passwords, use environment variables
5. **Testing:** Always test configuration changes with whatif mode
6. **Documentation:** Comment your configuration choices
7. **Backup:** Keep working configurations backed up

## Troubleshooting Configuration

### Common Issues

**Missing credentials:**
```bash
# Check what's loaded
python facebook_timeline_cleanup.py --config config.json --whatif --verbose
```

**Invalid JSON:**
```bash
# Validate JSON syntax
python -m json.tool config.json
```

**Performance issues:**
```bash
# Test with different timing
python facebook_timeline_cleanup.py --config config.json --min-delay 0.5 --whatif
```

### Debug Configuration Loading
```bash
# See what configuration is actually used
python facebook_timeline_cleanup.py --config config.json --whatif --verbose
```

The startup logs will show the final merged configuration.