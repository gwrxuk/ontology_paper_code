import json, csv, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import Counter

BLUE, AQUA, YELLOW, GREEN, VIOLET = "#2a78d6", "#1baf7a", "#eda100", "#008300", "#4a3aa7"
INK, MUTED = "#222222", "#777777"
plt.rcParams.update({"font.family": "Helvetica", "font.size": 10, "axes.edgecolor": MUTED,
                     "axes.labelcolor": INK, "text.color": INK, "xtick.color": INK, "ytick.color": INK,
                     "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 200})
FIG = "/Users/junghualiu/case/a2a/information_society/figures"
D = "/Users/junghualiu/case/a2a/information_society/data"

# --- Fig 1: bibliometric trends ---
oa = json.load(open(f"{D}/openalex_trends.json"))
years = list(range(2016, 2026))
series = [("AI agent(s)", "ai_agent", BLUE), ("LLM agent(s)", "llm_agent", AQUA),
          ("agentic AI", "agentic_ai", YELLOW), ("human-machine communication", "human_machine_communication", GREEN)]
fig, ax = plt.subplots(figsize=(7, 4.2))
for name, key, c in series:
    ys = [oa[key]["by_year"][y] if not isinstance(list(oa[key]["by_year"].keys())[0], str) else oa[key]["by_year"][str(y)] for y in years]
    ax.plot(years, ys, color=c, lw=2, marker="o", ms=4, label=name)
    ax.annotate(f"{name}  {ys[-1]:,}", (2025, ys[-1]), xytext=(6, 0), textcoords="offset points",
                va="center", fontsize=8.5, color=c, fontweight="bold")
ax.set_xlim(2016, 2025); ax.set_xticks(years)
ax.set_ylabel("Works per year (title/abstract match)")
ax.grid(axis="y", color="#e5e5e5", lw=0.6)
ax.set_title("Figure 1. The agentic turn in research, 2016–2025 (OpenAlex)", loc="left", fontsize=11, pad=12)
fig.subplots_adjust(right=0.72)
fig.savefig(f"{FIG}/fig1_bibliometrics.png", bbox_inches="tight"); plt.close(fig)

# --- Fig 2: GitHub ecosystem ---
gh = json.load(open(f"{D}/github_repos.json"))
items = sorted(gh.items(), key=lambda kv: kv[1]["stars"])
names = [k.split("/")[1] + f"  ({v['created_at'][:7]})" for k, v in items]
stars = [v["stars"] for k, v in items]
fig, ax = plt.subplots(figsize=(7, 3.6))
bars = ax.barh(names, stars, color=BLUE, height=0.62)
for b, s in zip(bars, stars):
    ax.annotate(f"{s:,}", (b.get_width(), b.get_y() + b.get_height()/2), xytext=(4, 0),
                textcoords="offset points", va="center", fontsize=8.5, color=INK)
ax.set_xlabel("GitHub stars (July 8, 2026)"); ax.set_xlim(0, max(stars)*1.15)
ax.grid(axis="x", color="#e5e5e5", lw=0.6)
ax.set_title("Figure 2. Agent framework and protocol adoption (repository creation month in parentheses)", loc="left", fontsize=10.5, pad=12)
fig.savefig(f"{FIG}/fig2_github.png", bbox_inches="tight"); plt.close(fig)

# --- Fig 3: news frames + mechanisms ---
na = json.load(open(f"{D}/news_analysis.json"))
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.2))
frames = [("Human/org-as-actor", na["frames"]["human/org-as-actor"]),
          ("Machine-as-actor", na["frames"]["machine-as-actor"]),
          ("Explainer/question", na["frames"]["explainer/question"]),
          ("Other", na["frames"]["other"])]
labs = [f[0] for f in frames][::-1]; vals = [f[1] for f in frames][::-1]
b = a1.barh(labs, vals, color=BLUE, height=0.6)
for bb, v in zip(b, vals):
    a1.annotate(f"{v}%", (bb.get_width(), bb.get_y()+bb.get_height()/2), xytext=(4,0), textcoords="offset points", va="center", fontsize=8.5)
a1.set_title("(a) Headline agency frames", loc="left", fontsize=10)
a1.set_xlim(0, 55); a1.grid(axis="x", color="#e5e5e5", lw=0.6)
mech = na["headline_mechanism_mentions"]
mlabs = ["Authorization", "Accountability", "Registration"]; mvals = [mech["authorization"], mech["accountability"], mech["registration"]]
b = a2.barh(mlabs[::-1], mvals[::-1], color=AQUA, height=0.5)
for bb, v in zip(b, mvals[::-1]):
    a2.annotate(f"{v}%", (bb.get_width(), bb.get_y()+bb.get_height()/2), xytext=(4,0), textcoords="offset points", va="center", fontsize=8.5)
a2.set_title("(b) Mechanism vocabulary in headlines", loc="left", fontsize=10)
a2.set_xlim(0, 20); a2.grid(axis="x", color="#e5e5e5", lw=0.6)
fig.suptitle("Figure 3. Agency in news discourse (N = 100 headlines, GDELT, Apr–Jul 2026)", x=0.01, ha="left", fontsize=11)
fig.tight_layout(rect=[0, 0, 1, 0.92])
fig.savefig(f"{FIG}/fig3_news.png", bbox_inches="tight"); plt.close(fig)

# --- Fig 4: YouTube lexicons ---
ya = json.load(open(f"{D}/yt_analysis.json"))
lex = ya["lexicon_per_10k"]; vm = ya["videos_mentioning"]
order = ["protocols", "human_in_loop", "authorization", "registration", "accountability", "autonomy", "delegation"]
pretty = {"protocols": "Protocol names (MCP, A2A)", "human_in_loop": "Human-in-the-loop / oversight",
          "authorization": "Authorization", "registration": "Registration", "accountability": "Accountability",
          "autonomy": "Autonomy", "delegation": "Delegation"}
labs = [pretty[k] for k in order][::-1]
vals = [lex[k]["per_10k"] for k in order][::-1]
pct = [vm[k] for k in order][::-1]
fig, ax = plt.subplots(figsize=(7, 3.8))
b = ax.barh(labs, vals, color=BLUE, height=0.6)
for bb, v, p in zip(b, vals, pct):
    ax.annotate(f"{v:.1f}   ({p}% of videos)", (bb.get_width(), bb.get_y()+bb.get_height()/2),
                xytext=(4,0), textcoords="offset points", va="center", fontsize=8.5)
ax.set_xlabel("Occurrences per 10,000 transcript words"); ax.set_xlim(0, 28)
ax.grid(axis="x", color="#e5e5e5", lw=0.6)
ax.set_title("Figure 4. Agency lexicons in YouTube transcripts (N = 100 videos; 640,462 words)", loc="left", fontsize=10.5, pad=12)
fig.savefig(f"{FIG}/fig4_youtube.png", bbox_inches="tight"); plt.close(fig)
print("figs 1-4 done")
