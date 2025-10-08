
import feedparser
from ..util import now_iso, tokenize_title

def topic_feed(tag: str):
    return f"https://medium.com/feed/tag/{tag}"

def fetch(topics):
    out = []
    for t in topics:
        url = topic_feed(t)
        try:
            feed = feedparser.parse(url)
        except Exception:
            continue
        for entry in feed.entries[:50]:
            title = entry.get('title','')
            link = entry.get('link', url)
            for term in tokenize_title(title):
                out.append({"term":term,"kind":"topic","metric_name":"medium_presence","metric_value":1,"url":link,"source":"medium","captured_at":now_iso(),"raw_title":title})
    return out
