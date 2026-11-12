#!/bin/bash
cd /app/conversations/6ae14dce9883f31f1959c9f7
while pgrep -f boundary_sweep > /dev/null; do sleep 60; done
echo "sweep complete at $(date), total hits: $(cat bnd_*.txt | wc -l)" >> FINAL_DERIVE.log
python3 derive_hits.py >> FINAL_DERIVE.log 2>&1
echo "FINAL DERIVE DONE $(date)" >> FINAL_DERIVE.log
