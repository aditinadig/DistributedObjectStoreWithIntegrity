import os
import math

# Configuration
NUM_NODES = 3  # Total storage nodes
DATA_NODES = NUM_NODES  # No parity now
DATA_DIR = "distributed_storage"

def encode_file(file_path):
    """Encodes a file using Reed-Solomon and stores it in storage nodes."""
    with open(file_path, 'rb') as f:
        data = f.read()

    # Split the data into NUM_NODES chunks (evenly)
    chunk_size = math.ceil(len(data) / NUM_NODES)
    fragments = [data[i * chunk_size: (i + 1) * chunk_size] for i in range(NUM_NODES)]

    # Store fragments in different nodes
    for i in range(NUM_NODES):
        fragment_path = f"{DATA_DIR}/node_{i}/fragment_{i}.bin"
        with open(fragment_path, 'wb') as f:
            f.write(fragments[i])

    # Print fragment details
    for i, fragment in enumerate(fragments):
        print(f"Fragment {i}: {fragment}")

    print(f"✅ File '{file_path}' successfully encoded into {NUM_NODES} fragments.")
    print(f"🔍 Data size: {len(data)} bytes")
    print(f"🔍 Storage nodes: {DATA_DIR}")

if __name__ == "__main__":
    input_file = "simple_text.txt"
    encode_file(input_file)