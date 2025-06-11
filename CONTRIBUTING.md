# Contributing to Facebook Timeline Cleanup

Thank you for your interest in contributing to Facebook Timeline Cleanup! This document provides guidelines for contributing to this project.

## Code of Conduct

This project adheres to a code of conduct that promotes respect, collaboration, and inclusivity. By participating, you are expected to uphold this standard.

## Before Contributing

### Important Considerations

This project involves automating interactions with Facebook, which:
- May violate Facebook's Terms of Service
- Can permanently delete user data
- Requires careful testing and validation
- Has significant security and privacy implications

**All contributions must prioritize user safety and data protection.**

## Ways to Contribute

### Reporting Issues

**Bug Reports:**
- Use the GitHub issue tracker
- Include detailed reproduction steps
- Provide system information (OS, Python version, Chrome version)
- Include relevant log files (remove personal information)
- Describe expected vs actual behavior

**Feature Requests:**
- Check existing issues first
- Describe the use case and benefits
- Consider security and safety implications
- Provide implementation suggestions if possible

### Documentation Improvements

**Always welcome:**
- Fixing typos and grammar
- Improving clarity and completeness
- Adding examples and use cases
- Translating documentation
- Updating outdated information

### Code Contributions

**Areas needing improvement:**
- Better error handling and recovery
- Support for additional browsers
- Enhanced rate limiting detection
- Improved post type detection
- Better configuration validation
- Testing framework improvements

## Development Setup

### Prerequisites

```bash
# Python 3.7 or higher
python --version

# Git for version control
git --version

# Chrome browser for testing
google-chrome --version
```

### Environment Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/facebook-timeline-cleanup.git
cd facebook-timeline-cleanup

# Create virtual environment
python -m venv dev-env
source dev-env/bin/activate  # or dev-env\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (if available)
pip install -r requirements-dev.txt
```

### Development Configuration

**Create test configuration:**
```bash
# Copy template
cp config_template.json test_config.json

# Edit with test account credentials (NEVER use your main account)
# Set "whatif": true for all development testing
```

## Contribution Guidelines

### Safety Requirements

**MANDATORY for all contributions:**

1. **No Real Account Testing**: Never test with real personal Facebook accounts
2. **Whatif Mode Default**: All examples must default to whatif mode
3. **Safety Warnings**: Include appropriate warnings in documentation
4. **Data Protection**: Never commit credentials or personal data
5. **Error Handling**: All code must handle errors gracefully

### Code Standards

**Python Style:**
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Include docstrings for all functions and classes
- Add type hints where beneficial
- Maintain consistency with existing code

**Example:**
```python
def delete_posts_batch(self, max_posts: int) -> int:
    """
    Delete a batch of posts from current page.
    
    Args:
        max_posts: Maximum number of posts to delete
        
    Returns:
        Number of posts actually deleted
        
    Raises:
        FacebookTimelineError: If critical error occurs
    """
```

**Logging Standards:**
- Use appropriate log levels (DEBUG, INFO, WARNING, ERROR)
- Include context in log messages
- Protect sensitive information in logs
- Follow existing logging patterns

### Testing Requirements

**Before submitting:**
1. Test with whatif mode extensively
2. Verify all command line arguments work
3. Test configuration file parsing
4. Ensure graceful error handling
5. Validate log output format
6. Test interruption handling (Ctrl+C)

**Testing checklist:**
```bash
# Basic functionality
python facebook_timeline_cleanup.py --whatif --verbose

# Configuration handling
python facebook_timeline_cleanup.py --save-config test.json
python facebook_timeline_cleanup.py --config test.json --whatif

# Error conditions
python facebook_timeline_cleanup.py --email invalid --whatif
python facebook_timeline_cleanup.py --sessions -1 --whatif
```

### Documentation Requirements

**For all changes:**
- Update relevant documentation files
- Add examples for new features
- Include safety warnings where appropriate
- Update configuration reference if needed
- Add to troubleshooting guide if relevant

**Documentation standards:**
- Clear, concise language
- Step-by-step instructions
- Include command examples
- Highlight safety considerations
- No assumed knowledge levels

## Submission Process

### Pull Request Process

1. **Fork the repository** on GitHub
2. **Create a feature branch** from main:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following the guidelines above
4. **Test thoroughly** with whatif mode
5. **Update documentation** as needed
6. **Commit with clear messages**:
   ```bash
   git commit -m "Add improved error handling for login failures"
   ```
7. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
8. **Create pull request** with detailed description

### Pull Request Description

**Include:**
- Clear description of changes
- Motivation and use case
- Testing performed
- Safety considerations
- Documentation updates
- Breaking changes (if any)

**Template:**
```markdown
## Description
Brief description of changes

## Motivation
Why this change is needed

## Testing
- [ ] Tested with whatif mode
- [ ] Verified configuration handling
- [ ] Tested error conditions
- [ ] Updated documentation

## Safety Review
- [ ] No security vulnerabilities introduced
- [ ] Proper error handling added
- [ ] Safety warnings included where needed
- [ ] No personal data in commits

## Breaking Changes
None / List any breaking changes
```

## Review Process

### What We Look For

**Code Quality:**
- Follows Python best practices
- Includes appropriate error handling
- Has clear, understandable logic
- Maintains consistency with existing code

**Safety:**
- Prioritizes user data protection
- Includes appropriate warnings
- Handles errors gracefully
- Doesn't introduce security vulnerabilities

**Documentation:**
- Clear and accurate
- Includes examples
- Updates all relevant files
- Maintains consistency

### Review Timeline

- Initial review within 1 week
- Follow-up reviews within 3 days
- Merge after approval from maintainers
- May require multiple iterations

## Feature Development Guidelines

### New Features

**Before implementing:**
1. Create an issue to discuss the feature
2. Get feedback from maintainers
3. Consider safety and security implications
4. Plan documentation updates

**Implementation:**
1. Follow existing code patterns
2. Include comprehensive error handling
3. Add configuration options if needed
4. Update all relevant documentation
5. Provide usage examples

### Backwards Compatibility

**Maintain compatibility:**
- Don't break existing command line arguments
- Support existing configuration formats
- Provide migration paths for breaking changes
- Document deprecations clearly

## Security Considerations

### Sensitive Information

**Never commit:**
- Passwords or credentials
- Personal Facebook data
- Private configuration files
- Log files with personal information
- API keys or tokens

### Security Review

**All contributions undergo security review for:**
- Credential handling
- Data protection
- Input validation
- Error message safety
- Log file content

## Getting Help

### Development Questions

**Channels:**
- GitHub issues for public discussion
- Code comments for specific implementation questions
- Documentation for usage guidance

**Response Times:**
- Issues: Within 1 week
- Pull requests: Within 1 week for initial review
- Critical security issues: Within 24 hours

### Resources

- [Python Style Guide](https://pep8.org/)
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [Facebook Developer Policies](https://developers.facebook.com/docs/development/policies/)

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes for significant contributions
- GitHub contributors list

Thank you for helping make Facebook Timeline Cleanup safer and more reliable!