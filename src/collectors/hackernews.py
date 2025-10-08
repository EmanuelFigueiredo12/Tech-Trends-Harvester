
import requests, time
from ..util import now_iso, tokenize_title

API = "https://hacker-news.firebaseio.com/v0"

def fetch(top_n=150):
    out, ids, seen = [], [], set()
    for endpoint in ["topstories","newstories"]:
        try:
            resp = requests.get(f"{API}/{endpoint}.json", timeout=20)
            resp.raise_for_status()
            ids.extend(resp.json()[:top_n])
        except Exception as e:
            print(f"HN: Failed to fetch {endpoint}: {e}")
            continue
    
    if not ids:
        print("HN: No story IDs retrieved")
        return []
    
    for i in ids[:top_n]:
        if i in seen: continue
        seen.add(i)
        try:
            resp = requests.get(f"{API}/item/{i}.json", timeout=10)
            resp.raise_for_status()
            it = resp.json() or {}
            title = it.get("title") or ""
            if not title:
                continue
            score = it.get("score", 0)
            url = f"https://news.ycombinator.com/item?id={i}"
            for term in tokenize_title(title):
                out.append({"term":term,"kind":"topic","metric_name":"hn_points","metric_value":score,"url":url,"source":"hackernews","captured_at":now_iso(),"raw_title":title})
        except Exception as e:
            continue
        time.sleep(0.03)
    return out
