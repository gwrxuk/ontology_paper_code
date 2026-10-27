import json, re, os
from collections import Counter

base = "/Users/junghualiu/case/a2a/information_society/data/yt"
vids = [json.loads(l) for l in open(f"{base}/yt_corpus_year.jsonl")]
texts = {v["id"]: open(f"{base}/subs/{v['id']}.txt").read().lower()
         for v in vids if os.path.exists(f"{base}/subs/{v['id']}.txt")}
total = sum(len(t.split()) for t in texts.values())
print("videos:", len(texts), "| words:", total)

verb_pat = re.compile(r'\bagents?\s+(?:can\s+|will\s+|to\s+|that\s+|which\s+|actually\s+|autonomously\s+)?(\w+)')
STOP = set("that which and or is are was were be been being the a an of in on to it they you we this these those with for as at have has had do does did not don't more so then just its their your our can will would could should may might".split())
verbs = Counter()
for t in texts.values():
    for m in verb_pat.finditer(t):
        w = m.group(1)
        if w not in STOP and len(w) > 2: verbs[w] += 1

LEX = {
 "autonomy": r'\b(autonomous(ly)?|on its own|by itself|without human|self-directed|independently)\b',
 "human_in_loop": r'\b(human in the loop|human-in-the-loop|approval|approve|oversight|supervis\w+|review\w*|check\w*|permission)\b',
 "registration": r'\b(agent card|agentcard|identity|identities|registr\w+|discover\w+|credential\w*|directory)\b',
 "authorization": r'\b(permission\w*|access|authoriz\w+|guardrail\w*|control\w*|security|scope\w*|policy|policies)\b',
 "accountability": r'\b(accountab\w+|audit\w*|log\w*|traceab\w+|liabilit\w+|responsib\w+|compliance)\b',
 "delegation": r'\b(delegate\w*|delegation|hand off|handoff|on your behalf|on behalf of|assign\w*)\b',
 "protocols": r'\b(mcp|model context protocol|a2a|agent2agent|agent-to-agent protocol)\b',
}
lex = {k: {"raw": (c := sum(len(re.findall(p, t)) for t in texts.values())),
           "per_10k": round(c/total*10000, 2)} for k, p in LEX.items()}
vm = {k: sum(1 for t in texts.values() if re.search(p, t)) for k, p in LEX.items()}
views = sorted((v.get("view_count") or 0) for v in vids)
chans = Counter(v.get("channel") for v in vids)
dates = Counter(v["upload_date"][:6] for v in vids)
out = {"n_videos": len(texts), "total_words": total, "median_views": views[len(views)//2],
       "upload_months": dict(sorted(dates.items())),
       "top_agent_verbs": verbs.most_common(20), "lexicon_per_10k": lex,
       "videos_mentioning": vm, "videos_mentioning_pct": {k: round(v/len(texts)*100) for k,v in vm.items()},
       "top_channels": chans.most_common(12)}
json.dump(out, open("/Users/junghualiu/case/a2a/information_society/data/yt_analysis_year.json", "w"), indent=2)
print(json.dumps(out, indent=2))
