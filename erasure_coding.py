import os
import reedsolo

# Configuration
NUM_NODES = 3  # Total storage nodes
DATA_SHARDS = 2  # Minimum fragments needed
PARITY_SHARDS = NUM_NODES - DATA_SHARDS  # Extra parity for recovery
DATA_DIR = "distributed_storage"  # Storage directory

def encode_file(file_path):
    """Encodes a file using Reed-Solomon and stores it in storage nodes."""
    with open(file_path, 'rb') as f:
        data = f.read()
    
    # Reed-Solomon Encoder
    rs = reedsolo.RSCodec(PARITY_SHARDS)  # Create encoder
    encoded_data = rs.encode(data)  # Get Reed-Solomon encoded data

    # Ensure encoded data is evenly divisible by NUM_NODES
    while len(encoded_data) % NUM_NODES != 0:
        encoded_data += b'\x00'  # Pad with null bytes to align sizes

    chunk_size = len(encoded_data) // NUM_NODES
    fragments = [encoded_data[i * chunk_size: (i + 1) * chunk_size] for i in range(NUM_NODES)]

    # Ensure each fragment has the same length by applying padding if necessary
    for i in range(NUM_NODES):
        while len(fragments[i]) < chunk_size:
            fragments[i] += b'\x00'  # Pad individual fragments to maintain uniformity

    # Store fragments in storage nodes
    for i in range(NUM_NODES):
        fragment_path = f"{DATA_DIR}/node_{i}/fragment_{i}.bin"
        with open(fragment_path, 'wb') as f:
            f.write(fragments[i])

    print(f"✅ File '{file_path}' successfully split into {NUM_NODES} fragments.")

    print(f"\n🔍 Full Encoded Data (Hex): {encoded_data.hex()}")
    print(f"🔍 Encoded Data Length: {len(encoded_data)}")   

    for i, fragment in enumerate(fragments):
        print(f"\n📝 Fragment {i} (Hex): {fragment.hex()} | Length: {len(fragment)}")


# Run Encoding
if __name__ == "__main__":
    input_file = "large_text.txt"

    # Create sample file
    # with open(input_file, 'w') as f:
    #     f.write("This is a test file for distributed storage with erasure coding.")

    encode_file(input_file)
