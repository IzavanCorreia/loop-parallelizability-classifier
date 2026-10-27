"""Writes the LaTeX tables of the results section from results/tables/*.csv (run summarize.py first).

Two variants are produced, with the same content: latex/tables/*.tex (decimal point) and
latex_ptbr/tables/*.tex (decimal comma). Only the tabular bodies are generated; captions live in
the manuscripts. Values are percentages with one decimal, AUC with three decimals.
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
PT_NAMES = {"Logistic regression": "Regressão logística", "Linear SVM": "SVM linear", "N-gram LR": "RL com n-gramas"}


def fmt(x, lang, digits=1, pct=True):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "--"
    v = 100 * x if pct else x
    s = f"{v:.{digits}f}"
    return s.replace(".", ",") if lang == "pt" else s


def pm(mean, sd, lang, pct=True, digits=1):
    return f"{fmt(mean, lang, digits, pct)} $\\pm$ {fmt(sd, lang, digits, pct)}"


def name(m, lang):
    return PT_NAMES.get(m, m) if lang == "pt" else m


def pval(p, lang):
    if p < 0.001:
        return "$<$0.001" if lang == "en" else "$<$0,001"
    return fmt(p, lang, 3, pct=False)


def write(fname, rows_by_lang):
    for lang, text in rows_by_lang.items():
        os.makedirs(OUT[lang], exist_ok=True)
        with open(os.path.join(OUT[lang], fname), "w", encoding="utf-8") as f:
            f.write(text)


def table_hybrid(summary):
    """Main comparison: all test samples of the hybrid scenario (30 folds)."""
    out = {}
    for lang in ("en", "pt"):
        lines = []
        for m in ORDER:
            r = summary[(summary.setting == "hybrid") & (summary.model == m)]
            if r.empty:
                continue
            r = r.iloc[0]
            cells = [pm(r[f"{k}_mean"], r[f"{k}_sd"], lang) for k in ("accuracy", "precision", "recall", "f1", "fpr")]
            cells.append(pm(r["auc_mean"], r["auc_sd"], lang, pct=False, digits=3))
            row = f"{name(m, lang)} & " + " & ".join(cells) + " \\\\"
            lines.append(("\\textbf{" + name(m, lang) + "}" + row[len(name(m, lang)):]) if m == "DistilBERT" else row)
        out[lang] = "\n".join(lines) + "\n"
    write("tab_hybrid.tex", out)


def table_synthetic(summary, audit_rules):
    """Validation of the synthetic set: surface rules and models on the synthetic test samples."""
    out = {}
    for lang in ("en", "pt"):
        lines = []
        for label_en, label_pt, acc, fpr in audit_rules:
            lab = label_en if lang == "en" else label_pt
            lines.append(f"{lab} & {fmt(acc, lang)} & -- & {fmt(fpr, lang)} \\\\")
        lines.append("\\midrule")
        for m in ORDER:
            r = summary[(summary.setting == "hybrid, synthetic test samples") & (summary.model == m)]
            if r.empty:
                continue
            r = r.iloc[0]
            lines.append(f"{name(m, lang)} & {pm(r.accuracy_mean, r.accuracy_sd, lang)} & "
                         f"{fmt(r.accuracy_min, lang)} & {pm(r.fpr_mean, r.fpr_sd, lang)} \\\\")
        out[lang] = "\n".join(lines) + "\n"
    write("tab_synthetic.tex", out)


def table_real(real):
    labels = {"(a) synthetic only -> real": ("Synthetic $\\rightarrow$ real", "Sintético $\\rightarrow$ real"),
              "(b) hybrid, real test samples": ("Hybrid (real test samples)", "Híbrido (amostras reais de teste)"),
              "(c) real only": ("Real only", "Somente real")}
    out = {}
    for lang in ("en", "pt"):
        lines = []
        for key, (len_, lpt) in labels.items():
            sub = real[real.setting == key]
            if sub.empty:
                continue
            lines.append("\\multicolumn{5}{@{}l}{\\emph{" + (len_ if lang == "en" else lpt) + "}} \\\\")
            for m in ORDER:
                r = sub[sub.model == m]
                if r.empty:
                    continue
                r = r.iloc[0]
                ci_acc = f"[{fmt(r.accuracy_boot_low, lang)}, {fmt(r.accuracy_boot_high, lang)}]"
                ci_fpr = f"[{fmt(r.fpr_boot_low, lang)}, {fmt(r.fpr_boot_high, lang)}]"
                nm = name(m, lang)
                nm = "\\textbf{" + nm + "}" if m == "DistilBERT" else nm
                lines.append(f"\\quad {nm} & {pm(r.accuracy_mean, r.accuracy_sd, lang)} {ci_acc} & "
                             f"{fmt(r.recall_mean, lang)} & {pm(r.fpr_mean, r.fpr_sd, lang)} {ci_fpr} & "
                             f"{fmt(r.auc_mean, lang, 3, pct=False)} \\\\")
        out[lang] = "\n".join(lines) + "\n"
    write("tab_real.tex", out)


def table_fpr_control(fc):
    # (setting, validation samples, test samples): group label in English and Portuguese
    groups = [(("hybrid", "all", "all"), ("Hybrid: all test samples; threshold from all validation samples",
                                          "Híbrido: todas as amostras de teste; limiar de toda a validação")),
              (("hybrid", "real", "real"), ("Hybrid: real test samples; threshold from real validation samples",
                                            "Híbrido: amostras reais de teste; limiar da validação real")),
              (("real", "all", "all"), ("Real only", "Somente real")),
              (("syn2real", "all", "all"), ("Synthetic $\\rightarrow$ real: threshold from synthetic validation samples",
                                            "Sintético $\\rightarrow$ real: limiar da validação sintética"))]
    keys = {"Logistic regression": "lr", "Linear SVM": "svm", "DNN": "dnn", "CNN": "cnn", "N-gram LR": "ngram", "DistilBERT": "distilbert"}
    out = {}
    for lang in ("en", "pt"):
        lines = []
        for (setting, vpart, tpart), labels in groups:
            sub = fc[(fc.setting == setting) & (fc.val_part == vpart) & (fc.test_part == tpart)]
            if sub.empty:
                continue
            lines.append("\\multicolumn{7}{@{}l}{\\emph{" + labels[0 if lang == "en" else 1] + "}} \\\\")
            for m in ORDER:
                rows = sub[sub.model == keys[m]]
                if rows.empty:
                    continue
                cells = [fmt(rows.iloc[0].base_fpr_mean, lang), fmt(rows.iloc[0].base_tpr_mean, lang)]
                for alpha in (0.05, 0.01):
                    r = rows[np.isclose(rows.alpha, alpha)]
                    cells += ["--", "--"] if r.empty else [fmt(r.iloc[0].fpr_mean, lang), fmt(r.iloc[0].tpr_mean, lang)]
                nm = name(m, lang)
                nm = "\\textbf{" + nm + "}" if m == "DistilBERT" else nm
                lines.append(f"\\quad {nm} & " + " & ".join(cells) + " \\\\")
        out[lang] = "\n".join(lines) + "\n"
    write("tab_fpr_control.tex", out)


def table_stats(friedman, pairwise):
    labels = {"hybrid": ("Hybrid, all test samples", "Híbrido, todas as amostras de teste"),
              "real": ("Real only", "Somente real")}
    out = {}
    for lang in ("en", "pt"):
        lines = []
        for setting, lab in labels.items():
            sub = pairwise[pairwise.setting == setting]
            if sub.empty:
                continue
            fr = friedman[friedman.setting == setting]
            head = lab[0 if lang == "en" else 1]
            if not fr.empty:
                p = fr.iloc[0].p
                ptxt = "p < 0.001" if p < 0.001 else f"p = {p:.3f}"
                chi = f"{fr.iloc[0].statistic:.1f}"
                if lang == "pt":
                    ptxt, chi = ptxt.replace(".", "{,}"), chi.replace(".", "{,}")
                head += f" (Friedman $\\chi^2 = {chi}$, ${ptxt}$)"
            lines.append("\\multicolumn{5}{@{}l}{\\emph{" + head + "}} \\\\")
            for _, r in sub.iterrows():
                other = r.test.replace("DistilBERT vs ", "")
                lines.append(f"\\quad DistilBERT vs.\\ {name(other, lang)} & {fmt(r.mean_diff_acc, lang)} & "
                             f"{pval(r.wilcoxon_p_holm, lang)} & {fmt(r.corrected_t, lang, 2, pct=False)} & "
                             f"{pval(r.corrected_t_p_holm, lang)} \\\\")
        out[lang] = "\n".join(lines) + "\n"
    write("tab_stats.tex", out)


def table_cost(eff, stab):
    out = {}
    for lang in ("en", "pt"):
        lines = []
        for m in ORDER:
            e = eff[eff.model == m]
            s = stab[(stab.setting == "hybrid") & (stab.model == m)]
            if e.empty or s.empty:
                continue
            e, s = e.iloc[0], s.iloc[0]
            params = f"{int(e.params):,}".replace(",", "." if lang == "pt" else ",")
            lines.append(f"{name(m, lang)} & {params} & {fmt(e.train_time_s_mean, lang, 0, pct=False)} & "
                         f"{fmt(e.infer_ms_per_sample, lang, 2, pct=False)} & {fmt(s.worst_acc, lang)} & "
                         f"{fmt(s.max_fpr, lang)} \\\\")
        out[lang] = "\n".join(lines) + "\n"
    write("tab_cost.tex", out)


def main():
    summary = pd.read_csv(os.path.join(T, "summary.csv"))
    real = pd.read_csv(os.path.join(T, "real_code.csv"))
    fc = pd.read_csv(os.path.join(T, "fpr_control.csv"))
    pairwise = pd.read_csv(os.path.join(T, "tests_pairwise.csv"))
    friedman = pd.read_csv(os.path.join(T, "tests_friedman.csv"))
    eff = pd.read_csv(os.path.join(T, "efficiency.csv"))
    stab = pd.read_csv(os.path.join(T, "stability.csv"))
    audit = json.load(open(os.path.join(T, "synthetic_rules.json"), encoding="utf-8"))
    rules = [(a["label_en"], a["label_pt"], a["accuracy"], a["fpr"]) for a in audit]
    table_hybrid(summary)
    table_synthetic(summary, rules)
    table_real(real)
    table_fpr_control(fc)
    table_stats(friedman, pairwise)
    table_cost(eff, stab)
    print("tables written to", OUT["en"], "and", OUT["pt"])


if __name__ == "__main__":
    main()
