# Contributing to Tech Trends Harvester

Thank you for your interest in contributing to Tech Trends Harvester! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on GitHub with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your environment (OS, Python version)
- Any relevant logs or screenshots

### Suggesting Enhancements

Enhancement suggestions are welcome! Please open an issue with:
- A clear description of the enhancement
- Why this enhancement would be useful
- Any implementation ideas you have

### Adding New Data Sources

Want to add a new data source? Great! Here's how:

1. Create a new collector in `src/collectors/your_source.py`
2. Implement a `fetch(**kwargs)` function that returns a list of dicts with these keys:
   - `term`: The keyword/phrase
   - `kind`: Type of data (e.g., "title", "tag", "package")
   - `metric_name`: What you're measuring (e.g., "points", "stars")
   - `metric_value`: The numeric value
   - `url`: Link to the source
   - `source`: Name of your source
   - `captured_at`: ISO timestamp

3. Register it in `src/app/registry.py`
4. Add configuration to `config/sources.yaml`
5. Document rate limits in `RATE_LIMITS.md`
6. Test thoroughly!

### Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit with clear, descriptive messages
6. Push to your fork
7. Open a Pull Request with:
   - Clear description of changes
   - Why the changes are needed
   - Any breaking changes
   - Screenshots if UI changes

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions
- Keep functions focused and small
- No emojis or em-dashes in source code (use bracketed tags like [OK], [ERROR])
- Add comments for complex logic

### Testing

- Test your changes with `./start.sh`
- Run diagnostics with `python diagnose.py`
- Test with both testing and production configs
- Verify no new linter errors

### Commit Messages

- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove)
- Reference issues when applicable (#123)

Example:
```
Add PyPI collector for Python package trends

- Implements fetch() function using pypistats API
- Adds configuration options for package list
- Includes rate limit documentation
- Fixes #123
```

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Respect different viewpoints and experiences

## Questions?

Feel free to open an issue for any questions about contributing!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
