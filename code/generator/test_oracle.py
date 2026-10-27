"""Hand-written cases with known labels for the dependence oracle."""

import sys
from oracle import analyze, PARALLELIZABLE as P, UNDEFINED as U

CASES = [
    (P, "def f():\n    xs = [1, 2, 3, 4]\n    res = []\n    for x in xs:\n        res.append(x * 2)\n    return res"),
    (P, "def f():\n    xs = [1, 2, 3, 4]\n    res = []\n    for x in xs:\n        t = x * 3\n        t += 1\n        res.append(t)\n    return res"),
    (U, "def f():\n    xs = [1, 2, 3, 4]\n    res = []\n    t = 0\n    for x in xs:\n        t += x * 3\n        res.append(t)\n    return res"),
    (P, "def f():\n    src = [5, 3, 8, 1]\n    res = [0] * len(src)\n    for i in range(1, len(src)):\n        res[i] = src[i] + src[i - 1]\n    return res"),
    (U, "def f():\n    src = [5, 3, 8, 1]\n    res = [0] * len(src)\n    for i in range(1, len(src)):\n        res[i] = res[i - 1] + src[i]\n    return res"),
    (U, "def f():\n    xs = [3, 1, 4, 1, 5, 9]\n    hist = [0] * 3\n    for x in xs:\n        hist[x % 3] += 1\n    return hist"),
    (P, "def f():\n    xs = [3, 1, 4, 1, 5, 9]\n    out = [0] * len(xs)\n    for i, x in enumerate(xs):\n        out[i] = x % 3\n    return out"),
    (U, "def f():\n    xs = [3, 1, 4]\n    prev = 0\n    res = []\n    for x in xs:\n        d = x - prev\n        prev = x\n        res.append(d)\n    return res"),
    (P, "def f():\n    xs = [3, 1, 4]\n    base = 2\n    res = []\n    for x in xs:\n        d = x - base\n        res.append(d)\n    return res"),
    (U, "def f():\n    xs = [3, -1, 4]\n    res = []\n    for x in xs:\n        if x < 0:\n            break\n        res.append(x)\n    return res"),
    (P, "def f():\n    xs = [3, -1, 4]\n    res = []\n    for x in xs:\n        if x < 0:\n            continue\n        res.append(x)\n    return res"),
    (U, "def f(n):\n    res = []\n    for i in range(n):\n        res.append(len(res) + i)\n    return res"),
    (U, "xs = [1, 2, 3]\ntotal = 0\nfor x in xs:\n    total = total + x\nprint(total)"),
    (U, "def f():\n    xs = [1, 2, 3]\n    for x in xs:\n        ultimo = x * 2\n    return ultimo"),
    (P, "import math\n\ndef f(n):\n    res = []\n    for i in range(n):\n        res.append(round(math.sin(i * 0.1), 2))\n    return res"),
    (U, "def f():\n    m = [[1, 2], [3, 4], [5, 6]]\n    for i in range(1, len(m)):\n        m[i][0] += m[i - 1][0]\n    return m"),
    (P, "def f():\n    m = [[1, 2], [3, 4], [5, 6]]\n    res = []\n    for row in m:\n        res.append(sum(v * 2 for v in row))\n    return res"),
    (U, "def f():\n    xs = [3, 9, 4, 12]\n    lim = 5\n    res = []\n    for x in xs:\n        if x > lim:\n            lim = x\n        res.append(lim)\n    return res"),
    (P, "def f():\n    words = ['a', 'b']\n    d = {}\n    for w in words:\n        d[w] = w.upper()\n    return d"),
    (U, "def f():\n    words = ['a', 'b', 'a']\n    d = {}\n    for w in words:\n        d[w] = d.get(w, 0) + 1\n    return d"),
    (U, "i = 0\nwhile i < 3:\n    i += 1"),
    (U, "vals = [1, 2, 2, 3]\nseen = set()\nout = []\nfor v in vals:\n    if v not in seen:\n        out.append(v)\n        seen.add(v)\nprint(out)"),
    (P, "vals = [1, 2, 2, 3]\nallowed = {1, 3}\nout = []\nfor v in vals:\n    if v in allowed:\n        out.append(v)\nprint(out)"),
    (U, "def f(g={'A': ['B'], 'B': ['C'], 'C': []}):\n    fe = {k: set(v) for k, v in g.items()}\n    for k in g:\n        for i in g:\n            if k in fe[i]:\n                fe[i].update(fe[k])\n    return fe"),
]

if __name__ == "__main__":
    bad = 0
    for expected, code in CASES:
        r = analyze(code)
        ok = r["label"] == expected
        bad += not ok
        print(("OK  " if ok else "FAIL"), expected, "->", r["label"], "|", r["reason"])
    print(f"{len(CASES) - bad}/{len(CASES)} correct")
    sys.exit(1 if bad else 0)
