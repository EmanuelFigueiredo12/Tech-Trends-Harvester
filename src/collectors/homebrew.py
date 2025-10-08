
import requests
from ..util import now_iso

BASE = "https://formulae.brew.sh/api/analytics/install-on-request/homebrew-core/{window}.json"

def fetch(window="30d"):
    out = []
    try:
        data = requests.get(BASE.format(window=window), timeout=30).json()
        items = data.get("items", [])
    except Exception:
        items = []
    for it in items[:500]:
        formula = it.get("formula") or it.get("cask") or ""
        count = it.get("count",0)
        url = f"https://formulae.brew.sh/formula/{formula}"
        out.append({"term":formula.lower(),"kind":"package","metric_name":"brew_installs","metric_value":count,"url":url,"source":"homebrew","captured_at":now_iso()})
    return out
