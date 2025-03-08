import os
import reedsolo
import hashlib

# Configuration
NUM_NODES = 3  # Total storage nodes
DATA_SHARDS = 2  # Minimum number of fragments needed
PARITY_SHARDS = NUM_NODES - DATA_SHARDS  # Extra redundancy
DATA_DIR = "distributed_storage"  # Storage directory
OUTPUT_FILE = "reconstructed.txt"  # Output file

def generate_fingerprint(data):
    """Generates a SHA-256 fingerprint for the given data."""
    return hashlib.sha256(data).hexdigest()

def verify_fragments():
    """Checks if stored fragments match their fingerprints and returns valid ones."""
    valid_fragments = {}

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
            valid_fragments[i] = fragment_data
        else:
            print(f"⚠️ Fragment {i} is CORRUPTED!")

    return valid_fragments

def reconstruct_file():
    """Reconstructs the original file using valid fragments."""
    valid_fragments = verify_fragments()

    if len(valid_fragments) < DATA_SHARDS:
        print("\n❌ Not enough valid fragments to reconstruct the file!")
        return False

    # Sort valid fragments by index
    sorted_fragments = [valid_fragments[i] for i in sorted(valid_fragments.keys())]
    encoded_data = b''.join(sorted_fragments)  # Reassemble encoded data

    # Reed-Solomon Decoder
    rs = reedsolo.RSCodec(PARITY_SHARDS)

    print(f"\n🔍 Reassembled Encoded Data (Hex): {encoded_data.hex()}")
    print(f"🔍 Reassembled Data Length: {len(encoded_data)}")

    try:
        reconstructed_data = rs.decode(encoded_data)  # Decode to original file data
        if isinstance(reconstructed_data, tuple):  
            reconstructed_data = reconstructed_data[0]  # Extract first item if tuple
    except reedsolo.ReedSolomonError:
        print("\n❌ Reconstruction failed: Too many errors to correct!")
        return False

    # ✅ Remove padding after decoding
    reconstructed_data = reconstructed_data.rstrip(b'\x00')

    # Write reconstructed data to file
    with open(OUTPUT_FILE, 'wb') as f:
        f.write(reconstructed_data)  # Save cleaned data

    print(f"\n✅ File successfully reconstructed as '{OUTPUT_FILE}'")
    return True

if __name__ == "__main__":
    reconstruct_file()