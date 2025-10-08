# API Setup Guide

This guide explains how to configure API credentials for data sources that require authentication.

---

## Reddit API Setup (Required for reddit_posts)

Reddit now **requires authentication** even for read-only access. Without proper credentials, you'll see `401 Unauthorized` errors.

### Steps to Get Reddit Credentials

1. **Go to Reddit Apps**: https://www.reddit.com/prefs/apps
2. **Click**: "create another app..." button at the bottom
3. **Fill out the form**:
   - **name**: `tech-trends-harvester` (or any name you want)
   - **App type**: Select **"script"**
   - **description**: `Personal tech trends research tool` (optional)
   - **about url**: Leave blank (optional)
   - **redirect uri**: `http://localhost:8080` (required but unused for scripts)
4. **Click**: "create app"

### Get Your Credentials

After creating the app, you'll see:
- **client_id**: 14-character string under the app name
- **client_secret**: Longer string labeled "secret"

### Configure in Environment Variables

Create a file called `.env` in the project root:

```bash
# Reddit API Credentials
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=tech-trends-harvester/1.0 by /u/your_reddit_username
```

Replace:
- `your_client_id_here` with your client ID
- `your_client_secret_here` with your client secret
- `your_reddit_username` with your actual Reddit username

### Alternative: Without Reddit

If you don't want to set up Reddit credentials, simply disable it in `config/sources.yaml`:

```yaml
collectors:
  reddit_posts:
    enabled: false  # Disable if no credentials
```

---

## Google Trends (Optional - No Auth Required)

Google Trends uses the unofficial `pytrends` library which doesn't require authentication, but **is heavily rate-limited**.

### Rate Limiting Issues

If you see `429 Too Many Requests`:
- Google has temporarily blocked your IP
- Wait 1-24 hours before trying again
- Reduce the number of keywords
- Increase delays between requests

### Safe Usage

For testing, **disable Google Trends**:

```yaml
collectors:
  google_trends:
    enabled: false  # Disable during rapid testing
```

Enable only for production runs (once per day or week).

---

## Stack Overflow (Optional API Key)

Stack Overflow works without authentication but has low limits:
- **Anonymous**: 300 requests/day
- **With API Key**: 10,000 requests/day (free!)

### Get a Stack Overflow API Key (Optional)

1. **Register your app**: https://stackapps.com/apps/oauth/register
2. Fill out the form (simple details, just for tracking)
3. **Get your API key**

### Add to config/sources.yaml:

```yaml
collectors:
  stackoverflow_tags:
    enabled: true
    api_key: "your_api_key_here"  # Add this line
    site: "stackoverflow"
    top_n: 200
```

---

## Summary

### Required for Full Functionality
- ✅ **Reddit**: Required for reddit_posts collector (otherwise disable it)

### Optional (Improves Limits)
- ⚠️ **Stack Overflow API Key**: Increases limit from 300/day to 10,000/day

### No Auth Needed
- ✅ Hacker News
- ✅ DEV.to  
- ✅ Lobsters
- ✅ Medium RSS
- ✅ Homebrew
- ✅ npm
- ✅ PyPI
- ✅ crates.io
- ✅ HN Algolia
- ⚠️ Google Trends (works but rate-limited)
- ⚠️ GitHub Trending (works but rate-limited)

---

## Security Notes

**Never commit credentials to git!**

The `.env` file is already in `.gitignore`. If you accidentally committed credentials:
1. Immediately revoke them on Reddit/Stack Overflow
2. Generate new ones
3. Remove from git history

**Safe practices:**
- Use environment variables (`.env` file)
- Never hardcode credentials in source files
- Don't share your `.env` file
- Each developer should have their own credentials

---

## Troubleshooting

### "401 Unauthorized" from Reddit
- You need to set up Reddit API credentials (see above)
- Or disable `reddit_posts` in config

### "429 Too Many Requests" from Google Trends
- You're being rate-limited
- Disable Google Trends during testing
- Only enable for production runs (daily/weekly)

### "Quota Exceeded" from Stack Overflow
- You hit the 300/day anonymous limit
- Get a free API key for 10,000/day
- Or wait until midnight UTC for quota reset

---

## Testing Configuration

For rapid development/testing, use this minimal config:

```yaml
collectors:
  # Safe sources (no rate limiting issues)
  hackernews:
    enabled: true
  stackoverflow_tags:
    enabled: true
  devto:
    enabled: true
  lobsters:
    enabled: true
  homebrew:
    enabled: true
  npm_downloads:
    enabled: true
  pypi:
    enabled: true
  crates:
    enabled: true
  
  # Disable during rapid testing
  reddit_posts:
    enabled: false  # Requires auth setup
  google_trends:
    enabled: false  # Heavy rate limiting
  github_trending:
    enabled: false  # Can get blocked
```

See [RATE_LIMITS.md](RATE_LIMITS.md) for detailed rate limiting information.

