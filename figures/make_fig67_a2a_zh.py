"""Figures 6 and 7 (v46): architecture and executor flow of the ACO reference
implementation on the A2A 1.0 protocol (a2a_sim/). Same palette and font as fig5."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon

fp = "/Users/junghualiu/Library/Fonts/NotoSansCJKtc-Regular.otf"
fm.fontManager.addfont(fp)
plt.rcParams["font.family"] = fm.FontProperties(fname=fp).get_name()
BOLD = fm.FontProperties(fname="/Users/junghualiu/Library/Fonts/NotoSansCJKtc-Bold.otf")
BLUE, AQUA, GREEN, VIOLET = "#2a78d6", "#1baf7a", "#008300", "#4a3aa7"
INK, MUTED, RED, AMBER = "#222222", "#777777", "#b5402a", "#c27a12"


def box(ax, x, y, w, h, title, sub, ec, fc="white", lw=2.2, tsize=12, ssize=9.5, tcolor=INK, scolor="#444444", ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.08",
                                ec=ec, fc=fc, lw=lw, ls=ls))
    if sub:
        ax.text(x + w / 2, y + h - 0.3, title, ha="center", va="center", fontproperties=BOLD, fontsize=tsize, color=tcolor)
        ax.text(x + w / 2, y + (h - 0.55) / 2, sub, ha="center", va="center", fontsize=ssize, color=scolor, linespacing=1.35)
    else:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center", fontproperties=BOLD, fontsize=tsize, color=tcolor)


def arrow(ax, p, q, color=INK, ls="-", rad=0.0, lw=1.6, label=None, lxy=None, lcolor=None, both=False, lsize=9.5):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="<|-|>" if both else "-|>", mutation_scale=13, color=color, lw=lw,
                                 ls=ls, connectionstyle=f"arc3,rad={rad}", shrinkA=2, shrinkB=2))
    if label:
        ax.text(*lxy, label, ha="center", va="center", fontsize=lsize, color=lcolor or color, linespacing=1.25,
                bbox=dict(fc="white", ec="none", pad=1.0))


def frame(ax, x, y, w, h, title):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", ec=MUTED, fc="#f6f7f9", lw=1.2, ls="--"))
    ax.text(x + w / 2, y + h - 0.32, title, ha="center", va="center", fontproperties=BOLD, fontsize=11.5, color=INK)


# ---------------- Figure 6: architecture ----------------
fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=200)
ax.set_xlim(0, 17.6); ax.set_ylim(0, 9.6); ax.axis("off")

# left: registration
frame(ax, 0.15, 0.2, 4.45, 9.2, "註冊（互動發生之前）")
box(ax, 0.4, 5.0, 3.95, 3.55, "registry　註冊機構",
    "（:8100）\n從名片網址取得AgentCard\n以受信任供應者的公鑰\n驗證JWS簽章（ES256）\n通過才登錄，否則DENIED\n提供 /agents/{名稱}、/keys/{kid}", BLUE, ssize=9.2)
box(ax, 0.4, 1.0, 3.95, 3.0, "card_host　名片主機",
    "（:8102）\ndesk-agent、intern-agent\n由taipei-daily-it簽署\nrogue-agent\n由不受信任的unknown-ltd簽署", BLUE, ssize=9.2)
arrow(ax, (2.37, 4.0), (2.37, 5.0), BLUE, label="取得名片", lxy=(2.37, 4.5))

# middle: the A2A server
frame(ax, 5.75, 0.2, 5.9, 9.2, "research-agent　A2A伺服器（:8101）")
box(ax, 6.0, 7.2, 5.4, 1.45, "AgentCard　代理人名片",
    "/.well-known/agent-card.json，ES256簽章\n技能：retrieve_court_records、publish_fact_check", BLUE, ssize=8.8)
box(ax, 6.0, 5.35, 5.4, 1.45, "JSON-RPC端點（a2a-sdk 1.2.3）",
    "SendMessage、GetTask\nDefaultRequestHandler＋InMemoryTaskStore", INK, ssize=8.8)
box(ax, 6.0, 3.15, 5.4, 1.8, "ACOExecutor　執行器",
    "依序進行五項檢查（流程見圖7）\n以TASK_STATE_*更新任務狀態", RED, tcolor=RED, ssize=9.2)
box(ax, 6.0, 0.45, 5.4, 2.3, "ACO本體論",
    "aco.ttl（類別與屬性）\nnewsroom.ttl（行動者、行動類型、權限）\n以rdflib的SPARQL查詢", AQUA, ssize=9.2)
arrow(ax, (8.7, 5.35), (8.7, 4.95))
arrow(ax, (8.7, 3.15), (8.7, 2.75), AQUA, label="SPARQL", lxy=(9.35, 2.95), lsize=8.8)
arrow(ax, (6.0, 4.3), (4.35, 6.2), BLUE, rad=-0.1, label="驗證呼叫者\n的憑證與登錄", lxy=(5.17, 5.2), lsize=8.8)

# right: clients, human principal, audit
frame(ax, 12.6, 0.2, 4.9, 9.2, "用戶端與人類委託人")
box(ax, 12.85, 6.55, 4.4, 2.1, "A2A用戶端（ClientFactory）",
    "desk-agent、intern-agent、rogue-agent\n先驗證伺服器名片的簽章\n每次呼叫附上Bearer JWT", INK, ssize=9.0)
box(ax, 12.85, 3.75, 4.4, 2.2, "人類委託人　editor-lin",
    "HumanPrincipal，持有發布權限\n簽署核可憑證（綁定task_id）\n恢復同一個任務", GREEN, ssize=9.0)
box(ax, 12.85, 0.45, 4.4, 2.75, "稽核軌跡",
    "註冊機構與執行器的每一個判斷\n行動者、行動、時間、結果（不含理由）\naudit_log.jsonl →\naudit.ttl（aco:AuditRecord）", VIOLET, ssize=8.8)

arrow(ax, (12.85, 8.2), (11.4, 7.95), BLUE, label="取得名片", lxy=(12.12, 8.45), lsize=8.6)
arrow(ax, (12.85, 7.0), (11.4, 6.1), INK, both=True, label="SendMessage\nGetTask", lxy=(12.12, 7.25), lsize=8.6)
arrow(ax, (12.85, 4.85), (11.4, 5.6), GREEN, label="核可", lxy=(12.12, 5.0), lsize=8.6)
arrow(ax, (11.4, 3.5), (12.85, 2.2), VIOLET, ls="--", label="每一步\n都寫入", lxy=(12.12, 2.75), lsize=8.6)

fig.savefig("fig6_a2a_arch_zh.png", bbox_inches="tight", facecolor="white")
plt.close(fig)

# ---------------- Figure 7: executor flow ----------------
fig, ax = plt.subplots(figsize=(9.6, 13.2), dpi=200)
ax.set_xlim(0, 11.6); ax.set_ylim(0, 16.0); ax.axis("off")
MX, OX = 3.7, 8.85  # main column, outcome column
DW, DH = 5.0, 1.3


def diamond(cx, cy, text, ec):
    ax.add_patch(Polygon([(cx, cy + DH / 2), (cx + DW / 2, cy), (cx, cy - DH / 2), (cx - DW / 2, cy)], closed=True, ec=ec, fc="white", lw=2.2))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=9.8, color=INK, linespacing=1.3)


def outcome(cx, cy, state, why, color, tag, w=3.3):
    box(ax, cx - w / 2, cy - 0.52, w, 1.04, state, why, color, fc=color, tcolor="white", scolor="white", tsize=10.5, ssize=8.8)
    if tag:
        ax.text(cx + w / 2 + 0.1, cy, tag, ha="left", va="center", fontsize=9.5, color=MUTED)


box(ax, MX - 2.5, 15.05, 5.0, 0.8, "SendMessage（Bearer JWT, action）", None, INK, tsize=10.5)
ys = [13.75, 12.15, 10.55, 8.95, 7.35]
checks = [("憑證可驗證，而且呼叫者\n已在註冊機構登錄？", BLUE), ("動詞是本體論中的\nActionType？", AQUA),
          ("本代理人的名片\n宣告了這項技能？", BLUE), ("所需權限已授予呼叫者？\n（SPARQL）", AQUA),
          ("requiresHumanApproval\n為true？", GREEN)]
fails = [("TASK_STATE_REJECTED", "不是已註冊的行動者", RED, "情境1"),
         ("TASK_STATE_REJECTED", "動詞不在本體論中", RED, "情境5"),
         ("TASK_STATE_REJECTED", "名片沒有宣告這項能力", RED, "情境7"),
         ("TASK_STATE_FAILED", "權限尚未授予", MUTED, "情境6"),
         ("TASK_STATE_COMPLETED", "例行行動直接完成", AQUA, "情境2")]
arrow(ax, (MX, 15.05), (MX, ys[0] + DH / 2))
for i, ((t, c), y) in enumerate(zip(checks, ys)):
    diamond(MX, y, t, c)
    if i < len(ys) - 1:
        arrow(ax, (MX, y - DH / 2), (MX, ys[i + 1] + DH / 2), label="是", lxy=(MX + 0.3, (y + ys[i + 1]) / 2))
    s, why, col, tag = fails[i]
    outcome(OX, y, s, why, col, tag)
    arrow(ax, (MX + DW / 2, y), (OX - 1.65, y), label="否", lxy=((MX + DW / 2 + OX - 1.65) / 2, y + 0.25))

outcome(MX, 5.9, "TASK_STATE_AUTH_REQUIRED", "任務暫停，等待人類委託人", AMBER, "情境3", w=3.9)
arrow(ax, (MX, ys[-1] - DH / 2), (MX, 6.42), label="是", lxy=(MX + 0.3, 6.58))
box(ax, MX - 2.5, 4.0, 5.0, 0.9, "編輯以核可憑證恢復同一個task_id", None, GREEN, tsize=10.3)
arrow(ax, (MX, 5.38), (MX, 4.9))
diamond(MX, 2.85, "核可憑證有效、簽署者是\nHumanPrincipal且持有權限？", GREEN)
arrow(ax, (MX, 4.0), (MX, 2.85 + DH / 2))
outcome(OX, 2.85, "TASK_STATE_REJECTED", "核可無法驗證", RED, "")
arrow(ax, (MX + DW / 2, 2.85), (OX - 1.65, 2.85), label="否", lxy=((MX + DW / 2 + OX - 1.65) / 2, 3.1))
outcome(MX, 1.0, "TASK_STATE_COMPLETED", "核可後完成", AQUA, "情境4")
arrow(ax, (MX, 2.85 - DH / 2), (MX, 1.52), label="是", lxy=(MX + 0.3, 1.85))

ax.text(OX, 0.95, "每一個判斷結果都以AuditRecord\n寫入稽核日誌：行動者、行動、\n時間與結果（不記錄理由）", ha="center", va="center",
        fontsize=9.3, color=VIOLET, linespacing=1.4,
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=VIOLET, lw=1.4, ls="--"))

fig.savefig("fig7_a2a_flow_zh.png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print("ok")
