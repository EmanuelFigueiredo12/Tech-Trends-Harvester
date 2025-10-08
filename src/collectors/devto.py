
import requests
from ..util import now_iso, tokenize_title

BASE = "https://dev.to/api/articles"

def fetch(per_page=80, pages=1):
    out = []
    for page in range(1, pages+1):
        try:
            items = requests.get(BASE, params={"per_page": per_page, "page": page}, timeout=20).json()
        except Exception:
            items = []
        for it in items:
            title = it.get("title") or ""
            url = it.get("url") or it.get("canonical_url") or ""
            metric = (it.get("public_reactions_count") or 0) + (it.get("comments_count") or 0)
            for term in tokenize_title(title):
                out.append({"term":term,"kind":"topic","metric_name":"devto_popularity","metric_value":metric,"url":url,"source":"devto","captured_at":now_iso(),"raw_title":title})
    return out
