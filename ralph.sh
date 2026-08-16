#!/usr/bin/env bash
# ralph.sh — CHRONON/TLY autonomous build loop. Run from repo root.
# One fresh Claude Code session per iteration; the repo is the memory.
# NEVER set ANTHROPIC_API_KEY here — subscription auth via `claude login` only.
set -u
MAX="${MAX:-25}"
for i in $(seq 1 "$MAX"); do
  if [ -f HALT ]; then
    echo "HALT present, stopping"
    exit 0
  fi
  echo "=== ralph iteration $i/$MAX $(date -u +%FT%TZ) ==="
  claude -p "Read RALPH_LOOP.md in the repo root and execute one iteration." \
    --permission-mode acceptEdits || true
done
