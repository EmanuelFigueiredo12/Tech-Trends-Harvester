# Rate Limiting & Blocking Risk Analysis

## Overview

This document identifies which data sources might block or rate-limit this tool during testing, and how to avoid issues.

## Legal & Ethical Commitment

This tool is designed as a research and content planning application that adheres to all applicable legal and ethical standards. We are committed to:

- **Respecting Terms of Service**: We honor the terms, conditions, and usage policies of all data providers
- **Following Rate Limits**: We implement reasonable delays and respect published rate limits to avoid service disruption
- **Preventing Abuse**: We take active measures to prevent any behavior that could be construed as abusive, excessive, or harmful to data providers
- **Using Public APIs**: Where available, we prioritize official, documented APIs over unofficial methods
- **Responsible Usage**: We encourage users to employ this tool responsibly, with consideration for the resources and communities they interact with
- **Transparency**: We document our data collection methods and provide clear guidance on ethical usage

Users of this tool are expected to exercise good judgment, comply with all applicable laws and terms of service, and use the tool in a manner that respects the rights and resources of data providers.

See the "Legal & Ethical Notes" section of this document for some details and additional guidance.

---

## 🔴 HIGH RISK - Will Block if Abused

### 1. Google Trends (pytrends)
**Risk Level**: 🔴 **VERY HIGH**

**Why it's risky:**
- Unofficial API (screen scraping Google)
- Google actively tries to prevent automated access
- Very aggressive rate limiting
- Can temporarily block your IP (24-48 hours)

**Rate Limits:**
- ~5-10 requests per minute (soft limit)
- ~100 requests per day (before triggering blocks)
- Blocks escalate: 1 hour → 24 hours → permanent IP ban

**Current Implementation:**
```python
# We fetch keywords in batches of 5 (Google's limit)
# 2 second delay between batches (built-in)
# Fetches 2 API calls per batch: interest_over_time + related_queries
```

**Safe Usage:**
- ✅ Run once every 30+ minutes during testing
- ✅ Disable during rapid testing (toggle off in config)
- ✅ Use only 5-10 keywords at a time
- ❌ Don't run multiple times in quick succession
- ❌ Don't query 50+ keywords in one go

**What happens if blocked:**
- Requests will timeout or return empty results
- You'll see "429 Too Many Requests" in debug
- Wait 1-24 hours before trying again
- Consider using a VPN to change IP if permanently blocked

**Recommendation for Testing:**
```yaml
google_trends:
  enabled: false  # DISABLE during rapid testing!
```

---

### 2. GitHub Trending
**Risk Level**: 🟡 **MEDIUM-HIGH**

**Why it's risky:**
- No official API for trending page
- Screen scraping HTML (detectable)
- GitHub monitors for scraping behavior
- Can trigger "unusual activity" blocks

**Rate Limits:**
- ~60 requests per hour (unauthenticated)
- Stricter if detected as bot
- IP-based blocking possible

**Current Implementation:**
```python
# Fetches 1 page per language
# Default: 1 request (all languages)
# If you add languages: 1 request per language
```

**Safe Usage:**
- ✅ Fetch every 1+ hours
- ✅ Use default (no language filter) = only 1 request
- ❌ Don't add many languages (each is a request)
- ❌ Don't run every few minutes

**What happens if blocked:**
- GitHub returns captcha page
- You'll get 0 results
- Block usually temporary (1-24 hours)

**Recommendation for Testing:**
```yaml
github_trending:
  enabled: false  # Or set languages: [] for minimal requests
  since: weekly   # Don't change too often
  languages: []   # Keep empty = 1 request only
```

---

### 3. HN Algolia
**Risk Level**: 🟡 **MEDIUM**

**Why it's risky:**
- Official API but has rate limits
- Enforces limits per IP address
- Paginated requests (fetches 3 pages by default)

**Rate Limits:**
- 10,000 requests per hour per IP (generous!)
- 1,000 requests per minute (very generous!)
- Rarely blocks, but can if you're extreme

**Current Implementation:**
```python
# Fetches 3 pages by default (3 requests)
# No built-in delay
# hits_per_page: 200 (maximum)
```

**Safe Usage:**
- ✅ Can run every few minutes safely
- ✅ Default config is fine
- ⚠️ Don't run in infinite loops
- ❌ Don't fetch 100+ pages

**What happens if rate limited:**
- Returns 429 error
- Temporary (usually clears in minutes)
- Won't block IP long-term

**Recommendation for Testing:**
```yaml
hn_algolia:
  enabled: true  # Safe to keep enabled
  hours_back: 48
  min_points: 10
  hits_per_page: 200  # Maximum allowed
```

---

## 🟢 LOW RISK - Safe for Frequent Testing

### 4. Hacker News (Firebase API)
**Risk Level**: 🟢 **LOW**

**Why it's safe:**
- Official Firebase API
- Very generous rate limits
- Designed for public access

**Rate Limits:**
- No documented hard limits
- Throttles gracefully if needed
- Firebase infrastructure (scalable)

**Current Implementation:**
```python
# Fetches 2 lists (top, new) = 2 requests
# Then fetches individual items (up to top_n)
# Default: ~152 requests (150 items + 2 lists)
# Has 0.03s sleep between items
```

**Safe Usage:**
- ✅ Can run multiple times per hour
- ✅ Current implementation is respectful
- ✅ Built-in delays prevent issues

**Recommendation:**
```yaml
hackernews:
  enabled: true  # Safe to keep enabled
  top_n: 150    # Can increase if needed
```

---

### 5. Reddit (PRAW)
**Risk Level**: 🟢 **LOW-MEDIUM**

**Why it's mostly safe:**
- Using read-only mode (no auth)
- Official PRAW library handles rate limiting
- Automatic retries built-in

**Rate Limits:**
- 60 requests per minute (read-only)
- PRAW automatically handles delays
- Graceful degradation (won't crash)

**Current Implementation:**
```python
# Fetches top posts from 11 subreddits
# Default: limit=30 per subreddit
# Total: ~11 requests (one per subreddit)
# PRAW handles rate limiting internally
```

**Safe Usage:**
- ✅ Can run every 10-15 minutes
- ✅ PRAW prevents you from hitting limits
- ⚠️ If you add many subreddits, will be slower
- ❌ Don't fetch from 50+ subreddits

**What happens if rate limited:**
- PRAW automatically waits and retries
- You'll see slower fetch times
- Won't crash or fail

**Recommendation:**
```yaml
reddit_posts:
  enabled: true  # Safe to keep enabled
  subreddits: [...]  # 10-15 is fine
  time_filter: "week"
  limit: 30
  min_score: 50
```

---

### 6. Stack Overflow (Stack Exchange API)
**Risk Level**: 🟢 **LOW**

**Why it's safe:**
- Official API
- Very generous rate limits for anonymous access
- Designed for public data access

**Rate Limits:**
- 300 requests per day (anonymous)
- 10,000 requests per day (with API key - free!)
- Quota resets at midnight UTC

**Current Implementation:**
```python
# Fetches tags in pages of 100
# Default: top_n=200 = 2 requests
# Has pagesize=100 (max allowed)
```

**Safe Usage:**
- ✅ Can run many times per day
- ✅ Consider getting free API key for 10K/day
- ✅ Current config uses minimal requests

**What happens if quota exceeded:**
- Returns error with quota info
- Resets at midnight UTC
- Get API key to increase limit

**Recommendation:**
```yaml
stackoverflow_tags:
  enabled: true  # Very safe
  site: "stackoverflow"
  top_n: 200  # Only 2 requests
```

**Pro Tip:** Get a free API key:
1. Register at https://stackapps.com/apps/oauth/register
2. Add to config: `api_key: "your-key-here"`
3. Now you get 10,000 requests/day!

---

### 7. DEV.to (Forem API)
**Risk Level**: 🟢 **LOW**

**Why it's safe:**
- Official public API
- Good rate limits
- Designed for external access

**Rate Limits:**
- Not strictly documented
- Generally very permissive
- Uses standard HTTP rate limiting

**Current Implementation:**
```python
# Fetches paginated articles
# Default: per_page=80, pages=1 = 1 request
# Can increase pages if needed
```

**Safe Usage:**
- ✅ Very safe for frequent access
- ✅ Can increase pages if needed
- ✅ No authentication required

**Recommendation:**
```yaml
devto:
  enabled: true  # Very safe
  per_page: 80
  pages: 1  # Increase to 2-3 if you want more data
```

---

### 8. Lobsters
**Risk Level**: 🟢 **LOW**

**Why it's safe:**
- Public JSON endpoints
- Small site, but tolerant of polite scrapers
- Community-friendly

**Rate Limits:**
- No official API, but JSON endpoints widely used
- Implicit rate limiting
- Very tolerant if you're not aggressive

**Current Implementation:**
```python
# Fetches 1 JSON endpoint
# Default: top_n=150 items in 1 request
```

**Safe Usage:**
- ✅ Safe for hourly access
- ✅ One request per fetch
- ✅ Respectful delays built-in

**Recommendation:**
```yaml
lobsters:
  enabled: true  # Safe
  endpoint: "https://lobste.rs/hottest.json"
  top_n: 150
```

---

### 9. Medium RSS
**Risk Level**: 🟢 **LOW**

**Why it's safe:**
- Public RSS feeds
- Designed for syndication
- No rate limits typically enforced

**Rate Limits:**
- RSS is public by design
- No enforced limits
- Standard politeness rules apply

**Current Implementation:**
```python
# Fetches RSS feed per topic
# Default: 4 topics = 4 requests
# Uses feedparser (respectful)
```

**Safe Usage:**
- ✅ Very safe
- ✅ Can add more topics
- ✅ RSS is meant to be accessed

**Recommendation:**
```yaml
medium:
  enabled: true  # Very safe
  topics: ["technology", "programming", ...]
```

---

### 10. Homebrew Analytics
**Risk Level**: 🟢 **VERY LOW**

**Why it's safe:**
- Static JSON files
- Public analytics data
- Updated daily, meant to be accessed

**Rate Limits:**
- None (static files on CDN)
- Public analytics URL
- Can access as often as needed

**Current Implementation:**
```python
# Fetches 1 JSON file
# Downloads install counts
```

**Safe Usage:**
- ✅ Completely safe
- ✅ Can run unlimited times
- ✅ It's just downloading a public JSON file

**Recommendation:**
```yaml
homebrew:
  enabled: true  # Totally safe
  window: "30d"
```

---

### 11. npm Downloads
**Risk Level**: 🟢 **LOW**

**Why it's safe:**
- Official npm API
- Public download stats
- Good rate limits

**Rate Limits:**
- Not strictly enforced
- Many requests per day allowed
- Per-package queries

**Current Implementation:**
```python
# Fetches download stats per package
# Default: 10 packages = 10 requests
```

**Safe Usage:**
- ✅ Very safe
- ✅ Can query 50+ packages
- ✅ Official API for public data

**Recommendation:**
```yaml
npm:
  enabled: true  # Safe
  packages: [...]  # 10-20 packages is fine
```

---

### 12. PyPI (pypistats/pepy)
**Risk Level**: 🟢 **LOW**

**Why it's safe:**
- Public stats APIs
- Designed for this use case
- Good rate limits

**Rate Limits:**
- pypistats: Generous, no issues
- pepy: Fallback, also generous
- Both designed for automated access

**Current Implementation:**
```python
# Tries pypistats first, falls back to pepy
# Fetches per package
# Default: 10 packages = 10-20 requests (with fallback)
```

**Safe Usage:**
- ✅ Very safe
- ✅ Can query many packages
- ✅ Has fallback if one API is slow

**Recommendation:**
```yaml
pypi:
  enabled: true  # Safe
  packages: [...]  # 10-20 packages is fine
```

---

### 13. crates.io
**Risk Level**: 🟢 **LOW**

**Why it's safe:**
- Official Rust package registry
- Public API
- Designed for automation

**Rate Limits:**
- Documented at 1 req/sec per IP
- Very reasonable
- 60+ requests per minute allowed

**Current Implementation:**
```python
# Fetches recent downloads
# Paginated: per_page=100
# Default: 1 request (100 crates)
```

**Safe Usage:**
- ✅ Safe for frequent access
- ✅ Respects 1 req/sec limit
- ✅ Official API

**Recommendation:**
```yaml
crates:
  enabled: true  # Safe
  per_page: 100  # Max allowed
```

---

## Summary Table

| Source | Risk | Requests/Fetch | Safe Interval | Can Block IP? | Notes |
|--------|------|----------------|---------------|---------------|-------|
| **Google Trends** | 🔴 Very High | 2-6 | 30+ min | ✅ YES | Disable during testing! |
| **GitHub Trending** | 🟡 Medium | 1-N | 1+ hour | ⚠️ Maybe | Don't use language filters |
| **HN Algolia** | 🟡 Medium | 3 | 5+ min | ⚠️ Rare | Very generous limits |
| **Hacker News** | 🟢 Low | ~152 | 10+ min | ❌ No | Official API, safe |
| **Reddit** | 🟢 Low | ~11 | 10+ min | ❌ No | PRAW handles limits |
| **Stack Overflow** | 🟢 Low | 2 | Unlimited | ❌ No | 300/day, get API key for 10K |
| **DEV.to** | 🟢 Low | 1 | Unlimited | ❌ No | Official API |
| **Lobsters** | 🟢 Low | 1 | 1+ hour | ❌ No | Small site, be polite |
| **Medium** | 🟢 Low | 4 | Unlimited | ❌ No | RSS feeds |
| **Homebrew** | 🟢 Very Low | 1 | Unlimited | ❌ No | Static JSON |
| **npm** | 🟢 Low | 10 | Unlimited | ❌ No | Official API |
| **PyPI** | 🟢 Low | 10-20 | Unlimited | ❌ No | Public stats |
| **crates.io** | 🟢 Low | 1 | 1+ min | ❌ No | Official API |

---

## Best Practices for Testing

### Safe Testing Configuration

**Option 1: Disable Risky Sources**
```yaml
collectors:
  google_trends:
    enabled: false  # ← Disable during rapid testing
  
  github_trending:
    enabled: false  # ← Or keep but use sparingly
  
  # Keep all the safe ones enabled
  hackernews:
    enabled: true
  reddit_posts:
    enabled: true
  stackoverflow_tags:
    enabled: true
  # ... etc
```

### Option 2: Minimal High-Signal Config
```yaml
collectors:
  # Only the safest + highest value sources
  reddit_posts:
    enabled: true     # Safe + High value
  
  hackernews:
    enabled: true     # Safe + Good value
  
  stackoverflow_tags:
    enabled: true     # Safe + Good value
  
  # Disable everything else during testing
  google_trends:
    enabled: false
  github_trending:
    enabled: false
  hn_algolia:
    enabled: false
  # ...
```

### Testing Workflow

**Phase 1: Rapid Development (multiple runs per minute)**
```yaml
# Enable ONLY these (safest):
- hackernews
- stackoverflow_tags
- devto
- homebrew
- npm
- pypi
```

**Phase 2: Integration Testing (every 15 minutes)**
```yaml
# Add medium-risk sources:
+ reddit_posts
+ lobsters
+ medium
+ crates
```

**Phase 3: Full Testing (hourly)**
```yaml
# Add remaining sources:
+ hn_algolia
+ github_trending
+ google_trends (carefully!)
```

**Production: Daily/Weekly Usage**
```yaml
# Enable everything
# Run once per day or week
# No blocking risk at this frequency
```

---

## What To Do If Blocked

### Google Trends Blocked
**Symptoms:**
- Timeouts
- Empty results
- "429 Too Many Requests"

**Solutions:**
1. Wait 1-24 hours
2. Change IP (VPN, mobile hotspot, etc.)
3. Use fewer keywords
4. Disable for testing, enable for production only

### GitHub Trending Blocked
**Symptoms:**
- Captcha page in HTML
- 0 results returned
- HTTP 403 errors

**Solutions:**
1. Wait 1-6 hours
2. Reduce frequency
3. Don't use language filters (reduces requests)
4. Consider GitHub API alternative (requires auth but safer)

### General Rate Limiting
**Symptoms:**
- HTTP 429 (Too Many Requests)
- Slow responses
- Partial data

**Solutions:**
1. Add delays between sources (done automatically)
2. Reduce fetch frequency
3. Get API keys where available (Stack Overflow)
4. Use VPN to rotate IPs (if needed)

---

## Pro Tips

1. **During Development:**
   - Disable Google Trends and GitHub Trending
   - Use only safe sources (green flags)
   - Test with minimal data first

2. **Get API Keys:**
   - Stack Overflow: Free 10K requests/day
   - Consider Reddit auth for higher limits (optional)

3. **Rotate User Agents:**
   - Already done! Using common Chrome UA
   - Consider rotating between Chrome/Firefox/Safari (advanced)

4. **Use Proxies (Advanced):**
   - If you need to run frequently
   - Rotate IPs to avoid blocks
   - Most users won't need this

5. **Monitor Debug Tab:**
   - Watch for errors
   - Adjust config based on which sources fail
   - Disable problematic sources temporarily

---

## Recommended Testing Schedule

**First Hour (Rapid Testing):**
- Refresh every 5-10 minutes
- Only safe sources enabled
- Test UI/features quickly

**Day 1-2 (Integration Testing):**
- Refresh every 30 minutes
- Add medium-risk sources
- Test data quality

**Week 1+ (Production Usage):**
- Refresh once per day
- All sources enabled
- Full data collection

**Monthly (Production):**
- Run daily or weekly
- No blocking concerns
- Archive historical data

---

## ⚠️ Legal & Ethical Notes

**All sources used here:**
- ✅ Provide public APIs or public data
- ✅ Are documented for external use (or widely used RSS/JSON)
- ✅ Don't require breaking ToS

**We avoid:**
- ❌ Bypassing login/paywalls
- ❌ Accessing private data
- ❌ Aggressive scraping
- ❌ Violating ToS

**Best practices:**
- Identify as browser (done)
- Respect rate limits (done)
- Add delays (done)
- Don't overload servers
- Use official APIs when available (done)

---

## Summary

**For Testing (Rapid Iterations):**
- ✅ Disable: Google Trends, GitHub Trending
- ✅ Enable: Everything else
- ✅ Safe to run every 5-10 minutes

**For Production (Daily/Weekly):**
- ✅ Enable: Everything
- ✅ Run once per day or week
- ✅ Zero blocking risk

**The Golden Rule:**
> If you're getting blocked, you're testing too aggressively. 
> Disable risky sources during development, enable for production.
