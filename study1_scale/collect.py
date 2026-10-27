import json, urllib.request, urllib.parse, time

MAILTO = "mailto=research@example.org"
def oa_group_by_year(query, extra=""):
    q = urllib.parse.quote(query)
    url = (f"https://api.openalex.org/works?filter=title_and_abstract.search:{q},"
           f"from_publication_date:2016-01-01,to_publication_date:2025-12-31{extra}"
           f"&group_by=publication_year&{MAILTO}")
    with urllib.request.urlopen(url) as r:
        d = json.load(r)
    years = {int(g["key"]): g["count"] for g in d["group_by"] if g["key"].isdigit()}
    return {y: years.get(y, 0) for y in range(2016, 2026)}, d["meta"]["count"]

terms = {
    "human_machine_communication": '"human-machine communication"',
    "ai_agent": '"AI agent" OR "AI agents"',
    "agentic_ai": '"agentic AI"',
    "llm_agent": '"LLM agent" OR "LLM agents" OR "large language model agent" OR "large language model agents"',
    "multi_agent_llm": '"multi-agent" AND "large language model"',
    "ontology_agent": '"ontology" AND "agent"',
}
out = {}
for k, q in terms.items():
    series, total = oa_group_by_year(q)
    out[k] = {"query": q, "total_2016_2025": total, "by_year": series}
    print(k, total, series)
    time.sleep(0.3)

with open("/Users/junghualiu/case/a2a/information_society/data/openalex_trends.json", "w") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print("saved")
