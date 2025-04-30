import os
import hashlib

# Configuration
NUM_NODES = 3  # Number of storage nodes
DATA_DIR = "distributed_storage"  # Storage directory

def generate_fingerprint(data):
    """Generates a SHA-256 fingerprint for the given data."""
    return hashlib.sha256(data).hexdigest()

def fingerprint_fragments():
    """Generates and stores fingerprints for all fragments in storage nodes."""
    for i in range(NUM_NODES):
        fragment_path = f"{DATA_DIR}/node_{i}/fragment_{i}.bin"
        fingerprint_path = f"{DATA_DIR}/node_{i}/fingerprint_{i}.txt"

        # Check if fragment exists
        if not os.path.exists(fragment_path):
            print(f"⚠️ Skipping missing fragment {i} (File not found)")
            continue  # Skip to the next fragment
        
        # Read the fragment
        with open(fragment_path, 'rb') as f:
            fragment_data = f.read()
        
        # Generate fingerprint
        fingerprint = generate_fingerprint(fragment_data)

        # Store fingerprint in a text file
        with open(fingerprint_path, 'w') as f:
            f.write(fingerprint)
        
        print(f"✅ Fingerprint for fragment {i} stored.")

if __name__ == "__main__":
    fingerprint_fragments()