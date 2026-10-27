"""Writes the LaTeX tables of the results section from results/tables/*.csv (run summarize.py first).

Two variants are produced, with the same content: latex/tables/*.tex (decimal point) and
latex_ptbr/tables/*.tex (decimal comma). Only the tabular bodies are generated; captions live in
the manuscripts. Values are percentages with one decimal, AUC with three decimals.

  tab_synthetic.tex    surface rules and models on the synthetic test samples of the hybrid scenario
  tab_real.tex         the 340 real-world loops in the three scenarios
  tab_fpr_control.tex  real-only scenario: default threshold and thresholds for a target FPR
  tab_cost.tex         parameters, training and inference time
"""

import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

T = os.path.join(common.RESULTS, "tables")
OUT = {"en": os.path.join(common.ROOT, "latex", "tables"), "pt": os.path.join(common.ROOT, "latex_ptbr", "tables")}
ORDER = ["Logistic regression", "Linear SVM", "DNN", "CNN", "N-gram LR", "DistilBERT"]
KEYS = {"Logistic regression": "lr", "Linear SVM": "svm", "DNN": "dnn", "CNN": "cnn", "N-gram LR": "ngram",
        "DistilBERT": "distilbert"}
PT_NAMES = {"Logistic regression": "Regressão logística", "Linear SVM": "SVM linear", "N-gram LR": "RL com n-gramas"}


def fmt(x, lang, digits=1, pct=True):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "--"
    v = 100 * x if pct else x
    s = f"{v:.{digits}f}"
    return s.replace(".", ",") if lang == "pt" else s


def pm(mean, sd, lang, pct=True, digits=1):
    return f"{fmt(mean, lang, digits, pct)} $\\pm$ {fmt(sd, lang, digits, pct)}"


def name(m, lang, bold=True):
    nm = PT_NAMES.get(m, m) if lang == "pt" else m
    return "\\textbf{" + nm + "}" if bold and m == "DistilBERT" else nm


def write(fname, rows_by_lang):
    for lang, text in rows_by_lang.items():
        os.makedirs(OUT[lang], exist_ok=True)
        with open(os.path.join(OUT[lang], fname), "w", encoding="utf-8") as f:
            f.write(text)


def table_synthetic(summary, audit_rules):
    """Surface rules on the 8,000 samples and models on the synthetic test samples (30 folds)."""
    out = {}
    for lang in ("en", "pt"):
        lines = [f"{lab_en if lang == 'en' else lab_pt} & {fmt(acc, lang)} & {fmt(fpr, lang)} & -- \\\\"
                 for lab_en, lab_pt, acc, fpr in audit_rules]
        lines.append("\\midrule")
        for m in ORDER:
            r = summary[(summary.setting == "hybrid, synthetic test samples") & (summary.model == m)]
            if r.empty:
                continue
            r = r.iloc[0]
            lines.append(f"{name(m, lang)} & {pm(r.accuracy_mean, r.accuracy_sd, lang)} & "
                         f"{pm(r.fpr_mean, r.fpr_sd, lang)} & {fmt(r.auc_mean, lang, 3, pct=False)} \\\\")
        out[lang] = "\n".join(lines) + "\n"
    write("tab_synthetic.tex", out)


def table_real(real):
    labels = {"(a) synthetic only -> real": ("Synthetic $\\rightarrow$ real", "Sintético $\\rightarrow$ real"),
              "(b) hybrid, real test samples": ("Hybrid (real test loops)", "Híbrido (laços reais de teste)"),
              "(c) real only": ("Real only", "Somente real")}
    out = {}
    for lang in ("en", "pt"):
        lines = []
        for key, (lab_en, lab_pt) in labels.items():
            sub = real[real.setting == key]
            if sub.empty:
                continue
            lines.append("\\multicolumn{5}{@{}l}{\\emph{" + (lab_en if lang == "en" else lab_pt) + "}} \\\\")
            for m in ORDER:
                r = sub[sub.model == m]
                if r.empty:
                    continue
                r = r.iloc[0]
                lines.append(f"\\quad {name(m, lang)} & {pm(r.accuracy_mean, r.accuracy_sd, lang)} & "
                             f"{fmt(r.recall_mean, lang)} & {pm(r.fpr_mean, r.fpr_sd, lang)} & "
                             f"{fmt(r.auc_mean, lang, 3, pct=False)} \\\\")
        out[lang] = "\n".join(lines) + "\n"
    write("tab_real.tex", out)


def table_fpr_control(fc):
    """Real-only scenario: thresholds chosen on the real-world validation loops."""
    sub = fc[(fc.setting == "real") & (fc.val_part == "all") & (fc.test_part == "all")]
    out = {}
    for lang in ("en", "pt"):
        lines = []
        for m in ORDER:
            rows = sub[sub.model == KEYS[m]]
            if rows.empty:
                continue
            cells = [fmt(rows.iloc[0].base_fpr_mean, lang), fmt(rows.iloc[0].base_tpr_mean, lang)]
            for alpha in (0.05, 0.01):
                r = rows[np.isclose(rows.alpha, alpha)]
                cells += ["--", "--"] if r.empty else [fmt(r.iloc[0].fpr_mean, lang), fmt(r.iloc[0].tpr_mean, lang)]
            lines.append(f"{name(m, lang)} & " + " & ".join(cells) + " \\\\")
        out[lang] = "\n".join(lines) + "\n"
    write("tab_fpr_control.tex", out)


def table_cost(eff):
    out = {}
    for lang in ("en", "pt"):
        lines = []
        for m in ORDER:
            e = eff[eff.model == m]
            if e.empty:
                continue
            e = e.iloc[0]
            params = f"{int(e.params):,}".replace(",", "." if lang == "pt" else ",")
            lines.append(f"{name(m, lang)} & {params} & {fmt(e.train_time_s_mean, lang, 0, pct=False)} & "
                         f"{fmt(e.infer_ms_per_sample, lang, 2, pct=False)} \\\\")
        out[lang] = "\n".join(lines) + "\n"
    write("tab_cost.tex", out)


def main():
    summary = pd.read_csv(os.path.join(T, "summary.csv"))
    real = pd.read_csv(os.path.join(T, "real_code.csv"))
    fc = pd.read_csv(os.path.join(T, "fpr_control.csv"))
    eff = pd.read_csv(os.path.join(T, "efficiency.csv"))
    audit = json.load(open(os.path.join(T, "synthetic_rules.json"), encoding="utf-8"))
    rules = [(a["label_en"], a["label_pt"], a["accuracy"], a["fpr"]) for a in audit]
    table_synthetic(summary, rules)
    table_real(real)
    table_fpr_control(fc)
    table_cost(eff)
    print("tables written to", OUT["en"], "and", OUT["pt"])


if __name__ == "__main__":
    main()
