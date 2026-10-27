"""Figures of the paper (PDF, fonts embedded) from results/raw and results/tables.

Colour use: the proposed model (DistilBERT) carries the accent hue, the n-gram reference a second hue,
and the four models of the previous study are drawn in neutral greys and told apart by line style /
position and labels, so identity never relies on colour alone. The per-category chart uses the first three slots of the reference categorical
palette (validated all-pairs) plus distinct markers.
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.metrics import roc_curve  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402
from summarize import MODELS, NAMES, load_runs  # noqa: E402

FIG = os.path.join(common.ROOT, "latex", "figures")
ACCENT = "#2a78d6"
SERIES3 = ["#2a78d6", "#eb6834", "#1baf7a"]
GREY = "#7d7c78"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
STYLES = {"lr": (0, (1, 1.5)), "svm": (0, (4, 1.5)), "dnn": (0, (6, 2, 1, 2)), "cnn": (0, (2, 2)),
          "ngram": (0, (5, 1.5)), "distilbert": "solid"}
SHORT = {"lr": "LR", "svm": "SVM", "dnn": "DNN", "cnn": "CNN", "ngram": "N-gram", "distilbert": "DistilBERT"}
NGRAM = "#eb6834"   # the additional lexical reference gets its own hue
WIDTH = 6.3   # inches, text width of the single-column CAS template
SETTING_LABELS = {"(a) synthetic only -> real": "(a) Synthetic only", "(b) hybrid, real test samples": "(b) Hybrid",
                  "(c) real only": "(c) Real only"}
CATEGORY_LABELS = {"scalar carried between iterations (accumulator/recurrence)": "Carried scalar (accumulator, recurrence)",
                   "output list read inside the loop": "Output list read in the loop",
                   "value used after the loop (live-out)": "Value used after the loop",
                   "container element shared between iterations": "Shared container element",
                   "while loop": "while loop", "recursion (no loop statement)": "Recursion, no loop statement",
                   "explicit loop, map with append": "Explicit loop, map with append",
                   "comprehension (map)": "List comprehension",
                   "explicit loop, writes to own position": "Explicit loop, own position",
                   "not executed (side effects)": "Not executed by the oracle"}

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8.5, "axes.labelsize": 8.5, "axes.titlesize": 9,
    "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 8, "pdf.fonttype": 42,
    "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2,
    "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.8,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
    "lines.linewidth": 1.6, "lines.solid_capstyle": "round",
})


def color(model):
    return ACCENT if model == "distilbert" else NGRAM if model == "ngram" else GREY


def _pooled(setting, model):
    ys, ss = [], []
    for r in load_runs(setting, model):
        keep = np.char.startswith(r["test_ids"].astype(str), "real-")
        ys.append(r["test_y"][keep])
        ss.append(r["test_score"][keep])
    return (np.concatenate(ys), np.concatenate(ss)) if ys else (None, None)


def fig_roc_real():
    fig, axes = plt.subplots(1, 3, figsize=(WIDTH, 2.9), sharey=True)
    titles = {"syn2real": "(a) Synthetic only", "hybrid": "(b) Hybrid", "real": "(c) Real only"}
    for ax, setting in zip(axes, ("syn2real", "hybrid", "real")):
        ax.plot([0, 1], [0, 1], color=GRID, linewidth=1.0, zorder=1)
        ax.axvline(0.05, color=INK2, linewidth=0.6, linestyle=(0, (2, 2)), zorder=1)
        for m in MODELS:
            y, s = _pooled(setting, m)
            if y is None:
                continue
            fpr, tpr, _ = roc_curve(y, s)
            ax.plot(fpr, tpr, color=color(m), linestyle=STYLES[m], linewidth=2.0 if m == "distilbert" else 1.3,
                    label=NAMES[m], zorder=3 if m == "distilbert" else 2)
        ax.set_title(titles[setting], loc="left", color=INK)
        ax.set_xlabel("False positive rate")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1.01)
    axes[0].set_ylabel("True positive rate (recall)")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.0))
    fig.tight_layout(rect=(0, 0.15, 1, 1), w_pad=2.0)
    fig.savefig(os.path.join(FIG, "fig_roc_real.pdf"))
    plt.close(fig)


def fig_real_categories():
    path = os.path.join(common.RESULTS, "tables", "real_code_by_category.csv")
    df = pd.read_csv(path)
    df = df[df.model == "DistilBERT"]
    if df.empty:
        return
    settings = list(dict.fromkeys(df.setting))
    cats = (df.groupby(["category", "label", "n"]).size().reset_index()
            .sort_values(["label", "n"], ascending=[True, True]))
    fig, ax = plt.subplots(figsize=(WIDTH, 0.22 * len(cats) + 0.8))
    markers = ["o", "s", "D"]
    for k, s in enumerate(settings):
        sub = df[df.setting == s].set_index("category")
        ys = np.arange(len(cats)) + (k - 1) * 0.2
        xs = [100 * sub.loc[c, "correct"] if c in sub.index else np.nan for c in cats.category]
        ax.scatter(xs, ys, s=22, marker=markers[k], color=SERIES3[k], label=SETTING_LABELS.get(s, s), zorder=3,
                   edgecolors="white", linewidths=0.6)
    ax.set_yticks(np.arange(len(cats)),
                  [f"{CATEGORY_LABELS.get(c, c)} ({'P' if l == 'Parallelizable' else 'U'}, n = {n})" for c, l, n in
                   zip(cats.category, cats.label, cats.n)])
    ax.set_xlabel("Correctly classified (%)")
    ax.set_xlim(-2, 102)
    ax.grid(axis="y", visible=False)
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, frameon=False)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.savefig(os.path.join(FIG, "fig_real_categories.pdf"))
    plt.close(fig)


def main():
    os.makedirs(FIG, exist_ok=True)
    fig_roc_real()
    fig_real_categories()
    print("figures written to", FIG)


if __name__ == "__main__":
    main()
