"""
Reddit Post Collector - Tracks full post titles from tech subreddits.

This is MUCH better than individual words because:
- Post titles ARE blog topic ideas
- They're validated by community (upvotes/comments)
- They show what people are actually interested in
"""

import os

import praw

from ..util import now_iso, USER_AGENT

def fetch(subreddits=None, time_filter="week", limit=50, min_score=50):
    """
    Fetch top posts from tech subreddits.
    
    Args:
        subreddits: List of subreddit names (without r/)
        time_filter: "day", "week", "month", "year", "all"
        limit: Number of posts per subreddit
        min_score: Minimum upvotes to include
    
    Returns:
        List of dicts with full post titles (actual blog topics!)
    """
    if subreddits is None:
        subreddits = [
            "programming",
            "webdev", 
            "learnprogramming",
            "devops",
            "javascript",
            "python",
            "rust",
            "golang",
            "MachineLearning",
            "artificial",
            "kubernetes",
        ]
    
    out = []
    
    # Check for Reddit credentials (required as of 2025)
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT", USER_AGENT)
    
    if not client_id or not client_secret:
        raise Exception(
            "Missing Reddit API credentials! "
            "Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET in .env file. "
            "See API_SETUP.md for setup instructions, or disable reddit_posts in config/sources.yaml"
        )
    
    try:
        # Reddit now requires authentication even for read-only access
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        
        for subreddit_name in subreddits:
            try:
                subreddit = reddit.subreddit(subreddit_name)
                
                # Get top posts for the time period
                for post in subreddit.top(time_filter=time_filter, limit=limit):
                    # Filter by score (upvotes)
                    if post.score < min_score:
                        continue
                    
                    # Skip stickied posts (usually meta/rules)
                    if post.stickied:
                        continue
                    
                    # Calculate engagement score
                    engagement = post.score + (post.num_comments * 2)  # Comments are worth 2x
                    
                    # The post title IS the blog topic!
                    out.append({
                        "term": post.title.lower(),  # Full title, not individual words
                        "kind": "discussion",
                        "metric_name": "reddit_engagement",
                        "metric_value": engagement,
                        "url": f"https://reddit.com{post.permalink}",
                        "source": "reddit_posts",
                        "captured_at": now_iso(),
                        "subreddit": subreddit_name,
                        "upvotes": post.score,
                        "comments": post.num_comments,
                    })
                    
            except Exception as e:
                error_msg = str(e)
                # If it's an auth error, raise it so user sees it
                if "401" in error_msg or "403" in error_msg or "Unauthorized" in error_msg or "credentials" in error_msg.lower():
                    raise Exception(f"Reddit authentication failed: {e}. Check your REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET in .env file.")
                print(f"Reddit: Failed to fetch r/{subreddit_name}: {e}")
                continue
                
    except Exception as e:
        error_msg = str(e)
        # Check for common auth errors
        if "401" in error_msg or "403" in error_msg or "Unauthorized" in error_msg or "credentials" in error_msg.lower():
            raise Exception(f"Reddit authentication failed: {e}. Verify your credentials in .env file are correct.")
        # Other errors - raise them too so user can see
        raise Exception(f"Reddit error: {e}")
    
    return out

