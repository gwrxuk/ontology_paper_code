import json, subprocess, os, glob, time

base = "/Users/junghualiu/case/a2a/information_society/data/yt"
seen, vids = set(), []
for f in sorted(glob.glob(f"{base}/yt_search_*.jsonl")):
    for line in open(f):
        d = json.loads(line)
        if d["id"] and d["id"] not in seen:
            seen.add(d["id"]); vids.append(d)
print("candidates:", len(vids), flush=True)

datecache = {}
dc_path = f"{base}/upload_dates.json"
if os.path.exists(dc_path): datecache = json.load(open(dc_path))

def get_date(vid):
    if vid in datecache: return datecache[vid]
    try:
        r = subprocess.run(["yt-dlp", "--skip-download", "--print", "%(upload_date)s",
                            "--no-warnings", "--quiet", f"https://www.youtube.com/watch?v={vid}"],
                           capture_output=True, timeout=60, text=True)
        d = r.stdout.strip().split("\n")[0]
        datecache[vid] = d if len(d) == 8 and d.isdigit() else None
    except Exception:
        datecache[vid] = None
    return datecache[vid]

def json3_to_text(path):
    d = json.load(open(path))
    out = []
    for ev in d.get("events", []):
        for seg in ev.get("segs", []) or []:
            s = seg.get("utf8", "")
            if s and s != "\n": out.append(s)
    return "".join(out).replace("\n", " ").strip()

LO, HI = "20250701", "20260709"
ok = []
for i, v in enumerate(vids):
    if len(ok) >= 150: break
    vid = v["id"]
    d = get_date(vid)
    if i % 20 == 0:
        json.dump(datecache, open(dc_path, "w"))
        print(f"[{i}/{len(vids)}] dated, {len(ok)} in corpus", flush=True)
    if not d or not (LO <= d <= HI): continue
    v["upload_date"] = d
    txtpath = f"{base}/subs/{vid}.txt"
    if os.path.exists(txtpath):
        v["transcript_words"] = len(open(txtpath).read().split())
        if v["transcript_words"] >= 100: ok.append(v)
        continue
    try:
        subprocess.run(["yt-dlp", "--skip-download", "--write-auto-subs", "--write-subs",
                        "--sub-langs", "en,en-US,en-GB,en-orig", "--sub-format", "json3",
                        "-o", f"{base}/subs/{vid}", "--no-warnings", "--quiet",
                        f"https://www.youtube.com/watch?v={vid}"], capture_output=True, timeout=90)
        cand = glob.glob(f"{base}/subs/{vid}*.json3")
        if cand:
            text = json3_to_text(cand[0])
            if len(text.split()) >= 100:
                open(txtpath, "w").write(text)
                v["transcript_words"] = len(text.split())
                ok.append(v)
                print(f"[corpus {len(ok)}] +{vid} ({d}) {v['title'][:55]}", flush=True)
            for c in cand: os.remove(c)
    except Exception as e:
        print("skip", vid, e, flush=True)
    time.sleep(0.8)

json.dump(datecache, open(dc_path, "w"))
with open(f"{base}/yt_corpus_year.jsonl", "w") as f:
    for v in ok: f.write(json.dumps(v) + "\n")
print("YEAR CORPUS:", len(ok), "videos")
