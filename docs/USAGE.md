# Usage Guide

This guide covers how to use Facebook Timeline Cleanup effectively and safely.

## Before You Start

### Essential Safety Steps

1. **Download your Facebook data backup** using Facebook's "Download Your Information" feature
2. **Always test with `--whatif` mode first**
3. **Start with small batches** (5-10 posts per session)
4. **Review the Safety Guidelines** in [safety.md](safety.md)

### Understanding the Tool

Facebook Timeline Cleanup works by:
- Logging into your Facebook account
- Navigating to your Activity Log
- Finding posts on the current page
- Attempting to delete them one by one
- Moving through multiple sessions with delays

## Basic Usage Patterns

### 1. Testing Mode (Always Start Here)

```bash
# Test what the tool would do without actually deleting anything
python facebook_timeline_cleanup.py --whatif --verbose --email your@email.com
```

This will:
- Log into your account
- Find posts on your timeline
- Show you what would be deleted
- Generate a detailed log
- Exit without deleting anything

### 2. Generate Configuration Template

```bash
python facebook_timeline_cleanup.py --save-config my_config.json
```

Edit the generated file with your preferences:
```json
{
    "credentials": {
        "email": "your@email.com",
        "password": ""
    },
    "cleaning": {
        "posts_per_session": 5,
        "max_sessions": 3
    },
    "timing": {
        "session_delay": 600
    },
    "execution": {
        "whatif": true,
        "verbose": true
    }
}
```

### 3. Small Scale Test

```bash
# Delete only 5 posts across 2 sessions for testing
python facebook_timeline_cleanup.py --config my_config.json --sessions 2 --posts-per-session 5
```

### 4. Production Usage

```bash
# Larger scale cleanup
python facebook_timeline_cleanup.py --config my_config.json --sessions 10 --posts-per-session 10
```

## Command Line Reference

### Basic Commands

```bash
# Minimal command (will prompt for missing info)
python facebook_timeline_cleanup.py --email your@email.com

# With password (not recommended for security)
python facebook_timeline_cleanup.py --email your@email.com --password yourpassword

# Using config file (recommended)
python facebook_timeline_cleanup.py --config config.json
```

### Session Control

```bash
# Control number of sessions and posts
python facebook_timeline_cleanup.py --sessions 5 --posts-per-session 10

# Add delays between sessions (seconds)
python facebook_timeline_cleanup.py --session-delay 600  # 10 minutes

# Control browser timeouts
python facebook_timeline_cleanup.py --page-timeout 45
```

### Execution Modes

```bash
# Test mode - no actual deletions
python facebook_timeline_cleanup.py --whatif

# Verbose output - detailed logging
python facebook_timeline_cleanup.py --verbose

# Headless mode - no browser window
python facebook_timeline_cleanup.py --headless

# Combine modes
python facebook_timeline_cleanup.py --whatif --verbose --headless
```

### Timing Control

```bash
# Control delays between actions
python facebook_timeline_cleanup.py --min-delay 2.0 --max-delay 5.0

# These help avoid detection and rate limiting
```

## Configuration File Usage

### Creating Configuration

```bash
# Generate template
python facebook_timeline_cleanup.py --save-config config.json

# Copy and customize
cp config.json my_personal_config.json
```

### Configuration Sections

**Credentials:**
```json
{
    "credentials": {
        "email": "your@email.com",
        "password": "optional_if_using_whatif"
    }
}
```

**Cleaning Parameters:**
```json
{
    "cleaning": {
        "posts_per_session": 10,
        "max_sessions": 5,
        "target_post_types": ["status", "photo", "video", "link", "all"]
    }
}
```

**Timing Configuration:**
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

**Browser Settings:**
```json
{
    "browser": {
        "headless": false,
        "user_agent": "Custom user agent string",
        "window_size": {
            "width": 1366,
            "height": 768
        }
    }
}
```

## Understanding the Output

### Log Levels

**INFO Level:**
- Session progress
- Posts found and deleted
- Major milestones

**DEBUG Level (with --verbose):**
- Individual browser actions
- Element searches
- Timing information
- Detailed error messages

### Sample Output

```
2024-06-11 10:30:15 | INFO     | main                 | Facebook Timeline Cleanup v1.0
2024-06-11 10:30:15 | INFO     | __init__             | Facebook Timeline Cleanup initialized with configuration:
2024-06-11 10:30:15 | INFO     | __init__             | Whatif mode: True
2024-06-11 10:30:15 | INFO     | __init__             | Posts per session: 5
2024-06-11 10:30:16 | INFO     | login                | Starting Facebook login procedure
2024-06-11 10:30:18 | INFO     | login                | Login completed successfully
2024-06-11 10:30:19 | INFO     | find_posts_on_page   | Found 12 unique posts on page
2024-06-11 10:30:20 | INFO     | attempt_post_deletion| WHATIF: Would delete post 1 (not executed)
```

### Statistics Report

At the end of each run:
```
======================================================================
FACEBOOK TIMELINE CLEANUP - FINAL REPORT
======================================================================
WHATIF MODE - No actual deletions performed
----------------------------------------------------------------------
Total duration:          0:05:23
Sessions completed:       2
Posts found:             25
Posts deleted:           10
Posts skipped:           3
Errors encountered:      0
Average speed:           1.85 posts/minute
Success rate:            76.9%
======================================================================
```

## Common Workflows

### First Time User

1. **Setup and test:**
```bash
python facebook_timeline_cleanup.py --save-config config.json
# Edit config.json with your email
python facebook_timeline_cleanup.py --config config.json --whatif --verbose
```

2. **Small test run:**
```bash
# Remove whatif, add small limits
python facebook_timeline_cleanup.py --config config.json --sessions 1 --posts-per-session 3
```

3. **Gradual scaling:**
```bash
# Increase gradually
python facebook_timeline_cleanup.py --config config.json --sessions 3 --posts-per-session 5
python facebook_timeline_cleanup.py --config config.json --sessions 5 --posts-per-session 10
```

### Regular User

```bash
# Weekly cleanup
python facebook_timeline_cleanup.py --config config.json --sessions 5 --posts-per-session 15

# Deep cleanup
python facebook_timeline_cleanup.py --config config.json --sessions 20 --posts-per-session 10 --session-delay 900
```

### Power User

```bash
# Maximum cleanup (use with caution)
python facebook_timeline_cleanup.py --config config.json --sessions 50 --posts-per-session 20 --session-delay 300
```

## Monitoring and Interruption

### Monitoring Progress

- Watch the console output for real-time progress
- Check log files for detailed information
- Monitor browser window (if not headless) for visual feedback

### Safe Interruption

Press `Ctrl+C` to safely interrupt the process:
- Current operation will complete
- Partial statistics will be generated
- Browser will be closed properly

### Resuming Operations

The tool doesn't have built-in resume functionality, but you can:
- Run again with the same configuration
- The tool will continue from where Facebook shows posts
- Already deleted posts won't appear again

## Troubleshooting Common Issues

### Login Problems

```bash
# Test login only
python facebook_timeline_cleanup.py --whatif --sessions 0 --email your@email.com
```

### No Posts Found

```bash
# Increase verbosity to see what's happening
python facebook_timeline_cleanup.py --verbose --whatif
```

### Slow Performance

```bash
# Reduce delays
python facebook_timeline_cleanup.py --min-delay 0.5 --max-delay 1.5 --session-delay 60
```

### Rate Limiting

```bash
# Increase delays
python facebook_timeline_cleanup.py --min-delay 3.0 --max-delay 8.0 --session-delay 1200
```

## Best Practices

1. **Always start with whatif mode**
2. **Use configuration files for repeatability**
3. **Monitor the first few sessions closely**
4. **Keep session sizes reasonable (10-20 posts)**
5. **Use appropriate delays between sessions**
6. **Run during off-peak hours**
7. **Keep backups of your data**
8. **Stop if you encounter repeated errors**

## Next Steps

- Review [Configuration Reference](configuration.md) for advanced options
- Read [Safety Guidelines](safety.md) for important warnings
- Check [examples/](../examples/) for sample configurations