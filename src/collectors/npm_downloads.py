
import requests
from ..util import now_iso

API = "https://api.npmjs.org/downloads/point/last-week/{pkg}"

def fetch(packages):
    out = []
    for p in packages:
        dl = 0
        try:
            dl = int(requests.get(API.format(pkg=p), timeout=20).json().get('downloads',0))
        except Exception:
            dl = 0
        url = f"https://www.npmjs.com/package/{p}"
        out.append({"term":p.lower(),"kind":"package","metric_name":"npm_downloads_week","metric_value":dl,"url":url,"source":"npm","captured_at":now_iso()})
    return out
