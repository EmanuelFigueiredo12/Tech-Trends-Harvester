"""
Google Trends Collector - Get ACTUAL search volume signals.

This tells you if people are SEARCHING for topics, not just discussing them.
This is the single most important signal for blog topics!
"""

from pytrends.request import TrendReq
import time
from ..util import now_iso

def fetch(keywords=None, timeframe="today 3-m", geo=""):
    """
    Fetch Google Trends data for keywords.
    
    Args:
        keywords: List of keywords to check (max 5 at a time)
        timeframe: "today 1-m", "today 3-m", "today 12-m", "today 5-y"
        geo: Country code (e.g., "US", "GB", "") for worldwide
    
    Returns:
        List of dicts with search interest data
    """
    if keywords is None:
        # Default: Check popular tech topics
        keywords = [
            "cursor ai",
            "anthropic claude", 
            "supabase",
            "bun javascript",
            "astro framework",
        ]
    
    out = []
    
    try:
        # Initialize pytrends (uses unofficial API)
        pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25))
        
        # Process in batches of 5 (Google Trends limit)
        for i in range(0, len(keywords), 5):
            batch = keywords[i:i+5]
            
            try:
                # Build payload
                pytrends.build_payload(batch, cat=0, timeframe=timeframe, geo=geo, gprop='')
                
                # Get interest over time
                interest_df = pytrends.interest_over_time()
                
                if not interest_df.empty:
                    # Get average interest for each keyword
                    for keyword in batch:
                        if keyword in interest_df.columns:
                            avg_interest = interest_df[keyword].mean()
                            recent_interest = interest_df[keyword].tail(4).mean()  # Last month
                            trend = "rising" if recent_interest > avg_interest else "stable"
                            
                            # Only include if there's actual search volume
                            if avg_interest > 0:
                                out.append({
                                    "term": keyword.lower(),
                                    "kind": "search_query",
                                    "metric_name": "search_interest",
                                    "metric_value": int(avg_interest),
                                    "url": f"https://trends.google.com/trends/explore?q={keyword.replace(' ', '+')}",
                                    "source": "google_trends",
                                    "captured_at": now_iso(),
                                    "trend_direction": trend,
                                    "recent_interest": int(recent_interest),
                                })
                
                # Get related queries (GOLD MINE!)
                try:
                    related = pytrends.related_queries()
                    for keyword in batch:
                        if keyword in related and related[keyword]['rising'] is not None:
                            rising_queries = related[keyword]['rising']
                            
                            # Add top 5 rising queries
                            for _, row in rising_queries.head(5).iterrows():
                                query = row['query']
                                value = row['value']  # Could be percentage or "Breakout"
                                
                                # Handle "Breakout" queries (new/explosive growth)
                                if value == "Breakout":
                                    metric_value = 1000  # High score for breakout terms
                                else:
                                    metric_value = int(value) if isinstance(value, (int, float)) else 100
                                
                                out.append({
                                    "term": query.lower(),
                                    "kind": "rising_query",
                                    "metric_name": "search_growth",
                                    "metric_value": metric_value,
                                    "url": f"https://trends.google.com/trends/explore?q={query.replace(' ', '+')}",
                                    "source": "google_trends",
                                    "captured_at": now_iso(),
                                    "parent_keyword": keyword,
                                    "trend_direction": "rising",
                                })
                except Exception as e:
                    print(f"Google Trends: Failed to get related queries for {keyword}: {e}")
                
                # Rate limit: Google Trends will block if you go too fast
                time.sleep(2)
                
            except Exception as e:
                print(f"Google Trends: Failed batch {batch}: {e}")
                continue
                
    except Exception as e:
        print(f"Google Trends: Failed to initialize: {e}")
        return []
    
    return out

