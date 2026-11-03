#!/usr/bin/env bash
# Two-stage training on the GPU: stage 1 (3 models on the synthetic pairs), then stage 2 (240 runs).
# Finished runs are skipped, so the script can be started again after an interruption.
# PY selects the Python interpreter (default: python), e.g. PY=/path/to/venv/bin/python bash launch_two_stage.sh
cd "$(dirname "$0")"
export HF_HUB_DISABLE_SYMLINKS_WARNING=1 TOKENIZERS_PARALLELISM=false
PY="${PY:-python} -W ignore"
LOG=../../results/logs
mkdir -p "$LOG"
$PY two_stage.py --stage 1 >> "$LOG/two_stage.log" 2>&1 || exit 1
$PY two_stage.py --stage 2 >> "$LOG/two_stage.log" 2>&1 || exit 1
echo "Two-stage experiment finished"
