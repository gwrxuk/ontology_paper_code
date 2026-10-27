import json, subprocess, os, glob, time

base = "/Users/junghualiu/case/a2a/information_society/data/yt"
os.makedirs(f"{base}/subs", exist_ok=True)

# dedupe candidates
seen, vids = set(), []
for f in sorted(glob.glob(f"{base}/yt_search_*.jsonl")):
    for line in open(f):
        d = json.loads(line)
        if d["id"] and d["id"] not in seen:
            seen.add(d["id"]); vids.append(d)
print("candidates:", len(vids), flush=True)

def json3_to_text(path):
    d = json.load(open(path))
    words = []
    for ev in d.get("events", []):
        for seg in ev.get("segs", []) or []:
            t = seg.get("utf8", "")
            if t and t != "\n": words.append(t)
    return "".join(words).replace("\n", " ").strip()

ok = []
for v in vids:
    if len(ok) >= 100: break
    vid = v["id"]
    txtpath = f"{base}/subs/{vid}.txt"
    if os.path.exists(txtpath):
        ok.append(v); continue
    try:
        r = subprocess.run(
            ["yt-dlp", "--skip-download", "--write-auto-subs", "--write-subs",
             "--sub-langs", "en,en-US,en-GB,en-orig", "--sub-format", "json3",
             "-o", f"{base}/subs/{vid}", "--no-warnings", "--quiet",
             f"https://www.youtube.com/watch?v={vid}"],
            capture_output=True, timeout=90)
        cand = glob.glob(f"{base}/subs/{vid}*.json3")
        if cand:
            text = json3_to_text(cand[0])
            if len(text.split()) >= 100:
                open(txtpath, "w").write(text)
                v["transcript_words"] = len(text.split())
                ok.append(v)
                print(f"[{len(ok)}/100] {vid} {v['title'][:60]}", flush=True)
            for c in cand: os.remove(c)
    except Exception as e:
        print("skip", vid, e, flush=True)
    time.sleep(1.0)

with open(f"{base}/yt_corpus.jsonl", "w") as f:
    for v in ok: f.write(json.dumps(v) + "\n")
print("FINAL corpus size:", len(ok))
