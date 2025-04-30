#!/bin/bash

echo "🧹 Organizing DistributedObjectStoreWithIntegrity..."

# Create folders
mkdir -p fragments fingerprints test_cases remote scripts

# Move fragment and fingerprint files
mv fragment_*.bin fragments/ 2>/dev/null
mv fingerprint_*.txt fingerprints/ 2>/dev/null

# Move test case utilities
mv run_tc.py run_all_tests.sh tc_utils.py test_cases/

# Move remote-related files
mv remote_config.py remote_utils.py remote/

# Move core scripts
mv setup_storage.py erasure_coding.py fingerprinting.py verify_fragments.py reconstruct_file.py run_all.sh scripts/

echo "✅ Project structure organized!"