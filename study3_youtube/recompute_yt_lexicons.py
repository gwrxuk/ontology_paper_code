"""Recompute the final YouTube lexicon table and Figure 4 from the archived corpus.

The final specification removes broad `check*`, `review*`, and `permission*`
matches from the human-oversight lexicon.  It also replaces `log*` in the
accountability lexicon with inflected logging terms so that logic, logo, and
login are not counted as accountability language.
"""

import json
import os
import re
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


DATA = Path("/Users/junghualiu/case/a2a/information_society/data/yt")
OUT = Path(__file__).resolve().parent

LEXICONS = {
    "autonomy": r"\b(autonomous(ly)?|on its own|by itself|without human|self-directed|independently)\b",
    "human_in_loop": r"\b(human in the loop|human-in-the-loop|approval|approve|oversight|supervis\w+)\b",
    "registration": r"\b(agent card|agentcard|identity|identities|registr\w+|discover\w+|credential\w*|directory)\b",
    "authorization": r"\b(permission\w*|access|authoriz\w+|guardrail\w*|control\w*|security|scope\w*|policy|policies)\b",
    "accountability": r"\b(accountab\w+|audit\w*|logs?|logged|logging|traceab\w+|liabilit\w+|responsib\w+|compliance)\b",
    "delegation": r"\b(delegate\w*|delegation|hand off|handoff|on your behalf|on behalf of|assign\w*)\b",
    "protocols": r"\b(mcp|model context protocol|a2a|agent2agent|agent-to-agent protocol)\b",
}

ORDER = [
    "protocols",
    "human_in_loop",
    "authorization",
    "registration",
    "accountability",
    "autonomy",
    "delegation",
]

LABELS = {
    "protocols": "協定名稱（MCP、A2A、Agent2Agent）",
    "human_in_loop": "人在迴路／監督",
    "authorization": "授權（權限、存取、護欄、資安）",
    "registration": "登錄（AgentCard、身分、註冊、發現、憑證）",
    "accountability": "課責（稽核、日誌、可追溯、責任、法遵）",
    "autonomy": "自主（autonomous、on its own、without human）",
    "delegation": "委派（delegate、on your behalf、handoff）",
}


def load_corpus():
    videos = [json.loads(line) for line in (DATA / "yt_corpus_year.jsonl").open()]
    texts = {}
    for video in videos:
        path = DATA / "subs" / f"{video['id']}.txt"
        if path.exists():
            texts[video["id"]] = path.read_text().lower()
    return videos, texts


def recompute():
    videos, texts = load_corpus()
    total_words = sum(len(text.split()) for text in texts.values())
    result = {
        "n_videos": len(texts),
        "total_words": total_words,
        "lexicon_per_10k": {},
        "videos_mentioning": {},
        "videos_mentioning_pct": {},
        "lexicon_specification": LEXICONS,
    }
    for key, pattern in LEXICONS.items():
        count = sum(len(re.findall(pattern, text)) for text in texts.values())
        mentioned = sum(bool(re.search(pattern, text)) for text in texts.values())
        result["lexicon_per_10k"][key] = {
            "raw": count,
            "per_10k": round(count / total_words * 10_000, 2),
        }
        result["videos_mentioning"][key] = mentioned
        result["videos_mentioning_pct"][key] = round(mentioned / len(texts) * 100)
    return result


def make_figure(result):
    width, height = 2040, 1000
    margin_left, margin_right, margin_top, margin_bottom = 680, 230, 65, 120
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    font_file = "/System/Library/Fonts/STHeiti Medium.ttc"
    label_font = ImageFont.truetype(font_file, 27)
    small_font = ImageFont.truetype(font_file, 28)
    tick_font = ImageFont.truetype(font_file, 25)
    keys = list(reversed(ORDER))
    values = [result["lexicon_per_10k"][key]["per_10k"] for key in keys]
    videos = [result["videos_mentioning_pct"][key] for key in keys]
    labels = [LABELS[key] for key in keys]
    maximum = 14
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom
    for tick in range(0, maximum + 1, 2):
        x = margin_left + plot_width * tick / maximum
        draw.line((x, margin_top, x, height - margin_bottom), fill="#e5e5e5", width=2)
        bbox = draw.textbbox((0, 0), str(tick), font=tick_font)
        draw.text((x - (bbox[2] - bbox[0]) / 2, height - margin_bottom + 15), str(tick), fill="#222222", font=tick_font)
    draw.line((margin_left, margin_top, margin_left, height - margin_bottom), fill="#777777", width=2)
    draw.line((margin_left, height - margin_bottom, width - margin_right, height - margin_bottom), fill="#777777", width=2)
    row_height = plot_height / len(keys)
    for index, (label, value, pct) in enumerate(zip(labels, values, videos)):
        y = margin_top + index * row_height + 11
        bar_height = row_height * 0.58
        draw.text((18, y + (bar_height - 32) / 2), label, fill="#222222", font=label_font)
        bar_end = margin_left + plot_width * value / maximum
        draw.rounded_rectangle((margin_left, y, bar_end, y + bar_height), radius=5, fill="#2a78d6")
        draw.text((bar_end + 12, y + (bar_height - 28) / 2), f"{value:.1f}（{pct}%）", fill="#222222", font=small_font)
    xlabel = "每萬字出現次數；括號內為提及該詞庫的影片比例"
    bbox = draw.textbbox((0, 0), xlabel, font=small_font)
    draw.text(((width - (bbox[2] - bbox[0])) / 2, height - 55), xlabel, fill="#222222", font=small_font)
    image.save(OUT / "fig4_youtube_recomputed.png", dpi=(240, 240))


if __name__ == "__main__":
    analysis = recompute()
    (OUT / "yt_analysis_year_recomputed.json").write_text(
        json.dumps(analysis, ensure_ascii=False, indent=2) + "\n"
    )
    make_figure(analysis)
    print(json.dumps(analysis, ensure_ascii=False, indent=2))
