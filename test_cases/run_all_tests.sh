#!/bin/bash

export PYTHONPATH="$(pwd)"
LOGFILE="all_tc_results.log"
rm -f "$LOGFILE"

echo "🧪 Starting full test case suite..." | tee -a "$LOGFILE"
echo "---------------------------------------" >> "$LOGFILE"

for i in {1..11}; do
    TC="TC$i"
    echo -e "\n🔹 Running $TC...\n" | tee -a "$LOGFILE"
    python3 test_cases/run_tc.py "$TC" >> "$LOGFILE" 2>&1
    echo -e "\n✅ Finished $TC\n---------------------------\n" | tee -a "$LOGFILE"
done

echo "✅ All test cases completed. Results logged in: $LOGFILE"