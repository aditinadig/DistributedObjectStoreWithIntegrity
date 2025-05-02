import os
import hashlib
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from remote.remote_utils import send_fragment
from remote.remote_config import REMOTE_IPS, KEY_PATH

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

NUM_SHARDS = 5
FRAG_DIR = "fragments"
FP_DIR = "fingerprints"

def generate_fingerprint(data):
    return hashlib.sha256(data).hexdigest()

def fingerprint_fragments():
    os.makedirs(FP_DIR, exist_ok=True)

    for i in range(NUM_SHARDS):
        frag_file = os.path.join(FRAG_DIR, f"fragment_{i:03d}")
        fp_file = os.path.join(FP_DIR, f"fingerprint_{i:03d}.txt")

        if not os.path.exists(frag_file):
            print(f"⚠️ Skipping fragment {i:03d}: not found.")
            continue

        with open(frag_file, "rb") as f:
            encrypted_data = f.read()

        fingerprint = generate_fingerprint(encrypted_data)

        with open(fp_file, "w") as f:
            f.write(fingerprint)

        print(f"✅ Fingerprint for fragment {i:03d} stored.")
        send_fragment(i, fp_file)

if __name__ == "__main__":
    fingerprint_fragments()