import os
import hashlib

# Configuration
NUM_NODES = 3  # Number of storage nodes
DATA_DIR = "distributed_storage"  # Storage directory

def generate_fingerprint(data):
    """Generates a SHA-256 fingerprint for the given data."""
    return hashlib.sha256(data).hexdigest()

def verify_fragments():
    """Checks if stored fragments match their original fingerprints."""
    valid_fragments = []

    for i in range(NUM_NODES):
        fragment_path = f"{DATA_DIR}/node_{i}/fragment_{i}.bin"
        fingerprint_path = f"{DATA_DIR}/node_{i}/fingerprint_{i}.txt"

        if not os.path.exists(fragment_path) or not os.path.exists(fingerprint_path):
            print(f"❌ Fragment {i} is missing!")
            continue
        
        # Read fragment
        with open(fragment_path, 'rb') as f:
            fragment_data = f.read()
        
        # Read stored fingerprint
        with open(fingerprint_path, 'r') as f:
            stored_fingerprint = f.read().strip()
        
        # Compute fingerprint again
        computed_fingerprint = generate_fingerprint(fragment_data)

        if computed_fingerprint == stored_fingerprint:
            print(f"✅ Fragment {i} is VALID.")
            valid_fragments.append(i)
        else:
            print(f"⚠️ Fragment {i} is CORRUPTED!")

    return valid_fragments

if __name__ == "__main__":
    valid_fragments = verify_fragments()

    if len(valid_fragments) >= 1:  # Ensure we have at least one valid fragment since no parity
        print("\n✅ Enough valid fragments available for reconstruction.")
    else:
        print("\n❌ Not enough valid fragments! Reconstruction might fail.")