#!/bin/bash

# === Set this first ===
KEY=~/.ssh/storage.pem
NODE0=ubuntu@18.222.44.184
NODE1=ubuntu@3.144.41.239
NODE2=ubuntu@3.148.212.212
NODE3=ubuntu@3.142.166.244
NODE4=ubuntu@18.216.8.230

# === Helper to clean local state ===
reset_local() {
    rm -rf fragments fingerprints reconstruction_temp reconstructed.txt
}

# === Helper to run core pipeline ===
run_pipeline() {
    python3 scripts/erasure_coding.py
    python3 scripts/fingerprinting.py
}

# === Helper to finalize and print result ===
finish_test() {
    python3 scripts/verify_fragments.py
    python3 scripts/reconstruct_file.py
    echo "📄 Final reconstructed.txt:"
    cat reconstructed.txt 2>/dev/null || echo "(No reconstructed.txt)"
}

# === Run the chosen test case ===
case $1 in
  TC1)
    echo "🧪 Running TC1 – No Faults"
    reset_local
    run_pipeline
    finish_test
    ;;
  TC2)
    echo "🧪 Running TC2 – Delete fragment_001"
    reset_local
    run_pipeline
    ssh -i $KEY $NODE1 'rm ~/storage_node/fragments/fragment_001'
    finish_test
    ;;
  TC3)
    echo "🧪 Running TC3 – Delete fragments 000, 001"
    reset_local
    run_pipeline
    ssh -i $KEY $NODE0 'rm ~/storage_node/fragments/fragment_000'
    ssh -i $KEY $NODE1 'rm ~/storage_node/fragments/fragment_001'
    finish_test
    ;;
  TC4)
    echo "🧪 Running TC4 – Delete fragments 000, 001, 002"
    reset_local
    run_pipeline
    ssh -i $KEY $NODE0 'rm ~/storage_node/fragments/fragment_000'
    ssh -i $KEY $NODE1 'rm ~/storage_node/fragments/fragment_001'
    ssh -i $KEY $NODE2 'rm ~/storage_node/fragments/fragment_002'
    finish_test
    ;;
  TC5)
    echo "🧪 Running TC5 – Corrupt fragment_002"
    reset_local
    run_pipeline
    ssh -i $KEY $NODE2 "echo 'XXXXX' > ~/storage_node/fragments/fragment_002"
    finish_test
    ;;
  TC6)
    echo "🧪 Running TC6 – Corrupt fragments 001, 002"
    reset_local
    run_pipeline
    ssh -i $KEY $NODE1 "echo 'BAD1' > ~/storage_node/fragments/fragment_001"
    ssh -i $KEY $NODE2 "echo 'BAD2' > ~/storage_node/fragments/fragment_002"
    finish_test
    ;;
  TC7)
    echo "🧪 Running TC7 – Corrupt fragments 000, 001, 002"
    reset_local
    run_pipeline
    ssh -i $KEY $NODE0 "echo 'C0' > ~/storage_node/fragments/fragment_000"
    ssh -i $KEY $NODE1 "echo 'C1' > ~/storage_node/fragments/fragment_001"
    ssh -i $KEY $NODE2 "echo 'C2' > ~/storage_node/fragments/fragment_002"
    finish_test
    ;;
  TC8)
    echo "🧪 Running TC8 – Delete fingerprint_001"
    reset_local
    run_pipeline
    ssh -i $KEY $NODE1 'rm ~/storage_node/fingerprints/fingerprint_001.txt'
    finish_test
    ;;
  TC9)
    echo "🧪 Running TC9 – Corrupt fragments 000, 002, 003, 004"
    reset_local
    run_pipeline
    ssh -i $KEY $NODE0 "echo 'CORRUPT0' > ~/storage_node/fragments/fragment_000"
    ssh -i $KEY $NODE2 "echo 'CORRUPT2' > ~/storage_node/fragments/fragment_002"
    ssh -i $KEY $NODE3 "echo 'CORRUPT3' > ~/storage_node/fragments/fragment_003"
    ssh -i $KEY $NODE4 "echo 'CORRUPT4' > ~/storage_node/fragments/fragment_004"
    finish_test
    ;;
  TC10)
    echo "🧪 Running TC10 – Overwrite fingerprint_001"
    reset_local
    run_pipeline
    ssh -i $KEY $NODE1 "echo '1234567890abcdef' > ~/storage_node/fingerprints/fingerprint_001.txt"
    finish_test
    ;;
  TC11)
    echo "🧪 Running TC11 – Delete 001, corrupt 002"
    reset_local
    run_pipeline
    ssh -i $KEY $NODE1 'rm ~/storage_node/fragments/fragment_001'
    ssh -i $KEY $NODE2 "echo 'MIXED_ERROR' > ~/storage_node/fragments/fragment_002"
    finish_test
    ;;
  TC12)
    echo "🧪 Running TC12 – Delete 000, 001; corrupt 002"
    reset_local
    run_pipeline
    ssh -i $KEY $NODE0 'rm ~/storage_node/fragments/fragment_000'
    ssh -i $KEY $NODE1 'rm ~/storage_node/fragments/fragment_001'
    ssh -i $KEY $NODE2 "echo 'BAD' > ~/storage_node/fragments/fragment_002"
    finish_test
    ;;
  TC13)
    echo "🧪 Running TC13 – Corrupt fragment_003"
    reset_local
    run_pipeline
    ssh -i $KEY $NODE3 "echo 'CORRUPT' > ~/storage_node/fragments/fragment_003"
    finish_test
    ;;
  TC14)
    echo "🧪 Running TC14 – Delete fragment_003 and fingerprint_003"
    reset_local
    run_pipeline
    ssh -i $KEY $NODE3 'rm ~/storage_node/fragments/fragment_003'
    ssh -i $KEY $NODE3 'rm ~/storage_node/fingerprints/fingerprint_003.txt'
    finish_test
    ;;
  TC15)
    echo "🧪 Running TC15 – Overwrite fingerprint_000"
    reset_local
    run_pipeline
    ssh -i $KEY $NODE0 "echo 'FAKEFINGERPRINT' > ~/storage_node/fingerprints/fingerprint_000.txt"
    finish_test
    ;;
  TC16)
    echo "🧪 Running TC16 – Delete 001, 002, 003"
    reset_local
    run_pipeline
    ssh -i $KEY $NODE1 'rm ~/storage_node/fragments/fragment_001'
    ssh -i $KEY $NODE2 'rm ~/storage_node/fragments/fragment_002'
    ssh -i $KEY $NODE3 'rm ~/storage_node/fragments/fragment_003'
    finish_test
    ;;
  TC17)
    echo "🧪 Running TC17 – Delete 000, fingerprint_001; corrupt 002"
    reset_local
    run_pipeline
    ssh -i $KEY $NODE0 'rm ~/storage_node/fragments/fragment_000'
    ssh -i $KEY $NODE1 'rm ~/storage_node/fingerprints/fingerprint_001.txt'
    ssh -i $KEY $NODE2 "echo 'CORRUPTED' > ~/storage_node/fragments/fragment_002"
    finish_test
    ;;
  *)
    echo "❌ Unknown test case. Usage: ./run_tc.sh TC<number>"
    ;;
esac