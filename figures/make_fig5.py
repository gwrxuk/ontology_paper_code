import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

BLUE, AQUA, GREEN, VIOLET = "#2a78d6", "#1baf7a", "#008300", "#4a3aa7"
INK = "#222222"
fig, ax = plt.subplots(figsize=(8.6, 5.6), dpi=200)
ax.set_xlim(0, 10); ax.set_ylim(0, 8.2); ax.axis("off")

def box(x, y, w, h, label, sub, ec):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.08",
                 ec=ec, fc="white", lw=1.6, zorder=3))
    yoff = 0.26 if sub else h/2
    ax.text(x+w/2, y+h-yoff, label, ha="center", va="center", fontsize=9.5, fontweight="bold", color=INK, zorder=4)
    if sub: ax.text(x+w/2, y+0.32, sub, ha="center", va="center", fontsize=7.2, color="#555555", zorder=4)

def arr(x1, y1, x2, y2, label="", lc=INK, ls="-", conn="arc3,rad=0", lx=0, ly=0.13):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=11,
                 color=lc, lw=1.1, linestyle=ls, shrinkA=3, shrinkB=3,
                 connectionstyle=conn, zorder=2))
    if label: ax.text((x1+x2)/2+lx, (y1+y2)/2+ly, label, fontsize=7.2, color=lc, ha="center", style="italic", zorder=5,
                      bbox=dict(fc="white", ec="none", pad=0.5))

# mechanism bands
for x0, name, c in [(0.2, "REGISTRATION", BLUE), (3.6, "AUTHORIZATION", AQUA), (7.0, "ACCOUNTABILITY", VIOLET)]:
    ax.add_patch(FancyBboxPatch((x0, 0.55), 2.8, 4.35, boxstyle="round,pad=0.05", ec=c, fc="none", lw=1.0, linestyle=(0,(4,3)), zorder=1))
    ax.text(x0+1.4, 0.8, name, ha="center", fontsize=8.5, fontweight="bold", color=c)

# actor hierarchy
box(4.1, 7.2, 1.8, 0.8, "aco:Actor", "", INK)
box(0.6, 5.7, 2.0, 0.8, "aco:HumanPrincipal", "", GREEN)
box(6.0, 5.7, 2.0, 0.8, "aco:MachineAgent", "", BLUE)
arr(1.7, 6.5, 4.2, 7.35, "rdfs:subClassOf", lc="#888888", ls=":", lx=-0.5)
arr(7.1, 6.5, 5.8, 7.35, "rdfs:subClassOf", lc="#888888", ls=":", lx=0.6)

# registration
box(0.5, 3.4, 2.2, 1.0, "aco:AgentCard", "name, skills,\nsecuritySchemes, signature", BLUE)
box(0.5, 1.7, 2.2, 0.95, "aco:Capability", "declared skill unit", BLUE)
arr(1.6, 3.4, 1.6, 2.65, "aco:declares", lc=BLUE, lx=0.8, ly=0)
arr(6.0, 6.0, 1.9, 4.4, "", lc=BLUE, conn="arc3,rad=0.25")
ax.text(2.75, 4.85, "aco:hasCard", fontsize=7.2, color=BLUE, style="italic", bbox=dict(fc="white", ec="none", pad=0.5))

# authorization
box(3.9, 3.4, 2.2, 1.0, "aco:ActionType", "verb defined in\nthe ontology", AQUA)
box(3.9, 1.7, 2.2, 0.95, "aco:Permission", "scope, securityScheme", AQUA)
arr(5.0, 3.4, 5.0, 2.65, "aco:requiresPermission", lc=AQUA, lx=1.15, ly=0)
arr(6.1, 2.15, 6.9, 5.7, "", lc=AQUA, conn="arc3,rad=-0.18")
arr(6.4, 5.7, 5.4, 4.4, "aco:mayExecute*", lc=AQUA, lx=0.95, ly=0)

# accountability
box(7.3, 3.4, 2.2, 1.0, "aco:Task", "8 lifecycle states\nincl. auth-required", VIOLET)
box(7.3, 1.7, 2.2, 0.95, "aco:AuditRecord", "actor, action,\ntime, outcome", VIOLET)
arr(8.4, 3.4, 8.4, 2.65, "aco:recordedIn", lc=VIOLET, lx=0.95, ly=0)
arr(7.6, 5.7, 8.2, 4.4, "aco:performedBy", lc=VIOLET, lx=1.0, ly=0)
arr(1.6, 5.7, 7.3, 4.55, "", lc=GREEN, conn="arc3,rad=0.18")
ax.text(3.35, 5.55, "aco:authorizes", fontsize=7.2, color=GREEN, style="italic", bbox=dict(fc="white", ec="none", pad=0.5))

ax.text(6.62, 3.15, "aco:\ngrantedTo", fontsize=7.0, color=AQUA, style="italic", ha="center", bbox=dict(fc="white", ec="none", pad=0.5))
ax.text(9.8, 0.15, "* derived: an agent may execute an action type iff its card declares the capability and the permission is granted to it",
        fontsize=6.8, ha="right", color="#777777")
fig.savefig("/Users/junghualiu/case/a2a/information_society/figures/fig5_ontology.png", bbox_inches="tight")
print("fig5 redone")
