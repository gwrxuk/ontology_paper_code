import json, urllib.request, urllib.parse, time, csv

def gdelt(query, start, end, maxrec=100, tries=10):
    params = {"query": f'{query} sourcelang:english', "mode": "artlist", "format": "json",
              "maxrecords": str(maxrec), "startdatetime": start, "enddatetime": end, "sort": "hybridrel"}
    url = "https://api.gdeltproject.org/api/v2/doc/doc?" + urllib.parse.urlencode(params)
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "academic-research"})
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode("utf-8", "ignore")).get("articles", [])
        except Exception as ex:
            print("  retry", i+1, ex, flush=True); time.sleep(75)
    return []

path = "/Users/junghualiu/case/a2a/information_society/data/news_corpus_year.csv"
rows = list(csv.DictReader(open(path)))
seen = {r["title"].strip().lower() for r in rows}
q = '("agentic AI" OR "AI agents")'
windows = [("20251101000000","20251201000000","2025-11"), ("20251201000000","20260101000000","2025-12"),
           ("20260701000000","20260708235959","2026-07")]
for s, e, lab in windows:
    arts = gdelt(q, s, e, 100)
    n0 = len(rows)
    for a in arts:
        key = a.get("title","").strip().lower()
        u = a.get("url","")
        if not key or key in seen or not u: continue
        seen.add(key)
        rows.append({"title": a.get("title","").strip(), "url": u, "domain": a.get("domain",""),
                     "seendate": a.get("seendate",""), "sourcecountry": a.get("sourcecountry","")})
    print(f"{lab}: +{len(rows)-n0} (total {len(rows)})", flush=True)
    time.sleep(30)

with open(path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["title","url","domain","seendate","sourcecountry"])
    w.writeheader(); w.writerows(rows)
print("FILLED TOTAL:", len(rows))
