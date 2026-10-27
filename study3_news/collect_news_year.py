import json, urllib.request, urllib.parse, time, csv

def gdelt(query, start, end, maxrec=100, tries=6):
    params = {"query": f'{query} sourcelang:english', "mode": "artlist", "format": "json",
              "maxrecords": str(maxrec), "startdatetime": start, "enddatetime": end, "sort": "hybridrel"}
    url = "https://api.gdeltproject.org/api/v2/doc/doc?" + urllib.parse.urlencode(params)
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "academic-research"})
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode("utf-8", "ignore")).get("articles", [])
        except Exception as ex:
            print("  retry", i+1, ex, flush=True); time.sleep(40)
    return []

q = '("agentic AI" OR "AI agents")'
months = [("2025",m) for m in range(7,13)] + [("2026",m) for m in range(1,8)]
seen, rows = set(), []
for y, m in months:
    s = f"{y}{m:02d}01000000"
    if y=="2026" and m==7: e = "20260708235959"
    else:
        ny, nm = (int(y)+1, 1) if m==12 else (int(y), m+1)
        e = f"{ny}{nm:02d}01000000"
    arts = gdelt(q, s, e, 100)
    n0 = len(rows)
    for a in arts:
        key = a.get("title","").strip().lower()
        u = a.get("url","")
        if not key or key in seen or not u: continue
        seen.add(key)
        rows.append({"title": a.get("title","").strip(), "url": u, "domain": a.get("domain",""),
                     "seendate": a.get("seendate",""), "sourcecountry": a.get("sourcecountry","")})
    print(f"{y}-{m:02d}: {len(arts)} fetched, {len(rows)-n0} new unique (total {len(rows)})", flush=True)
    time.sleep(12)

with open("/Users/junghualiu/case/a2a/information_society/data/news_corpus_year.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["title","url","domain","seendate","sourcecountry"])
    w.writeheader(); w.writerows(rows)
print("YEAR CORPUS TOTAL:", len(rows))
