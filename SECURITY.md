# Security Policy

## Supported Versions

Currently supported versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.6.x   | :white_check_mark: |
| < 0.6   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do NOT** open a public issue
2. Email security concerns to: 1149213+RichLewis007@users.noreply.github.com
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Any suggested fixes

We will respond within 48 hours and work with you to address the issue.

## Security Best Practices for Users

### API Keys and Credentials

- Never commit API keys or credentials to the repository
- Use environment variables for sensitive data
- Keep your `.env` files in `.gitignore`

### Rate Limiting

- Follow the rate limiting guidelines in `RATE_LIMITS.md`
- Use the testing configuration during development
- Respect Terms of Service for all data sources

### Network Security

- The application makes HTTP requests to public APIs
- Review `RATE_LIMITS.md` for details on data collection methods
- Use official APIs when available
- Be aware of the legal and ethical implications (see `RATE_LIMITS.md`)

### Dependencies

- Keep dependencies up to date: `uv sync --upgrade`
- Review dependency changes before updating
- Report any suspicious dependency behavior

## Known Limitations

- Google Trends uses an unofficial API (pytrends) which may break
- Some sources use HTML parsing which may be fragile
- No authentication is implemented (read-only access only)

## Disclosure Policy

- We will acknowledge receipt of vulnerability reports within 48 hours
- We will provide regular updates on our progress
- We will credit reporters (unless they prefer anonymity)
- We will disclose vulnerabilities after fixes are released
