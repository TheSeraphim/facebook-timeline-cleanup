# Configuration Examples

This directory contains example configurations for different use cases and experience levels.

## Available Examples

### basic_config.json
**For: First-time users and testing**
- Conservative settings
- Small batch sizes (5 posts per session)
- Long delays between operations
- Verbose logging enabled
- Whatif mode enabled by default

**Usage:**
```bash
# Copy and customize
cp examples/basic_config.json my_config.json
# Edit my_config.json with your email
python facebook_timeline_cleanup.py --config my_config.json
```

### advanced_config.json
**For: Experienced users and bulk operations**
- Optimized for performance
- Larger batch sizes (15 posts per session)
- Shorter delays
- Headless mode enabled
- Higher risk but faster execution

**Usage:**
```bash
# Only use after extensive testing
cp examples/advanced_config.json my_advanced_config.json
# Edit configuration and test thoroughly first
python facebook_timeline_cleanup.py --config my_advanced_config.json --whatif
```

## Command Line Examples

### Testing and Validation

**Initial testing:**
```bash
# Test login and basic functionality
python facebook_timeline_cleanup.py --whatif --verbose --email your@email.com --sessions 1 --posts-per-session 3
```

**Configuration testing:**
```bash
# Test a configuration file
python facebook_timeline_cleanup.py --config examples/basic_config.json --whatif --verbose
```

**Generate your own template:**
```bash
# Create customized template
python facebook_timeline_cleanup.py --save-config my_template.json --sessions 3 --posts-per-session 5 --session-delay 900
```

### Progressive Usage

**Stage 1: Minimal test**
```bash
python facebook_timeline_cleanup.py --config my_config.json --sessions 1 --posts-per-session 2
```

**Stage 2: Small cleanup**
```bash
python facebook_timeline_cleanup.py --config my_config.json --sessions 3 --posts-per-session 5
```

**Stage 3: Regular cleanup**
```bash
python facebook_timeline_cleanup.py --config my_config.json --sessions 5 --posts-per-session 10
```

**Stage 4: Bulk cleanup (experienced users only)**
```bash
python facebook_timeline_cleanup.py --config my_config.json --sessions 10 --posts-per-session 15 --session-delay 300
```

### Specialized Scenarios

**Conservative approach (high safety):**
```bash
python facebook_timeline_cleanup.py \
    --email your@email.com \
    --sessions 2 \
    --posts-per-session 3 \
    --session-delay 1200 \
    --min-delay 3.0 \
    --max-delay 8.0 \
    --verbose
```

**Performance approach (experienced users):**
```bash
python facebook_timeline_cleanup.py \
    --config examples/advanced_config.json \
    --sessions 15 \
    --posts-per-session 20 \
    --session-delay 180 \
    --headless
```

**Debugging mode:**
```bash
python facebook_timeline_cleanup.py \
    --config my_config.json \
    --whatif \
    --verbose \
    --sessions 1 \
    --posts-per-session 1
```

## Environment Variable Examples

**Setup with environment variables:**
```bash
# Linux/macOS
export FB_EMAIL="your@email.com"
export FB_PASSWORD="your_password"
python facebook_timeline_cleanup.py --config examples/basic_config.json

# Windows
set FB_EMAIL=your@email.com
set FB_PASSWORD=your_password
python facebook_timeline_cleanup.py --config examples/basic_config.json
```

**Advanced environment setup:**
```bash
export FB_EMAIL="your@email.com"
export FB_PASSWORD="your_password"
export FB_POSTS_PER_SESSION=10
export FB_MAX_SESSIONS=5
export FB_VERBOSE=true
python facebook_timeline_cleanup.py
```

## Custom Configuration Examples

### Ultra-Conservative
For maximum safety:
```json
{
    "cleaning": {
        "posts_per_session": 3,
        "max_sessions": 1
    },
    "timing": {
        "session_delay": 1800,
        "min_delete_delay": 8.0,
        "max_delete_delay": 15.0
    },
    "execution": {
        "whatif": true,
        "verbose": true
    }
}
```

### Weekend Batch
For unattended weekend runs:
```json
{
    "cleaning": {
        "posts_per_session": 12,
        "max_sessions": 20
    },
    "timing": {
        "session_delay": 900,
        "min_delete_delay": 4.0,
        "max_delete_delay": 8.0
    },
    "browser": {
        "headless": true
    }
}
```

### Development/Testing
For developers testing the tool:
```json
{
    "cleaning": {
        "posts_per_session": 1,
        "max_sessions": 1
    },
    "timing": {
        "session_delay": 10,
        "min_action_delay": 0.5,
        "max_action_delay": 1.0
    },
    "execution": {
        "whatif": true,
        "verbose": true
    }
}
```

## Best Practices for Configuration

### Safety First
1. Always start with `basic_config.json`
2. Test extensively with `"whatif": true`
3. Gradually increase batch sizes
4. Monitor Facebook for any restrictions

### Performance Optimization
1. Start with conservative settings
2. Measure actual deletion rates
3. Adjust delays based on performance
4. Use headless mode for better performance

### Troubleshooting
1. Use verbose mode for debugging
2. Reduce batch sizes if errors occur
3. Increase delays if rate limited
4. Test with whatif mode when changing settings

## Warning Signs

Stop and reconfigure if you see:
- Frequent login prompts
- Facebook security warnings
- Unusual error messages
- Significantly slower performance
- Browser crashes or timeouts

## Getting Help

For configuration assistance:
1. Start with provided examples
2. Read the [Configuration Reference](../docs/configuration.md)
3. Check GitHub issues for similar setups
4. Create an issue with your specific use case