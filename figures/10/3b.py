import numpy as np
import matplotlib.pyplot as plt

# =========================
# Data
# =========================
K = np.array([1, 3, 5, 10])

self_judge    = [57.50, 72.50, 78.33, 84.17]
unified_judge = [51.67, 65.83, 69.17, 71.67]
human_review  = [54.17, 67.50, 71.67, 75.00]

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["axes.unicode_minus"] = False

fig, ax = plt.subplots(figsize=(6.6, 5.5))

ax.plot(K, self_judge,
        marker="o", linestyle="-", linewidth=2.2,
        markersize=7, markerfacecolor="white",
        markeredgewidth=1.4, label="Self-Judge")

ax.plot(K, unified_judge,
        marker="s", linestyle="--", linewidth=2.2,
        markersize=7, markerfacecolor="white",
        markeredgewidth=1.4, label="Unified Judge")

ax.plot(K, human_review,
        marker="^", linestyle="-.", linewidth=2.2,
        markersize=7, markerfacecolor="white",
        markeredgewidth=1.4, label="Human Review")

ax.set_xlim(0.5, 10.5)
ax.set_ylim(0, 100)

ax.set_xticks(K)
ax.set_yticks(np.arange(0, 101, 20))

ax.set_xlabel("Attempt Budget K", fontsize=13)
ax.set_ylabel("ASR (%)", fontsize=13)

ax.tick_params(axis="both", labelsize=11)

ax.grid(axis="y", linewidth=0.7, alpha=0.25)
ax.set_axisbelow(True)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, -0.18),
    ncol=3,
    frameon=False,
    fontsize=10
)

plt.subplots_adjust(
    left=0.14, right=0.98,
    top=0.97, bottom=0.36
)

plt.savefig("AdvBench_Doubao_EN.png",
            dpi=600, bbox_inches="tight")
plt.savefig("AdvBench_Doubao_EN.svg",
            bbox_inches="tight")
plt.savefig("AdvBench_Doubao_EN.pdf",
            bbox_inches="tight")

plt.show()