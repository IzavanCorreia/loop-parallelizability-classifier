"""Random-search baseline for the ablation of the genetic algorithm (GA_ABLATION_PROTOCOL.md).

Same decoder, oracle, validity checks, archive and final selection as ga.py; the only difference is
that the genomes are drawn uniformly at random instead of evolved. The budget is the number of genomes
the GA evaluated: a population of 10,000 over 51 evaluations (initial population + 50 generations),
i.e. 510,000 genomes, drawn here in 51 batches of 10,000.

Usage: python random_search.py --out ../../data/synthetic_random [--batches 51 --batch-size 10000]
"""

import argparse
import hashlib
import os
import random
import time
from collections import Counter, defaultdict
from multiprocessing import Pool

import numpy as np

from ga import evaluate_genome, normalise, select_pairs, write_dataset, SEP
from loopgen import GENE_MAX, N_GENES


def run(args):
    rng = np.random.default_rng(args.seed)
    rng_archive = random.Random(args.seed + 1)
    archive, archive_keys, seen_per_family = defaultdict(list), set(), Counter()
    all_sigs, n_valid, n_total, log = set(), 0, 0, []
    t0 = time.time()
    with Pool(args.workers) as pool:
        for batch in range(args.batches):
            genomes = [tuple(int(g) for g in row) for row in rng.integers(0, GENE_MAX, size=(args.batch_size, N_GENES))]
            results = pool.map(evaluate_genome, genomes, chunksize=64)
            batch_sigs, batch_valid = set(), 0
            for genome, r in zip(genomes, results):
                if not r["valid"]:
                    continue
                batch_valid += 1
                batch_sigs.add(r["signature"])
                fam = r["meta"]["family"]
                key = hashlib.md5((r["P"] + SEP + r["U"]).encode()).hexdigest()
                if key in archive_keys:
                    continue
                archive_keys.add(key)
                seen_per_family[fam] += 1
                entry = dict(r, genome=list(genome), key=key)
                bucket = archive[fam]
                if len(bucket) < args.archive_cap:
                    bucket.append(entry)
                else:
                    j = rng_archive.randrange(seen_per_family[fam])
                    if j < args.archive_cap:
                        bucket[j] = entry
            n_valid += batch_valid
            n_total += len(genomes)
            all_sigs |= batch_sigs
            row = {"batch": batch, "valid_frac": batch_valid / len(genomes), "distinct_signatures": len(batch_sigs),
                   "cumulative_signatures": len(all_sigs), "archive": sum(map(len, archive.values())),
                   "valid_unique_seen": len(archive_keys), "elapsed_s": round(time.time() - t0, 1)}
            log.append(row)
            print(row, flush=True)
    return archive, log


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "..", "data", "synthetic_random"))
    ap.add_argument("--batches", type=int, default=51)
    ap.add_argument("--batch-size", type=int, default=10000)
    ap.add_argument("--pairs", type=int, default=4000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--archive-cap", type=int, default=3000, help="max archived pairs per family")
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    args = ap.parse_args()
    archive, log = run(args)
    chosen = select_pairs(archive, args.pairs, args.seed)
    write_dataset(chosen, log, args)
    os.replace(os.path.join(args.out, "ga_log.csv"), os.path.join(args.out, "search_log.csv"))
    fam = Counter(r["meta"]["family"] for r in chosen)
    print(f"archive={sum(map(len, archive.values()))} chosen={len(chosen)} per family={dict(fam)}")
    print("structurally distinct P variants:", len({normalise(r['P']) for r in chosen}))


if __name__ == "__main__":
    main()
