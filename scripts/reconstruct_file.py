import os
import sys
import subprocess
import hashlib
from zfec import Decoder

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from remote.remote_config import REMOTE_IPS, KEY_PATH

NUM_SHARDS = 5
K_SHARDS = 3
REMOTE_FOLDER = "storage_node"
LOCAL_FOLDER = "reconstruction_temp"
OUTPUT_FILE = "reconstructed.txt"

def fetch_fragment_and_fingerprint(node_id):
    success = True
    for fname in [f"fragment_{node_id:03d}", f"fingerprint_{node_id:03d}.txt"]:
        subdir = "fragments" if "fragment" in fname else "fingerprints"
        remote_path = f"{REMOTE_IPS[node_id]}:~/{REMOTE_FOLDER}/{subdir}/{fname}"
        local_path = os.path.join(LOCAL_FOLDER, fname)
        result = subprocess.run(
            ["scp", "-i", KEY_PATH, remote_path, local_path],
            capture_output=True
        )
        if result.returncode != 0:
            print(f"❌ Failed to fetch {fname} from node {node_id}")
            success = False
    return success

def generate_fingerprint(data):
    return hashlib.sha256(data).hexdigest()

def reconstruct_file():
    os.makedirs(LOCAL_FOLDER, exist_ok=True)
    valid_data = {}

    for i in range(NUM_SHARDS):
        fetch_fragment_and_fingerprint(i)

        frag_path = os.path.join(LOCAL_FOLDER, f"fragment_{i:03d}")
        fp_path = os.path.join(LOCAL_FOLDER, f"fingerprint_{i:03d}.txt")
        if not os.path.exists(frag_path) or not os.path.exists(fp_path):
            continue

        with open(frag_path, 'rb') as f:
            data = f.read()
        with open(fp_path, 'r') as f:
            expected = f.read().strip()

        if generate_fingerprint(data) == expected:
            print(f"✅ Fragment {i:03d} is VALID.")
            valid_data[i] = data

    if len(valid_data) < K_SHARDS:
        print("❌ Not enough valid fragments.")
        return

    block_ids = sorted(valid_data.keys())[:K_SHARDS]
    block_data = [valid_data[i] for i in block_ids]

    # 🩹 Fix: Remove the first byte from each fragment
    block_data = [b[1:] for b in block_data]

    print(f"🛠️ Reconstructing from fragments: {block_ids}")
    # Decode and strip first byte from each block before joining
    original = Decoder(K_SHARDS, NUM_SHARDS).decode(block_data, block_ids)

    # ⚠️ Strip the first byte from each decoded block
    cleaned_blocks = [block[1:] for block in original]

    with open(OUTPUT_FILE, 'wb') as f:
        f.write(b''.join(cleaned_blocks))

    print(f"✅ Reconstructed file written to '{OUTPUT_FILE}'")

if __name__ == "__main__":
    reconstruct_file()