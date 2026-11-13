"""Accuracy and FPR of one-line surface rules on the synthetic set -> results/tables/synthetic_rules.json, and of
rules of the same kind on the 340 real-world loops -> results/tables/real_rules.json.

Each rule predicts Undefined (0) or Parallelizable (1) from a surface property of the sample."""

import ast
import json
import os
import re

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SEP = "=" * 40
LABELS = {
    "literal-on-RHS rule": ("Rule: no literal on the right-hand side $\\rightarrow$ U",
                            "Regra: sem literal no lado direito $\\rightarrow$ U"),
    "has '+=' -> Undefined": ("Rule: contains \\texttt{+=} $\\rightarrow$ U", "Regra: contém \\texttt{+=} $\\rightarrow$ U"),
    "has 'break' -> Undefined": ("Rule: contains \\texttt{break} $\\rightarrow$ U",
                                 "Regra: contém \\texttt{break} $\\rightarrow$ U"),
    "longer than median -> Undefined": ("Rule: longer than the median $\\rightarrow$ U",
                                        "Regra: mais longo que a mediana $\\rightarrow$ U"),
}


def load(path):
    txt = open(path, encoding="utf-8").read()
    return [re.sub(r"^Code \d+:\s*\n", "", c.strip()) for c in txt.split(SEP) if c.strip()]


def metrics(y, p):
    tp, tn = int(((p == 1) & (y == 1)).sum()), int(((p == 0) & (y == 0)).sum())
    fp = int(((p == 1) & (y == 0)).sum())
    return (tp + tn) / len(y), fp / (y == 0).sum()


def surface_rules(codes):
    lit_rhs = re.compile(r"^\s*for\s+\w+\s+in\s+range\([^)]*\):\s*\n\s+\w+\s*=\s*(.+)$", re.M)

    def literal_rule(c):   # first assignment of a range loop has no numeric literal on the right -> Undefined
        return 0 if any(not re.search(r"\d", m.group(1)) for m in lit_rhs.finditer(c)) else 1

    med = np.median([len(c) for c in codes])
    return {
        "literal-on-RHS rule": literal_rule,
        "has '+=' -> Undefined": lambda c: 0 if "+=" in c else 1,
        "has 'break' -> Undefined": lambda c: 0 if "break" in c else 1,
        "longer than median -> Undefined": lambda c: 0 if len(c) > med else 1,
    }


def comprehension_only(code):
    """True when the sample has no loop statement and builds its result with a comprehension."""
    tree = ast.parse(code)
    if any(isinstance(n, (ast.For, ast.While)) for n in ast.walk(tree)):
        return False
    return any(isinstance(n, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)) for n in ast.walk(tree))


def real_rules():
    """Surface rules on the real-world loops; the keyword rules match whole words."""
    P = load(os.path.join(ROOT, "data", "real", "Parallelizable_codes.py"))
    U = load(os.path.join(ROOT, "data", "real", "Undefined_codes.py"))
    codes = P + U
    y = np.array([1] * len(P) + [0] * len(U))
    med = np.median([len(c) for c in codes])
    kw = lambda word: (lambda c: re.search(rf"\b{word}\b", c) is not None)
    rules = {
        "has '+=' -> Undefined": lambda c: "+=" in c,
        "has 'while' -> Undefined": kw("while"),
        "has 'break' -> Undefined": kw("break"),
        "has '+=', 'while' or 'break' -> Undefined": lambda c: "+=" in c or kw("while")(c) or kw("break")(c),
        "longer than median -> Undefined": lambda c: len(c) > med,
        "not a comprehension -> Undefined": lambda c: not comprehension_only(c),
    }
    out = []
    for key, is_undefined in rules.items():
        acc, fpr = metrics(y, np.array([0 if is_undefined(c) else 1 for c in codes]))
        out.append({"rule": key, "accuracy": float(acc), "fpr": float(fpr)})
        print(f"real: {key:45s} acc={acc*100:.2f}% FPR={fpr*100:.2f}%")
    json.dump(out, open(os.path.join(ROOT, "results", "tables", "real_rules.json"), "w", encoding="utf-8"), indent=2)


def main():
    P = load(os.path.join(ROOT, "data", "synthetic", "Parallelizable_codes.py"))
    U = load(os.path.join(ROOT, "data", "synthetic", "Undefined_codes.py"))
    codes = P + U
    y = np.array([1] * len(P) + [0] * len(U))
    out = []
    for key, rule in surface_rules(codes).items():
        acc, fpr = metrics(y, np.array([rule(c) for c in codes]))
        out.append({"rule": key, "label_en": LABELS[key][0], "label_pt": LABELS[key][1],
                    "accuracy": float(acc), "fpr": float(fpr)})
        print(f"{key:35s} acc={acc*100:.2f}% FPR={fpr*100:.2f}%")
    path = os.path.join(ROOT, "results", "tables", "synthetic_rules.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(out, open(path, "w", encoding="utf-8"), indent=2)
    real_rules()


if __name__ == "__main__":
    main()
