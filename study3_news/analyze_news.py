import csv, json, re, random
from collections import Counter

random.seed(42)
rows = list(csv.DictReader(open("/Users/junghualiu/case/a2a/information_society/data/news_corpus.csv")))

# stratified sample of 100 by month
by_month = {}
for r in rows:
    m = r["seendate"][:6]
    by_month.setdefault(m, []).append(r)
months = sorted(by_month)
sample, quota = [], 100
# proportional allocation
total = len(rows)
alloc = {m: max(1, round(len(by_month[m]) / total * 100)) for m in months}
# adjust to exactly 100
while sum(alloc.values()) > 100:
    m = max(alloc, key=lambda k: alloc[k]); alloc[m] -= 1
while sum(alloc.values()) < 100:
    m = max(by_month, key=lambda k: len(by_month[k]) - alloc[k]); alloc[m] += 1
for m in months:
    pool = by_month[m]
    sample.extend(random.sample(pool, min(alloc[m], len(pool))))
sample = sample[:100]

with open("/Users/junghualiu/case/a2a/information_society/data/news_sample_100.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(sample)

AI_SUBJ = re.compile(r'^(the\s+)?(ai\s+agents?|agentic\s+ai|ai|agents?|autonomous\s+agents?|chatbots?|bots?)\b', re.I)
ACTION_VERBS = re.compile(r'\b(transform|reshape|take over|takes? |disrupt|replace|drive|power|change|revolutioni|automate|decide|act|work|help|handle|manage|boost|threaten|outpace|accelerate|redefine|could|will|are|is)\b', re.I)
ORG_SUBJ = re.compile(r'^([A-Z][\w&.\-]*(\s+[A-Z&][\w&.\-]*)*)\s+(launch|unveil|introduc|debut|roll|release|deploy|bring|add|partner|invest|bet|build|expand|acquir|announc|open|integrat|offer|push|plan|report|say|warn|use)', re.I)

def code_headline(t):
    t = t.strip()
    if AI_SUBJ.match(t): return "machine-as-actor"
    if ORG_SUBJ.match(t): return "human/org-as-actor"
    if re.search(r'\b(how|why|what|guide|top \d+|best|vs|explained|\?)\b', t, re.I): return "explainer/question"
    return "other"

frames = Counter(code_headline(r["title"]) for r in sample)
domains = Counter(r["domain"] for r in sample)
countries = Counter(r["sourcecountry"] for r in sample)
months_c = Counter(r["seendate"][:6] for r in sample)

MECH = {
 "registration": r'\b(identit(y|ies)|registr|directory|discover|card|credential|verify|verification|passport|onboard)\w*',
 "authorization": r'\b(permission|access|authoriz|guardrail|control|trust|security|zero.trust|governance|policy|policies|oversight)\w*',
 "accountability": r'\b(accountab|audit|liabilit|responsib|legal|regulat|compliance|risk)\w*',
}
mech_counts = {k: sum(1 for r in sample if re.search(p, r["title"], re.I)) for k, p in MECH.items()}

out = {"n": len(sample), "frames": dict(frames), "top_domains": domains.most_common(12),
       "countries": countries.most_common(10), "by_month": dict(sorted(months_c.items())),
       "headline_mechanism_mentions": mech_counts}
json.dump(out, open("/Users/junghualiu/case/a2a/information_society/data/news_analysis.json", "w"), indent=2)
print(json.dumps(out, indent=2))
# examples per frame
for fr in ["machine-as-actor", "human/org-as-actor"]:
    print("\n==", fr)
    n=0
    for r in sample:
        if code_headline(r["title"]) == fr:
            print(" -", r["title"][:100]); n+=1
        if n>=6: break
