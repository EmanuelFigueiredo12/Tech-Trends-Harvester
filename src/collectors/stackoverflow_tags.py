
import requests
from ..util import now_iso

API = "https://api.stackexchange.com/2.3/tags"

def fetch(site="stackoverflow", top_n=200):
    out = []
    page = 1
    pagesize = 100
    got = 0
    while got < top_n and page < 10:
        try:
            data = requests.get(API, params={"order":"desc","sort":"popular","site":site,"page":page,"pagesize":pagesize}, timeout=20).json()
        except Exception:
            break
        for tag in data.get("items", []):
            name = tag.get("name","")
            count = tag.get("count",0)
            out.append({"term":name.lower(),"kind":"tag","metric_name":"so_tag_count","metric_value":count,"url":f"https://stackoverflow.com/questions/tagged/{name}","source":"stackoverflow_tags","captured_at":now_iso()})
            got += 1
            if got >= top_n: break
        if not data.get("has_more"): break
        page += 1
    return out
