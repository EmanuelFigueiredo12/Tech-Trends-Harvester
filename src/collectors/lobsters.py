
import requests
from ..util import now_iso, tokenize_title

def fetch(endpoint="https://lobste.rs/hottest.json", top_n=150):
    out = []
    try:
        items = requests.get(endpoint, timeout=20).json()[:top_n]
    except Exception:
        return out
    for it in items:
        title = it.get("title","")
        url = it.get("short_id_url") or it.get("url") or "https://lobste.rs/"
        score = it.get("score",0)
        for term in tokenize_title(title):
            out.append({"term":term,"kind":"topic","metric_name":"lobsters_score","metric_value":score,"url":url,"source":"lobsters","captured_at":now_iso(),"raw_title":title})
    return out
