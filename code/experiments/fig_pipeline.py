"""Figure 1: overview of the approach (vector PDF drawn with matplotlib)."""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "latex", "figures", "fig_pipeline.pdf")
INK, INK2, EDGE, FILL, ACCENT, ACCENT_FILL = "#0b0b0b", "#52514e", "#7d7c78", "#f4f3f0", "#2a78d6", "#e8f1fc"

plt.rcParams.update({"font.family": "DejaVu Sans", "pdf.fonttype": 42})


def box(ax, x, y, w, h, title, lines, accent=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.018",
                                linewidth=1.1, edgecolor=ACCENT if accent else EDGE,
                                facecolor=ACCENT_FILL if accent else FILL))
    ax.text(x + w / 2, y + h - 0.035, title, ha="center", va="top", fontsize=7.9, fontweight="bold", color=INK)
    ax.text(x + w / 2, y + h - 0.105, "\n".join(lines), ha="center", va="top", fontsize=6.9, color=INK2,
            linespacing=1.35)


def arrow(ax, a, b, dashed=False, rad=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=9, linewidth=1.0, color=INK2,
                                 linestyle=(0, (3, 2)) if dashed else "solid",
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=2, shrinkB=2))


def main():
    fig = plt.figure(figsize=(6.3, 3.2))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1.68)
    ax.set_ylim(0, 0.91)
    ax.axis("off")
    h, w = 0.25, 0.29
    xs = [0.02, 0.35, 0.68, 1.01]
    y1, y2 = 0.47, 0.07
    arrow_right = "→"
    # synthetic branch
    box(ax, xs[0], y1, w, h, "Genetic algorithm",
        ["10,000 genomes", "50 generations (DEAP)", "fitness: validity,", "minimality, sharing"])
    box(ax, xs[1], y1, w, h, "Decoder", [f"genome {arrow_right} loop pair", "9 loop families",
                                         "shared names and data"])
    box(ax, xs[2], y1, w, h, "Dependence oracle", ["runs each loop", "iteration by iteration", "confirms the label"])
    box(ax, xs[3], y1, w, h, "Synthetic set", ["4,000 minimal pairs", "8,000 loops"])
    # real branch
    box(ax, xs[1], y2, w, h, "Real-world loops", ["340 Python snippets", "public repositories", "researchers' labels"])
    box(ax, xs[2], y2, w, h, "Oracle check", ["agreement 97.6%", "Cohen's kappa 0.953", "8 labels adjudicated"])
    box(ax, xs[3], y2, w, h, "Real-world set", ["176 Parallelizable", "164 Undefined"])
    # models and evaluation
    box(ax, 1.36, 0.42, 0.30, 0.33, "Models",
        ["DistilBERT", "(subword text)", "", "LR, SVM, DNN, CNN", "(previous study)", "n-gram LR"], accent=True)
    box(ax, 1.36, 0.02, 0.30, 0.33, "Evaluation",
        ["hybrid", f"synthetic {arrow_right} real", "real only", "", "3 × 10-fold CV", "FPR, AUC, thresholds"])
    for a, b in zip(xs[:3], xs[1:]):
        arrow(ax, (a + w, y1 + h / 2), (b, y1 + h / 2))
    for a, b in zip(xs[1:3], xs[2:]):
        arrow(ax, (a + w, y2 + h / 2), (b, y2 + h / 2))
    arrow(ax, (xs[3] + w, y1 + h / 2), (1.36, y1 + h / 2))
    arrow(ax, (xs[3] + w, y2 + h / 2), (1.36, 0.47))
    arrow(ax, (1.51, 0.42), (1.51, 0.35))
    arrow(ax, (xs[2] + w / 2, y1 + h), (xs[0] + w / 2, y1 + h), dashed=True, rad=0.30)
    ax.text((xs[0] + xs[2] + w) / 2, 0.875, "valid pairs raise the fitness", ha="center", va="center", fontsize=6.8,
            color=INK2, style="italic")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    fig.savefig(OUT)
    print("written", os.path.abspath(OUT))


if __name__ == "__main__":
    main()
