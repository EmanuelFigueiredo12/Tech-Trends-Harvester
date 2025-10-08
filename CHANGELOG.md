# Changelog

All notable changes to Tech Trends Harvester are documented in this file.

---

## [0.6.1] - 2025-10-08

### GitHub Repository Enhancements

**Professional Repository Setup**
- Added MIT LICENSE file
- Created CONTRIBUTING.md with contribution guidelines
- Created SECURITY.md with security policy and vulnerability reporting
- Created CODE_OF_CONDUCT.md (Contributor Covenant 2.0)
- Added comprehensive README badges (Python version, License, GUI framework)
- Added Table of Contents to README
- Enhanced project metadata in pyproject.toml (license, keywords, classifiers, URLs)

**GitHub Actions & Templates**
- Added comprehensive CI/CD workflow (.github/workflows/ci.yml)
- CI tests on Ubuntu, macOS, Windows with Python 3.9 and 3.12 (minimum and latest supported versions)
- Added ci-success summary job for branch protection (single status check for all 6 matrix combinations)
- Fixed dependency installation in CI (uses `uv pip install -e .`)
- Created issue templates (Bug Report, Feature Request, New Data Source)
- Created Pull Request template with checklist

**CI/CD Pipeline Features**
- Automated testing with pytest and coverage reporting
- Code linting with ruff (PEP 8 compliance)
- Code formatting checks with ruff
- Type checking with mypy
- Security scanning with bandit
- Dependency vulnerability checks with safety
- All quality checks run on every push and PR

**Application Icon**
- Added SVG application icon (assets/icon.svg)
- Icon displays trending chart with "TTH" branding
- Integrated icon into main window

**Version Display**
- Window title now shows version number automatically from pyproject.toml
- Supports Python 3.9+ (uses tomli for older versions, tomllib for 3.11+)
- Graceful fallback if version cannot be read

**Unit Tests**
- Created test suite in `tests/` directory
- Tests for utility functions (tokenization, question detection, term filtering)
- Tests for aggregation functions (categorization)
- All tests run automatically in CI
- Fixed test assertions to match actual implementation behavior

### Dependencies

**New Dependencies**
- tomli 2.0+ (for Python < 3.11, conditional)

**New Dev Dependencies**
- pytest 7.4+ (unit testing framework)
- pytest-cov 4.1+ (code coverage)
- ruff 0.1+ (linting and formatting)
- mypy 1.7+ (type checking)
- bandit 1.7+ (security scanning)
- safety 2.3+ (dependency vulnerability checking)
- types-PyYAML, types-requests (type stubs)

---

## [0.6.0] - 2025-10-08

### Major Features - Blog Topics Intelligence

**New: Blog Topics View**
- Added dedicated "Blog Topics" tab focused on blog-worthy content
- Intelligent question detection with intent categorization (how-to, what-is, comparison, troubleshooting)
- N-gram phrase extraction (2-5 word phrases) for actual search queries
- Blog worthiness scoring algorithm combining multiple signals
- Auto-categorization: Framework, Language, Tool, Database, Cloud, AI/ML, DevOps, Security

**New Data Sources**
- Reddit Posts collector - extracts full post titles from tech subreddits
- Google Trends integration - real search volume data from actual users
- Configured for 11+ relevant subreddits (programming, webdev, rust, kubernetes, etc.)
- Keywords tracking: cursor ai, anthropic claude, supabase, bun, astro, langchain, and more

### Enhancements

**Smart Filtering & Scoring**
- Expanded stop words list to filter common/boring terms
- Added `BORING_TERMS` blacklist (lib, src, app, utils, common system words)
- Added `INTERESTING_TECH` whitelist for high-value terms
- Advanced blog worthiness scoring: length, question status, search volume, engagement
- Year-aware bonus scoring (2025/2026 content prioritized)
- Multi-source validation (terms appearing across multiple sources ranked higher)

**Configuration Management**
- Created `sources-testing.yaml` - safe config with rate-limit-prone sources disabled
- Created `sources-production.yaml` - full data collection config
- Added `switch-config.sh` script for easy config switching
- Status checking to see which config is active

**User Experience**
- Clickable URLs in all table views (opens in default browser)
- Better visual styling for URL columns (blue, underlined)
- Tooltips showing full URLs on hover
- Updated user-agent to common browser string to avoid detection

### Dependencies

**Updated to Latest Stable Versions**
- requests 2.32+ (was 2.31)
- pandas 2.3+ (was 2.2)
- PyYAML 6.0.2+ (was 6.0.1)
- beautifulsoup4 6.0+ (was 4.12)
- lxml 6.0+ (new, for better HTML parsing)

**New Dependencies**
- praw 7.8+ - Reddit API wrapper
- pytrends 4.9+ - Google Trends unofficial API

### Documentation

- Created `CONFIG_SWITCHING.md` - guide for testing vs production configs
- Created `RATE_LIMITS.md` - documentation of rate limiting risks per source
- Created `PACKAGE_VERSIONS.md` - detailed dependency version info
- Created `QUICK_FIXES_COMPLETE.md` - summary of recent improvements
- Created `TOOL_LINKS.md` - SEO and trend research tools with pricing
- Updated README with new features and workflow

### Bug Fixes

- Fixed year references: now using 2025 throughout (was 2024)
- Updated Next.js tracking from v14 to v15 in Google Trends keywords

---

## [0.5.0] - 2025-10-05

### New Features

**URL Interactivity**
- Made URLs clickable in "By Source" tab
- Visual feedback (blue color, underline) for clickable URLs
- Click to open source in default browser

**Enhanced Data Presentation**
- Better column formatting in all table views
- Improved sorting functionality
- Source attribution for all terms

### Improvements

- Refactored tokenization logic for better term extraction
- Added minimum threshold filtering for aggregated results
- Improved term clustering preparation

---

## [0.4.2] - 2025-10-02

### Critical Bug Fixes

**Fixed: "Refresh All" button not working**
- Root Cause: QThread was created with parent (`self`), causing threading issues on macOS
- Solution: Removed parent parameter from QThread creation
- Impact: Application now properly fetches data from all sources

**Fixed: Buttons never re-enabling after refresh**
- Root Cause: `allRefreshDone` signal was never emitted
- Solution: Implemented proper thread tracking with `_active_threads` and `_expected_threads` sets
- Impact: UI buttons now properly enable/disable based on fetch status

### New Features

**Progress Updates**
- Added `progressUpdate` signal to show real-time status
- Messages appear in status panel and debug tab
- Shows when fetches start, complete, or encounter issues

**Thread Safety Improvements**
- Proper thread lifecycle management with `_on_thread_finished()`
- Strong references stored in `_thread_refs` to prevent garbage collection
- Thread cleanup properly disconnects signals and deletes objects
- Duplicate fetch prevention (won't start if already running)

**Enhanced Error Handling**
- Better error messages with specific error types
- HTTP status code checking with `raise_for_status()`
- Graceful degradation when sources fail
- Debug logging for network issues

**Source Status Tracking**
- Added `status` field to `SourceState`: idle, fetching, done, error
- UI reflects current state of each source

### Technical Improvements

**Controller** (`src/app/controller.py`)
- Changed thread tracking to use `Set[str]` for active threads
- Added `_expected_threads` set for batch operation tracking
- Improved `refresh_all()` to fetch ALL sources
- Improved `refresh_selected()` to only fetch enabled sources
- Added comprehensive docstrings

**Collectors**
- `hackernews.py`: Status code checking, better error messages
- `hn_algolia.py`: Per-request exception handling, empty title filtering
- `github_trending.py`: Improved HTML parsing, better regex safety

**UI** (`src/app/mainwindow.py`)
- Connected `progressUpdate` signal for real-time feedback
- Added `_onProgress()` handler for progress messages

**Utils** (`src/util.py`)
- Added `safe_fetch` decorator for error handling

### Documentation

- Completely rewrote README.md with feature list and troubleshooting
- Created CHANGELOG.md for version tracking
- Added inline documentation and type hints
- Created project structure diagram

### Testing

- Created `test_threading.py` for isolated validation
- Verified all imports load without errors
- Tested collectors with live API calls

---

## [0.4.1] - 2025-09-28

### New Features

**Movers (Week-over-Week) Tracking**
- Added third tab showing biggest gainers/decliners
- Compares current aggregate against last snapshot
- Highlights emerging and declining trends
- Historical data stored in `data/history/`

**New Package Ecosystem Collectors**
- PyPI collector: weekly downloads via pypistats
- crates.io collector: Rust package recent downloads
- Better coverage of language ecosystems

### Improvements

- Added snapshot storage to `data/last_agg.json`
- Historical tracking in `data/history/` directory
- Export to Markdown now includes Movers section

### Documentation

- Added first-run checklist
- Platform-specific gotchas guide
- Troubleshooting for common errors

---

## [0.4.0] - 2025-09-24

### Major UI Overhaul

**PySide6 GUI Implementation**
- Full desktop GUI replacing command-line interface
- Two main views: Aggregated and By Source
- Source toggles with individual refresh buttons
- Live status panel showing collection progress
- Export to Markdown functionality

**Source Management**
- Toggle sources on/off in the UI
- Refresh all or individual sources
- Visual error indicators per source
- Real-time row counts and timing

### Architecture Improvements

**Modular Collector System**
- Clean structure for adding new sources
- Each collector is a simple `fetch(**kwargs)` function
- Registry system in `src/app/registry.py`
- Easy to extend and maintain

**Better Data Flow**
- Source state management
- Aggregation engine improvements
- Z-score normalization per metric
- Weighted scoring system

---

## [0.3.5] - 2025-09-20

### New Data Sources

**HN Algolia Integration**
- Pulls recent stories via `search_by_date`
- Filters by points and time
- Hotness metric: points ÷ hours since post

**GitHub Trending (Weekly)**
- Parses `github.com/trending?since=weekly`
- Extracts "stars this week" per repo
- Optional language filtering

### Configuration

- `config/sources.yaml` additions:
  - HN Algolia: `hours_back`, `min_points` settings
  - GitHub Trending: `since` (daily/weekly/monthly), language filters
  - Adjustable weights per source

---

## [0.3.0] - 2025-09-15

### Initial Release

**Core Collectors**
- Hacker News (Firebase API)
- Lobsters (JSON feeds)
- DEV.to (Forem API)
- Medium (RSS feeds)
- Stack Overflow (tags API)
- Homebrew (analytics JSON)
- npm (weekly downloads)

**Data Processing**
- Keyword extraction from titles
- Z-score normalization
- Weighted scoring system
- Configurable source weights

**Output Formats**
- CSV: `data/day-YYYY-MM-DD.csv`
- JSON: `docs/data/latest.json`
- HTML dashboard: `docs/index.html`

### Scoring System

- Per-source metric normalization
- Weighted aggregation
- Segment-based weighting (enterprise/SMB/hobbyist/programming)

### Configuration

- YAML-based source configuration
- Enable/disable collectors
- Adjust weights
- Customize collection parameters

---

## [0.2.0] - 2025-09-08

### Foundation

**Project Structure**
- Modular collector architecture
- Configuration management
- Data aggregation pipeline
- Export functionality

**Data Sources Research**
- Identified key tech trend sources
- API research and documentation
- Rate limit analysis
- Terms of service review

---

## [0.1.0] - 2025-09-01

### Initial Concept

**Project Goals**
- Daily collection of top tech search terms
- Multi-source aggregation
- Enterprise, SMB, and hobbyist coverage
- Programming language trends
- Source attribution and ranking

**Planned Sources**
- Social platforms (HN, Reddit, X)
- Developer communities (Stack Overflow, DEV.to)
- Package ecosystems (npm, PyPI, Homebrew)
- Version control (GitHub, GitLab)
- Blog platforms (Medium)

---

## Version History Summary

- **v0.6.0** (Oct 8, 2025) - Blog Topics Intelligence, Reddit, Google Trends
- **v0.5.0** (Oct 5, 2025) - Clickable URLs, Enhanced Presentation
- **v0.4.2** (Oct 2, 2025) - Critical Threading Fixes
- **v0.4.1** (Sep 28, 2025) - Movers Tracking, PyPI, crates.io
- **v0.4.0** (Sep 24, 2025) - PySide6 GUI, Export to Markdown
- **v0.3.5** (Sep 20, 2025) - HN Algolia, GitHub Trending
- **v0.3.0** (Sep 15, 2025) - Initial Release with Core Collectors
- **v0.2.0** (Sep 8, 2025) - Foundation and Architecture
- **v0.1.0** (Sep 1, 2025) - Initial Concept

---

## Migration Notes

### From v0.5.x to v0.6.0

**New Dependencies**
```bash
uv sync  # Installs praw, pytrends, lxml
```

**Configuration**
- New collectors added to `config/sources.yaml`
- Consider using `sources-testing.yaml` for rapid testing
- Use `./switch-config.sh` to switch between configs

**No Breaking Changes**
- Existing data files fully compatible
- Configuration backward compatible
- All previous features retained

### From v0.4.x to v0.5.0

- No breaking changes
- Enhanced UI elements
- Better data presentation

### From v0.3.x to v0.4.x

- Command-line interface replaced with GUI
- Data storage location changed to `data/` directory
- Configuration now in `config/sources.yaml`

---

## Upgrade Instructions

```bash
cd tech-trends-harvester
git pull
uv sync
./start.sh  # or: uv run python run_app.py
```

Your configuration and historical data are preserved across updates.

---

## Credits

Built with Python, PySide6, and data from multiple open-source and public APIs.

Special thanks to the communities maintaining:
- Hacker News (Y Combinator)
- Reddit API (PRAW)
- Google Trends (pytrends)
- GitHub, Stack Overflow, npm, PyPI, crates.io
- DEV.to, Medium, Lobsters, Homebrew

---

For issues, feature requests, or contributions, please visit the GitHub repository.
