# Configuration Switching Guide

## Quick Answer

You have 3 ways to disable Google Trends for testing:

---

## Method 1: Quick Manual Edit (Simplest)

**Edit `config/sources.yaml`:**

```yaml
google_trends:
  enabled: false  # ← Change true to false
```

**To re-enable:**
```yaml
google_trends:
  enabled: true  # ← Change back to true
```

---

## Method 2: Use the Switcher Script (Recommended)

I've created a script that switches between configs for you:

### Switch to Testing Config (Safe for Rapid Testing)

```bash
./switch-config.sh testing
```

**What it does:**
- ✅ Disables Google Trends (won't block you)
- ✅ Disables GitHub Trending (won't captcha you)
- ✅ Keeps all safe sources enabled
- ✅ Safe to run every 5-10 minutes

### Switch to Production Config (Full Data Collection)

```bash
./switch-config.sh production
```

**What it does:**
- ✅ Enables all sources including Google Trends
- ✅ Full data collection
- ⚠️ Only run hourly or daily

### Check Current Config

```bash
./switch-config.sh status
```

Shows which config is active and source status.

---

## Method 3: Use Different Config Files

You can also manually swap config files:

```bash
# For testing
cp config/sources-testing.yaml config/sources.yaml

# For production
cp config/sources-production.yaml config/sources.yaml
```

---

## Available Config Files

After running the setup, you have these files:

| File | Purpose | Google Trends | GitHub Trending | Use When |
|------|---------|---------------|-----------------|----------|
| **sources.yaml** | Active config | ✅ Enabled | ✅ Enabled | Current (whatever you set) |
| **sources-testing.yaml** | Safe testing | ❌ Disabled | ❌ Disabled | Rapid development |
| **sources-production.yaml** | Full collection | ✅ Enabled | ✅ Enabled | Production/daily runs |
| **sources.yaml.backup** | Auto backup | - | - | Automatic backup |

---

## Typical Workflow

### During Development

```bash
# Switch to safe testing config
./switch-config.sh testing

# Now you can test rapidly
./start.sh
# Test, close, modify, repeat every 5-10 min

# When ready for real data
./switch-config.sh production
```

### Production Use

```bash
# Make sure you're in production mode
./switch-config.sh status

# If not, switch
./switch-config.sh production

# Run daily or weekly
./start.sh
```

---

## What Gets Disabled in Testing Mode

### Disabled (Risky):
- ❌ **Google Trends** - Can block IP for 24+ hours
- ❌ **GitHub Trending** - Can trigger captchas

### Still Enabled (Safe):
- ✅ **Reddit Posts** - Official API, handles rate limits
- ✅ **Hacker News** - Official API, very generous
- ✅ **HN Algolia** - Official API, high limits
- ✅ **Stack Overflow** - Official API, generous
- ✅ **DEV.to** - Official API
- ✅ **Lobsters** - Public JSON, tolerant
- ✅ **Medium** - RSS feeds (public)
- ✅ **Homebrew** - Static JSON (unlimited)
- ✅ **npm** - Official API
- ✅ **PyPI** - Official API
- ✅ **crates.io** - Official API

---

## Manual Configuration Options

If you want to customize further, edit `config/sources.yaml`:

### Disable Individual Sources

```yaml
collectors:
  google_trends:
    enabled: false  # ← Disable this source
  
  hackernews:
    enabled: true   # ← Keep this enabled
```

### Adjust Fetch Frequency

For testing, reduce data volumes:

```yaml
reddit_posts:
  limit: 10        # ← Fewer posts (default: 30)
  min_score: 100   # ← Higher threshold (default: 50)

hackernews:
  top_n: 50        # ← Fewer items (default: 150)
```

---

## Verification

After switching configs, verify what's enabled:

```bash
# Check which sources are enabled
grep -A 1 "enabled:" config/sources.yaml | grep -E "(enabled|google|github)"

# Or use the status command
./switch-config.sh status
```

---

## Troubleshooting

### "Permission denied" when running switch-config.sh

```bash
chmod +x switch-config.sh
```

### Config file not found

Make sure you're in the project root:

```bash
cd /Users/rich/dev/github/richlewis007/tech-trends-harvester
./switch-config.sh status
```

### Want to create your own config

```bash
# Copy current config
cp config/sources.yaml config/sources-mycustom.yaml

# Edit it
nano config/sources-mycustom.yaml

# Use it
cp config/sources-mycustom.yaml config/sources.yaml
```

---

## Quick Reference

```bash
# TESTING (safe, rapid development)
./switch-config.sh testing
./start.sh
# Run as often as you want!

# PRODUCTION (full data, run infrequently)
./switch-config.sh production
./start.sh
# Run once per day/week

# CHECK STATUS
./switch-config.sh status

# MANUAL EDIT
nano config/sources.yaml
# Change enabled: true/false for any source
```

---

## Best Practices

### For Testing New Features
1. Switch to testing config
2. Test rapidly (every 5-10 min is safe)
3. Focus on UI/logic, not data quality
4. Switch to production when ready

### For Production Data Collection
1. Switch to production config
2. Run once per day or week
3. All sources enabled
4. No blocking risk

### For Blog Research
1. Use production config
2. Run in the morning
3. Review Blog Topics tab
4. Write posts during the day

---

## Summary

**Quickest Method:**
```bash
# Edit this file
nano config/sources.yaml

# Find this line (around line 47)
google_trends:
  enabled: false  # ← Change to false for testing
```

**Best Method:**
```bash
# Use the switcher script
./switch-config.sh testing      # Safe for testing
./switch-config.sh production   # Full data collection
./switch-config.sh status       # Check current
```

That's it! Now you can safely test without worrying about getting blocked.

