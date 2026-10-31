# Code for the paper

This folder collects the scripts behind the Chinese manuscript (`chatgpt/v46_natural.docx`) and maps each one to the terms, numbers, tables and figures used in the paper.

The files here are **copies**. The originals are still in `data/`, `data/yt/`, `artifact/` and `chatgpt/`. Most scripts use absolute paths to those original locations, so they read and write the data in the repository's `data/` folder, not in this folder. Copies of the datasets the paper reports are in `paper_code/data/` (see the Datasets section). The tables below name output files by their path inside `data/`, which is the same in both places.

The data were collected July 7–9, 2026 through public APIs (OpenAlex, GitHub, GDELT DOC 2.0) and yt-dlp. Re-running a collection script now returns different data. The frozen datasets in `data/` are the ones the paper reports.

## Folder layout

```
paper_code/
  study1_scale/      研究一: OpenAlex and GitHub
  study3_news/       研究三: news corpus, rule-based classifier v1/v2
  study3_youtube/    研究三: YouTube corpus, collocates, lexicons
  study4_aco/        研究四: ACO ontology and reference implementation
  figures/           Figure scripts
  data/              Frozen datasets the paper reports (copies)
```

研究二 (document analysis of the Palantir and A2A documents) was done by reading, so it has no code.

## 研究一：代理人轉向的規模

| Term in the paper | Script | Output (in `data/`) |
|---|---|---|
| 文獻數量取自OpenAlex學術資料庫API, 2016–2025; 表1 OpenAlex文獻趨勢; 圖1 | `study1_scale/collect.py` | `openalex_trends.json` |
| GitHub採用指標; 圖2 GitHub上代理人框架與協定的採用 (A2A 24,685 stars, etc.) | `study1_scale/github.py` | `github_repos.json` |

## 研究三：新聞語料庫 (N = 260)

| Term in the paper | Script | Output (in `data/`) |
|---|---|---|
| GDELT DOC 2.0 API, 「"agentic AI" OR "AI agents"」, 十三個期間, 每期擷取100篇, 去除重複後1,097篇 | `study3_news/collect_news_year.py`, then `study3_news/fill_months.py` (re-queries 2025-11, 2025-12 and 2026-07, which came back short) | `news_corpus_year.csv` |
| 依月份分層隨機抽出260篇 (每月20篇, 隨機種子為42) | `study3_news/analyze_news_year.py` | `news_sample_year.csv` |
| 從年度語料庫另外抽出60則 (種子=21) | `study3_news/analyze_news_year.py` (end of file) | `validation_60_year.json` |
| 規則式分類器（rule-based classifier）**v1**; 第一步: 開發樣本30則, 63.3%, κ = .50 | `study3_news/analyze_news.py`, lines 30–39 (`code_headline`) | v1 runs on the pilot corpus: `news_corpus.csv`, `news_sample_100.csv`, `news_analysis.json` |
| Pilot news corpus that v1 was developed on (前導研究) | `study3_news/collect_news.py` | `news_corpus.csv` |
| 規則式分類器 **v2**; 主詞位置法（subject-position heuristic）; 附錄一 判定步驟與50個動詞詞幹 | `study3_news/classifier_v2.py` (`code_v2`) | used by `analyze_news_year.py` |
| 次要估計: v2對全部260則標題的輸出 | `study3_news/analyze_news_year.py` | `news_analysis_year.json` (`frames_v2`) |
| 機制詞庫 (附錄一: 註冊／授權／課責, 套用於全部260則標題) | `study3_news/analyze_news_year.py` (`MECH`) | `news_analysis_year.json` (`mechanisms`) |
| 主要語言模型編碼程序（primary LLM coding process） | none: a Claude Fable 5 session, July 2026 | labels stored in `classifier_validation.json` (`llm_a_codes`) |
| 獨立盲測語言模型程序（independent blind LLM coding process） | none: a separate Claude agent run that saw only the codebook and headlines | `coder_b_annotations.json` (60 labels) |
| 第二步/第三步 agreement and κ (66.7%/.51, 56.7%/.42, 98.3%/.98); 附錄一 分類流程摘要 | none: computed during the July 2026 session | results stored in `classifier_validation.json` |
| 圖3 新聞論述中的能動性 | no surviving script (see Figures) | data from `news_analysis_year.json` |

## 研究三：YouTube語料庫 (N = 138)

| Term in the paper | Script | Output (in `data/yt/` or `data/`) |
|---|---|---|
| 以五組關鍵字在YouTube上檢索 | none: yt-dlp searches run from the command line | `yt/yt_search_*.jsonl` (5 files) |
| 200支不重複的候選影片, 逐一確認上傳日期, 保留過去一年內上傳 (2025-07-01 to 2026-07-09) 而且英語逐字稿在100字以上的影片, 共138支; 987,600字 | `study3_youtube/expand_year.py` (dedupes the 5 search files, checks each upload date, downloads English captions, keeps transcripts of 100+ words) | `yt/upload_dates.json`, `yt/subs/*.txt`, `yt/yt_corpus_year.jsonl` |
| Pilot YouTube corpus (earlier version; some of its transcripts are reused by `expand_year.py`) | `study3_youtube/get_transcripts.py` | `yt/yt_corpus.jsonl` |
| 緊接在「agent(s)」右側的搭配詞 | `study3_youtube/analyze_yt_year.py` | `yt_analysis_year.json` |
| 七組詞庫的每萬字頻率, 提到各詞庫的影片比例; 詞庫經過縮窄後再計算 (例如不把login算成課責詞彙); 表3 | `study3_youtube/recompute_yt_lexicons.py` | `chatgpt/yt_analysis_year_recomputed.json`, `chatgpt/fig4_youtube_recomputed.png` |
| 圖4 YouTube逐字稿中的能動性詞庫 | no surviving script for the final version (see Figures) | data from `yt_analysis_year_recomputed.json` |

`analyze_yt_year.py` also computes lexicon counts, but those use the earlier, broader lexicons. The paper reports the narrowed counts from `recompute_yt_lexicons.py`.

## 研究四：能動性配置本體論（ACO）與參考系統

| Term in the paper | File |
|---|---|
| 以網路本體語言（OWL）撰寫的精簡本體論, 九個類別與八個屬性; 附錄二（一）, Turtle原始碼約80行 | `study4_aco/aco.ttl` |
| 在A2A協定上實際運作的Python參考實作; 附錄二（二） | `a2a_sim/` at the repository root (a2a-sdk 1.2.3) |
| 實例檔newsroom.ttl: retrieve_court_records, translate_article, publish_fact_check; desk-agent, intern-agent, editor-lin | `a2a_sim/ontology/newsroom.ttl` |
| 註冊機構（registry）, JWS簽章驗證 | `a2a_sim/registry.py` |
| 研究代理人的執行器（ACOExecutor）依序檢查五個條件 | `a2a_sim/research_agent.py` (`ACOExecutor.execute`) |
| 系統的邊界則以七個情境測試; 稽核日誌共12筆 | `a2a_sim/run_scenarios.py` → `a2a_sim/results/scenarios.json`, `a2a_sim/results/audit.ttl` |

Run it with `cd a2a_sim && .venv/bin/python run_scenarios.py` (setup in `a2a_sim/README.md`). Task IDs and timestamps change on each run; the seven task states do not.

`study4_aco/agency_demo.py` is the earlier in-memory, standard-library-only demonstration that versions up to v45 described (137 lines, five scenarios). v46 reports the A2A version instead.

## Figures

| Figure in the paper | Image embedded in the paper | Script |
|---|---|---|
| 圖1 研究中的代理人轉向 | `figures/fig1_bibliometrics.png` | `figures/make_figures.py` |
| 圖2 GitHub上代理人框架與協定的採用 | `figures/fig2_github.png` | `figures/make_figures.py` |
| 圖3 新聞論述中的能動性 | `chatgpt/fig3_news_v29.png` | **not found.** `make_figures.py` draws the earlier English version from the pilot data. |
| 圖4 YouTube逐字稿中的能動性詞庫 | `chatgpt/fig4_youtube_v29.png` | **not found.** `recompute_yt_lexicons.py` draws an earlier layout (`fig4_youtube_recomputed.png`) from the same numbers. |
| 圖6 ACO參考實作的架構; 圖7 研究代理人執行器的判斷流程與七個測試情境 | `chatgpt/fig6_a2a_arch_zh.png`, `chatgpt/fig7_a2a_flow_zh.png` | `figures/make_fig67_a2a_zh.py` |
| 圖5 能動性配置本體論（ACO）的架構 | `chatgpt/fig5_ontology_zh_v34.png` | closest is `figures/make_fig5_zh.py` (Chinese). The v34 image was edited after it. `make_fig5.py` draws the English version. |

## Datasets (`paper_code/data/`)

| File | Contents | Where it appears in the paper |
|---|---|---|
| `openalex_trends.json` | Publication counts per year, 2016–2025 | 研究一, 表1, 圖1 |
| `github_repos.json` | Stars, forks and creation dates of 7 agent repositories (July 2026) | 研究一, 圖2 |
| `news_corpus_year.csv` | 1,097 unique GDELT headlines, July 2025 to July 2026 | 研究三, 去除重複後得到1,097篇 |
| `news_sample_year.csv` | Month-stratified sample, 260 headlines (seed 42) | 研究三, 新聞語料庫（N = 260） |
| `news_analysis_year.json` | v2 frame counts and mechanism-lexicon counts for the 260 headlines, top domains | 研究三, 次要估計; 附錄一 機制詞庫; 圖3 |
| `validation_60_year.json` | The 60 held-out headlines (seed 21) with v2 labels | 第二步, 第三步 |
| `holdout_titles.json` | The 30 pilot held-out headlines | 第二步, 前導研究30則 |
| `classifier_validation.json` | All agreement and κ results, plus the primary LLM coding process's labels (`llm_a_codes`) | 第一步 to 第三步; 附錄一 分類流程摘要 |
| `coder_b_annotations.json` | The independent blind LLM coding process's 60 labels | 第三步, 98.3%, κ = .98 |
| `news_corpus.csv`, `news_sample_100.csv`, `news_analysis.json` | Pilot news corpus, sample and v1 results | 第一步 (v1 development) |
| `yt/yt_search_*.jsonl` | Results of the 5 YouTube keyword searches | 以五組關鍵字在YouTube上檢索 |
| `yt/upload_dates.json` | Upload date for each candidate video | 逐一確認上傳日期 |
| `yt/yt_corpus_year.jsonl` | The 138 videos in the YouTube corpus | YouTube語料庫（N = 138）, 觀看次數的中位數80,211 |
| `yt/subs/*.txt` | English transcripts (166 files: the 138 corpus videos plus pilot videos) | 逐字稿總計987,600字 |
| `yt/yt_corpus.jsonl` | Pilot YouTube corpus | not reported |
| `yt_analysis_year.json` | Collocates to the right of "agent(s)", and earlier broad-lexicon counts | 搭配詞 |
| `yt_analysis_year_recomputed.json` | Narrowed-lexicon counts per 10,000 words and share of videos | 表3, 圖4 |

The ACO files (`aco.ttl`, `agency_demo.py`) are in `study4_aco/`. `data/human_coding_sheet.csv` in the repository is a blank sheet with no codes filled in, so it is not copied.

## Gaps

These parts of the paper have no script in the repository:

- the two LLM coding processes and their prompts
- the agreement and κ calculations for the headline coding
- the YouTube keyword searches
- the final versions of 圖3, 圖4 and 圖5
