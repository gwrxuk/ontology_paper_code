"""Figures 6 and 7: architecture and execute() flow of the ACO reference
implementation (artifact/agency_demo.py). Same palette and font as fig5."""
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
    if sub and sub.count("\n") >= 2:
        ax.text(x + w / 2, y + h - 0.32, title, ha="center", va="center", fontproperties=BOLD, fontsize=tsize, color=tcolor)
        ax.text(x + w / 2, y + (h - 0.6) / 2, sub, ha="center", va="center", fontsize=ssize, color=scolor, linespacing=1.35)
    elif sub:
        ax.text(x + w / 2, y + h * 0.66, title, ha="center", va="center", fontproperties=BOLD, fontsize=tsize, color=tcolor)
        ax.text(x + w / 2, y + h * 0.3, sub, ha="center", va="center", fontsize=ssize, color=scolor, linespacing=1.35)
    else:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center", fontproperties=BOLD, fontsize=tsize, color=tcolor)


def arrow(ax, p, q, color=INK, ls="-", rad=0.0, lw=1.6, label=None, lxy=None, lcolor=None):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=13, color=color, lw=lw, ls=ls,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=2, shrinkB=2))
    if label:
        ax.text(*lxy, label, ha="center", va="center", fontsize=9.5, color=lcolor or color,
                bbox=dict(fc="white", ec="none", pad=1.0))


# ---------------- Figure 6: architecture ----------------
fig, ax = plt.subplots(figsize=(11.5, 6.6), dpi=200)
ax.set_xlim(0, 14.6); ax.set_ylim(0, 8.4); ax.axis("off")

# phase frames
ax.add_patch(FancyBboxPatch((0.15, 0.55), 4.1, 7.5, boxstyle="round,pad=0.02,rounding_size=0.1", ec=MUTED, fc="#f6f7f9", lw=1.2, ls="--"))
ax.text(2.2, 7.75, "① 設定階段（互動發生之前）", ha="center", fontproperties=BOLD, fontsize=12, color=INK)
ax.add_patch(FancyBboxPatch((10.35, 0.55), 4.1, 7.5, boxstyle="round,pad=0.02,rounding_size=0.1", ec=MUTED, fc="#f6f7f9", lw=1.2, ls="--"))
ax.text(12.4, 7.75, "② 執行階段", ha="center", fontproperties=BOLD, fontsize=12, color=INK)

# setup steps
box(ax, 0.45, 5.3, 3.5, 2.05, "define_action()", "定義行動類型\nsummarize_report → perm:read\nsend_payment → perm:pay\n（需人類核可）", AQUA, ssize=8.8)
box(ax, 0.45, 3.02, 3.5, 2.05, "register()", "寫入代理人名片 AgentCard\nassistant-agent（DemoCorp）\n技能：summarize_report、\nsend_payment", BLUE, ssize=8.8)
box(ax, 0.45, 0.75, 3.5, 2.05, "grant()", "授予權限\nassistant-agent ← perm:read\nassistant-agent ← perm:pay", AQUA, ssize=8.8)

# ontology object with four stores
ax.add_patch(FancyBboxPatch((4.85, 0.55), 4.9, 7.5, boxstyle="round,pad=0.02,rounding_size=0.1", ec=INK, fc="white", lw=2.4))
ax.text(7.3, 7.75, "Ontology 物件（資料綱要層）", ha="center", fontproperties=BOLD, fontsize=12, color=INK)
box(ax, 5.2, 5.75, 4.2, 1.35, "registry　註冊表", "誰被辨識為行動者（AgentCard）", BLUE)
box(ax, 5.2, 4.05, 4.2, 1.35, "action_types　行動類型", "可以做什麼（動詞與所需權限）", AQUA)
box(ax, 5.2, 2.35, 4.2, 1.35, "grants　授權表", "誰取得哪一項權限", AQUA)
box(ax, 5.2, 0.8, 4.2, 1.2, "audit_log　稽核日誌", "行動者、行動、時間、結果（不含理由）", VIOLET)

arrow(ax, (3.95, 6.3), (5.2, 4.75), AQUA, rad=-0.15)
arrow(ax, (3.95, 4.05), (5.2, 6.4), BLUE, rad=0.15)
arrow(ax, (3.95, 1.95), (5.2, 3.0), AQUA, rad=0.1)
arrow(ax, (3.95, 1.25), (5.2, 1.25), VIOLET, ls="--", rad=0.0, label="寫入", lxy=(4.57, 1.48))

# runtime
box(ax, 10.55, 5.85, 1.75, 1.35, "行動請求", "assistant-agent\nrogue-agent", INK, tsize=10.5, ssize=8.8)
box(ax, 12.5, 5.85, 1.75, 1.35, "人類委託人", "HumanPrincipal\nhuman_approver", GREEN, tsize=10.5, ssize=8.8)
box(ax, 10.65, 3.55, 3.5, 1.75, "execute()", "依序檢查：註冊 → 動詞 → 名片能力\n→ 權限 → 人類核可\n（流程見圖7）", RED, tcolor=RED, ssize=9)
box(ax, 10.65, 1.0, 3.5, 1.6, "回傳 TaskState", "rejected／failed／\nauth-required／completed", INK, tsize=11, ssize=9)

arrow(ax, (11.42, 5.85), (11.42, 5.3), label="(actor, verb)", lxy=(11.42, 5.58))
arrow(ax, (13.37, 5.85), (13.37, 5.3), GREEN, label="核可", lxy=(13.37, 5.58))
arrow(ax, (12.4, 3.55), (12.4, 2.6))
arrow(ax, (10.65, 4.7), (9.4, 6.35), BLUE, rad=0.1, label="讀取", lxy=(10.0, 5.75))
arrow(ax, (10.65, 4.45), (9.4, 4.7), AQUA, rad=0.0)
arrow(ax, (10.65, 4.2), (9.4, 3.0), AQUA, rad=-0.1)
arrow(ax, (10.65, 3.75), (9.4, 1.4), VIOLET, ls="--", rad=-0.1, label="每一步都寫入", lxy=(10.0, 2.3))

fig.savefig("fig6_reference_arch_zh.png", bbox_inches="tight", facecolor="white")
plt.close(fig)

# ---------------- Figure 7: execute() flow ----------------
fig, ax = plt.subplots(figsize=(9.2, 11.2), dpi=200)
ax.set_xlim(0, 11); ax.set_ylim(0, 14.2); ax.axis("off")
MX, OX = 3.6, 8.4  # main column, outcome column


def diamond(cx, cy, text, ec):
    w, h = 4.4, 1.25
    ax.add_patch(Polygon([(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)], closed=True, ec=ec, fc="white", lw=2.2))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=10.5, color=INK, linespacing=1.3)


def outcome(cy, state, why, color, tag):
    box(ax, OX - 1.45, cy - 0.5, 2.9, 1.0, state, why, color, fc=color, tcolor="white", scolor="white", tsize=11.5, ssize=9)
    ax.text(OX + 1.62, cy, tag, ha="left", va="center", fontsize=9.5, color=MUTED)


box(ax, MX - 2.2, 13.1, 4.4, 0.85, "execute(actor, verb, human_approver)", None, INK, tsize=10.5)
ys = [11.75, 10.15, 8.55, 6.95, 5.35, 3.75]
checks = [("行動者在註冊表中？", BLUE), ("動詞定義在本體論中？", AQUA), ("名片宣告了這項技能？", BLUE),
          ("已授予所需權限？", AQUA), ("這個行動類型\n需要人類核可？", GREEN), ("有人類核可者？", GREEN)]
arrow(ax, (MX, 13.1), (MX, ys[0] + 0.63))
for i, ((t, c), y) in enumerate(zip(checks, ys)):
    diamond(MX, y, t, c)
    if i < len(ys) - 1:
        lab = "是"
        arrow(ax, (MX, y - 0.63), (MX, ys[i + 1] + 0.63), label=lab, lxy=(MX + 0.3, (y + ys[i + 1]) / 2))

outcome(ys[0], "rejected", "不是已註冊的行動者", RED, "情境1")
outcome(ys[1], "rejected", "動詞不在本體論中", RED, "情境5")
outcome(ys[2], "rejected", "名片沒有宣告這項能力", RED, "")
outcome(ys[3], "failed", "權限尚未授予", MUTED, "")
outcome(ys[4], "completed", "例行行動直接完成", AQUA, "情境2")
outcome(ys[5], "auth-required", "等待人類委託人核可", AMBER, "情境3")
for i, y in enumerate(ys):
    lab = "否"
    arrow(ax, (MX + 2.2, y), (OX - 1.45, y), label=lab, lxy=((MX + 2.2 + OX - 1.45) / 2, y + 0.25))

box(ax, MX - 2.0, 1.95, 4.0, 0.85, "記錄人類核可（approve:verb）", None, GREEN, tsize=10.5)
arrow(ax, (MX, ys[5] - 0.63), (MX, 2.8), label="是", lxy=(MX + 0.3, 2.95))
box(ax, MX - 1.45, 0.55, 2.9, 0.95, "completed", "核可後完成", AQUA, fc=AQUA, tcolor="white", scolor="white", tsize=11.5, ssize=9)
ax.text(MX + 1.62, 1.02, "情境4", ha="left", va="center", fontsize=9.5, color=MUTED)
arrow(ax, (MX, 1.95), (MX, 1.5))

ax.text(OX, 0.95, "每一個判斷結果都以 AuditRecord\n寫入稽核日誌：行動者、行動、\n時間與結果（不記錄理由）", ha="center", va="center",
        fontsize=9.5, color=VIOLET, linespacing=1.4,
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=VIOLET, lw=1.4, ls="--"))

fig.savefig("fig7_execute_flow_zh.png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print("ok")
