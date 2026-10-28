"""Additional analyses of existing results (no new experiments), used by the extended manuscript:

- ga_evolution.csv: validity, fitness and diversity of the GA population per generation (data/synthetic/ga_log.csv)
- ga_summary.csv: first/last-generation values and the range of distinct signatures
- real_errors.csv: DistilBERT (real-only scenario) on each real-world loop, over the 3 repetitions
- error_summary.csv: loops misclassified in all repetitions, by class and dependence type
- score_summary.csv: DistilBERT scores on the real-world loops per scenario and class
- tests_fpr.csv: Friedman, Wilcoxon and corrected resampled t-tests (Holm) on the fold-level FPR, real-only scenario
- family_accuracy.csv: DistilBERT and n-gram accuracy on the synthetic test samples of the hybrid scenario, by family
Figures: latex/figures/fig_ga_evolution.pdf and fig_scores_real.pdf (same style as figures.py)."""

import os
import re
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402
import figures  # noqa: E402  (style, palette, WIDTH)
import summarize  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402

OUT = os.path.join(common.RESULTS, "tables")
FIG = figures.FIG
SETTINGS = [("syn2real", "(a) Synthetic only"), ("hybrid", "(b) Hybrid"), ("real", "(c) Real only")]


def ga_tables():
    log = pd.read_csv(os.path.join(common.DATA, "synthetic", "ga_log.csv"))
    log.to_csv(os.path.join(OUT, "ga_evolution.csv"), index=False)
    first, last = log.iloc[0], log.iloc[-1]
    summary = pd.DataFrame([{
        "generations": int(last.gen), "population": 10000,
        "valid_first": first.valid_frac, "valid_last": last.valid_frac,
        "fit_mean_first": first.fit_mean, "fit_mean_last": last.fit_mean,
        "fit_max_first": first.fit_max, "fit_max_last": last.fit_max,
        "signatures_min": int(log.distinct_signatures.min()), "signatures_max": int(log.distinct_signatures.max()),
        "signatures_first": int(first.distinct_signatures), "signatures_last": int(last.distinct_signatures),
        "valid_seen_last": int(last.valid_unique_seen), "minutes": last.elapsed_s / 60}])
    summary.to_csv(os.path.join(OUT, "ga_summary.csv"), index=False)
    return log, summary.iloc[0]


def fig_ga(log):
    fig, axes = plt.subplots(1, 3, figsize=(figures.WIDTH, 2.1))
    g = log.gen
    axes[0].plot(g, 100 * log.valid_frac, color=figures.ACCENT)
    axes[0].set_title("(a) Valid individuals (%)", loc="left")
    axes[1].plot(g, log.fit_max, color=figures.INK2, linestyle="--", label="maximum")
    axes[1].plot(g, log.fit_mean, color=figures.ACCENT, label="mean")
    axes[1].set_title("(b) Fitness", loc="left")
    axes[1].set_ylim(2.75, 3.05)
    axes[1].legend(frameon=False, loc="center right", bbox_to_anchor=(1, 0.64))
    axes[2].plot(g, log.distinct_signatures / 1000, color=figures.ACCENT)
    axes[2].set_title("(c) Signatures (thousands)", loc="left")
    axes[2].set_ylim(0, 10)
    for ax in axes:
        ax.set_xlabel("Generation")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_ga_evolution.pdf"))
    plt.close(fig)


def pooled_distilbert(setting):
    return summarize.pooled_real(setting)["distilbert"]


def error_tables():
    real = {it["id"]: it for it in common.load_real()}
    runs = pooled_distilbert("real")
    rows = {}
    for rep, d in runs.items():
        for i, y, s in zip(d["ids"], d["y"], d["s"]):
            r = rows.setdefault(i, {"id": i, "label": "Parallelizable" if y == 1 else "Undefined",
                                    "category": real[i]["category"], "scores": []})
            r["scores"].append(float(s))
    out = []
    for r in rows.values():
        s = np.array(r["scores"])
        pred_p = s > 0.5
        correct = int((pred_p == (r["label"] == "Parallelizable")).sum())
        out.append({"id": r["id"], "label": r["label"], "category": r["category"], "reps": len(s),
                    "mean_score": s.mean(), "min_score": s.min(), "max_score": s.max(), "correct_reps": correct,
                    "tokens": len(real[r["id"]]["code"].split())})
    df = pd.DataFrame(out).sort_values(["correct_reps", "label", "mean_score"])
    df.to_csv(os.path.join(OUT, "real_errors.csv"), index=False)
    always_wrong = df[df.correct_reps == 0]
    summary = (always_wrong.groupby(["label", "category"]).size().reset_index(name="loops"))
    # persistent false negatives whose surface resembles a recurrence: a read at a neighbor index (x[i-1]) or a
    # nested loop that carries a value
    neighbor = lambda code: re.search(r"\[\s*\w+\s*-\s*\d\s*\]", code) is not None
    nested = lambda code: len(re.findall(r"^\s*for\b", code, re.M)) > 1
    fn = always_wrong[always_wrong.label == "Parallelizable"]
    look_like_recurrence = sum(neighbor(real[i]["code"]) or nested(real[i]["code"]) for i in fn.id)
    totals = pd.DataFrame([{"label": "all", "category": "always wrong", "loops": len(always_wrong)},
                           {"label": "Undefined", "category": "always wrong (false positives)",
                            "loops": int((always_wrong.label == "Undefined").sum())},
                           {"label": "Parallelizable", "category": "always wrong (false negatives)",
                            "loops": int((always_wrong.label == "Parallelizable").sum())},
                           {"label": "all", "category": "right in some repetitions only",
                            "loops": int(((df.correct_reps > 0) & (df.correct_reps < df.reps)).sum())},
                           {"label": "Parallelizable", "category": "always wrong, neighbor read or nested loop",
                            "loops": int(look_like_recurrence)}])
    pd.concat([totals, summary]).to_csv(os.path.join(OUT, "error_summary.csv"), index=False)
    return df


def score_tables():
    rows, data = [], {}
    for setting, title in SETTINGS:
        d = pooled_distilbert(setting)
        y = np.concatenate([v["y"] for v in d.values()])
        s = np.concatenate([v["s"] for v in d.values()])
        data[setting] = (y, s)
        for label, cls in ((1, "Parallelizable"), (0, "Undefined")):
            v = s[y == label]
            rows.append({"setting": setting, "class": cls, "n": len(v), "median": np.median(v),
                         "q25": np.percentile(v, 25), "q75": np.percentile(v, 75),
                         "above_05": (v > 0.5).mean(), "above_09": (v > 0.9).mean(), "below_01": (v < 0.1).mean()})
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "score_summary.csv"), index=False)
    return data


def family_accuracy():
    """Accuracy of DistilBERT and of the n-gram model on the synthetic test samples of the hybrid scenario, by
    family of minimal pairs (all repetitions and folds pooled; threshold 0.5 on the probability)."""
    meta = pd.read_csv(os.path.join(common.DATA, "synthetic", "metadata.csv"))
    family = dict(zip(meta.pair_id, meta.family))
    rows = []
    for model in ("distilbert", "ngram"):
        for run in summarize.load_runs("hybrid", model):
            for i, y, s in zip(run["test_ids"], run["test_y"], run["test_score"]):
                i = str(i)
                if i.startswith("syn"):
                    rows.append({"model": summarize.NAMES[model], "family": family[int(i.split("-")[2])],
                                 "correct": int((s > 0.5) == y)})
    out = (pd.DataFrame(rows).groupby(["family", "model"]).correct.agg(["mean", "size"]).reset_index()
           .rename(columns={"mean": "accuracy", "size": "predictions"}))
    out.to_csv(os.path.join(OUT, "family_accuracy.csv"), index=False)
    return out


def fpr_tests():
    """Friedman over all models and DistilBERT against each model (Wilcoxon and corrected resampled t-test, Holm)
    on the fold-level false positive rate of the real-only scenario, as summarize.py does for accuracy."""
    df = pd.read_csv(os.path.join(OUT, "folds_real.csv"))
    piv = df.pivot_table(index=["rep", "fold"], columns="model", values="fpr")
    models = [m for m in summarize.MODELS if m in piv.columns]
    piv = piv[models].dropna()
    chi, p = summarize.stats.friedmanchisquare(*[piv[m] for m in models])
    runs = summarize.load_runs("real", "distilbert")
    n_train = np.mean([r["info"]["n_train"] + r["info"]["n_val"] for r in runs])
    n_test = np.mean([r["info"]["n_test"] for r in runs])
    rows = []
    for m in models:
        if m == "distilbert":
            continue
        diff = piv["distilbert"] - piv[m]
        t, pt = summarize.corrected_t(diff, n_train, n_test)
        rows.append({"test": f"DistilBERT vs {summarize.NAMES[m]}", "mean_diff_fpr": diff.mean(),
                     "wilcoxon_p": summarize.stats.wilcoxon(piv["distilbert"], piv[m]).pvalue,
                     "corrected_t": t, "corrected_t_p": pt, "n": len(diff)})
    for key in ("wilcoxon_p", "corrected_t_p"):
        for row, adj in zip(rows, summarize.holm(np.array([r[key] for r in rows]))):
            row[key + "_holm"] = adj
    out = pd.DataFrame([{"test": "Friedman (FPR, all models)", "statistic": chi, "friedman_p": p, "n": len(piv)}] + rows)
    out.insert(0, "setting", "real")
    out.to_csv(os.path.join(OUT, "tests_fpr.csv"), index=False)
    return out


def fig_scores(data):
    fig, axes = plt.subplots(1, 3, figsize=(figures.WIDTH, 2.3), sharey=True)
    bins = np.linspace(0, 1, 21)
    for ax, (setting, title) in zip(axes, SETTINGS):
        y, s = data[setting]
        ax.hist(s[y == 1], bins=bins, histtype="step", linewidth=1.6, color=figures.ACCENT, label="Parallelizable")
        ax.hist(s[y == 0], bins=bins, histtype="step", linewidth=1.6, color=figures.NGRAM, linestyle="--",
                label="Undefined")
        ax.axvline(0.5, color=figures.INK2, linewidth=0.6, linestyle=(0, (2, 2)))
        ax.set_title(title, loc="left")
        ax.set_xlabel("DistilBERT score")
    axes[0].set_ylabel("Predictions")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False)
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    fig.savefig(os.path.join(FIG, "fig_scores_real.pdf"))
    plt.close(fig)


def main():
    os.makedirs(FIG, exist_ok=True)
    log, ga = ga_tables()
    fig_ga(log)
    errors = error_tables()
    data = score_tables()
    fig_scores(data)
    tests = fpr_tests()
    families = family_accuracy()
    print(ga.to_string())
    print(tests.to_string())
    print(families.pivot(index="family", columns="model", values="accuracy").round(3).to_string())
    print(pd.read_csv(os.path.join(OUT, "error_summary.csv")).to_string())
    print(pd.read_csv(os.path.join(OUT, "score_summary.csv")).round(3).to_string())


if __name__ == "__main__":
    main()
