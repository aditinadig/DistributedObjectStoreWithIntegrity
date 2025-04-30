import os
import subprocess
import hashlib
import sys

# Add the project root directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from remote.remote_config import REMOTE_IPS, KEY_PATH

NUM_NODES = 3
REMOTE_FOLDER = "storage_node"
LOCAL_FOLDER = "reconstruction_temp"
OUTPUT_FILE = "reconstructed.txt"

def fetch_fragment_and_fingerprint(node_id):
    remote = REMOTE_IPS[node_id]
    success = True
    for fname in [f"fragment_{node_id}.bin", f"fingerprint_{node_id}.txt"]:
        subdir = "fingerprints" if "fingerprint" in fname else "fragments"
        remote_path = f"{remote}:~/{REMOTE_FOLDER}/{subdir}/{fname}"
        result = subprocess.run(["scp", "-i", KEY_PATH, remote_path, LOCAL_FOLDER], capture_output=True)
        if result.returncode != 0:
            print(f"❌ Failed to fetch {fname} from node {node_id}: {result.stderr.decode().strip()}")
            success = False
    return success

def generate_fingerprint(data):
    """SHA-256 fingerprint"""
    return hashlib.sha256(data).hexdigest()

def reconstruct_file():
    os.makedirs(LOCAL_FOLDER, exist_ok=True)
    fragment_status = {}
    fragment_size = None

    for i in range(NUM_NODES):
        fetch_fragment_and_fingerprint(i)

        frag_path = os.path.join(LOCAL_FOLDER, f"fragment_{i}.bin")
        fp_path = os.path.join(LOCAL_FOLDER, f"fingerprint_{i}.txt")

        frag_exists = os.path.exists(frag_path)
        fp_exists = os.path.exists(fp_path)

        status = {
            "exists": frag_exists,
            "fingerprint": fp_exists,
            "valid": False,
            "data": None
        }

        if frag_exists and fp_exists:
            with open(frag_path, 'rb') as f:
                data = f.read()
            with open(fp_path, 'r') as f:
                expected_fp = f.read().strip()

            actual_fp = generate_fingerprint(data)
            if actual_fp == expected_fp:
                print(f"✅ Fragment {i} is VALID.")
                status["valid"] = True
                status["data"] = data
                if fragment_size is None:
                    fragment_size = len(data)
            else:
                print(f"⚠️ Fragment {i} is CORRUPTED!")
        else:
            print(f"❌ Fragment {i} or its fingerprint is missing!")

        fragment_status[i] = status

    # Assemble final output
    fragments = []
    for i in range(NUM_NODES):
        status = fragment_status[i]
        if status["valid"]:
            fragments.append(status["data"])
        else:
            if not status["exists"]:
                label = "[MISSING FRAGMENT]"
            elif not status["fingerprint"]:
                label = "[MISSING FINGERPRINT]"
            else:
                label = "[CORRUPT]"

            padded = label.encode().ljust(fragment_size or 0, b'_')
            fragments.append(padded)
            print(f"🔄 Replacing fragment {i} with placeholder: {label}")

    output_data = b''.join(fragments).rstrip(b'\x00')
    with open(OUTPUT_FILE, 'wb') as f:
        f.write(output_data)

    print(f"\n✅ File reconstructed as '{OUTPUT_FILE}'")

if __name__ == "__main__":
    reconstruct_file()