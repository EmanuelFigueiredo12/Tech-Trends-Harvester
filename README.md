
# Tech Trends Harvester

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PySide6](https://img.shields.io/badge/GUI-PySide6-green.svg)](https://www.qt.io/qt-for-python)

Desktop app that aggregates tech trends from 11+ sources to help you discover blog-worthy topics.

**Find blog-worthy tech topics** from 11+ sources! Get smart, filtered insights into what developers are actually talking about, using, and searching for.

Perfect for **tech bloggers**, **content creators**, and **developers** who want to write about trending topics that attract readers.

## Data Sources

This tool aggregates data from:
- **Hacker News** (Firebase API)
- **Reddit** (PRAW API)
- **GitHub Trending** (HTML parsing)
- **Google Trends** (pytrends)
- **Stack Overflow** (Stack Exchange API)
- **DEV.to** (Forem API)
- **Medium** (RSS feeds)
- **PyPI** (pypistats)
- **npm** (npm registry API)
- **crates.io** (crates.io API)
- **Homebrew** (analytics JSON)
- **Lobsters** (JSON feeds)

## Table of Contents

- [Key Features](#key-features)
- [Quick Start](#quick-start-with-uv-recommended)
- [Usage](#usage)
- [Configuration](#configuration)
- [Data Sources](#data-sources)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Key Features

- **Blog Topics View**: Smart filtering shows only blog-worthy trends
- **11 Data Sources**: Hacker News, GitHub Trending, Stack Overflow, PyPI, npm, DEV.to, Medium, and more
- **Auto-Categorization**: AI/ML, Cloud, Frontend, Backend, etc. - find your niche
- **Multi-Source Validation**: Topics mentioned in multiple sources = more trustworthy
- **Movers Tracking**: Catch trends early with week-over-week momentum
- **Clickable URLs**: Jump directly to discussions and repos
- **Customizable**: Adjust weights, enable/disable sources, add your own filters
- **Export to Markdown**: Generate shareable reports

## Quick Start with uv (Recommended)

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
cd tech-trends-harvester

# Option 1: Use the start script (easiest)
./start.sh

# Option 2: Manual setup
uv sync
uv run python run_app.py

# Optional: Run diagnostics to verify setup
uv run python diagnose.py
```

## Alternative Setup (pip/venv)

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt  # You'll need to generate this from pyproject.toml
python run_app.py
```

## Usage

### Quick Workflow for Blog Research

1. **Launch**: Run `./start.sh` or `uv run python run_app.py`
2. **Refresh**: Click "Refresh Selected" (takes 10-30 seconds)
3. **Find Topics**: Go to **"Blog Topics"** tab (your main view!)
   - Sorted by "blog worthiness" score
   - Filtered to remove noise (common words, system libraries, etc.)
   - Shows category, score, and source count
4. **Research**: Click URLs to read discussions and validate interest
5. **Write**: Pick high-scoring topics from multiple sources and write your blog post!

### All Tabs Explained

- **Blog Topics**: **START HERE** - Only blog-worthy, high-signal terms
- **Aggregated**: All terms ranked by score (unfiltered for deep analysis)
- **By Source**: Individual source data for validation
- **Movers (WoW)**: Week-over-week changes to catch emerging trends
- **Debug**: Status messages and error logs

### What Makes a Good Blog Topic?

- **Score > 2.0**: Definitely worth writing about
- **Sources ≥ 3**: Validated across different communities
- **Category matches your niche**: AI/ML, Cloud, Frontend, etc.
- **URLs show real discussion**: Active conversations = reader interest

## Configuration

Edit `config/sources.yaml` to:
- Enable/disable sources
- Adjust weights for scoring
- Configure parameters (e.g., npm packages to track, GitHub languages, etc.)

## Troubleshooting

### macOS Issues
- If the app is slow on first launch, wait a moment for Qt to 'warm up'.
- Network/SSL issues: Run `/Applications/Python*/Install\ Certificates.command` (Google it..)

### Linux Issues
- Missing Qt platform plugin? Install: `sudo apt-get install libxcb-xinerama0 libxcb-cursor0 libxkbcommon-x11-0`

### Windows Issues
- Missing MSVC runtime? Install "Microsoft Visual C++ Redistributable"

### Source Errors
- **HN Algolia 429**: Rate limited, wait a minute and retry
- **GitHub Trending 0 items**: GitHub may have changed their HTML, usually recovers
- **Timeouts**: Network hiccup, just retry

## Project Structure

```
tech-trends-harvester/
├── config/
│   └── sources.yaml          # Source configuration & weights
├── src/
│   ├── collectors/           # Data source modules
│   │   ├── hackernews.py
│   │   ├── github_trending.py
│   │   ├── stackoverflow_tags.py
│   │   └── ...
│   ├── app/                  # GUI components
│   │   ├── controller.py     # Business logic & threading
│   │   ├── mainwindow.py     # UI layout
│   │   ├── models.py         # Table models
│   │   └── registry.py       # Source registry
│   ├── aggregate.py          # Scoring & aggregation
│   └── util.py               # Utilities
├── data/                     # Output directory
│   ├── last_agg.json        # Latest aggregated results
│   └── history/             # Historical snapshots
├── run_app.py               # Entry point
└── pyproject.toml           # Dependencies & metadata
```

## Adding New Sources

1. Create a new collector in `src/collectors/your_source.py`:
```python
from ..util import now_iso

def fetch(**params):
    # Your data fetching logic
    return [
        {
            "term": "example",
            "kind": "topic",
            "metric_name": "score",
            "metric_value": 100,
            "url": "https://...",
            "source": "your_source",
            "captured_at": now_iso()
        }
    ]
```

2. Register it in `src/app/registry.py`:
```python
from ..collectors import your_source
REGISTRY["your_source"] = SourceSpec("your_source", your_source.fetch, {...})
```

3. Add configuration in `config/sources.yaml`:
```yaml
weights:
  your_source: 1.0

collectors:
  your_source:
    enabled: true
    # your params
```

See `RATE_LIMITS.md` for usage guidelines and ethical considerations.

## Development

### Running Tests

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing
```

### Code Quality

```bash
# Linting
ruff check src/

# Formatting
ruff format src/

# Type checking
mypy src/ --ignore-missing-imports

# Security scanning
bandit -r src/

# Dependency vulnerabilities
safety check
```

### CI/CD

The project uses GitHub Actions for continuous integration:
- Runs on Ubuntu, macOS, and Windows
- Tests Python 3.9 and 3.12
- Includes linting, formatting, type checking, and security scans
- All checks must pass before merging PRs

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Reporting bugs
- Suggesting enhancements
- Adding new data sources
- Code style and standards
- Pull request process

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Built with Python, PySide6, and data from multiple open-source and public APIs.

Special thanks to the communities maintaining the data sources listed above.
