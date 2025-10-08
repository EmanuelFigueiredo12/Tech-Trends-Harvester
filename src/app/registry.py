
from dataclasses import dataclass
from typing import Callable, Dict, Any
from ..collectors import (
    hackernews, hn_algolia, github_trending, lobsters, devto, medium_rss,
    stackoverflow_tags, homebrew, npm_downloads, pypi, crates,
    reddit_posts, google_trends
)

@dataclass
class SourceSpec:
    key: str
    fetch_fn: Callable[..., list]
    config_keys: Dict[str, Any]

REGISTRY = {
    # NEW: High-value sources with full phrases and search data
    "reddit_posts":     SourceSpec("reddit_posts", reddit_posts.fetch, {"subreddits": list, "time_filter": str, "limit": int, "min_score": int}),
    "google_trends":    SourceSpec("google_trends", google_trends.fetch, {"keywords": list, "timeframe": str, "geo": str}),
    
    # Original sources (still useful)
    "hackernews":       SourceSpec("hackernews", hackernews.fetch, {"top_n": int}),
    "hn_algolia":       SourceSpec("hn_algolia", hn_algolia.fetch, {"hours_back": int, "min_points": int, "hits_per_page": int}),
    "github_trending":  SourceSpec("github_trending", github_trending.fetch, {"since": str, "languages": list}),
    "lobsters":         SourceSpec("lobsters", lobsters.fetch, {"endpoint": str, "top_n": int}),
    "devto":            SourceSpec("devto", devto.fetch, {"per_page": int, "pages": int}),
    "medium":           SourceSpec("medium", medium_rss.fetch, {"topics": list}),
    "stackoverflow_tags": SourceSpec("stackoverflow_tags", stackoverflow_tags.fetch, {"site": str, "top_n": int}),
    "homebrew":         SourceSpec("homebrew", homebrew.fetch, {"window": str}),
    "npm":              SourceSpec("npm", npm_downloads.fetch, {"packages": list}),
    "pypi":             SourceSpec("pypi", pypi.fetch, {"packages": list}),
    "crates":           SourceSpec("crates", crates.fetch, {"per_page": int}),
}
