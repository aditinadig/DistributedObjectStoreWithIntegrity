import os
import subprocess
import hashlib
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from remote.remote_config import REMOTE_IPS, KEY_PATH

NUM_SHARDS = 5
TEMP_DIR = "verify_temp"

def generate_fingerprint(data):
    return hashlib.sha256(data).hexdigest()

def fetch_from_remote(node_id, filename, subdir):
    remote = REMOTE_IPS[node_id]
    remote_path = f"{remote}:~/storage_node/{subdir}/{filename}"
    local_path = os.path.join(TEMP_DIR, filename)
    result = subprocess.run(["scp", "-i", KEY_PATH, remote_path, local_path], capture_output=True)
    if result.returncode != 0:
        print(f"❌ Failed to fetch {filename} from node {node_id}: {result.stderr.decode().strip()}")
        return False
    return True

def verify_fragments():
    os.makedirs(TEMP_DIR, exist_ok=True)

    valid_fragments = []

    for i in range(NUM_SHARDS):
        frag_name = f"fragment_{i:03d}"
        fp_name = f"fingerprint_{i:03d}.txt"

        frag_fetched = fetch_from_remote(i, frag_name, "fragments")
        fp_fetched = fetch_from_remote(i, fp_name, "fingerprints")

        frag_path = os.path.join(TEMP_DIR, frag_name)
        fp_path = os.path.join(TEMP_DIR, fp_name)

        if not frag_fetched or not fp_fetched or not os.path.exists(frag_path) or not os.path.exists(fp_path):
            print(f"❌ Fragment {i:03d} or fingerprint is missing — skipping.")
            continue

        with open(frag_path, "rb") as f:
            fragment_data = f.read()
        with open(fp_path, "r") as f:
            expected_fp = f.read().strip()

        actual_fp = generate_fingerprint(fragment_data)

        if actual_fp == expected_fp:
            print(f"✅ Fragment {i:03d} is VALID.")
            valid_fragments.append(i)
        else:
            print(f"⚠️ Fragment {i:03d} fingerprint mismatch!")

    if len(valid_fragments) >= 3:
        print("\n✅ Enough valid fragments available for reconstruction.")
    else:
        print("\n❌ Not enough valid fragments. Reconstruction may fail.")

if __name__ == "__main__":
    verify_fragments()