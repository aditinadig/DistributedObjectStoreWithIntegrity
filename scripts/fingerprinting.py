# fingerprinting.py

import os
import hashlib
import sys
import subprocess

# Add the project root directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from remote.remote_utils import send_fragment  # Reuse for fingerprint upload
from remote.remote_config import REMOTE_IPS, KEY_PATH

NUM_NODES = 3


def remote_fragment_exists(node_id, fragment_name):
    """Checks if the fragment exists remotely on the given node."""
    cmd = f"test -f ~/storage_node/fragments/{fragment_name} && echo EXISTS"
    result = subprocess.run(
        ["ssh", "-i", KEY_PATH, REMOTE_IPS[node_id], cmd],
        capture_output=True,
        text=True
    )
    return "EXISTS" in result.stdout

def generate_fingerprint(data):
    """Generates SHA-256 fingerprint of given data."""
    return hashlib.sha256(data).hexdigest()

def fingerprint_fragments():
    """Generates fingerprint for each local fragment and uploads it to the correct remote node."""
    os.makedirs("fingerprints", exist_ok=True)  # <- Ensure fingerprints directory exists
    for i in range(NUM_NODES):
        frag_path = f"fragments/fragment_{i}.bin"
        fingerprint_path = f"fingerprints/fingerprint_{i}.txt"

        if not os.path.exists(frag_path):
            print(f"⚠️ Skipping fragment {i}: file not found locally.")
            continue

        # Read fragment and compute fingerprint
        with open(frag_path, 'rb') as f:
            data = f.read()
        fingerprint = generate_fingerprint(data)

        # Write fingerprint to a local text file
        with open(fingerprint_path, 'w') as f:
            f.write(fingerprint)
        print(f"✅ Fingerprint for fragment {i} stored.")

        # Upload fingerprint to corresponding remote node
        if remote_fragment_exists(i, f"fragment_{i}.bin"):
            send_fragment(i, fingerprint_path)
        else:
            print(f"⚠️ Skipping fingerprint upload for fragment {i}: fragment missing on remote node.")

if __name__ == "__main__":
    fingerprint_fragments()