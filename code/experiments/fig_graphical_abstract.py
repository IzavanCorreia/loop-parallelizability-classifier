"""Graphical abstract (required by Applied Soft Computing; at least 1328 x 531 px, read from left to
right). Numbers are read from results/tables, so the image always matches the paper.
Writes latex/figures/graphical_abstract.pdf and a 300 dpi PNG for the submission system."""

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

INK, INK2, EDGE, FILL, ACCENT, ACCENT_FILL, GREY = "#0b0b0b", "#52514e", "#7d7c78", "#f4f3f0", "#2a78d6", "#e8f1fc", "#9a9994"
plt.rcParams.update({"font.family": "DejaVu Sans", "pdf.fonttype": 42})


def panel(ax, x, y, w, h, title, accent=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.02", linewidth=1.2,
                                edgecolor=ACCENT if accent else EDGE, facecolor=ACCENT_FILL if accent else FILL))
    ax.text(x + w / 2, y + h - 0.04, title, ha="center", va="top", fontsize=11, fontweight="bold", color=INK)


def arrow(ax, a, b):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=14, linewidth=1.6, color=INK2))


def main():
    real = pd.read_csv(os.path.join(common.RESULTS, "tables", "real_code.csv"))
    syn = pd.read_csv(os.path.join(common.RESULTS, "tables", "summary.csv"))
    syn = syn[syn.setting == "hybrid, synthetic test samples"].set_index("model")
    fig = plt.figure(figsize=(13.28, 5.31), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 2.5)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # 1. minimal pair
    panel(ax, 0.03, 0.08, 0.66, 0.84, "Evolved minimal loop pairs")
    code_p = "for x in xs:\n    t = f(x)\n    t += c\n    out.append(t)"
    code_u = "for x in xs:\n    t += f(x)\n    t += c\n    out.append(t)"
    ax.text(0.07, 0.72, "Parallelizable", fontsize=10, color=INK, fontweight="bold")
    ax.text(0.07, 0.69, code_p, fontsize=10, family="monospace", va="top", color=INK)
    ax.text(0.38, 0.72, "Undefined", fontsize=10, color=INK, fontweight="bold")
    ax.text(0.38, 0.69, code_u, fontsize=10, family="monospace", va="top", color=INK)
    ax.text(0.36, 0.30, "genetic algorithm + dependence oracle\n4,000 oracle-verified pairs, 9 families\n"
                        "same names and data in both loops", ha="center", va="top", fontsize=9.5, color=INK2,
            linespacing=1.4)
    arrow(ax, (0.71, 0.5), (0.80, 0.5))

    # 2. models on synthetic pairs
    panel(ax, 0.82, 0.08, 0.66, 0.84, "Synthetic pairs: accuracy (%)", accent=True)
    names = ["Logistic regression", "Linear SVM", "DNN", "CNN", "N-gram LR", "DistilBERT"]
    short = ["LR", "SVM", "DNN", "CNN", "N-gram LR", "DistilBERT"]
    for i, (n, s) in enumerate(zip(names, short)):
        v = 100 * syn.loc[n, "accuracy_mean"] if n in syn.index else 0
        yy = 0.72 - i * 0.095
        ax.text(0.86, yy, s, fontsize=10, va="center", color=INK)
        ax.add_patch(FancyBboxPatch((1.02, yy - 0.026), 0.38 * v / 100, 0.052, boxstyle="square,pad=0",
                                    facecolor=ACCENT if s == "DistilBERT" else GREY, edgecolor="none"))
        ax.text(1.02 + 0.38 * v / 100 + 0.01, yy, f"{v:.1f}", fontsize=10, va="center", color=INK)
    ax.text(1.15, 0.13, "models of the previous study stay at chance level", ha="center", fontsize=9.5, color=INK2,
            style="italic")
    arrow(ax, (1.50, 0.5), (1.59, 0.5))

    # 3. real-world code: the scenarios with real training loops and the threshold control
    fc = pd.read_csv(os.path.join(common.RESULTS, "tables", "fpr_control.csv"))
    thr = fc[(fc.setting == "real") & (fc.model == "distilbert") & (fc.alpha == 0.05)].iloc[0]
    panel(ax, 1.61, 0.08, 0.86, 0.84, "340 real-world loops (DistilBERT)")
    ax.text(2.10, 0.76, "accuracy", fontsize=9.5, ha="center", color=INK2)
    ax.text(2.33, 0.76, "FPR", fontsize=9.5, ha="center", color=INK2)
    rows = [("synthetic + real training", "(b) hybrid, real test samples"),
            ("real training only", "(c) real only")]
    for i, (label, key) in enumerate(rows):
        r = real[(real.setting == key) & (real.model == "DistilBERT")].iloc[0]
        yy = 0.66 - i * 0.13
        ax.text(1.65, yy, label, fontsize=10, va="center", color=INK)
        ax.text(2.10, yy, f"{100 * r.accuracy_mean:.1f}%", fontsize=12, ha="center", va="center", color=INK,
                fontweight="bold")
        ax.text(2.33, yy, f"{100 * r.fpr_mean:.1f}%", fontsize=12, ha="center", va="center", color=INK,
                fontweight="bold")
    yy = 0.40
    ax.text(1.65, yy, "+ threshold set on real\n   validation loops", fontsize=10, va="center", color=INK,
            linespacing=1.3)
    ax.text(2.10, yy, f"recall {100 * thr.tpr_mean:.1f}%", fontsize=10, ha="center", va="center", color=INK2)
    ax.text(2.33, yy, f"{100 * thr.fpr_mean:.1f}%", fontsize=12, ha="center", va="center", color=ACCENT,
            fontweight="bold")
    ng = real[(real.setting == "(c) real only") & (real.model == "N-gram LR")].iloc[0]
    ax.text(2.04, 0.22, f"n-gram model, real only: {100 * ng.accuracy_mean:.1f}% accuracy, "
                        f"{100 * ng.fpr_mean:.1f}% FPR", ha="center", fontsize=9.5, color=INK2, style="italic")
    ax.text(2.04, 0.13, "FPR = Undefined loops reported as parallelizable", ha="center", fontsize=9.5,
            color=INK2, style="italic")
    out = os.path.join(common.ROOT, "latex", "figures", "graphical_abstract")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out + ".pdf")
    fig.savefig(out + ".png", dpi=300)
    print("written", out + ".pdf/.png")


if __name__ == "__main__":
    main()
