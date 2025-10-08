"""
Reddit Post Collector - Tracks full post titles from tech subreddits.

This is MUCH better than individual words because:
- Post titles ARE blog topic ideas
- They're validated by community (upvotes/comments)
- They show what people are actually interested in
"""

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
    
    try:
        # Use read-only Reddit instance (no auth needed!)
        reddit = praw.Reddit(
            client_id="tech-trends-harvester",  # Dummy ID for read-only
            client_secret=None,
            user_agent=USER_AGENT  # Standard browser user-agent
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
                print(f"Reddit: Failed to fetch r/{subreddit_name}: {e}")
                continue
                
    except Exception as e:
        print(f"Reddit: Failed to initialize: {e}")
        return []
    
    return out

