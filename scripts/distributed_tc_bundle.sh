#!/bin/bash

echo '🧹 Cleaning up old data...'
rm -rf fragments fingerprints reconstruction_temp reconstructed.txt

# Function to run erasure coding and fingerprinting
run_pipeline() {
  echo '⚙️ Running erasure coding and fingerprinting pipeline...'
  python3 scripts/erasure_coding.py
  python3 scripts/fingerprinting.py
}

# Function to run verification and reconstruction
run_verification() {
  echo '🔍 Verifying fragments and reconstructing file...'
  python3 scripts/verify_fragments.py
  python3 scripts/reconstruct_file.py
  echo '📄 Reconstructed output:'
  cat reconstructed.txt 2>/dev/null || echo '(No reconstructed.txt file found)'
  echo '--------------------------------------------------'
}


echo '🏁 Starting TC1...'
rm -rf fragments fingerprints reconstruction_temp reconstructed.txt
run_pipeline
run_verification
echo '✅ Finished TC1'
echo ''
sleep 2

echo '🏁 Starting TC2...'
rm -rf fragments fingerprints reconstruction_temp reconstructed.txt
run_pipeline
ssh -i ~/.ssh/storage.pem ubuntu@3.144.41.239 "rm ~/storage_node/fragments/fragment_001"
run_verification
echo '✅ Finished TC2'
echo ''
sleep 2

echo '🏁 Starting TC3...'
rm -rf fragments fingerprints reconstruction_temp reconstructed.txt
run_pipeline
ssh -i ~/.ssh/storage.pem ubuntu@18.222.44.184 "rm ~/storage_node/fragments/fragment_000"
ssh -i ~/.ssh/storage.pem ubuntu@3.144.41.239 "rm ~/storage_node/fragments/fragment_001"
run_verification
echo '✅ Finished TC3'
echo ''
sleep 2

echo '🏁 Starting TC4...'
rm -rf fragments fingerprints reconstruction_temp reconstructed.txt
run_pipeline
ssh -i ~/.ssh/storage.pem ubuntu@18.222.44.184 "rm ~/storage_node/fragments/fragment_000"
ssh -i ~/.ssh/storage.pem ubuntu@3.144.41.239 "rm ~/storage_node/fragments/fragment_001"
ssh -i ~/.ssh/storage.pem ubuntu@3.148.212.212 "rm ~/storage_node/fragments/fragment_002"
run_verification
echo '✅ Finished TC4'
echo ''
sleep 2

echo '🏁 Starting TC5...'
rm -rf fragments fingerprints reconstruction_temp reconstructed.txt
run_pipeline
ssh -i ~/.ssh/storage.pem ubuntu@3.148.212.212 "echo 'XXXXX' > ~/storage_node/fragments/fragment_002"
run_verification
echo '✅ Finished TC5'
echo ''
sleep 2

echo '🏁 Starting TC6...'
rm -rf fragments fingerprints reconstruction_temp reconstructed.txt
run_pipeline
ssh -i ~/.ssh/storage.pem ubuntu@3.144.41.239 "echo 'BAD1' > ~/storage_node/fragments/fragment_001"
ssh -i ~/.ssh/storage.pem ubuntu@3.148.212.212 "echo 'BAD2' > ~/storage_node/fragments/fragment_002"
run_verification
echo '✅ Finished TC6'
echo ''
sleep 2

echo '🏁 Starting TC7...'
rm -rf fragments fingerprints reconstruction_temp reconstructed.txt
run_pipeline
ssh -i ~/.ssh/storage.pem ubuntu@18.222.44.184 "echo 'C0' > ~/storage_node/fragments/fragment_000"
ssh -i ~/.ssh/storage.pem ubuntu@3.144.41.239 "echo 'C1' > ~/storage_node/fragments/fragment_001"
ssh -i ~/.ssh/storage.pem ubuntu@3.148.212.212 "echo 'C2' > ~/storage_node/fragments/fragment_002"
run_verification
echo '✅ Finished TC7'
echo ''
sleep 2

echo '🏁 Starting TC8...'
rm -rf fragments fingerprints reconstruction_temp reconstructed.txt
run_pipeline
ssh -i ~/.ssh/storage.pem ubuntu@3.144.41.239 "rm ~/storage_node/fingerprints/fingerprint_001.txt"
run_verification
echo '✅ Finished TC8'
echo ''
sleep 2

echo '🏁 Starting TC9...'
rm -rf fragments fingerprints reconstruction_temp reconstructed.txt
run_pipeline
ssh -i ~/.ssh/storage.pem ubuntu@18.222.44.184 "echo 'CORRUPT0' > ~/storage_node/fragments/fragment_000"
ssh -i ~/.ssh/storage.pem ubuntu@3.148.212.212 "echo 'CORRUPT2' > ~/storage_node/fragments/fragment_002"
ssh -i ~/.ssh/storage.pem ubuntu@3.142.166.244 "echo 'CORRUPT3' > ~/storage_node/fragments/fragment_003"
ssh -i ~/.ssh/storage.pem ubuntu@18.216.8.230 "echo 'CORRUPT4' > ~/storage_node/fragments/fragment_004"
run_verification
echo '✅ Finished TC9'
echo ''
sleep 2

echo '🏁 Starting TC10...'
rm -rf fragments fingerprints reconstruction_temp reconstructed.txt
run_pipeline
ssh -i ~/.ssh/storage.pem ubuntu@3.144.41.239 "echo '1234567890abcdef' > ~/storage_node/fingerprints/fingerprint_001.txt"
run_verification
echo '✅ Finished TC10'
echo ''
sleep 2

echo '🏁 Starting TC11...'
rm -rf fragments fingerprints reconstruction_temp reconstructed.txt
run_pipeline
ssh -i ~/.ssh/storage.pem ubuntu@3.144.41.239 "rm ~/storage_node/fragments/fragment_001"
ssh -i ~/.ssh/storage.pem ubuntu@3.148.212.212 "echo 'MIXED_ERROR' > ~/storage_node/fragments/fragment_002"
run_verification
echo '✅ Finished TC11'
echo ''
sleep 2

echo '🏁 Starting TC12...'
rm -rf fragments fingerprints reconstruction_temp reconstructed.txt
run_pipeline
ssh -i ~/.ssh/storage.pem ubuntu@18.222.44.184 "rm ~/storage_node/fragments/fragment_000"
ssh -i ~/.ssh/storage.pem ubuntu@3.144.41.239 "rm ~/storage_node/fragments/fragment_001"
ssh -i ~/.ssh/storage.pem ubuntu@3.148.212.212 "echo 'BAD' > ~/storage_node/fragments/fragment_002"
run_verification
echo '✅ Finished TC12'
echo ''
sleep 2

echo '🏁 Starting TC13...'
rm -rf fragments fingerprints reconstruction_temp reconstructed.txt
run_pipeline
ssh -i ~/.ssh/storage.pem ubuntu@3.142.166.244 "echo 'CORRUPT' > ~/storage_node/fragments/fragment_003"
run_verification
echo '✅ Finished TC13'
echo ''
sleep 2

echo '🏁 Starting TC14...'
rm -rf fragments fingerprints reconstruction_temp reconstructed.txt
run_pipeline
ssh -i ~/.ssh/storage.pem ubuntu@3.142.166.244 "rm ~/storage_node/fragments/fragment_003"
ssh -i ~/.ssh/storage.pem ubuntu@3.142.166.244 "rm ~/storage_node/fingerprints/fingerprint_003.txt"
run_verification
echo '✅ Finished TC14'
echo ''
sleep 2

echo '🏁 Starting TC15...'
rm -rf fragments fingerprints reconstruction_temp reconstructed.txt
run_pipeline
ssh -i ~/.ssh/storage.pem ubuntu@18.222.44.184 "echo 'FAKEFINGERPRINT' > ~/storage_node/fingerprints/fingerprint_000.txt"
run_verification
echo '✅ Finished TC15'
echo ''
sleep 2

echo '🏁 Starting TC16...'
rm -rf fragments fingerprints reconstruction_temp reconstructed.txt
run_pipeline
ssh -i ~/.ssh/storage.pem ubuntu@3.144.41.239 "rm ~/storage_node/fragments/fragment_001"
ssh -i ~/.ssh/storage.pem ubuntu@3.148.212.212 "rm ~/storage_node/fragments/fragment_002"
ssh -i ~/.ssh/storage.pem ubuntu@3.142.166.244 "rm ~/storage_node/fragments/fragment_003"
run_verification
echo '✅ Finished TC16'
echo ''
sleep 2

echo '🏁 Starting TC17...'
rm -rf fragments fingerprints reconstruction_temp reconstructed.txt
run_pipeline
ssh -i ~/.ssh/storage.pem ubuntu@18.222.44.184 "rm ~/storage_node/fragments/fragment_000"
ssh -i ~/.ssh/storage.pem ubuntu@3.144.41.239 "rm ~/storage_node/fingerprints/fingerprint_001.txt"
ssh -i ~/.ssh/storage.pem ubuntu@3.148.212.212 "echo 'CORRUPTED' > ~/storage_node/fragments/fragment_002"
run_verification
echo '✅ Finished TC17'
echo ''
sleep 2