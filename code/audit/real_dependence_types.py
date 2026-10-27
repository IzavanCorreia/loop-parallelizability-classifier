"""Groups the 340 real-world samples by dependence type (from the oracle reasons and simple AST
features) -> results/real_dependence_types.csv and a summary printed as a table."""

import ast
import csv
import os
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def has_loop_statement(code):
    try:
        return any(isinstance(n, (ast.For, ast.While)) for n in ast.walk(ast.parse(code)))
    except SyntaxError:
        return False


def nested(code):
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False
    return any(isinstance(m, (ast.For, ast.While)) for n in ast.walk(tree) if isinstance(n, (ast.For, ast.While))
               for m in ast.walk(n) if m is not n)


def category(r):
    reason, code = r["reason"], r["code"]
    if r["oracle"] == "n/a":
        if "no top-level loop" in reason:
            return "recursion (no loop statement)"
        return "not executed (side effects)"
    if r["oracle"] == "Parallelizable":
        if not has_loop_statement(code):
            return "comprehension (map)"
        if ".append(" in code:
            return "explicit loop, map with append"
        return "explicit loop, writes to own position"
    if "loop-carried scalar" in reason:
        return "scalar carried between iterations (accumulator/recurrence)"
    if "appended to and read" in reason:
        return "output list read inside the loop"
    if "element" in reason or "whole" in reason or "index" in reason:
        return "container element shared between iterations"
    if "early exit" in reason:
        return "early exit (break/return)"
    if "while" in reason:
        return "while loop"
    if "live-out" in reason:
        return "value used after the loop (live-out)"
    return "other"


def main():
    rows = list(csv.DictReader(open(os.path.join(ROOT, "results", "real_oracle_before_adjudication.csv"), encoding="utf-8")))
    final = {(m["original_class"], m["original_index"]): m["class"]
             for m in csv.DictReader(open(os.path.join(ROOT, "data", "real", "metadata.csv"), encoding="utf-8"))}
    out_rows = []
    for r in rows:
        out_rows.append({"original_class": r["class"], "original_index": r["index"],
                         "class": final[(r["class"], r["index"])], "oracle": r["oracle"],
                         "category": category(r), "nested_loops": nested(r["code"])})
    with open(os.path.join(ROOT, "results", "real_dependence_types.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0]))
        w.writeheader()
        w.writerows(out_rows)
    for cls in ("Parallelizable", "Undefined"):
        c = Counter(r["category"] for r in out_rows if r["class"] == cls)
        print(f"{cls} (final label after adjudication), n={sum(c.values())}")
        for k, v in c.most_common():
            print(f"  {v:4d}  {k}")
    print("samples with nested loops:", Counter(r["class"] for r in out_rows if r["nested_loops"]))


if __name__ == "__main__":
    main()
