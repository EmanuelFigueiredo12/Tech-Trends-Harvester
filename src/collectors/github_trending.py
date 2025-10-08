
import requests, re
from bs4 import BeautifulSoup
from ..util import now_iso, USER_AGENT

BASE = "https://github.com/trending"

def fetch(since="weekly", languages=None):
    out = []
    headers = {"User-Agent": USER_AGENT}
    langs = languages or [None]
    for lang in langs:
        url = f"{BASE}/{lang}?since={since}" if lang else f"{BASE}?since={since}"
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            resp.raise_for_status()
            html = resp.text
        except requests.exceptions.RequestException as e:
            print(f"GitHub Trending: Request failed for {lang or 'all'}: {e}")
            continue
        except Exception as e:
            print(f"GitHub Trending: Unexpected error for {lang or 'all'}: {e}")
            continue
        
        try:
            soup = BeautifulSoup(html, "html.parser")
            for row in soup.select(".Box .Box-row"):
                a = row.select_one("h2 a")
                if not a: continue
                href = a.get("href","").lstrip("/")
                if not href:
                    continue
                repo_url = f"https://github.com/{href}"
                cand = row.find(string=lambda s: isinstance(s, str) and "stars this" in s)
                stars_week = 0
                if cand:
                    m = re.search(r"(\d[\d,]*)\s+stars this", cand, flags=re.I)
                    if m: stars_week = int(m.group(1).replace(",",""))
                out.append({"term":href.lower(),"kind":"repo","metric_name":"github_stars_week","metric_value":stars_week,"url":repo_url,"source":"github_trending","captured_at":now_iso()})
        except Exception as e:
            print(f"GitHub Trending: Failed to parse HTML: {e}")
            continue
    return out
