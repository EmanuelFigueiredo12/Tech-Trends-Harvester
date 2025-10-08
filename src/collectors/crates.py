
import requests
from ..util import now_iso

BASE = "https://crates.io/api/v1/crates"

def fetch(per_page=100):
    out = []
    try:
        # Sort by total downloads (all-time), not recent downloads
        data = requests.get(BASE, params={"page":1, "per_page": per_page, "sort":"downloads"}, timeout=30).json()
        crates = data.get("crates", [])
    except Exception:
        crates = []
    for c in crates:
        name = c.get("id","")
        downloads = int(c.get("downloads") or 0)
        url = f"https://crates.io/crates/{name}"
        out.append({"term":name.lower(),"kind":"package","metric_name":"crates_downloads","metric_value":downloads,"url":url,"source":"crates","captured_at":now_iso()})
    return out
