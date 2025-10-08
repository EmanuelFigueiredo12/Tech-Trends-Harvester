
import requests
from ..util import now_iso

API_PYPISTATS = "https://pypistats.org/api/packages/{pkg}/recent"
API_PEPY = "https://pepy.tech/api/v2/projects/{pkg}"

def _pypistats_week(pkg):
    try:
        r = requests.get(API_PYPISTATS.format(pkg=pkg), timeout=20)
        r.raise_for_status()
        data = r.json()
        return int(data.get("data", {}).get("last_week", 0))
    except Exception:
        return None

def _pepy_week(pkg):
    try:
        r = requests.get(API_PEPY.format(pkg=pkg), timeout=20)
        r.raise_for_status()
        data = r.json()
        return int((data.get("downloads") or {}).get("last_week", 0))
    except Exception:
        return None

def fetch(packages):
    out = []
    for p in packages:
        week = _pypistats_week(p)
        if week is None:
            week = _pepy_week(p) or 0
        url = f"https://pypi.org/project/{p}/"
        out.append({"term":p.lower(),"kind":"package","metric_name":"pypi_downloads_week","metric_value":week,"url":url,"source":"pypi","captured_at":now_iso()})
    return out
