import csv, json, re, random, sys
from collections import Counter
sys.path.insert(0, "/Users/junghualiu/case/a2a/information_society/data")
from classifier_v2 import code_v2

random.seed(42)
rows = list(csv.DictReader(open("news_corpus_year.csv")))
print("year corpus unique articles:", len(rows))

by_month = {}
for r in rows:
    by_month.setdefault(r["seendate"][:6], []).append(r)
sample = []
for m in sorted(by_month):
    pool = by_month[m]
    sample.extend(random.sample(pool, min(20, len(pool))))
print("stratified sample:", len(sample), "| months:", {m: min(20, len(by_month[m])) for m in sorted(by_month)})

with open("news_sample_year.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(sample)

frames = Counter(code_v2(r["title"]) for r in sample)
MECH = {
 "registration": r'\b(identit(y|ies)|registr|directory|discover|card|credential|verify|verification|passport|onboard)\w*',
 "authorization": r'\b(permission|access|authoriz|guardrail|control|trust|security|zero.trust|governance|policy|policies|oversight)\w*',
 "accountability": r'\b(accountab|audit|liabilit|responsib|legal|regulat|compliance|risk)\w*',
}
mech = {k: sum(1 for r in sample if re.search(p, r["title"], re.I)) for k, p in MECH.items()}
domains = Counter(r["domain"] for r in sample)
countries = Counter(r["sourcecountry"] for r in sample)
n = len(sample)
out = {"corpus_unique": len(rows), "n_sample": n,
       "frames_v2": dict(frames), "frames_v2_pct": {k: round(v/n*100,1) for k,v in frames.items()},
       "mechanisms": mech, "mechanisms_pct": {k: round(v/n*100,1) for k,v in mech.items()},
       "top_domains": domains.most_common(12), "countries": countries.most_common(8),
       "by_month_sample": Counter(r["seendate"][:6] for r in sample)}
json.dump(out, open("news_analysis_year.json", "w"), indent=2, default=dict)
print(json.dumps(out, indent=2, default=dict))

# validation subsample for hand-coding
random.seed(21)
val = random.sample(sample, 60)
json.dump([{"title": r["title"], "v2": code_v2(r["title"])} for r in val], open("validation_60_year.json", "w"), indent=2)
print("\n=== 60 validation headlines (hand-code these) ===")
for i, r in enumerate(val, 1):
    print(f"{i:2}. {r['title'][:110]}")
