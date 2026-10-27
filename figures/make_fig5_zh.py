import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
fp="/Users/junghualiu/Library/Fonts/NotoSansCJKtc-Regular.otf"
fm.fontManager.addfont(fp)
plt.rcParams["font.family"]=fm.FontProperties(fname=fp).get_name()
BOLD=fm.FontProperties(fname="/Users/junghualiu/Library/Fonts/NotoSansCJKtc-Bold.otf")
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

BLUE, AQUA, GREEN, VIOLET = "#2a78d6", "#1baf7a", "#008300", "#4a3aa7"
INK = "#222222"
fig, ax = plt.subplots(figsize=(8.6, 5.6), dpi=200)
ax.set_xlim(0, 10); ax.set_ylim(0, 8.2); ax.axis("off")

def box(x, y, w, h, label, sub, ec):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.08",
                 ec=ec, fc="white", lw=1.6, zorder=3))
    yoff = 0.26 if sub else h/2
    ax.text(x+w/2, y+h-yoff, label, ha="center", va="center", fontsize=9.5, fontproperties=BOLD, color=INK, zorder=4)
    if sub: ax.text(x+w/2, y+0.32, sub, ha="center", va="center", fontsize=7.2, color="#555555", zorder=4)

def arr(x1, y1, x2, y2, label="", lc=INK, ls="-", conn="arc3,rad=0", lx=0, ly=0.13):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=11,
                 color=lc, lw=1.1, linestyle=ls, shrinkA=3, shrinkB=3,
                 connectionstyle=conn, zorder=2))
    if label: ax.text((x1+x2)/2+lx, (y1+y2)/2+ly, label, fontsize=7.2, color=lc, ha="center", zorder=5,
                      bbox=dict(fc="white", ec="none", pad=0.5))

# mechanism bands
for x0, name, c in [(0.2, "註冊（registration）", BLUE), (3.6, "授權（authorization）", AQUA), (7.0, "課責（accountability）", VIOLET)]:
    ax.add_patch(FancyBboxPatch((x0, 0.55), 2.8, 4.35, boxstyle="round,pad=0.05", ec=c, fc="none", lw=1.0, linestyle=(0,(4,3)), zorder=1))
    ax.text(x0+1.4, 0.8, name, ha="center", fontsize=8.5, fontproperties=BOLD, color=c)

# actor hierarchy
box(4.1, 7.2, 1.8, 0.8, "aco:Actor", "行動者", INK)
box(0.6, 5.7, 2.0, 0.8, "aco:HumanPrincipal", "人類委託人", GREEN)
box(6.0, 5.7, 2.0, 0.8, "aco:MachineAgent", "機器代理人", BLUE)
arr(1.7, 6.5, 4.2, 7.35, "rdfs:subClassOf（子類別）", lc="#888888", ls=":", lx=-0.5)
arr(7.1, 6.5, 5.8, 7.35, "rdfs:subClassOf（子類別）", lc="#888888", ls=":", lx=0.6)

# registration
box(0.5, 3.4, 2.2, 1.0, "aco:AgentCard", "名稱、技能、\n安全機制、數位簽章", BLUE)
box(0.5, 1.7, 2.2, 0.95, "aco:Capability", "宣告的技能單位", BLUE)
arr(1.6, 3.4, 1.6, 2.65, "aco:declares（宣告）", lc=BLUE, lx=0.8, ly=0)
arr(6.0, 6.0, 1.9, 4.4, "", lc=BLUE, conn="arc3,rad=0.25")
ax.text(3.35, 4.62, "aco:hasCard（持有名片）", fontsize=7.2, color=BLUE, bbox=dict(fc="white", ec="none", pad=0.5))

# authorization
box(3.9, 3.4, 2.2, 1.0, "aco:ActionType", "本體論中定義的\n行動（動詞）", AQUA)
box(3.9, 1.7, 2.2, 0.95, "aco:Permission", "權限範圍、安全機制", AQUA)
arr(5.0, 3.4, 5.0, 2.65, "aco:requiresPermission\n（需要權限）", lc=AQUA, lx=0, ly=-0.2)
arr(6.1, 2.15, 6.9, 5.7, "", lc=AQUA, conn="arc3,rad=-0.18")
arr(6.4, 5.7, 5.4, 4.4, "aco:mayExecute*\n（可以執行）", lc=AQUA, lx=0.95, ly=0)

# accountability
box(7.3, 3.4, 2.2, 1.0, "aco:Task", "八種生命週期狀態\n（含auth-required）", VIOLET)
box(7.3, 1.7, 2.2, 0.95, "aco:AuditRecord", "行動者、行動、\n時間、結果", VIOLET)
arr(8.4, 3.4, 8.4, 2.65, "aco:recordedIn\n（記錄於）", lc=VIOLET, lx=0.75, ly=-0.2)
arr(7.6, 5.7, 8.2, 4.4, "aco:performedBy\n（執行者）", lc=VIOLET, lx=1.0, ly=0)
arr(1.6, 5.7, 7.3, 4.55, "", lc=GREEN, conn="arc3,rad=0.18")
ax.text(3.35, 5.55, "aco:authorizes（核可）", fontsize=7.2, color=GREEN, bbox=dict(fc="white", ec="none", pad=0.5))

ax.text(6.72, 2.55, "aco:grantedTo\n（授予對象）", fontsize=6.6, color=AQUA, ha="center", bbox=dict(fc="white", ec="none", pad=0.5))
ax.text(9.8, 0.15, "* 推導關係：只有在名片宣告了相應的能力，且權限已授予該代理人時，代理人才可以執行該行動類型",
        fontsize=6.8, ha="right", color="#777777")
fig.savefig("fig5_ontology_zh.png", bbox_inches="tight")
print("fig5 redone")
