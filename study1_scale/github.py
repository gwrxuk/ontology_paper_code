import json, urllib.request

repos = ["a2aproject/A2A", "modelcontextprotocol/modelcontextprotocol",
         "modelcontextprotocol/servers", "microsoft/autogen", "crewAIInc/crewAI",
         "langchain-ai/langgraph", "openai/openai-agents-python"]
out = {}
for r in repos:
    req = urllib.request.Request(f"https://api.github.com/repos/{r}",
                                 headers={"Accept": "application/vnd.github+json",
                                          "User-Agent": "research-script"})
    try:
        with urllib.request.urlopen(req) as resp:
            d = json.load(resp)
        out[r] = {"stars": d["stargazers_count"], "forks": d["forks_count"],
                  "created_at": d["created_at"], "description": d["description"],
                  "open_issues": d["open_issues_count"]}
        print(r, out[r]["stars"], "stars, created", out[r]["created_at"])
    except Exception as e:
        print(r, "ERROR", e)
with open("/Users/junghualiu/case/a2a/information_society/data/github_repos.json", "w") as f:
    json.dump(out, f, indent=2)
