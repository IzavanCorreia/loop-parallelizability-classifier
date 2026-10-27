#!/usr/bin/env bash
# Models of the previous study and the n-gram reference on the CPU. One process per model and repetition:
# on Windows, more processes can exhaust the page file. Finished folds are skipped on a restart.
# PY selects the Python interpreter (default: python); a CPU-only PyTorch build avoids loading the CUDA libraries.
cd "$(dirname "$0")"
PY="${PY:-python} -W ignore"
LOG=../../results/logs
mkdir -p "$LOG"

(for s in real syn2real hybrid; do for m in lr svm ngram; do $PY run.py --model $m --setting $s; done; done) >> "$LOG/cpu_lr_svm_ngram.log" 2>&1 &

for m in dnn cnn; do
  for r in 0 1 2; do
    (for s in hybrid syn2real real; do $PY run.py --model $m --setting $s --reps $r; done) >> "$LOG/cpu_${m}_rep${r}.log" 2>&1 &
  done
done
wait
echo "CPU experiments finished"
