import json, urllib.request, urllib.parse, time, csv

def gdelt_once(query, start, end, maxrec=250, tries=8):
    params = {
        "query": f'{query} sourcelang:english',
        "mode": "artlist", "format": "json", "maxrecords": str(maxrec),
        "startdatetime": start, "enddatetime": end, "sort": "hybridrel",
    }
    url = "https://api.gdeltproject.org/api/v2/doc/doc?" + urllib.parse.urlencode(params)
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "academic-research gwrx2005@gmail.com"})
            with urllib.request.urlopen(req, timeout=90) as r:
                txt = r.read().decode("utf-8", "ignore")
            return json.loads(txt).get("articles", [])
        except Exception as ex:
            print("  retry", i+1, ex, flush=True); time.sleep(45)
    return []

q = '("agentic AI" OR "AI agents")'
arts = gdelt_once(q, "20250101000000", "20260707235959")
print("fetched:", len(arts), flush=True)
seen, rows = set(), []
for a in arts:
    key = a.get("title", "").strip().lower()
    u = a.get("url", "")
    if not key or key in seen or not u: continue
    seen.add(key)
    rows.append({"title": a.get("title","").strip(),
                 "url": u, "domain": a.get("domain",""),
                 "seendate": a.get("seendate",""),
                 "sourcecountry": a.get("sourcecountry","")})

with open("/Users/junghualiu/case/a2a/information_society/data/news_corpus.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["title","url","domain","seendate","sourcecountry"])
    w.writeheader(); w.writerows(rows)
print("TOTAL unique articles saved:", len(rows))
