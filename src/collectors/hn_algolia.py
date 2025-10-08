
import time, requests, datetime as dt
from ..util import now_iso, tokenize_title, USER_AGENT

BASE = "https://hn.algolia.com/api/v1/search_by_date"

def fetch(hours_back=48, min_points=10, hits_per_page=200):
    out = []
    cutoff = int((dt.datetime.utcnow() - dt.timedelta(hours=hours_back)).timestamp())
    params = {"tags":"story","numericFilters":[f"created_at_i>{cutoff}", f"points>{min_points}"],"hitsPerPage":hits_per_page,"page":0}
    headers = {"User-Agent": USER_AGENT}
    for page in range(0,3):
        params["page"] = page
        try:
            resp = requests.get(BASE, params=params, headers=headers, timeout=20)
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.RequestException as e:
            print(f"HN Algolia: Request failed on page {page}: {e}")
            break
        except Exception as e:
            print(f"HN Algolia: Unexpected error on page {page}: {e}")
            break
        hits = data.get("hits", [])
        if not hits: 
            break
        now = int(time.time())
        for h in hits:
            title = h.get("title") or ""
            if not title:
                continue
            url = h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}"
            points = h.get("points") or 0
            created = int(h.get('created_at_i') or cutoff)
            hours_old = max(1.0, (now - created)/3600.0)
            hot = points / hours_old
            for term in tokenize_title(title):
                out.append({"term":term,"kind":"topic","metric_name":"hn_algolia_hotness","metric_value":hot,"url":url,"source":"hn_algolia","captured_at":now_iso(),"raw_title":title})
    return out
