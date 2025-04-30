import os
import hashlib
import subprocess
import sys

# Add the project root directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from remote.remote_config import REMOTE_IPS, KEY_PATH

# Configuration
NUM_NODES = 3
TEMP_DIR = "verify_temp"

def generate_fingerprint(data):
    return hashlib.sha256(data).hexdigest()

def fetch_from_remote(node_id, filename):
    subdir = "fingerprints" if "fingerprint" in filename else "fragments"
    remote_path = f"{REMOTE_IPS[node_id]}:~/storage_node/{subdir}/{filename}"
    result = subprocess.run(["scp", "-i", KEY_PATH, remote_path, TEMP_DIR], capture_output=True)
    if result.returncode != 0:
        print(f"❌ Failed to fetch {filename} from node {node_id}: {result.stderr.decode().strip()}")
        return False
    return True

def verify_fragments():
    os.makedirs(TEMP_DIR, exist_ok=True)
    valid_fragments = []

    for i in range(NUM_NODES):
        frag_name = f"fragment_{i}.bin"
        fp_name = f"fingerprint_{i}.txt"

        fetched_frag = fetch_from_remote(i, frag_name)
        fetched_fp = fetch_from_remote(i, fp_name)

        fragment_path = os.path.join(TEMP_DIR, frag_name)
        fingerprint_path = os.path.join(TEMP_DIR, fp_name)

        if not (fetched_frag and fetched_fp and os.path.exists(fragment_path) and os.path.exists(fingerprint_path)):
            print(f"❌ Fragment {i} or fingerprint is missing!")
            continue

        with open(fragment_path, 'rb') as f:
            fragment_data = f.read()
        with open(fingerprint_path, 'r') as f:
            stored_fingerprint = f.read().strip()

        computed_fingerprint = generate_fingerprint(fragment_data)

        if computed_fingerprint == stored_fingerprint:
            print(f"✅ Fragment {i} is VALID.")
            valid_fragments.append(i)
        else:
            print(f"⚠️ Fragment {i} is CORRUPTED!")

    return valid_fragments

if __name__ == "__main__":
    valid_fragments = verify_fragments()
    if len(valid_fragments) >= 1:
        print("\n✅ Enough valid fragments available for reconstruction.")
    else:
        print("\n❌ Not enough valid fragments! Reconstruction might fail.")