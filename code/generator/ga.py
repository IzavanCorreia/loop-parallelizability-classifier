"""Genetic algorithm (DEAP) that evolves loop-pair genomes and builds the synthetic dataset.

The evolutionary set-up keeps the parameters of the earlier generators (population of 10,000,
50 generations, roulette selection, crossover probability 0.9, mutation probability 0.1). The
fitness of a genome is

    f = 1 + minimality + sharing      if both variants compile, run and the dependence oracle
                                       confirms Parallelizable for P and Undefined for U
    f = 0.01                          otherwise

where *minimality* (0..1) rewards pairs whose two variants differ in few tokens and *sharing*
(0..1) is a fitness-sharing term that favours structural signatures that are rare in the current
population, which keeps the population diverse. Every valid pair found during the run goes to an
archive, from which the final dataset is sampled with the same number of pairs per loop family.

Usage: python ga.py --out ../../data/synthetic [--pop 10000 --ngen 50 --pairs 4000]
"""

import argparse
import builtins
import csv
import difflib
import hashlib
import json
import keyword
import os
import random
import re
import time
from collections import Counter, defaultdict
from multiprocessing import Pool

import numpy as np
from deap import base, creator, tools, algorithms

from loopgen import decode, N_GENES, GENE_MAX, FAMILIES, NUM_EXPR
from oracle import analyze, PARALLELIZABLE, UNDEFINED

BUILTIN_NAMES = set(dir(builtins))
TOKEN_RE = re.compile(r"[A-Za-z_]\w*|\d+\.?\d*|\S")
SEP = "=" * 40


def tokens(code):
    return TOKEN_RE.findall(code)


def identifiers(toks):
    """User-defined names (keywords and builtins such as round/len are not counted)."""
    return {t for t in toks if (t[0].isalpha() or t[0] == "_") and not keyword.iskeyword(t)
            and t not in BUILTIN_NAMES}


def normalise(code):
    code = re.sub(r"'[^']*'|\"[^\"]*\"", "S", code)
    code = re.sub(r"\b[A-Za-z_]\w*\b", "V", code)
    return re.sub(r"\b\d+(\.\d+)?\b", "N", code)


def evaluate_genome(genome):
    """Worker-side evaluation. Returns a dict (picklable) describing the pair."""
    try:
        pair = decode(genome)
    except Exception as e:  # noqa: BLE001
        return {"valid": False, "why": f"decode: {e}"}
    rp, ru = analyze(pair["P"]), analyze(pair["U"])
    if rp["label"] != PARALLELIZABLE or ru["label"] != UNDEFINED:
        return {"valid": False, "why": f"oracle P={rp['label']} U={ru['label']}"}
    tp, tu = tokens(pair["P"]), tokens(pair["U"])
    if identifiers(tp) != identifiers(tu):
        # a name used by only one variant would identify the class by itself
        return {"valid": False, "why": "asymmetric identifiers"}
    sm = difflib.SequenceMatcher(a=tp, b=tu, autojunk=False)
    changed = sum(max(i2 - i1, j2 - j1) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal")
    minimality = 1.0 - changed / max(len(tp), len(tu))
    meta = dict(pair["meta"])
    sig = (meta["family"], meta["form"], meta["wrapper"], meta["kind"], meta["lang"],
           genome[11] % len(NUM_EXPR), genome[16] % 16)
    return {"valid": True, "P": pair["P"], "U": pair["U"], "meta": meta, "minimality": minimality,
            "signature": sig, "reason_U": ru["reason"], "n_tokens": len(tp)}


def sel_roulette(individuals, k):
    """Roulette-wheel (fitness-proportionate) selection with replacement; equivalent to
    deap.tools.selRoulette but vectorised, which matters for a population of 10,000."""
    fits = np.array([ind.fitness.values[0] for ind in individuals], dtype=float)
    idx = np.random.choice(len(individuals), size=k, replace=True, p=fits / fits.sum())
    return [individuals[i] for i in idx]


def setup_deap():
    if not hasattr(creator, "FitnessMax"):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
    tb = base.Toolbox()
    tb.register("gene", random.randrange, GENE_MAX)
    tb.register("individual", tools.initRepeat, creator.Individual, tb.gene, n=N_GENES)
    tb.register("population", tools.initRepeat, list, tb.individual)
    tb.register("mate", tools.cxOnePoint)
    tb.register("mutate", tools.mutUniformInt, low=0, up=GENE_MAX - 1, indpb=0.1)
    tb.register("select", sel_roulette)
    return tb


def run(args):
    random.seed(args.seed)
    np.random.seed(args.seed)
    tb = setup_deap()
    cache, archive, archive_keys = {}, defaultdict(list), set()
    seen_per_family = Counter()
    rng_archive = random.Random(args.seed + 1)
    log = []
    pool = Pool(args.workers)

    def evaluate(population):
        todo = [tuple(ind) for ind in population if tuple(ind) not in cache]
        todo = list(dict.fromkeys(todo))
        for genome, result in zip(todo, pool.map(evaluate_genome, todo, chunksize=64)):
            # the cache keeps only what the fitness needs; full pairs go to a bounded archive
            cache[genome] = {k: result.get(k) for k in ("valid", "minimality", "signature")}
            if result["valid"]:
                # reservoir sampling per family: the archive is a uniform sample of every valid,
                # unique pair met during the whole run (not only the first generations)
                fam = result["meta"]["family"]
                key = hashlib.md5((result["P"] + SEP + result["U"]).encode()).hexdigest()
                if key in archive_keys:
                    continue
                archive_keys.add(key)
                seen_per_family[fam] += 1
                entry = dict(result, genome=list(genome), key=key)
                bucket = archive[fam]
                if len(bucket) < args.archive_cap:
                    bucket.append(entry)
                else:
                    j = rng_archive.randrange(seen_per_family[fam])
                    if j < args.archive_cap:
                        bucket[j] = entry
        # fitness sharing over the structural signatures present in this population
        sigs = Counter(cache[tuple(ind)]["signature"] for ind in population if cache[tuple(ind)]["valid"])
        max_count = max(sigs.values()) if sigs else 1
        for ind in population:
            r = cache[tuple(ind)]
            if r["valid"]:
                sharing = 1.0 - (sigs[r["signature"]] - 1) / max_count
                ind.fitness.values = (1.0 + r["minimality"] + sharing,)
            else:
                ind.fitness.values = (0.01,)

    t0 = time.time()
    pop = tb.population(n=args.pop)
    evaluate(pop)
    for gen in range(args.ngen + 1):
        if gen > 0:
            offspring = tb.select(pop, len(pop))
            offspring = algorithms.varAnd(offspring, tb, args.cxpb, args.mutpb)
            evaluate(offspring)
            pop = offspring
        fits = [ind.fitness.values[0] for ind in pop]
        valid = [cache[tuple(ind)]["valid"] for ind in pop]
        sigs = {cache[tuple(ind)]["signature"] for ind in pop if cache[tuple(ind)]["valid"]}
        row = {"gen": gen, "valid_frac": float(np.mean(valid)), "fit_mean": float(np.mean(fits)),
               "fit_max": float(np.max(fits)), "distinct_signatures": len(sigs), "archive": sum(map(len, archive.values())), "valid_unique_seen": len(archive_keys),
               "elapsed_s": round(time.time() - t0, 1)}
        log.append(row)
        print(row, flush=True)
    pool.close()
    return archive, log


def select_pairs(archive, n_pairs, seed):
    """Same number of pairs per family; inside a family, structurally distinct pairs first
    (random order otherwise)."""
    rng = random.Random(seed)
    by_family = {fam: list(recs) for fam, recs in archive.items()}
    quota = {f: n_pairs // len(FAMILIES) + (1 if i < n_pairs % len(FAMILIES) else 0)
             for i, f in enumerate(FAMILIES)}
    chosen, seen_codes = [], set()
    for fam in FAMILIES:
        recs = by_family.get(fam, [])
        rng.shuffle(recs)
        first, rest, seen_struct = [], [], set()
        for r in recs:
            s = normalise(r["P"])
            (rest if s in seen_struct else first).append(r)
            seen_struct.add(s)
        picked = 0
        for r in first + rest:
            if picked == quota[fam]:
                break
            if r["P"] in seen_codes or r["U"] in seen_codes:
                continue
            seen_codes.update((r["P"], r["U"]))
            chosen.append(r)
            picked += 1
        if picked < quota[fam]:
            raise RuntimeError(f"family {fam}: only {picked} pairs in the archive (quota {quota[fam]})")
    rng.shuffle(chosen)
    return chosen


def write_dataset(chosen, log, args):
    os.makedirs(args.out, exist_ok=True)
    for label, key in (("Parallelizable", "P"), ("Undefined", "U")):
        with open(os.path.join(args.out, f"{label}_codes.py"), "w", encoding="utf-8") as f:
            for i, r in enumerate(chosen, 1):
                f.write(f"Code {i}:\n{r[key].rstrip()}\n\n{SEP}\n")
    with open(os.path.join(args.out, "metadata.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["pair_id", "family", "form", "wrapper", "domain", "kind", "lang", "minimality",
                    "n_tokens", "oracle_reason_U", "genome"])
        for i, r in enumerate(chosen, 1):
            m = r["meta"]
            w.writerow([i, m["family"], m["form"], m["wrapper"], m["domain"], m["kind"], m["lang"],
                        round(r["minimality"], 4), r["n_tokens"], r["reason_U"], " ".join(map(str, r["genome"]))])
    with open(os.path.join(args.out, "ga_log.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(log[0]))
        w.writeheader()
        w.writerows(log)
    with open(os.path.join(args.out, "generator_config.json"), "w", encoding="utf-8") as f:
        json.dump(vars(args), f, indent=2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "..", "data", "synthetic"))
    ap.add_argument("--pop", type=int, default=10000)
    ap.add_argument("--ngen", type=int, default=50)
    ap.add_argument("--cxpb", type=float, default=0.9)
    ap.add_argument("--mutpb", type=float, default=0.1)
    ap.add_argument("--pairs", type=int, default=4000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--archive-cap", type=int, default=3000, help="max archived pairs per family")
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    args = ap.parse_args()
    archive, log = run(args)
    chosen = select_pairs(archive, args.pairs, args.seed)
    write_dataset(chosen, log, args)
    fam = Counter(r["meta"]["family"] for r in chosen)
    print(f"archive={sum(map(len, archive.values()))} chosen={len(chosen)} per family={dict(fam)}")
    print("structurally distinct P variants:", len({normalise(r['P']) for r in chosen}))


if __name__ == "__main__":
    main()
