#!/usr/bin/env bash
# DistilBERT on the GPU: the short settings first, then the hybrid 3 x 10-fold CV.
# Finished folds are skipped, so the script can be started again after an interruption.
# PY selects the Python interpreter (default: python), e.g. PY=/path/to/venv/bin/python bash launch_gpu.sh
cd "$(dirname "$0")"
export HF_HUB_DISABLE_SYMLINKS_WARNING=1 TOKENIZERS_PARALLELISM=false
PY="${PY:-python} -W ignore"
LOG=../../results/logs
mkdir -p "$LOG"
for s in real syn2real hybrid; do
  $PY run.py --model distilbert --setting $s >> "$LOG/gpu_distilbert.log" 2>&1
done
echo "GPU experiments finished"
